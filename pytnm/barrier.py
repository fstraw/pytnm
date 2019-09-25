# -*- coding: utf-8 -*-
"""
Purpose: Quickly assess the feasibility and reasonableness 
of a given barrier design, given a reduction design goal,
a reasonable cost, and any other state-specific criteria
"""

import os
import sys
import openpyxl as p


def rds_to_list(ws):
    """
    Returns filtered list of roads    
    :param ws: 
    :return: road_list
    """    
    roads_ws = ws
    rds = []
    for row in roads_ws.rows:
        vals = [cell.value for cell in row]
        rds.append(vals)
    rds_no_header = rds[15:] #clip TNM2.5 header
    roads = []
    for rd in rds_no_header:
        rd_name = rd[1]
        rd_width = rd[2]
        pnt = rd[4].strip()
        x, y, z = rd[6], rd[7], rd[8]
        #check for empty end rows
        if None in (x, y, z):
            break
        if rd_name:
            roads.append([rd_name.strip(), rd_width, [[pnt,[x, y, z]]]])
            found_road = True
        else:
            found_road = False
            if not found_road:
                roads[-1][2].append([pnt,[x, y, z]])
    return roads

def _validate_xlsx(xlsx):
	pass

def _read_roadways(xlsx):
	workbook = p.load_workbook(xlsx)
	try:
		roadways_worksheet = [ws for ws in workbook.worksheets if ws['B5'].value == 'INPUT: ROADWAYS'][0]
	except IndexError:
		print('Roadways worksheet not found') # assume roadways does not exist
	return(rds_to_list(roadways_worksheet))

class Roadway(object):
	pass

class Receiver(object):
	pass

class Barrier(object):
	pass

class TerrainLine(object):
	pass

class BuildingRow(object):
	pass


class Model(object):
	"""[summary]
	
	>> build_run = pytnm.Model(string(.xlsx))
	>> print(build_run.info)
	>> '(('Build Run', 'Project', 'Company', 'Analyst', 'Date'))
	>> roadways = build_run.roadways
	>> roadway = roadways[0]
	>> print(roadway.name)
	>> 'I-10 On Ramp 1'
	>> print(roadway.width)
	>> 22
	>> print(roadway.geometry)
	>> ((123456, 4355422, 12), (123456, 4355422, 15), (123456, 4355422, 12))
	>> print(roadway.traffic)
	>> (125, 10, 5, 3, 1)
	>> print(roadway.traffic.autos)
	>> 125
	>> print(roadway.traffic.autos.speed)
	>> 45

	Arguments:
		object {[type]} -- [description]
	"""

	def __init__(self, worksheet_template):
		pass

class Analysis(object):
	"""Barrier analysis class
	
	This class will contain several read-only properties
	that will aid in documenting the feasibility and 
	reasonableness of a given barrier design modeled in the FHWA
	TNM 2.5. Information is pulled from an ".xlsx" wb of any name 
	with the assumption that the Barrier Design Table results and
	Sound Level Results tables are copied AS-IS directly from TNM 2.5
	to two separate worksheets in the ".xlsx" workbook.
	
	:param wbname: ".xlsx" file on disk (i.g. "Barriers.xlsx")
	:param barsheet: worksheet in ".xlsx" containing Barrier Design Table
	:param sndsheet: "worksheet in ".xlsx" containing Sound Level Results
	:param barriercost: cost of barrier design, as reported by TNM 2.5
	"""

	def __init__(self, wbname, barsheet, sndsheet, barcost=0):
		self._wbname = wbname
		self._barsheet = barsheet
		self._sndsheet = sndsheet
		if barsheet == sndsheet:
			raise ValueError("Worksheets cannot be identical!")
		self.barriercost = barcost
		self._barrecs = self._wbhandler(barsheet)
		self._sndrecs = self._wbhandler(sndsheet)
		"""Receivers listed in the Sound Results worksheet"""
		self.snd_rec_list = [
                                  (i[0].value, i[2].value, i[8].value) 
                                      for i in self._sndrecs
                               ]
		self.impacted_recs = [(i[0], i[1]) for i in self.recs_analysis 
                                      if i[4] != " ----"
                                ]
		self.impact_num = sum([tup[1] for tup in self.impacted_recs])
		self.du_analysis = sum([tup[1] for tup in self.recs_analysis])
		self.benefitted =  [
                                  (i[0], i[1]) for i in self.recs_analysis 
                                      if i[2] >= 5
                              ]
		self.benefit_num = sum([tup[1] for tup in self.benefitted])
		self.ben_and_imp = [
                                  (i[0], i[1]) for i in self.recs_analysis 
                                      if i[2] >= 5 and i[4] != " ----"
                               ]
		self.ben_and_imp_num = sum([tup[1] for tup in self.ben_and_imp])
		self.reas_red_recs = [
                                  (i[0], i[1]) for i in self.recs_analysis
                                      if i[2] >= i[3]
                                ]
		self.reas_red_num = sum([tup[1] for tup in self.reas_red_recs])
	def _wbhandler(self, sht):
		"""
		Load Excel workbook and generate appropriate receiver list
		depending on the type of results contained in the worksheet
		"""
		wb = p.load_workbook(self._wbname)
		ws = wb.get_sheet_by_name(sht)
		if not ws:
			raise ValueError("Excel worksheet not found!" + 
                                       "Is it spelled correctly?")
		if sht == self._barsheet:
			lastrow = ws.max_row
			#assumes copied from TNM bar sound results in cell A1
			datarange = 'B18:L{}'.format(lastrow)
		elif sht == self._sndsheet:
			#omit last 8 rows in snd results
			lastrow = ws.max_row - 8
			datarange = 'B20:N{}'.format(lastrow)
		reclist = list(ws.iter_rows(range_string=datarange))
		return reclist
	@property		
	def recs_analysis(self):
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
		return sorted(r)
	@property
	def benefits(self):
		"""
		Return tuple of benefited receiver/receptor counts
		"""
		return [(r[0], r[1]) for r in self.recs_analysis
					if r[2] >= 5]
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
		    return 0
		else:
		    return self.barriercost / self.benefit_num
	def report(self):
		"""
		Report of results. Useful for report writing or debugging.
		"""
		pass
		# print("Receivers/receptors in barrier analysis: {} ({})".format(\
        #                       len(self.recs_analysis), self.du_analysis))
		# print "Impacts in barrier analysis: {} ({})".format(\
        #                       len(self.impacted_recs), self.impact_num)
		# print "Benefits in barrier analysis: {} ({})".format(\
        #                       len(self.benefitted), self.benefit_num)
		# print "Number of impacts receiving 5dBA reduction: {}".format(\
        #                       self.ben_and_imp_num)
		# print "Impacts (%) receiving 5dBA reduction: {}".format(\
        #                       self.perc_imp_benefitted)
		# print "Benefits receiving 8dBA reduction: {} ({})".format(\
        #                       len(self.reas_red_recs), self.reas_red_num) 
		# print "Benefits (%) receiving reasonable reduction: {}".format(\
        #                       self.perc_ben_reasonable) 
		# print "Barrier design is feasible: {}".format(\
        #                       self.feasible)
		# print "Barrier design is reasonable: {}".format(\
        #                       self.reasonable)

# class GAAnalysis(Analysis):
#     def __init__(self, wbname, barsheet, sndsheet, barcost=0):
#         super(GAAnalysis, self).__init__(wbname, barsheet, sndsheet, barcost=0)
# 	@property
# 	def feasible(self):
# 		"""
#         Barrier design is feasible if one or more of impacted receivers
#         receive a 5dBA or more noise reduction
#         """
#         if self.ben_and_imp_num >= 1:
#             return True
#         return False

# 	@property
# 	def reasonable(self):
# 		"""
#         Barrier design is reasonable if 80% or more of benefitted receivers
#         receive a 8dBA or more noise reduction
#         """
# 		perc_crit = self.benefit_num * 0.80
# 		if perc_crit == 0:
# 			return False
# 		elif self.reas_red_num >= perc_crit:
# 			return True
# 		else:
# 			return False

if __name__ == '__main__':
	os.chdir(os.path.dirname(__file__))
	model_xlsx = '../files/tnm_model.xlsx'
	print(_read_roadways(model_xlsx))