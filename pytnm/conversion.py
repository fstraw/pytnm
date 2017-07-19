# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:31:11 2016

@author: bbatt
"""

import openpyxl
import shapefile

xlsx = r'C:\Users\brbat\Dropbox\!Python\pytnm\pytnm\Build_Geom_Test.xlsx'

def _xlsx_to_traffic(xlsx):
    """ Converts .xlsx spreadsheet of TNM Traffic to dictionary """
    filter_rows = 6 ##omit these rows at start of spreadsheet
    wb = openpyxl.load_workbook(xlsx, read_only=True)
    traf_ws = wb['Traffic']
    traf_dict = dict([(r[1].value.strip(), (r[5].value, r[7].value, r[9].value))
                    for r in traf_ws.rows if r[1].value][filter_rows:])
    return traf_dict

def xlsx_to_list(xlsx):
    """ Converts .xlsx spreadsheet of TNM Roadways to Z-enabled feature class """
    wb = openpyxl.load_workbook(xlsx, read_only=True)
    rds_ws=wb['Roads']
    i = 15 #starting row of feature names in TNM output format
    fc_list = []
    for row in rds_ws.rows:
        #Skip header rows
        if i > 0:
            i-=1
        else:
            rd_name = row[1].value             
            if rd_name:
                rd_val = rd_name.strip()
                x = row[6].value
                y = row[7].value
                z = row[8].value            
                fc_list.append((rd_val, x, y, z))
            else:
                x = row[6].value
                y = row[7].value
                z = row[8].value            
                fc_list.append((rd_val, x, y, z))
    return fc_list

def tnm_rds_to_fc(fc_list, output):
    t = _xlsx_to_traffic(xlsx)
    w = shapefile.Writer(shapeType=13)    
    w.field('RdName', 'C', 32)
    w.field('Auto', 'N', 4)
    w.field('Medium', 'N', 4)
    w.field('Heavy', 'N', 4)
    rds = sorted(set([road[0] for road in fc_list]))
    for rd in rds:
        pnt_list = []        
        for item in fc_list:
            if item[0] == rd:
                pnt_list.append([float(item[1]), float(item[2]), float(item[3])])
        w.line(parts=[pnt_list], shapeType=13)
        w.record(rd, t[rd][0],  t[rd][1],  t[rd][2]) ##filler        
    w.save(output)

if __name__ == '__main__':
    x = _xlsx_to_traffic(xlsx)   
    t = xlsx_to_list(xlsx)
    l = tnm_rds_to_fc(t, r'C:\Users\bbatt\Dropbox\!Python\pytnm\tests\test_files\test_shp')