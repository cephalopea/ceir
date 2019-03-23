#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:49:38 2019

@author: Logan
"""

import pandas as pd

def formatMatrix(m, n):
    result="[("
    result+=str(m[0][0])+","+str(n[0][0])+"), ("
    result+=str(m[0][1])+","+str(n[0][1])+")]\n"
    result+="[("+str(m[1][0])+","+str(n[1][0])+"), ("
    result+=str(m[1][1])+","+str(n[1][1])+")]"
    return result

ntlData = pd.read_csv("./datasets/geert-hofstede.csv")
ntlData = ntlData.replace('#NULL!', 'NaN')
                          
#MAS strong correlation to prefering war
#PDI weak correlation to preferring war
#UAI minimizie negative outcomes in uncertain situations
#LTO how much they tend to repeat prev behavior (implement later for repeated game)

#Test for idv and ivr (using R, see datasets in repo)

#for idv (individualism): VERY weak neg cor (maybe enough to ignore)
#for ivr (indulgence vs restraint): medium neg cor

#default matrix w-- cost of going to war, v: value of land at stake
#[(-w,-w), (v,0)]
#[(0,v), (0,0)]

#here lets pick some values
w=100
v=50
country1 = "India"
country2 = "Pakistan"

data1 = ntlData.loc[ntlData['country']==country1]
data2 = ntlData.loc[ntlData['country']==country2]

#and load the initial game matrix
matrix1 = [[-w, v], [0, 0]]
matrix2 = [[-w, 0], [v, 0]]

#modify game mx according to gh values (untested coeficients here)
war_bias1 = data1.iloc[0]['mas'] + (-.3)*data1.iloc[0]['ivr'] + (-.05)*data1.iloc[0]['idv'] + (0.1)*data1.iloc[0]['pdi']
war_bias2 = data2.iloc[0]['mas'] + (-.3)*data2.iloc[0]['ivr'] + (-.05)*data2.iloc[0]['idv'] + (0.1)*data2.iloc[0]['pdi']

matrix1[0][0]+=war_bias1
matrix1[0][1]+=war_bias1

matrix2[0][0]+=war_bias2
matrix2[1][0]+=war_bias2

print(formatMatrix(matrix1, matrix2))

#play game with complete info--print results
#check for dom strat
#if none, compute %chance of opponent playing various responses (using uai)
#compute best play

#play game w limited info--print results
#same as above but w less info

#FOR LATER: play game in multiple rounds
