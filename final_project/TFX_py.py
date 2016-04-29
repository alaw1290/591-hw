# -*- coding: utf-8 -*-
"""
TFX_Caller:
    Class to get updated currency rates using API web-caller.
    Creates an authenticated session to get exchange rates between USD, EUR,
    JPY, CAD, AUD, and CHF (CSV formate delinated by comma)
    1) Authenticate session, get session ID
    2) Retrieve rates as frequently as possible
    3) snapshot=Y:return all rates even if not updated
"""
import config
import requests
import time

class TFX_caller:
    
    def __init__(self):
        curr_pairs = 'EUR/USD,USD/CAD,USD/JPY,USD/CHF,AUD/USD,EUR/CAD,EUR/JPY,EUR/CHF,EUR/AUD,CAD/JPY,CAD/CHF,AUD/CAD,CHF/JPY,AUD/JPY,AUD/CHF'
        bookname = 'bluebook'
        # currency pairs 'EUR/USD,USD/CAD,USD/JPY,USD/CHF,AUD/USD,EUR/CAD,EUR/JPY,EUR/CHF,EUR/AUD,CAD/JPY,CAD/CHF,AUD/CAD,CHF/JPY,AUD/JPY,AUD/CHF'
        r = requests.get('http://webrates.truefx.com/rates/connect.html?u=' + config.user + '&p=' + config.pasw + '&q='+ bookname + '&c=' + curr_pairs + '&f=csv&s=y')     
        self.authsessID = r.text[:len(r.text)-2]
        self.curr_pairs = set(['EUR/USD','USD/CAD','USD/JPY','USD/CHF','AUD/USD','EUR/CAD','EUR/JPY','EUR/CHF','EUR/AUD','CAD/JPY','CAD/CHF','AUD/CAD','CHF/JPY','AUD/JPY','AUD/CHF'])
        curr = ['USD','EUR','JPY','CAD','CHF','AUD']
        self.curr = []
        for i in curr:
            for j in curr:
                if i != j:
                    self.curr.append((i,j)) 
        
    def update(self):
        line = requests.get('http://webrates.truefx.com/rates/connect.html?id=' + self.authsessID)
        rates = str(line.text).split()
        line = {'time': time.time()}
        for r in rates:
            r = r.split(',')
            cA,cB = r[0].split('/')
            rAB = float(r[2]+r[3])
            rBA = 1.0/float(r[4]+r[5])
            if cA not in line:
                line[cA] = {cB:rAB}
            else:
                line[cA][cB] = rAB
            if cB not in line:
                line[cB] = {cA:rBA}
            else:
                line[cB][cA] = rBA
        return line
