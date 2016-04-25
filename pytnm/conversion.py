# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:31:11 2016

@author: bbatt
"""

import openpyxl
import shapefile

xlsx = r'C:\Users\bbatt\Dropbox\!Python\pytnm\pytnm\Build_Geom_Test.xlsx'

def tnm_rds_to_fc(xlsx):
    """ Converts .xlsx spreadsheet of TNM Roadways to Z-enabled feature class """
    wb = openpyxl.load_workbook(xlsx)
    try:
        rds_ws = [ws for ws in wb.worksheets if ws['B5'].value == 'INPUT: ROADWAYS'][0]
    except IndexError:
        return 'Roads spreadsheet not found!'
    i = 15 #starting row of feature names in TNM output format
    fc_list = []
    while i < rds_ws.max_row:
        row = rds_ws.rows[i]
        rd_name = row[1].value                    
        if rd_name:
            rd_val = rd_name
            x = row[6].value
            y = row[7].value
            z = row[8].value            
            fc_list.append((rd_val, x, y, z))
            i+=1
        else:
            x = row[6].value
            y = row[7].value
            z = row[8].value            
            fc_list.append((rd_val, x, y, z))
            i+=1
    return fc_list

def list_to_shp(fc_list):
    w = shapefile.Writer(shapeType=13)    
    w.field('RdName', 'C', 50)
    rds = set([road[0] for road in fc_list])    
    for rd in rds:
        pnt_list = []        
        for item in fc_list:
            if item[0] == rd:
                pnt_list.append([float(item[1]), float(item[2]), float(item[3])])
        w.line(parts=[pnt_list], shapeType=13)
        w.record(rd, 'Line')        
    w.save('test')
    return pnt_list
    
[
    [
        [1,5],[5,5],[5,1],[3,3],[1,1]
    ]
]

if __name__ == '__main__':
    t = tnm_rds_to_fc(xlsx)
    l = list_to_shp(t)    