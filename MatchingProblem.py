#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 15:47:46 2018

@author: Aysun Far
"""

import pandas as pd
#matching library
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

#Read
girls = pd.read_csv('/Users/EyeSun/Downloads/Sheet6.csv')
boys = pd.read_csv('/Users/EyeSun/Downloads/Sheet7.csv')


def create_graph(girls,boys):
    B = nx.Graph()
    B.add_nodes_from(list(girls['Girls']),bipartite=0)
    B.add_nodes_from(list(boys['Boys']),bipartite=1)
    def edge_make(row):
        s = sum(row[[2,4,6]])
        result = []
        for i in [1,3,5]:
            if row[i] in B.nodes:
                result.append((row[0],row[i],row[i+1]/s))
        return result

    lst = list(girls.apply(edge_make,axis=1))
    edges_g = [e[0] for e in lst] 
    B.add_weighted_edges_from(edges_g)
    lst = list(boys.apply(edge_make,axis=1))
    edges_b = [e[0] for e in lst] 
    B.add_weighted_edges_from(edges_b)
    return B
    
def find_matching(B):
    # find all components
    componates = list(nx.connected_component_subgraphs(B))
    # for each components finds the maximum matching
    dic_result = {}
    for cm in componates:
        dic_result.update(nx.bipartite.maximum_matching(cm))
    return dic_result

def non_matched(dic_result):
    alone_girls = set(girls['Girls']) - set(dic_result.keys()) 
    alone_boys = set(girls['Girls']) - set(dic_result.keys()) 
    print('Not Matched')
    if alone_girls:
        print(alone_girls)
    if alone_boys:
        print(alone_boys)
    
def save_result(dic_result):
    df= pd.DataFrame({'Guest': dic_result.keys(),
              'Partner': dic_result.values()})
    df.sort_values('Guest',inplace=True)
    df.set_index('Guest',inplace = True)

    df.to_csv('/Users/EyeSun/Downloads/results.csv')

def plot_graph(B):
    componates = list(nx.connected_component_subgraphs(B))
    for cm in componates:
       # X, Y = bipartite.sets(cm)
        X = set(n for n,d in cm.nodes(data=True) if d['bipartite']==0)
        Y = set(cm) - X
        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
        nx.draw_networkx(cm, pos=pos)
        plt.axis('off')
        plt.show()
        
if __name__== "__main__":
    B = create_graph(girls,boys)
    dic_result = find_matching(B)
    non_matched(dic_result)
    save_result(dic_result)
    plot_graph(B)






