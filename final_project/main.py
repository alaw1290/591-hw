# -*- coding: utf-8 -*-
"""
Main: contains all functions and their descriptions of their functions
"""

from TFX_py import TFX_caller
currencies = TFX_caller().curr


# Data interperters and formatters 
from FXscraper_parser import FXparser
'''Read raw FX data to to find arbitrage tick by tick and create BFO data'''
from FXscraper_parser import BFA_normalizer
'''Read BFO data and formats to minute by minute data'''
from converter import converter
'''Read stock index data and formats them in correct order and include stock info'''
# Data refitting for pandas dataframe
from data_formatter import reformatter
'''Read normalized BFO minute data and formats a dataframe for analysis'''
# Data analysis tools
from distributions import time_dist
'''plots time-series distribution of abritrage using BFO data'''
from distributions import arbitrage_dist
'''plots distribution of arbitrage magnitude and persistence using BFO data'''
from clustering_regression import KMeansClustering
'''Kmeans cluster to show time effects of the arbitrage clusters'''
from clustering_regression import regression
'''linear OLS regression to show correlation of magnitude and persistence'''