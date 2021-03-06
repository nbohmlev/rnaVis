from django.shortcuts import render, get_object_or_404
from sumStats.models import Genotype, SequenceLength
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from collections import defaultdict
import json as JSON
from scipy import stats
import numpy as np
from django.db import models
from sumStats.forms import StatForm
import pandas as pd
from random import shuffle
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os
from django.http import HttpResponse
#class IndexView(generic.ListView):
 #   template_name = 'sumStats/index.html'
  #  context_object_name = 'latest_genotype_list'
    
   # def get_queryset(self):
    #    return Genotype.objects.filter(
     #       pub_date__lte = timezone.now()
      #      ).order_by('-pub_date')[:5]
    

class DetailView(generic.DetailView):
    model = Genotype
    template_name = 'sumStats/detail.html'

def getModelNames():
    allModels = models.get_models(models.get_app('sumStats'))
    allModelNames=[]
    for model in allModels:
        allModelNames.append(model._meta.verbose_name_raw.replace(" ",""))
    return allModelNames[1:]

def index(request):
    latest_genotype_list = Genotype.objects.order_by('-pub_date')
    form = StatForm(auto_id=False)
    context = {'latest_genotype_list': latest_genotype_list, 'form':form, 'user':request.user.first_name}
    return render(request, 'sumStats/index.html', context)

def result(request, pk):
    genotype = get_object_or_404(Genotype, pk=pk)
    allSeqs = genotype.sequencelength_set.all()
    itemSum = 0
    count = 0
    for item in allSeqs:
        itemSum += item.seqLen
        count += 1
    meanVal = float(itemSum)/count
    return render(request, 'sumStats/result.html', {'mean':meanVal})

def makeBar(request, genotype_ids, modelName):
    
    if modelName[-2:]=='gc':
        yAxisText = 'GC Content'
    else:
        yAxisText = 'Length'


    data = []
    for item in genotype_ids:
        genotype = get_object_or_404(Genotype, pk=item)
        exec("seqSet = genotype.%s_set.all()"%modelName)
        genotype_name = "%s" % genotype
        dataDict = defaultdict(list)
        dataDict['genotype_name'] = genotype_name
        allSeqLens = []
        for innerItem in seqSet:  
            seqName = "%s" % innerItem
            seqLen = innerItem.seqLen
            allSeqLens.append(seqLen)
            dataDict['seqObject'].append({'genotype_name':genotype_name, 'seqName':seqName, 'seqLen':seqLen})
        
        allSeqLens = np.array(allSeqLens)
        seqLenMean = np.mean(allSeqLens)
        seqLenSem = stats.sem(allSeqLens)
        dataDict['seqLenMean'] = seqLenMean
        dataDict['seqLenSem'] = seqLenSem
        data.append(dataDict)
    return {'result':JSON.dumps(data), 'yAxisText': yAxisText, 'modelName':modelName}

def makeStat(request, genotype_ids, modelName):
    allModelNames = getModelNames()
    criticalValue = 0.05

    data = []
    for model in allModelNames:
        modelAttr = []
        for item in genotype_ids:
            genotype = get_object_or_404(Genotype, pk=item)
            exec("seqSet = genotype.%s_set.all()"%model)
            allSeqLens = []
            for innerItem in seqSet:
                allSeqLens.append(innerItem.seqLen)
            modelAttr.append(allSeqLens)
        mu = stats.mannwhitneyu(modelAttr[0], modelAttr[1])
        if mu[1] < criticalValue:
            hyp = True
        else:
            hyp = False
        data.append({'model':model, 'muStat':mu[0], 'muP':mu[1], 'hyp':hyp})       
    return {'result':data}
    
    
def makeKS(request, genotype_ids, modelName):
    allModelNames = getModelNames()
    
    data = {}
    criticalValue = 0.05
    
    for model in allModelNames:
        genotype = get_object_or_404(Genotype, pk=genotype_ids[0])
        exec("seqSet = genotype.%s_set.all()"%model)
        allSeqLens = []
        for innerItem in seqSet:
            allSeqLens.append(innerItem.seqLen)

        allSeqLens = np.array(allSeqLens)
        mu = np.mean(allSeqLens)
        sigma = np.std(allSeqLens)
    
        normed_allSeqLens = (allSeqLens - mu)/sigma
        result = stats.kstest(normed_allSeqLens, 'norm')
        
        if result[1] >= 0.05:
            hyp = True
        else:
            hyp = False
        
        data[model] = {"kstest":result, "hypothesis":hyp} 
    return {'result': data, 'modelName':modelName}

def makeHist(request, genotype_ids, modelName):
    
    data = []
    for item in genotype_ids:
        genotype = get_object_or_404(Genotype, pk=item)
        exec("seqSet = genotype.%s_set.all()"%modelName)

        if modelName[-2:]=='gc':
            xAxisText = 'GC Content'
            bandwidth = 7
        else:
            xAxisText = 'Length'
            bandwidth = 700
        if modelName == 'fiveutrlength':
            bandwidth = 200
            
        genotype_name = "%s" % genotype
        dataDict = defaultdict(list)
        dataDict['genotype_name'] = genotype_name

        allSeqLens = []
        for innerItem in seqSet:
            seqLen = innerItem.seqLen
            allSeqLens.append(seqLen)
        
        dataDict['allSeqLens'] = allSeqLens
        data.append(dataDict)
    return {'result': JSON.dumps(data), 'modelName':modelName, 'xAxisText': xAxisText, 'bandwidth':bandwidth, 'yAxisText':'Probability'}

def genBar(request):

    queryList = dict(request.POST.iterlists())
    genotype_ids = queryList.get('genotype_ids')

    modelName = str(queryList.get('modelName')[0])

       
    dataJson = {'result':"Select appropriate number of genotypes. n=1 for K-S, n=2 for hypothesis test, n>0 for bar graphs"}
    template = 'warning.html'
    
    if genotype_ids != None:
        if 'makeBar' in request.POST:
            dataJson = makeBar(request, genotype_ids, modelName)
            template = 'genBar.html'
        elif 'genStat' in request.POST:
            if len(genotype_ids) ==2:
                dataJson = makeStat(request, genotype_ids, modelName)
                template = 'genStats.html' 
        elif 'genKS' in request.POST:
            if len(genotype_ids) == 1:
                dataJson = makeKS(request, genotype_ids, modelName)
                template = 'genKS.html'
        elif 'genHist' in request.POST:
            dataJson = makeHist(request, genotype_ids, modelName)
            template = 'genHist.html'
        elif 'genHeatMap' in request.POST:
            dataJson = genHeatMap(request, genotype_ids)
            template = 'genHeatMap.html'
    return render(request, 'sumStats/%s'%(template), dataJson)
 
#def detail(request, genotype_id):
 #    genotype = get_object_or_404(Genotype, pk=genotype_id)
  #   return render(request, 'sumStats/detail.html', {'genotype':genotype})
def genHeatMap(request, genotype_ids):

    allGenotypes=[]
    for item in genotype_ids:
        allGenotypes.append(get_object_or_404(Genotype, pk=item))

    allTargetCounts = []
    gNames = []
    for outerItem in allGenotypes:
        allMirs = outerItem.mir_set.all()
        gNames.append(outerItem.genotype_name)
        targetCounts = {}
        for item in allMirs:
            allTargetSet = item.mirtarget_set.all()
            modTargetSet = []
            for innerItem in allTargetSet:
                if innerItem.tScore > 80:
                    modTargetSet.append(innerItem)

            fullName = '%s_%s'%(item.mir_name, item.mir_reg)
            targetCounts[fullName] = float(len(modTargetSet))
        allTargetCounts.append(targetCounts)
            
    allData = pd.DataFrame(allTargetCounts, index=gNames)

    allData = allData.transpose()

    
    pairWiseDist = dist.pdist(allData)
    pairWiseDist = dist.squareform(pairWiseDist) #EXTREMELY IMPORTANT!
    linkage = hier.linkage(pairWiseDist)
    hierarchialOrder = hier.leaves_list(linkage)
    #dataSortedByRowCluster = allData.ix[hierarchialOrder,:]

    #allData = dataSortedByRowCluster

    nRows = allData.shape[0]
    nCols = allData.shape[1]
    PROJECT_ROOT =  os.path.abspath(os.path.dirname(__file__))
    fPath = os.path.join(PROJECT_ROOT, 'static/sumStats/hmpDat.tsv')
    with open(fPath, 'w') as f:
        f.write('row_idx\tcol_idx\tlog2ratio\n')
        for col in range(nCols):
            tempCol = allData.ix[:,col]
            num = 0
            for item in tempCol.iteritems():
                f.write('%d\t%d\t%d\n' %(num+1, col+1, item[1]))
                num+=1
    
    hcrow = list(hierarchialOrder + 1)
    hcrow = ','.join(str(e) for e in hcrow)
    hcrow = '[%s]'%hcrow

    hccol = np.array(range(nCols))+1
    hccol = ','.join(str(e) for e in hccol)
    hccol = '[%s]'%hccol

    cNames = JSON.dumps((list(allData.columns.values)))
    rNames = JSON.dumps(list(allData.index))

    return {'hcrow':hcrow, 'hccol': hccol, 'rowLabel': rNames, 'colLabel': cNames, 'row_number':nRows, 'col_number':nCols}
    
   # return render(request, 'sumStats/genHeatMap.html', context)
