# -*- coding: utf-8 -*-
"""
Bellman Ford Algorithm:
    Implementation of Bellman-Ford based on joninvski's implementation 
    (github.com/joninvski/701720)
    Our modification includes detection of negative cycles in a directed graph 
    and representation of adjacency matrices
    
    Uses adjacency matrices as dictionaries of edge weights and interperts them
    as -1*log(Ew) in order to find negative weight cycles consistent to the 
    implementation of Bellman-Ford
"""
###it's fucking this one. Fuck, it's this one.  Use this one, fuck.######
### If there's no arbitrage, this returns false.  If there is ###########
###arbitrage then it returns each currency and a list of the possible ###
###paths you can take from that currency to get there, as a tuple.#######

from math import log

def bf_init(exchDict):

    for i in exchDict:
        for j in exchDict[i]:
		exchDict[i][j] = -1*(log(exchDict[i][j],2))


    for i in exchDict:
        case,cycle = bellman_ford(exchDict,i)
        if case == False:
            continue
        else:
            return True,cycle
    return False, 0


def initialize(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for predecessor
    for node in graph:
        d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p

def relax(node, neighbour, graph, d, p):
    # If the distance between the node and the neighbour is lower than the one I have now
    if d[neighbour] > d[node] + graph[node][neighbour]:
        # Record this lower distance
        d[neighbour]  = d[node] + graph[node][neighbour]
        p[neighbour] = node

def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbour of u
                relax(u, v, graph, d, p) #Lets relax it
    
    for u in graph:
        for v in graph[u]:
            if d[v] > d[u] + graph[u][v]:
                cycle = [v]
                cycle_n = p[v]
                while cycle_n not in cycle:
                    cycle.append(cycle_n)
                    cycle_n = p[cycle_n]
                cycle.append(cycle_n)
                return True,cycle
    return False, 0



