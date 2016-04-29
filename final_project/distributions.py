# -*- coding: utf-8 -*-
"""
Distribution: Calculate list of arbitrage persistance and magnitude for distribution
              Collect data to show time distribution in 1 minute intervals
"""
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.stats.stats import pearsonr   

data_folder = 'data/'

def time_dist(filename,currency = ''):
    '''parse raw BFA output to compute list for time distribution for currency 
    (can leave blank for all currencies)'''
    arbitrage_times = []
    start_time = 9999999999.0
    end_time = 0.0
    with open(data_folder + filename) as data:
        for line in data:
            if line[0:4] == 'Time':
                continue
            else:
                line = line.replace('\n','').split(',')
                if start_time > float(line[0]):
                    start_time = int(float(line[0]))
                else:
                    if line[1] == 'True':
                        if currency != '':
                            if currency in line[3].split('-'):
                                arbitrage_times.append(int(float(line[0]) - start_time))
                        else:
                            arbitrage_times.append(int(float(line[0]) - start_time))
                    end_time = int(float(line[0]))
    plt_bins = range(0,arbitrage_times[-1],60)
    plt.figure(figsize=(26,10))
    x_locs = range(0,arbitrage_times[-1],3600)
    x_labels = [str(time.gmtime(i).tm_hour).zfill(2) + ':' + str(time.gmtime(i).tm_min).zfill(2) for i in range(start_time,end_time,3600)]
    plt.xticks(x_locs,x_labels,rotation='vertical')
    plt.hist(arbitrage_times,bins = plt_bins)
    plt.title('Distribution of Arbitrage Opportunities over Time')
    plt.xlabel('GMT hours (23:59 format)')
    plt.ylabel('# of Opportunities') 
    plt.show()

def arbitrage_dist(filename,currency = ''):
    '''parse raw BFA output to compute list for magnitude and persistence 
    distribution for currency (can leave blank for all currencies)'''
    
    arbitrage_persistence = []
    arbitrage_magnitude = []
    
    arb = False
    with open(data_folder + filename) as data:
        for line in data:
            if line[0:4] == 'Time':
                continue
            else:
                line = line.replace('\n','').split(',')
                if currency != '':
                    if line[1] == 'True' and arb == False:
                        if currency in line[3].split('-'):
                            arb = True
                            arb_start = float(line[0])
                            arb_val = float(line[2])-1.0
                    elif line[1] == 'True' and arb == True:
                        if currency in line[3].split('-'):
                            arb_val += float(line[2])-1.0
                    elif line[1] == 'False' and arb == True:
                        arb = False
                        if arb_val > 0.0:
                            arbitrage_persistence.append(float(line[0])- arb_start)
                            arbitrage_magnitude.append(arb_val)
                    else:
                        continue
                else:
                    if line[1] == 'True' and arb == False:
                        arb = True
                        arb_start = float(line[0])
                        arb_val = float(line[2])-1.0
                    elif line[1] == 'True' and arb == True:
                        arb_val += float(line[2])-1.0
                    elif line[1] == 'False' and arb == True:
                        arb = False
                        if arb_val > 0.0:
                            arbitrage_persistence.append(float(line[0])- arb_start)
                            arbitrage_magnitude.append(arb_val)
                    else:
                        continue
                
    plt_bins = np.arange(0.0,max(arbitrage_magnitude),0.00001)
    plt.figure(figsize=(14,10))
    plt.ylim(0,500)
    plt.xlim(0,0.005)
    plt.hist(arbitrage_magnitude,bins = plt_bins)
    plt.title('Distribution of Arbitrage Magnitudes (rescaled for better viewing)')
    plt.xlabel('Degree of Magnitude')
    plt.ylabel('# of Opportunities') 
    plt.show()
    
    print "Number of arbitrage opportunities: " + str(len(arbitrage_magnitude))
    print "Min non-zero arbitrage value: " + str(min([i for i in arbitrage_magnitude if i > 0.0]))
    print "Max arbitrage value: "+ str(max(arbitrage_magnitude))
    print "Average arbitrage value:" + str(np.average(arbitrage_magnitude))
    print "Median arbitrage value: "+ str(np.median(arbitrage_magnitude))
    print "Value variance: "+ str(np.var(arbitrage_magnitude))
    
    plt_bins = np.arange(0.0,max(arbitrage_persistence),min(arbitrage_persistence))
    plt.figure(figsize=(14,10))
    plt.xlim(0,19)
    plt.hist(arbitrage_persistence,bins = plt_bins)
    plt.title('Distribution of Arbitrage Durations (rescaled for better viewing)')
    plt.xlabel('Length of Persistence')
    plt.ylabel('# of Opportunities') 
    plt.show()
    
    print "Total arbitrage time: " + str(sum(arbitrage_persistence))
    print "Min arbitrage length: " + str(min(arbitrage_persistence))
    print "Max arbitrage length: " + str(max(arbitrage_persistence))
    print "Average arbitrage length:" + str(np.average(arbitrage_persistence))
    print "Median arbitrage length: " + str(np.median(arbitrage_persistence))
    print "Length variance: " + str(np.var(arbitrage_persistence))
    
    plt.figure(figsize=(14,10))
    plt.xlim(0,142)
    plt.ylim(0.0,0.09)
    plt.scatter(arbitrage_persistence,arbitrage_magnitude)
    plt.title('Distribution of Arbitrage Magnitudes vs Persistence')
    plt.xlabel('Length of Persistence')
    plt.ylabel('Degree of Magnitude') 
    plt.show()
    
    print "Pearson correlation coeefficent: " + str(pearsonr(arbitrage_magnitude,arbitrage_persistence)[0])
    print "P-value of coefficient: " + str(pearsonr(arbitrage_magnitude,arbitrage_persistence)[1])