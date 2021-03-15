# -*- coding: utf-8 -*-
"""
Purpose: Quickly assess the feasibility and reasonableness 
of a given barrier design, given a reduction design goal,
a reasonable cost, and any other state-specific criteria
"""

import os
import sys
import openpyxl as p


def _xlsx_to_traffic(ws):
    """Converts .xlsx spreadsheet of TNM Traffic to dictionary
	
	Arguments:
		ws {openpyxl.worksheet} -- [description]
	
	Returns:
		[type] -- [description]
	"""
    filter_rows = 7 ##omit these rows at start of spreadsheet    
    traf_ws = ws
    traf_dict = dict([(r[1].value.strip(), ((r[5].value, r[6].value), (r[7].value, r[8].value), (r[9].value, r[10].value)))
                    for r in traf_ws.rows if r[1].value][filter_rows:])
    return traf_dict

def _barriers_to_list(ws):
    """Returns filtered list of barriers
	
	Arguments:
		ws {openpyxl.worksheet} -- [description]
	
	Returns:
		[type] -- [description]
	"""
    barriers_ws = ws
    bars = []
    for row in barriers_ws.rows:
        vals = [cell.value for cell in row]
        bars.append(vals)
    bars_no_header = bars[15:] # clip TNM2.5 header
    barriers = []
    for bar in bars_no_header:
        bar_name, bar_max_height, square_foot_cost = bar[1], bar[4], bar[5]
        x, y, z = bar[13], bar[14], bar[15]
        # check for empty end rows
        if None in (x, y, z):
            break
        if bar_name:
            barriers.append((bar_name, bar_max_height, square_foot_cost, [(x, y, z)]))
            found_bar = True
        else:
            found_bar = False
            if not found_bar:
                barriers[-1][3].append((x, y, z))
    return barriers

def _receivers_to_list(ws):
	receivers_raw = []	
	for row in ws.rows:
		vals = [cell.value for cell in row]
		receivers_raw.append(vals)
	receivers_no_header = receivers_raw[16:] # clip TNM2.5 header
	receivers = []
	for receiver in receivers_no_header:
		rec_id = receiver[1]
		receptors = receiver[3]
		x, y, z = receiver[4], receiver[5], receiver[6]
		height = receiver[7]
		nac_level = receiver[9]
		if None in (x, y, z):
			break
		else:
			receivers.append((rec_id.strip(), receptors, height, nac_level, (x, y, z)))
	return receivers
			
def _rds_to_list(ws):
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
    rds_no_header = rds[15:] # clip TNM2.5 header
    roads = []
    for rd in rds_no_header:
        rd_name = rd[1]
        rd_width = rd[2]
        pnt = rd[4].strip()
        x, y, z = rd[6], rd[7], rd[8]
        # check for empty end rows
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
		print('Roadways worksheet not found')
	return(_rds_to_list(roadways_worksheet))

def _read_traffic(xlsx):
	workbook = p.load_workbook(xlsx)
	try:
		traffic_worksheet = [ws for ws in workbook.worksheets if ws['B5'].value == 'INPUT: TRAFFIC FOR LAeq1h Volumes'][0]
	except IndexError:
		print('Traffic worksheet not found')
	return(_xlsx_to_traffic(traffic_worksheet))

def _read_receivers(xlsx):
	workbook = p.load_workbook(xlsx)
	try:
		receiver_worksheet = [ws for ws in workbook.worksheets if ws['B5'].value == 'INPUT: RECEIVERS'][0]
	except IndexError:
		print('Receiver worksheet not found')
	return(_receivers_to_list(receiver_worksheet))

def _read_barriers(xlsx):
	workbook = p.load_workbook(xlsx)
	try:
		barrier_worksheet = [ws for ws in workbook.worksheets if ws['B5'].value == 'INPUT: BARRIERS'][0]
	except IndexError:
		print('Barrier worksheet not found')
	return(_barriers_to_list(barrier_worksheet))

class VehicleClassification(object):
	def __init__(self, volume, speed):
		self.volume = volume
		self.speed = speed

class Auto(VehicleClassification):
	def __repr__(self):
		return 'Auto'

class Medium(VehicleClassification):
	def __repr__(self):
		return 'Medium'

class Heavy(VehicleClassification):
	def __repr__(self):
		return 'Heavy'

class Traffic(object):
	"""Represents Traffic TNM object
	
	Arguments:
		object {[type]} -- [description]
	
	Returns:
		[type] -- [description]
	"""
	def __init__(self, auto, medium, heavy, bus=None, motorcycle=None):
		self.auto = auto
		self.medium = medium
		self.heavy = heavy
		self.bus = bus
		self.motorcycle = motorcycle
	def __repr__(self):
		return self.auto

class Roadway(object):
	"""Represents Roadway TNM object
	
	Arguments:
		object {[type]} -- [description]
	
	Returns:
		[type] -- [description]
	"""
	def __init__(self, name, width, points, traffic=None):
		self.name = name
		self.width = width
		self.points = points
		self.traffic = traffic
		self.geometry = None
	def __repr__(self):
		return self.name


class Receiver(object):
	"""Represents Receiver TNM object
	
	Arguments:
		object {[type]} -- [description]
	"""
	def __init__(self, rec_id, receptors, height, nac_level, geometry, nac=None):
		self.rec_id = rec_id
		self.receptors = receptors
		self.height = height
		self.nac_level = nac_level
		self.geometry = geometry
	def __repr__(self):
		return self.rec_id

class Barrier(object):
	"""Represents Barrier TNM object
	
	Arguments:
		object {[type]} -- [description]
	
	Returns:
		[type] -- [description]
	"""
	def __init__(self, name, max_height, geometry, square_foot_cost=0):
		self.name = name
		self.max_height = max_height
		self.geometry = geometry
		self.square_foot_cost = square_foot_cost
	def __repr__(self):
		return self.name

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
	>> print(roadway.traffic.auto)
	>> 125
	>> print(roadway.traffic.auto.speed)
	>> 45

	Arguments:
		object {[type]} -- [description]
	"""

	def __init__(self, xlsx):
		self.TRAFFIC = _read_traffic(xlsx)
		self._roads = _read_roadways(xlsx)
		self._receivers = _read_receivers(xlsx)
		self._barriers = _read_barriers(xlsx)
	
	@property
	def barriers(self):
		barriers = []
		for barrier in self._barriers:
			name = barrier[0]
			max_height = barrier[1]
			geometry = barrier[2]
			barriers.append(Barrier(name, max_height, geometry))		
		return barriers

	@property
	def receivers(self):
		receivers = []		
		for receiver in self._receivers:
			rec_id = receiver[0]
			receptors = receiver[1]			
			height = receiver[2]
			nac_level = receiver[3]
			x, y, z = receiver[4]
			receivers.append(Receiver(rec_id, receptors, height, nac_level, geometry=(x, y, z)))
		return receivers

	@property	
	def roadways(self):
		roads = []
		for road in self._roads:
			name = road[0]
			width = road[1]
			points = road[2]
			autos = self.TRAFFIC[name][0]
			medium = self.TRAFFIC[name][1]
			heavy = self.TRAFFIC[name][2]
			traffic = Traffic(Auto(autos[0], autos[1]), Medium(medium[0], medium[1]), Heavy(heavy[0], heavy[1]))
			roads.append(Roadway(name, width, points, traffic))
		return roads		

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
	:param sndsheet: "worksheet in ".xlsx" containing Sound Level Results
	:param barriercost: cost of barrier design, as reported by TNM 2.5
	"""

	def __init__(self, wbname, sndsheet, barcost=0):
		self._wbname = wbname
		self._sndsheet = sndsheet
		self.barriercost = barcost		
		self._sndrecs = self._wbhandler(sndsheet)
		"""Receivers listed in the Sound Results worksheet"""
		self.snd_rec_list = [(f"{i[0].value}".strip(), i[2].value, i[8].value.strip()) for i in self._sndrecs]
		self.impacted_recs = [i for i in self.snd_rec_list if i[2] != "----"]
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
		# omit last 8 rows in snd results
		lastrow = ws.max_row - 8
		# limit to appropriate columns 
		reclist = list(ws.iter_rows(min_col=2, max_col=14, min_row=20, max_row=lastrow))
		return reclist
	@property		
	def recs_analysis(self):
		"""
		List receivers, DU, barrier reduction value, reduction goal, and
		impact status in chosen barrier analysis
		"""
		sndreclist = self._sndrecs
		return [("1A", 1, 5.5, 8, " ----")]
		# return (rec, du, barred, redgoal, impstat)
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

class LouisianaAnalysis(Analysis):

	def barrier_segments(self):
		"""
		"""
		wb = p.load_workbook(self._wbname)
		ws = wb.get_sheet_by_name("Barrier_Segments")
		if not ws:
			raise ValueError("Excel worksheet not found!" + 
                                       "Is it spelled correctly?")
		lastrow = ws.max_row
		# limit to appropriate columns 
		barrierlist = list(ws.iter_rows(min_col=2, max_col=14, min_row=16, max_row=lastrow))
		return barrierlist

	def _barrier_names(self):
		barrier_names = {}		
		for barrier in self.barrier_segments():
			barrier_name = barrier[0].value
			if barrier_name:
				barrier_names[barrier_name] = {}		
		return barrier_names
	
	def _barrier_infos(self):
		"""[summary]
		{ barrier: [(hgt, length, sqft)] }
		Returns:
			[list]: [[{ barrier: [(hgt, length, sqft)] }]]
		"""
		barrier_list = []
		barrier_info = {}
		barrier_tag = ""
		row_count = (len(self.barrier_segments()))
		for idx, row in enumerate(self.barrier_segments()):
			barrier_name = row[0].value
			barrier_point = row[4].value
			barrier_height = row[6].value
			barrier_length = row[8].value
			barrier_sq_footage = row[9].value			
			if (barrier_name and barrier_point): # check for barrier name or last row
				barrier_tag = barrier_name.strip()
				barrier_dimensions = (barrier_length, barrier_height, barrier_sq_footage)
				barrier_info[barrier_name.strip()] = []			
				barrier_info[barrier_name.strip()].append(barrier_dimensions)
			elif barrier_point:
				barrier_dimensions = (barrier_length, barrier_height, barrier_sq_footage)
				if (idx == row_count - 1): # deal with last row					
					barrier_info[barrier_tag].append(barrier_dimensions)
					barrier_list.append(barrier_info)
				barrier_info[barrier_tag].append(barrier_dimensions)
			elif not barrier_point:				
				barrier_list.append(barrier_info)			
				barrier_info = {}
		return barrier_list

	def _barrier_dimensions(self):
		"""[summary]

		Returns:
			[dict]: [{ barrier: {hgt: sqfootage, hgt:sqfootage, ...} }]
		"""
		barrier_info = {}
		for barrier in self._barrier_infos():
			barrier_name = [k for k in barrier.keys()][0]
			barrier_segment_info = {}
			segment_descriptions_list = barrier.values()
			for segment_descriptions in segment_descriptions_list:
				unique_heights = set([i[1] for i in segment_descriptions if i[1]]) #exclude zero height segments
				for height in unique_heights:
					square_footage = sum([i[2] for i in segment_descriptions if i[1] == height])
					barrier_segment_info[height] = square_footage
			barrier_info[barrier_name] = barrier_segment_info
		return barrier_info

def barrier_cost(bar):
	total_height = 0
	total_cost = 0
	print(bar)
	for hgt, total_sqft in bar.items():
		# print(hgt, total_sqft)
		if hgt <= 10:
			if total_sqft <= 10000:
				total_cost += (total_sqft * 27)
			elif 10001 <= total_sqft <= 15000:
				total_cost += (total_sqft * 26)
			elif 15001 <= total_sqft <= 20000:
				total_cost += (total_sqft * 24)
			elif 20001 <= total_sqft <= 25000:
				total_cost += (total_sqft * 23)
			elif 25001 <= total_sqft <= 30000:
				total_cost += (total_sqft * 22)
			elif 30001 <= total_sqft <= 35000:
				total_cost += (total_sqft * 22)
			elif 35001 <= total_sqft <= 40000:
				total_cost += (total_sqft * 21)
			elif 40001 <= total_sqft <= 45000:
				total_cost += (total_sqft * 21)
			elif 45001 <= total_sqft <= 50000:
				total_cost += (total_sqft * 20)
			elif 50001 <= total_sqft <= 55000:
				total_cost += (total_sqft * 20)
			elif 55001 <= total_sqft <= 60000:
				total_cost += (total_sqft * 20)
			elif 60001 <= total_sqft <= 65000:
				total_cost += (total_sqft * 20)
			elif 65001 <= total_sqft <= 70000:
				total_cost += (total_sqft * 19)
			elif 70001 <= total_sqft <= 75000:
				total_cost += (total_sqft * 19)
			elif 75001 <= total_sqft <= 80000:
				total_cost += (total_sqft * 19)
			elif total_sqft >= 80001:
				total_cost += (total_sqft * 19)																																														
		elif 11 <= hgt <= 14:
			if total_sqft <= 10000:
				total_cost += (total_sqft * 43)
			elif 10001 <= total_sqft <= 15000:
				total_cost += (total_sqft * 41)
			elif 15001 <= total_sqft <= 20000:
				total_cost += (total_sqft * 39)
			elif 20001 <= total_sqft <= 25000:
				total_cost += (total_sqft * 37)
			elif 25001 <= total_sqft <= 30000:
				total_cost += (total_sqft * 36)
			elif 30001 <= total_sqft <= 35000:
				total_cost += (total_sqft * 35)
			elif 35001 <= total_sqft <= 40000:
				total_cost += (total_sqft * 34)
			elif 40001 <= total_sqft <= 45000:
				total_cost += (total_sqft * 33)
			elif 45001 <= total_sqft <= 50000:
				total_cost += (total_sqft * 33)
			elif 50001 <= total_sqft <= 55000:
				total_cost += (total_sqft * 32)
			elif 55001 <= total_sqft <= 60000:
				total_cost += (total_sqft * 32)
			elif 60001 <= total_sqft <= 65000:
				total_cost += (total_sqft * 31)
			elif 65001 <= total_sqft <= 70000:
				total_cost += (total_sqft * 31)
			elif 70001 <= total_sqft <= 75000:
				total_cost += (total_sqft * 30)
			elif 75001 <= total_sqft <= 80000:
				total_cost += (total_sqft * 30)
			elif total_sqft >= 80001:
				total_cost += (total_sqft * 30)
		elif 15 <= hgt <= 19:
			if total_sqft <= 10000:
				total_cost += (total_sqft * 78)
			elif 10001 <= total_sqft <= 15000:
				total_cost += (total_sqft * 76)
			elif 15001 <= total_sqft <= 20000:
				total_cost += (total_sqft * 71)
			elif 20001 <= total_sqft <= 25000:
				total_cost += (total_sqft * 68)
			elif 25001 <= total_sqft <= 30000:
				total_cost += (total_sqft * 66)
			elif 30001 <= total_sqft <= 35000:
				total_cost += (total_sqft * 64)
			elif 35001 <= total_sqft <= 40000:
				total_cost += (total_sqft * 62)
			elif 40001 <= total_sqft <= 45000:
				total_cost += (total_sqft * 61)
			elif 45001 <= total_sqft <= 50000:
				total_cost += (total_sqft * 60)
			elif 50001 <= total_sqft <= 55000:
				total_cost += (total_sqft * 59)
			elif 55001 <= total_sqft <= 60000:
				total_cost += (total_sqft * 58)
			elif 60001 <= total_sqft <= 65000:
				total_cost += (total_sqft * 57)
			elif 65001 <= total_sqft <= 70000:
				total_cost += (total_sqft * 56)
			elif 70001 <= total_sqft <= 75000:
				total_cost += (total_sqft * 56)
			elif 75001 <= total_sqft <= 80000:
				total_cost += (total_sqft * 55)
			elif total_sqft >= 80001:
				total_cost += (total_sqft * 55)
		elif 20 <= hgt <= 25:
			if total_sqft <= 10000:
				total_cost += (total_sqft * 151)
			elif 10001 <= total_sqft <= 15000:
				total_cost += (total_sqft * 145)
			elif 15001 <= total_sqft <= 20000:
				total_cost += (total_sqft * 136)
			elif 20001 <= total_sqft <= 25000:
				total_cost += (total_sqft * 130)
			elif 25001 <= total_sqft <= 30000:
				total_cost += (total_sqft * 126)
			elif 30001 <= total_sqft <= 35000:
				total_cost += (total_sqft * 122)
			elif 35001 <= total_sqft <= 40000:
				total_cost += (total_sqft * 119)
			elif 40001 <= total_sqft <= 45000:
				total_cost += (total_sqft * 117)
			elif 45001 <= total_sqft <= 50000:
				total_cost += (total_sqft * 115)
			elif 50001 <= total_sqft <= 55000:
				total_cost += (total_sqft * 113)
			elif 55001 <= total_sqft <= 60000:
				total_cost += (total_sqft * 111)
			elif 60001 <= total_sqft <= 65000:
				total_cost += (total_sqft * 110)
			elif 65001 <= total_sqft <= 70000:
				total_cost += (total_sqft * 108)
			elif 70001 <= total_sqft <= 75000:
				total_cost += (total_sqft * 107)
			elif 75001 <= total_sqft <= 80000:
				total_cost += (total_sqft * 106)
			elif total_sqft >= 80001:
				total_cost += (total_sqft * 105)
		elif hgt >= 26:
			if total_sqft <= 10000:
				total_cost += (total_sqft * 229)
			elif 10001 <= total_sqft <= 15000:
				total_cost += (total_sqft * 221)
			elif 15001 <= total_sqft <= 20000:
				total_cost += (total_sqft * 208)
			elif 20001 <= total_sqft <= 25000:
				total_cost += (total_sqft * 199)
			elif 25001 <= total_sqft <= 30000:
				total_cost += (total_sqft * 192)
			elif 30001 <= total_sqft <= 35000:
				total_cost += (total_sqft * 186)
			elif 35001 <= total_sqft <= 40000:
				total_cost += (total_sqft * 182)
			elif 40001 <= total_sqft <= 45000:
				total_cost += (total_sqft * 178)
			elif 45001 <= total_sqft <= 50000:
				total_cost += (total_sqft * 175)
			elif 50001 <= total_sqft <= 55000:
				total_cost += (total_sqft * 172)
			elif 55001 <= total_sqft <= 60000:
				total_cost += (total_sqft * 169)
			elif 60001 <= total_sqft <= 65000:
				total_cost += (total_sqft * 167)
			elif 65001 <= total_sqft <= 70000:
				total_cost += (total_sqft * 165)
			elif 70001 <= total_sqft <= 75000:
				total_cost += (total_sqft * 163)
			elif 75001 <= total_sqft <= 80000:
				total_cost += (total_sqft * 161)
			elif total_sqft >= 80001:
				total_cost += (total_sqft * 160)
	return total_cost

if __name__ == '__main__':
	os.chdir(os.path.dirname(__file__))
	barrier_xlsx = '../files/CNE_P.xlsx'
	# barrier_analysis = Analysis(barrier_xlsx, "CNE_A_WB9", "CNE_A_SND")
	barrier_analysis = LouisianaAnalysis(barrier_xlsx, "CNE_P_SND")
	bar = barrier_analysis._barrier_dimensions()['EB5']
	print(bar)
	print(barrier_cost(bar))
	# barrier_analysis.barrier_cost(bar)
	# print(wb9a)
	# print(wb9b)

