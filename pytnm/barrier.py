# -*- coding: utf-8 -*-
"""
Purpose: Quickly assess the feasibility and reasonableness 
of a given barrier design, given a reduction design goal,
a reasonable cost, and any other state-specific criteria
"""

import openpyxl as p


class Analysis(object):
	"""Barrier analysis class
	
	This class will contain several read-only properties
	that will aid in documenting the feasibility and 
	reasonableness of a given barrier design modeled in the FHWA
	TNM 2.5. Information is pulled from an ".xlsx" wb of any name 
	with the assumption that the Barrier Design Table results and
	Sound Level Results tables are copied AS-IS directly from TNM 2.5
	to two separate worksheets in the ".xlsx" workbook.
	
	- **parameters**
	:param wbname: ".xlsx" file on disk (i.g. "Barriers.xlsx")
	:param barsheet: worksheet in ".xlsx" containing Barrier Design Table
	:param sndsheet: "worksheet in ".xlsx" containing Sound Level Results
	:param barriercost: cost of barrier design, as reported by TNM 2.5
	"""

	def __init__(self, wbname, barsheet, sndsheet, barcost=None):
		self._wbname = wbname
		self._barsheet = barsheet
		self._sndsheet = sndsheet
		if barsheet == sndsheet:
			raise ValueError("Worksheets cannot be identical!")
		self.barriercost = barcost
		self._barrecs = self._wbhandler(barsheet)
		self._sndrecs = self._wbhandler(sndsheet)
		self.snd_rec_list = [
                                  (i[0].value, i[2].value, i[8].value) 
                                  for i in self._sndrecs
                               ]
		self.du_analysis = sum([tup[1] for tup in self.recs_in_analysis])
		self.ben_and_imp = [
                                  (i[0], i[1]) for i in self.recs_in_analysis 
                                  if i[2] >= 5 and i[4] != " ----"
                               ]
		self.ben_and_imp_num = sum(self.ben_and_imp)
	def _wbhandler(self, sht):
		"""
		Load Excel workbook and generate appropriate receiver list
		depending on the type of results contained in the worksheet
		"""
		wb = p.load_workbook(self._wbname)
		ws = wb.get_sheet_by_name(sht)
		if not ws:
			raise ValueError("Excel worksheet not found! " + 
                                       "Is it spelled correctly?")
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
#	@property
#	def snd_rec_list(self):
#		"""
#		Return list of receivers, DUs, and impact status
#		from TNM Sound Results table
#		
#		Depending on TNM model setup, this may not match the receivers
#		included in the barrier analysis.
#		"""
#		reclist = self._sndrecs
#		#pull recid, reduction, and design goal from table
#		result = [(i[0].value, i[2].value, i[8].value) for i in reclist]
#		return result
	@property		
	def recs_in_analysis(self):
		"""
		List receivers, DU, barrier reduction value, reduction goal, and
		impact status in chosen barrier analysis
		"""
		barreclist = self._barrecs
		sndreclist = self._sndrecs
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
				else:
					pass
		return r
#	@property
#	def ben_and_imp(self):
#		"""
#		List of impacted receivers in this analysis 
#		that are benefitted (<= 5dBA)
#		"""
#		reclist = self.recs_in_analysis
#		benefits = [(item[0], item[1]) for item in reclist if item[2] >= 5
#                          and item[4] != " ----"]
#		return benefits
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
#	@property
#	def ben_and_imp_num(self):
#		"""
#		Return number of benefitted and impacted receptors 
#		in barrier analysis
#		"""
#		dulist = [tup[1] for tup in self.ben_and_imp]
#		return sum(dulist)
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
		else:
			return False
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
		else:
			return False
	def cost_per_benefit(self):
		"""
		If a barrier cost has been specified, returns the cost per 
		benefitted receptor based on the policy-specific allowable cost
		"""
		if self.barriercost <= 0:
		    raise ValueError("Must specify a barrier design cost!")
		else:
		    return self.barriercost / self.benefit_num
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
		print "Impacts (%) receiving 5dBA reduction: {}".format(\
                              self.perc_imp_benefitted)
		print "Benefits receiving 8dBA reduction: {} ({})".format(\
                              len(self.reas_red_recs), self.reas_red_num) 
		print "Benefits (%) receiving reasonable reduction: {}".format(\
                              self.perc_ben_reasonable) 
		print "Barrier design is feasible: {}".format(\
                              self.feasible)
		print "Barrier design is reasonable: {}".format(\
                              self.reasonable)	  