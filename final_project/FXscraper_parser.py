# -*- coding: utf-8 -*-
"""
FXscraper: 
    Uses TFX_caller to collect up to date forex data every 0.1 secs
    Format forex data as A -> B rates for each time step 
    Write to data file as comma separated values
FXparser:
    Uses Bellman Ford to find arbitrage tick by tick
    writes to new file
BFAnormalizer:
    rewrites parsed data to fit minute by minute information for stock indicies
"""

from TFX_py import TFX_caller
from BFord import bf_init
import time
import copy
import math

data_folder = 'data/'

def FXscraper(t=1.0):
    '''t = number of minutes after start time to record using TFX_caller'''    
    end = t*60
    T = TFX_caller()
    current_line = T.update()
    currencies = T.curr
    fn = data_folder+'fx_raw-'+str(int(time.time()+end))+'.txt'
    with open(fn,'w') as data_file:
        data_file.write('Time,(USD/EUR),(USD/JPY),(USD/CAD),(USD/CHF),(USD/AUD),(EUR/USD),(EUR/JPY),(EUR/CAD),(EUR/CHF),(EUR/AUD),(JPY/USD),(JPY/EUR),(JPY/CAD),(JPY/CHF),(JPY/AUD),(CAD/USD),(CAD/EUR),(CAD/JPY),(CAD/CHF),(CAD/AUD),(CHF/USD),(CHF/EUR),(CHF/JPY),(CHF/CAD),(CHF/AUD),(AUD/USD),(AUD/EUR),(AUD/JPY),(AUD/CAD),(AUD/CHF)\n')
        end = time.time() + end
        while(time.time() <= end):
            wait_until = time.time()+0.1
            string = str(current_line['time'])
            for (cA,cB) in currencies:
                string = string + ','+ str(current_line[cA][cB])
            string = string + '\n'
            data_file.write(string)
            if wait_until - time.time() > 0:
                time.sleep(wait_until - time.time())
            current_line = T.update()
    return fn,currencies
    
def FXparser(filename, currencies):
    '''reinterpert FXdata for Bellman-Ford algorithm given currencies list
       no arbitrage = false
       else write true, cycle, value of cycle'''
    rates_line = {}
    bfa_out = open(data_folder + filename[0:-4] + '-BellmanFordOutput.txt','w')
    with open(data_folder + filename,'r') as data_file:
        for line in data_file:
            if line[0:4] == 'Time':
                continue
            else:
                line = line.replace('\n','').split(',')
                time = float(line[0])
                count = 1
                for (cA,cB) in currencies:
                    if cA not in rates_line:
                        rates_line[cA] = {cB: float(line[count])}
                        count += 1
                    else:
                        rates_line[cA][cB] = float(line[count])
                        count += 1
                try:
                    bf_dict = copy.deepcopy(rates_line)
                    out,cycle = bf_init(bf_dict)
                    if out != False:
                        cycle = cycler(cycle,rates_line)
                        bfa_out.write(str(time) + "," + str(out) + ',' + str(cycle[0]) +  ',' + str('-'.join(cycle[1]) + '\n'))
                    else:
                        bfa_out.write(str(time) + "," + str(out) + ',0\n')
                except KeyError:
                    bfa_out.write(str(time) + "," + "False" + ',0\n')
    bfa_out.close()

def cycler(cy,rates):
    '''given the BF dict output, return the cycle in list form''' 
    cycle_val = 1
    cycle = [cy[-1]]
    for i in range(len(cy)-1,0,-1):
        cycle_val = cycle_val*rates[cy[i]][cy[i-1]]
        if cy[i-1] == cycle[0]:        
            return cycle_val,cycle
        else:
            cycle.append(cy[i-1])

def BFA_normalizer(filename):
    '''Grab Bellman Ford output and normalize data to minute units and sum
    currencies and value'''
    normalized = open(data_folder + 'BFO_normdata'+ filename[6:-4] + '.txt','w')
    f = open(data_folder + filename, 'r')
    priorMinute = math.trunc(float((f.readline().split(','))[0])/60)
    summ = 0
    Arbcurrencies = set()
    persist = 0
    persist_helper = 0
    for line in f:
        parts = line.replace('\n',"").split(',')
        minute = math.trunc(float((parts[0]))/60)
        if parts[1] == "True":
            persist += float(parts[0]) - persist_helper
            if persist_helper == 0:
                persist += 0.1
            summ += (float(parts[2])-1)
            currencies = parts[3].split('-')
            for i in currencies:
                if i not in Arbcurrencies:
                    Arbcurrencies.add(i)
        persist_helper = float(parts[0])
        if minute != priorMinute:
            priorMinute = minute
            if summ:
                normalized.write(str(priorMinute*60) + "," + str(1+summ) + ',' + str(persist) + ',' + str('-'.join(Arbcurrencies))+'\n')
            else:
                normalized.write(str(priorMinute*60) + "," + 'False' + '\n')
            summ = 0
            Arbcurrencies = set()
            persist = 0
    f.close()


currencies_all = TFX_caller().curr
