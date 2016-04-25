import barrier

xlsx = r'C:\TNM25\KHA_1605\Comparison.xlsx'

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


for bar in barriers:
    old_bar = 'Barrier{}_Old'.format(bar)
    old_snd = 'Barrier{}_Old_Snd'.format(bar)
    new_bar = 'Barrier{}_New'.format(bar)
    new_snd = 'Barrier{}_New_Snd'.format(bar)
    old = barrier.Analysis(xlsx, old_bar, old_snd)
    new = barrier.Analysis(xlsx, new_bar, new_snd)
    print 'Barrier {}'.format(bar), benefit_cost(old.ben_and_imp_num, old_cost[bar]), new.benefit_num

#bar1_old = barrier.Analysis(xlsx, 'Barrier1_Old', 'Barrier1_Old_Snd')
#bar1_new = barrier.Analysis(xlsx, 'Barrier1_New', 'Barrier1_New_Snd')
#
#bar3_old = barrier.Analysis(xlsx, 'Barrier3_Old', 'Barrier3_Old_Snd')
#bar3_new = barrier.Analysis(xlsx, 'Barrier3_New', 'Barrier3_New_Snd')
#
#bar4_old = barrier.Analysis(xlsx, 'Barrier4_Old', 'Barrier4_Old_Snd')
#bar4_new = barrier.Analysis(xlsx, 'Barrier4_New', 'Barrier4_New_Snd')
#
#bar5_old = barrier.Analysis(xlsx, 'Barrier5_Old', 'Barrier5_Old_Snd')
#bar5_new = barrier.Analysis(xlsx, 'Barrier5_New', 'Barrier5_New_Snd')
#
#bar6_old = barrier.Analysis(xlsx, 'Barrier6_Old', 'Barrier6_Old_Snd')
#bar6_new = barrier.Analysis(xlsx, 'Barrier6_New', 'Barrier6_New_Snd')
#
#bar7_old = barrier.Analysis(xlsx, 'Barrier7_Old', 'Barrier7_Old_Snd')
#bar7_new = barrier.Analysis(xlsx, 'Barrier7_New', 'Barrier7_New_Snd')
#
#bar8_old = barrier.Analysis(xlsx, 'Barrier8_Old', 'Barrier8_Old_Snd')
#bar8_new = barrier.Analysis(xlsx, 'Barrier8_New', 'Barrier8_New_Snd')


#l = bar1_new.recs_analysis
#old_benefits = bar1_old.benefits
#new_benefits = bar1_new.benefits
#
#l = bar3_new.recs_analysis
#old_benefits = bar3_old.benefits
#new_benefits = bar3_new.benefits
#
#l = bar4_new.recs_analysis
#old_benefits = bar4_old.benefits
#new_benefits = bar4_new.benefits
#
#l = bar5_new.recs_analysis
#old_benefits = bar5_old.benefits
#new_benefits = bar5_new.benefits
#
#l = bar6_new.recs_analysis
#old_benefits = bar6_old.benefits
#new_benefits = bar6_new.benefits

#l = bar7_new.recs_analysis
#old_benefits = bar7_old.benefits
#new_benefits = bar7_new.benefits
#
#l = bar8_new.recs_analysis
#old_benefits = bar8_old.benefits
#new_benefits = bar8_new.benefits


#for rec in old_benefits:
#    if rec in new_benefits:
#        pass
#    else:
#        print rec
#        
#print len(old_benefits)
#print len(new_benefits)