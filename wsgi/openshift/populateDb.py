from sumStats.models import Genotype
import ipdb

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

    #ipdb.set_trace()
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

    populate_all_fields('sumStats/static/sumStats/dhpgFxsOnlyUp.txt', 'dhpg_Fxs_only Up')
    populate_all_fields('sumStats/static/sumStats/dhpgFxsOnlyDown.txt', 'dhpg_Fxs_only Down')
    
    populate_all_fields('sumStats/static/sumStats/dhpgWtOnlyUp.txt', 'dhpg_WT_only Up')
    populate_all_fields('sumStats/static/sumStats/dhpgWtOnlyDown.txt', 'dhpg_WT_only Down')
    
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapSameDirUp.txt', 'dhpg_FXS_wt common_same_dir Up')
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapSameDirDown.txt', 'dhpg_FXS_wt common_same_dir Down')

    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapOppositeDirFxsUpWtDown.txt', 'dhpg_FXS_wt common_opp_dir fxs_Up Wt_down')
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapOppositeDirFxsDownWtUp.txt', 'dhpg_FXS_wt common_opp_dir fxs_Down Wt_Up')
