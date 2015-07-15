# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:14:37 2015

Purpose: Quickly assess the feasibility and reasonableness 
of a given barrier design, given a reduction design goal,
a reasonable cost, and any other state-specific criteria

@author: Brandon
"""

import openpyxl as p


class Analysis(object):
	def __init__(self, wbname, barsheet, sndsheet, barcost=None):
		self._wbname = wbname
		self._barsheet = barsheet
		self._sndsheet = sndsheet
		if barsheet == sndsheet:
			raise ValueError("Worksheets cannot be identical!")
		self.barriercost = barcost
		self._barrecs = self._wbhandler(barsheet)
		self._sndrecs = self._wbhandler(sndsheet)
	def _wbhandler(self, sht):
		"""
		Load Excel workbook and generate appropriate receiver list
		depending on the type of results contained in the worksheet
		"""
		wb = p.load_workbook(self._wbname)
		ws = wb.get_sheet_by_name(sht)
#		if not ws:
#			raise ValueError("Excel worksheet not found! " + 
#                                       "Is it spelled correctly?")
		if sht == self._barsheet:
			lastrow = ws.get_highest_row()
			#assumes copied from TNM bar sound results in cell A1
			datarange = 'B18:L{}'.format(lastrow)
		elif sht == self._sndsheet:
			#omit last 8 rows in snd results
			lastrow = ws.get_highest_row() - 8
			datarange = 'B20:N{}'.format(lastrow)
		reclist = list(ws.iter_rows(range_string=datarange))
		return reclist
	@property
	def snd_rec_list(self):
		"""
		Return list of receivers, DUs, and impact status
		from TNM Sound Results table
		
		Depending on TNM model setup, this may not match the receivers
		included in the barrier analysis.
		"""
		reclist = self._sndrecs
		#pull recid, reduction, and design goal from table
		result = [(i[0].value, i[2].value, i[8].value) for i in reclist]
		return result
	@property		
	def recs_in_analysis(self):
		"""
		List receivers, DU, barrier reduction value, reduction goal, and
		impact status in chosen barrier analysis
		"""
		reclist = self._barrecs
		#pull recid, reduction, and design goal from barrier design table
		recs = [(i[0].value, i[3].value, i[4].value) for i in reclist]
		result = []
		for rec in self.snd_rec_list:
			for r in recs:
				if rec[0] == r[0]:
					result.append((rec[0], rec[1], r[1], r[2], rec[2]))
				pass
		return result
	@property		
	def recs_in_analysis_test(self):
		"""
		List receivers, DU, barrier reduction value, reduction goal, and
		impact status in chosen barrier analysis
		"""
		barreclist = self._barrecs
		sndreclist = self._sndrecs
		#pull recid, reduction, and design goal from barrier design table
#		recs = [(i[0].value, i[3].value, i[4].value) for i in reclist]
		r = []
		for barrec in barreclist:
			rec = barrec[0].value
			barred = barrec[3].value
			redgoal = barrec[4].value
			for sndrec in sndreclist:
				if rec == sndrec[0].value:
					du = sndrec[2].value
					impstat = sndrec[8].value
					r.append((rec, du, barred, redgoal, impstat))
				pass
		return r
	@property
	def du_in_analysis(self):
		"""
		Number of receptors in this analysis 
		"""
		dulist = [tup[1] for tup in self.recs_in_analysis]
		return sum(dulist)
	@property
	def ben_and_imp(self):
		"""
		List of impacted receivers in this analysis 
		that are benefitted (<= 5dBA)
		"""
		reclist = self.recs_in_analysis
		benefits = [(item[0], item[1]) for item in reclist if item[2] >= 5
                          and item[4] != " ----"]
		return benefits
	@property
	def benefitted(self):
		"""
		List any receivers in this analysis that are benefitted (<= 5dBA)
		"""
		reclist = self.recs_in_analysis
		benefits = [(item[0], item[1]) for item in reclist if item[2] >= 5]
		return benefits
	@property
	def reas_red_recs(self):
		"""
		List receivers from this barrier analysis that are receiving
		a reasonable noise reduction, as determined by the noise reduction
		design goal
		"""
		reclist = self.recs_in_analysis
		reasredlist = [(i[0], i[1]) for i in reclist if i[2] >= i[3]]
		return reasredlist
	@property
	def impacted_recs(self):
		"""
		List impacted receivers that are part of this barrier analysis
		"""
		reclist = self.recs_in_analysis
		result = [(i[0], i[1]) for i in reclist if i[4] != " ----"]
		return result
	@property
	def impact_num(self):
		"""
		Return number of impacted receptors in barrier analysis
		"""
		dulist = [tup[1] for tup in self.impacted_recs]
		return sum(dulist)
	@property
	def benefit_num(self):
		"""
		Return number of benefitted receptors in barrier analysis
		"""
		dulist = [tup[1] for tup in self.benefitted]
		return sum(dulist)
	@property
	def ben_and_imp_num(self):
		"""
		Return number of benefitted and impacted receptors 
		in barrier analysis
		"""
		dulist = [tup[1] for tup in self.ben_and_imp]
		return sum(dulist)
	@property
	def reas_red_num(self):
		"""
		Return number of benefitted receptors in barrier analysis
		that are receiving a reasonable noise reduction
		"""
		dulist = [tup[1] for tup in self.reas_red_recs]
		return sum(dulist)
	@property
	def perc_imp_benefitted(self):
		"""
		Return percentage of total receivers in barrier analysis that
		receive a 5 dBA reduction
		"""
		perc = float(self.ben_and_imp_num) / float(self.impact_num)
		return "{:.0%}".format(perc)
	@property
	def perc_ben_reasonable(self):
		"""
		Return percentage of benefits in barrier analysis that
		receive an reasonable reduction
		"""
		if self.benefit_num == 0:
			perc = 0
		else:
			perc = float(self.reas_red_num) / float(self.benefit_num)
		return "{:.0%}".format(perc)
	@property
	def feasible(self):
		"""
		Barrier design is feasible if 75% or more of impacted receivers
		receive a 5dBA or more noise reduction
		"""
		perc_crit = self.impact_num * 0.75
		if self.benefit_num >= perc_crit:
			return True
#			return perc_crit
		else:
			return False
#			return perc_crit
	@property
	def reasonable(self):
		"""
		Barrier design is reasonable if 80% or more of benefitted receivers
		receive a 8dBA or more noise reduction
		"""
		perc_crit = self.benefit_num * 0.80
		if perc_crit == 0:
			return False
		elif self.reas_red_num >= perc_crit:
			return True
#			return perc_crit
		else:
			return False
#			return perc_crit
	def report(self):
		"""
		Report of results. Useful for report writing or debugging.
		"""
		print "Receivers/receptors in barrier analysis: {} ({})".format(\
                              len(self.recs_in_analysis), self.du_in_analysis)
		print "Impacts in barrier analysis: {} ({})".format(\
                              len(self.impacted_recs), self.impact_num)
		print "Benefits in barrier analysis: {} ({})".format(\
                              len(self.benefitted), self.benefit_num)
		print "Number of impacts receiving 5dBA reduction: {}".format(\
                              self.ben_and_imp_num)
		print "%  of impacts receiving 5dBA reduction: {}".format(\
                              self.perc_imp_benefitted)
		print "Number of benefits receiving 8dBA reduction: {} ({})".format(\
                              len(self.reas_red_recs), self.reas_red_num) 
		print "%  of benefits receiving reasonable reduction: {}".format(\
                              self.perc_ben_reasonable) 
		print "Barrier design is feasible: {}".format(\
                              self.feasible)
		print "Barrier design is reasonable: {}".format(\
                              self.reasonable)

#l = [
#    ("Sheet1", "Bars1_2_3_Snd"),
#    ("Sheet2", "Bars1_2_3_Snd"),
#    ("Sheet3", "Bars1_2_3_Snd"),
#    ("Sheet4", "Bars4_5_6_7_8_Snd"),
#    ("Sheet5", "Bars4_5_6_7_8_Snd"),
#    ("Sheet6", "Bars4_5_6_7_8_Snd"),
#    ("Sheet7", "Bars4_5_6_7_8_Snd"),
#    ("Sheet8", "Bars4_5_6_7_8_Snd"),
#    ]
#wbname = "./tests/test_files/test.xlsx"
#for bar in l:
#    print "Barrier {}".format(l.index(bar) + 1)
#    b = Analysis(wbname, bar[0], bar[1])
#    b.report()
#    print ("-"*20)

wbname = r"U:\Brandon Batt\!!!ICE1401\CompletedRuns\Barrier_Analysis.xlsx"

b = Analysis(wbname, "Bar20_Analysis", "Bar20_21Snd")
b.report()
