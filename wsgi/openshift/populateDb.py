from sumStats.models import Genotype
import ipdb
from django.utils import timezone

def populate_all_fields(fileName, genoTypeName):
        
    genotype = Genotype.objects.create(genotype_name=genoTypeName, pub_date=timezone.now())
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

    populate_all_fields('sumStats/static/sumStats/dhpgFxsOnlyUp.txt', 'A_Up')#'dhpg_Fxs_only Up')
    populate_all_fields('sumStats/static/sumStats/dhpgFxsOnlyDown.txt', 'A_Down')#'dhpg_Fxs_only Down')
    
    populate_all_fields('sumStats/static/sumStats/dhpgWtOnlyUp.txt', 'B_Up')#'dhpg_WT_only Up')
    populate_all_fields('sumStats/static/sumStats/dhpgWtOnlyDown.txt', 'B_Down')#'dhpg_WT_only Down')
    
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapSameDirUp.txt', 'A_int_B_Up')#'dhpg_FXS_wt common_same_dir Up')
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapSameDirDown.txt', 'A_int_B_Down')#'dhpg_FXS_wt common_same_dir Down')

    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapOppositeDirFxsUpWtDown.txt', 'A_int_B A_Up_B_Down')#'dhpg_FXS_wt common_opp_dir fxs_Up Wt_down')
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapOppositeDirFxsDownWtUp.txt', 'A_int_B A_Down_B_Up')#'dhpg_FXS_wt common_opp_dir fxs_Down Wt_Up')

    populate_all_fields('sumStats/static/sumStats/dhpgFxsOnlyUp3C.txt', 'A_Up 3C') #'dhpg_Fxs_only Up 3C'
    populate_all_fields('sumStats/static/sumStats/dhpgFxsOnlyDown3C.txt', 'A_Down 3C')#'dhpg_Fxs_only Down 3C'
    
    populate_all_fields('sumStats/static/sumStats/dhpgWtOnlyUp3C.txt', 'B_Up 3C')#'dhpg_WT_only Up 3C'
    populate_all_fields('sumStats/static/sumStats/dhpgWtOnlyDown3C.txt', 'B_Down 3C')#'dhpg_WT_only Down 3C'
    
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapSameDirUp3C.txt', 'A_int_B_Up 3C')#'dhpg_FXS_wt common_same_dir Up 3C'
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapSameDirDown3C.txt', 'A_int_B_Down 3C')#'dhpg_FXS_wt common_same_dir Down 3C'

    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapOppositeDirFxsUpWtDown3C.txt', 'A_int_B A_Up_B_Down 3C')#'dhpg_FXS_wt common_opp_dir fxs_Up Wt_down'
    populate_all_fields('sumStats/static/sumStats/dhpgFxsWtOverlapOppositeDirFxsDownWtUp3C.txt', 'A_int_B A_Down_B_Up 3C')#'dhpg_FXS_wt common_opp_dir fxs_Down Wt_Up'
