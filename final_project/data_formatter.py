# -*- coding: utf-8 -*-
"""
Data reformatter: 
    refits all minute by minute data (i.e. BFO normed data and stock indicies)
    into data frame of arbitrage opportunities: 
    GMT (porportion by day), magnitude, persistence, stock price, % change, |% change|
"""

import pandas as pd
import time

data_folder = "data/"

def reformatter(filename):
    '''creates data frame for arbitrage'''
    
    SPX = {}    
    N100 = {}
    SMI = {}
    AXJO = {}
    SPTSX = {}
    NKY = {}
    cur_stk = {'USD':SPX,'EUR':N100,'CHF':SMI,'AUD':AXJO,'CAD':SPTSX,'JPY':NKY}
    
    with open(data_folder + 'Ordered_SPX.txt','r') as f:
        for line in f:
            line = line.replace('\n','').split(' ')
            SPX[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
    with open(data_folder + 'Ordered_N100.txt','r') as f:
        for line in f:
            line = line.replace('\n','').split(' ')
            N100[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
    with open(data_folder + 'Ordered_SMI.txt','r') as f:
        for line in f:
            line = line.replace('\n','').split(' ')
            SMI[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
    with open(data_folder + 'Ordered_AXJO.txt','r') as f:
        for line in f:
            line = line.replace('\n','').split(' ')
            AXJO[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
    with open(data_folder + 'Ordered_SPTSX.txt','r') as f:
        for line in f:
            line = line.replace('\n','').split(' ')
            SPTSX[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
    with open(data_folder + 'Ordered_NKY.txt','r') as f:
        for line in f:
            line = line.replace('\n','').split(' ')
            NKY[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
    
    dataset = []
    with open(data_folder + filename,'r') as f:
        for line in f:
            line = line.replace('\n','').split(',')
            #load gmt, mag and persist first
            if line[1] != 'False':
                time_of_day = time.gmtime(int(line[0]))
                time_of_day = (int(time_of_day.tm_min * 60) + int(time_of_day.tm_hour * pow(60,2))) / 86400.0
                dataline = [time_of_day,float(line[1]),float(line[2])]
                data_curr = line[3].split('-')
                for c in data_curr:
                    try:
                        x = dataline + cur_stk[c][int(line[0])] + [c]
                        dataset.append(x)
                    except KeyError:
                        continue
    dataset = pd.DataFrame(dataset,columns=['GMT','Magnitude','Persistence','StockPrice','PerChg','AbsPerChg','Currency'])
    dataset.to_csv(data_folder + 'ArbitrageDF.csv')
    return dataset
            