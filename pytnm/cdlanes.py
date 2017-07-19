import barrier
from arcpy import da

xlsx = r'U:\Shared\JOBS\KHA\KHA1401 GA 400 CD Lanes\Noise\TNM\2016\Comparison.xlsx'

def benefit_cost(num_receptors, wall_cost):
    result = float(num_receptors) * (55000.0 / float(wall_cost))
    return round(result, 2)

barriers = [1,3,4,5,6,7,8]
old_cost = {1:1838530,
            3:608374,
            4:1023585,
            5:2857249,
            6:2006648,
            7:2341662,
            8:2525999,            
            }

def parcel_addresses(fc):
    """ Pull addresses from feature class """
    sql = """ EP_REC_NO > 0 """
    result =  [r for r in da.SearchCursor(fc, ('EP_REC_NO', 
                                               'Owner', 'Address', 'ZipCode'), sql)]
    return result            

def previous_imp(old, new):    
    old_impacted_benefits = [oi[0] for oi in old.ben_and_imp]
    new_impacted_benefits = [ni[0] for ni in new.ben_and_imp]
    old_impacts = [oi[0] for oi in old.impacted_recs]    
    new_impacts = [ni[0] for ni in new.impacted_recs]
    for old_impacted_benefit in old_impacted_benefits:
        if old_impacted_benefit in new_impacted_benefits:
            pass #old impacted benefit is currently benefitted
        else:
            if not old_impacted_benefit in new_impacts:
                pass #old impacted benefit is no longer impacted
            else:
                print old_impacted_benefit
        
def benefits_to_barrier():
    """ Map benefits to barrier """
    benefit_list = []
    for bar in barriers:
        new_bar = 'Barrier{}_New'.format(bar)
        new_snd = 'May2016_Bld_Results'
        new = barrier.Analysis(xlsx, new_bar, new_snd)
        for benefit in new.benefits:
            benefit_list += [(b[0], bar) for b in new.benefits]
    result = dict(benefit_list)
    return result

def benefits_to_file():
    f = open('benefits.csv', 'wb')
    f.write('Receiver, Barrier\n')
    for bar in barriers:
        old_bar = 'Barrier{}_Old'.format(bar)
        old_snd = 'Dec2014_Bld_Results'
        new_bar = 'Barrier{}_New'.format(bar)
        new_snd = 'May2016_Bld_Results'
        old = barrier.Analysis(xlsx, old_bar, old_snd)
        new = barrier.Analysis(xlsx, new_bar, new_snd)
        new_impacts = new.impact_num
        new_benefits = new.ben_and_imp_num
        print 'Barrier {}'.format(bar), old.impact_num, old.ben_and_imp_num,  '|', new.impact_num, new.ben_and_imp_num
        previous_imp(old, new)
        print 'Barrier {}'.format(bar), benefit_cost(old.ben_and_imp_num, old_cost[bar]), new.ben_and_imp_num
        for benefit in new.benefits:
            f.write('{}, Barrier{}\n'.format(benefit[0], bar))
    f.close()

if __name__ == '__main__':
    pass