# -*- coding: utf-8 -*-
"""
Clustering: runs k-means as part of our analysis of the arbitrage dataset
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter
import statsmodels.formula.api as sm
import sklearn.metrics as metrics

data_folder = 'data/'

def KMeansClustering(filename,n_iterations=20,error_range=100):
    '''Use Kmeans to determine optimum cluster and plot clusters of risk'''    
    data = pd.DataFrame.from_csv(data_folder + filename)
    
    #plot x,y remove currency to prevent errors
    x_coor = data['PerChg']
    y_coor = data['GMT']
    data_noName = data.drop('Currency',1)
    
    #rescale vectors (col num = 6)
    vectors = data_noName.as_matrix()
    for p in range(0,len(vectors[0])):
        #GMT
        if p in [0]:
            vectors[:,p] *= 1
        #Magnitude
        if p in [1]:
            vectors[:,p] *= 5
        #Persistence
        if p in [2]:
            vectors[:,p] *= 5
        #StockPrice
        if p in [3]:
            vectors[:,p] *= 0
        #PerChg
        if p in [4]:
            vectors[:,p] *= 3
        #AbsPerChg
        if p in [5]:
            vectors[:,p] *= 0
            
    #Elbow method and plotting
    error = np.zeros(n_iterations)
    error[0] = 0
    for k in range(1,n_iterations):
        kmeans = KMeans(init='k-means++', n_clusters=k, n_init=10)
        kmeans.fit_predict(vectors)
        error[k] = kmeans.inertia_
    plt.figure(figsize=(16,10))
    plt.plot(range(1,len(error)),error[1:], label = 'Function of Error and Clusters')
    plt.plot(range(1,len(error)),np.diff(error), label = 'Marginal reduction of Error')
    plt.title('Elbow plot of Clusters vs Error')
    plt.xlabel('Number of clusters')
    plt.ylabel('Error (Variance)')
    plt.legend()
    plt.show()
    
    #Find best number of clusters
    ic = 0
    error_diff = np.diff(error)
    while(abs(error_diff[ic]) > error_range):
        ic += 1
    print "Best number of Clusters (at the elbow)= %i   Error = %.4f   Marginal Reduction of Error = %.4f"%(ic,error[ic],sum(abs(np.diff(error)[:ic]))) 
    
    #i = ideal # of clusters, rerun clustering using n_clusters = i
    num_clusters = ic
    k_means = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)
    k_means.fit_predict(vectors)
    coordinates_labels = k_means.labels_
    coordinates_cluster_centers = k_means.cluster_centers_
    coordinates_unique_labels = np.unique(coordinates_labels)    
    
    #store cluster assignment into dataframe
    data['Clusters'] = coordinates_labels
    data.to_csv(data_folder + filename[:-4] + '_kmeans.csv')
    
    #Find the most common currency, average persistance, and average magnitude in each cluster
    label_data = find_common_types(data,coordinates_unique_labels,'Clusters')    
    
    #visually show clusters
    colors = ['b','g','r','c','m','y','k','w']    
    plt.figure(figsize=(14,14))
    plt.scatter(x_coor, y_coor, c = [colors[i] for i in coordinates_labels])
    #x: 0-0.7
    #y: 1-1.015    
    plt.xlim([-0.3,0.4])
    plt.ylim([0.0,1.0])
    
    
    #Use label data to label cluster centers
    for j in range(len(coordinates_cluster_centers)):
        plt.scatter(coordinates_cluster_centers[j][0],coordinates_cluster_centers[j][1], c = colors[j], label = label_data[j])
        #plt.annotate(label_data[j],xy=coordinates_cluster_centers[j][0:2])
    
    plt.legend()
    
    plt.title('Distribution of Arbitrage across GMT and Stock % Change')
    plt.xlabel('Stock Index % Change')
    plt.ylabel('GMT porportion (i.e. 1.0 = 23:59)') 
    plt.show()    
    
    #In each cluster, calculate a euclidean similarity matrix using categories and attributes
    sim_matrices = []
    for l in coordinates_unique_labels:
        sim_matrices.append(calc_sim_matrix(data_noName.loc[data['Clusters'] == l],'cosine'))
    
    #Return the average similarity of all items inside the cluster
    sim_list = []
    for l in range(len(coordinates_unique_labels)):
        minimum = sim_matrices[l].flatten().min()
        average = np.average(sim_matrices[l].flatten())
        sim_list.append([minimum,average])

    #Return the average similarity of all items inside the cluster
    sim_list = []
    for l in range(len(coordinates_unique_labels)):
        minimum = sim_matrices[l].flatten().min()
        average = np.average(sim_matrices[l].flatten())
        sim_list.append([minimum,average])
    
    #Print statstics, cluster details, similarity minimums and averages
    print("Number of Clusters: %i"%len(coordinates_unique_labels))
    print("")
    label_data = find_common_types(data,coordinates_unique_labels,'Clusters')
    for l in range(len(coordinates_unique_labels)):
        print("\tCluster #: %i"%coordinates_unique_labels[l])
        print("\tColor of cluster: " + colors[l%len(colors)])
        print("\tName of cluster (based on common elements in cluster): " + label_data[l])
        data_range = data.loc[data['Clusters'] == coordinates_unique_labels[l]]
        currencies_list = Counter(list(data_range['Currency'])).most_common()
        print("\tList of currencies: " + str(currencies_list))
        print("\tMinimum cosine similarity value: " + str(sim_list[l][0]))
        print("\tAverage cosine similarity value: " + str(sim_list[l][1]))
        
def find_common_types(data,labels,name):
    '''For each cluster, sum up columns and return the most common currency, average persistance, and average magnitude'''
    
    label_data = []
    
    for label in labels:
        data_range = data.loc[data[name] == label]
        currencies_list = Counter(list(data_range['Currency']))
        currencies_list = currencies_list.most_common()[0][0]
        avg_mag = round(np.average(data_range['Magnitude']),6)
        avg_per = round(np.average(data_range['Persistence']),6)
        label_data.append(str(currencies_list) + ', ' + str(avg_mag) + ', ' + str(avg_per))
    
    return label_data
    
def calc_sim_matrix(data,met):
    return 1-metrics.pairwise_distances(data, metric=met)
    
def regression(filename):
    df = pd.DataFrame.from_csv(data_folder + filename)  
    result = sm.ols(formula="Persistence ~ Magnitude", data=df).fit()
    print result.summary()
    
    
    
    