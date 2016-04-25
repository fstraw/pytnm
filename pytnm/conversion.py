# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:31:11 2016

@author: bbatt
"""

import openpyxl
import shapefile

xlsx = r'C:\Users\bbatt\Dropbox\!Python\pytnm\pytnm\Build_Geom_Test.xlsx'

def xlsx_to_list(xlsx, input_type='ROADS'):
    if input_type.upper() == 'TRAFFIC':
        fld_idx = [5, 7, 9]
    """ Converts .xlsx spreadsheet of TNM Roadways to Z-enabled feature class """
    wb = openpyxl.load_workbook(xlsx, read_only=True)
    try:
        rds_ws=wb['Roads']
    except IndexError:
        return 'Roads spreadsheet not found!'
    i = 15 #starting row of feature names in TNM output format
    fc_list = []
    for row in rds_ws.rows:
        #Skip header rows
        if i > 0:
            i-=1
        else:
            rd_name = row[1].value              
            if rd_name:
                rd_val = rd_name
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

def tnm_rds_to_fc(fc_list):
    w = shapefile.Writer(shapeType=13)    
    w.field('RdName', 'C', 32)
    w.field('Auto', 'C', 4)
    w.field('Medium', 'C', 4)
    w.field('Heavy', 'C', 4)
    rds = sorted(set([road[0] for road in fc_list]))
    for rd in rds:
        pnt_list = []        
        for item in fc_list:
            if item[0] == rd:
                pnt_list.append([float(item[1]), float(item[2]), float(item[3])])
        w.line(parts=[pnt_list], shapeType=13)
        w.record(rd, 8766, 6874, 886)
        
    w.save('test')

if __name__ == '__main__':
    t = xlsx_to_list(xlsx)
    l = tnm_rds_to_fc(t)
    for i in t:
        print i