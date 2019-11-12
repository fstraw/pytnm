from os import path

import pytest
from pytnm.barrier import Analysis

wbname = path.join(path.dirname(__file__), "test_files\\test.xlsx")
print(wbname)
#Barrier description worksheet
bardessheet = "Sheet1"
#Model sound results that correspond with barrier description worksheet.
#These results may include receivers that are not part of the barrier
#analysis, but are part of the model run. This will be the case if one
#TNM model contains several barrier designs.
sndressheet = "Bars1_2_3_Snd"
b = Analysis(wbname, bardessheet, sndressheet)

def test_recs_in_analysis_not_empty():
	"""
	There should be some receivers in the excel sheet to analyze
	"""
	receiver_list_length = len(b.snd_rec_list)
	pytest.assert_true(receiver_list_length > 0)

def test_impacts_included_in_analysis():
	"""
	There should be some impacted receivers in the excel sheet to analyze,
      otherwise, why are you doing a barrier analysis, silly?
	
	This test may also reveal any copy/paste errors in the spreadsheet
	"""
	impacted_list_length = len(b.impacted_recs)
	nose.tools.assert_true(impacted_list_length > 0)
	
def test_filter_barrier_receivers_from_tnm_sound_results():
	"""
	Barrier analysis receiver list should not include receivers from
	TNM sound results that are not part of the individual barrier
	analysis.	
	"""
	analysis_receivers = b.snd_rec_list
	filtered_impacts_from_snd_results = b.impacted_recs
	analysis_length = len(analysis_receivers)
	filtered_length = len(filtered_impacts_from_snd_results)
	nose.tools.assert_true(analysis_length >= filtered_length)

#def test_cost_per_benefit_method_requires_barrier_cost():
#    """
#    Because barrier cost is an optional parameter, it will be
#    easy to forget if this information is required.
#    """
#    b.barriercost = 0    
#    nose.tools.assert_raises(ValueError, b.cost_per_benefit)

def test_user_can_change_du():
    b.du_analysis = 5
    nose.tools.assert_true(b.du_analysis == 5)

def test_vals_correct_from_known_test_xlsx():
    bsheet = "Sheet7"
    ssheet = "Bars4_5_6_7_8_Snd"
    b = Analysis(wbname, bsheet, ssheet)
    nose.tools.assert_true(len(b.recs_analysis) == 8)
    nose.tools.assert_true(len(b.impacted_recs) == 3)
    nose.tools.assert_true(b.impact_num == 6)
    nose.tools.assert_true(b.du_analysis == 15)
    nose.tools.assert_true(len(b.benefitted) == 6)
    nose.tools.assert_true(b.benefit_num == 11)
    nose.tools.assert_true(len(b.ben_and_imp) == 3)
    nose.tools.assert_true(b.ben_and_imp_num == 6)
    nose.tools.assert_true(len(b.reas_red_recs) == 2)
    nose.tools.assert_true(b.reas_red_num == 4)