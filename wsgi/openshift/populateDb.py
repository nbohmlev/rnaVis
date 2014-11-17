from sumStats.models import Genotype

def populate_all_fields(fileName, genoTypeName):
    
    
    genotype = Genotype.objects.get(genotype_name=genoTypeName)
    allModels={'sequencelength': 1, 
               'sequencegc': 2,
               'codingseqlength': 3,
               'codingseqgc': 4,
               'fiveutrlength': 5,
               'fiveutrgc': 6,
               'threeutrlength': 7,
               'threeutrgc': 8}

    for key, value in allModels.iteritems():
        exec('genotype.%s_set.all().delete()' % key) ##(DANGER!!!)
        with open(fileName, 'rU') as f:
            next(f)
            for line in f:
                ll = line.split()
                exec('genotype.%s_set.create(seqName=ll[0], seqLen=float(ll[%s])).save()' % (key, value))
        
if __name__=="__main__":
    populate_all_fields('sumStats/static/sumStats/fxsUp.txt', 'fmr1_up')
    populate_all_fields('sumStats/static/sumStats/fxsDown.txt', 'fmr1_down')
            
