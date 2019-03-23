"""
@author: Caiti
"""

import pandas as pd
import numpy as np

ntlData = pd.read_csv("./datasets/geert-hofstede.csv")
ntlData.fillna(60, inplace=True) #center val as placeholder for missing vals

sampleOutcome = {'pdi': 0, 'idv': 10, 'mas': 20, 'uai': 30, 'ltowvs': 40, 'ivr': 50}

#next two functions are unnecessary, but convenient for clarity

#creates a dataframe of just the relevant country's data
def getCountryData(ctr):
    return ntlData.loc[ntlData['country'] == ctr]

#returns only data from a single cell as one comparable value
def getDataPoint(row, attribute):
    return row.iloc[0][attribute]

#finds the average distance between two countries' attributes
def getDistance(ctr1, ctr2):
    ctrData1 = getCountryData(ctr1) #dataframe of just the input country
    ctrData2 = getCountryData(ctr2) 
    attributes = ['pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    differenceData = {}
    avgDist = 0
    for attribute in attributes:
        distance = abs(getDataPoint(ctrData1, attribute) - getDataPoint(ctrData2, attribute))
        avgDist += distance
        differenceData[attribute] = distance
    avgDist /= 6
    differenceData['avgDist'] = avgDist
    print(differenceData)
    return differenceData

#modify the base utils according to cultural modifiers (based on Logan's data)
def modAttributes(ctr1, ctr2, matrix1, matrix2):
    ctrData1 = getCountryData(ctr1)
    ctrData2 = getCountryData(ctr2)
    #ctrDifference = getDistance(ctr1, ctr2)
    war_bias1 = getDataPoint(ctrData1, 'mas') + (-.3)*getDataPoint(ctrData1, 'ivr') + (-.05)*getDataPoint(ctrData1, 'idv') + (0.1)*getDataPoint(ctrData1, 'pdi')
    war_bias2 = getDataPoint(ctrData2, 'mas') + (-.3)*getDataPoint(ctrData2, 'ivr') + (-.05)*getDataPoint(ctrData2, 'idv') + (0.1)*getDataPoint(ctrData2, 'pdi')
    matrix1[0][0]+=war_bias1
    matrix1[0][1]+=war_bias1
    matrix2[0][0]+=war_bias2
    matrix2[1][0]+=war_bias2

def formatMatrix(m, n):
    result="[("
    result+=str(m[0][0])+","+str(n[0][0])+"), ("
    result+=str(m[0][1])+","+str(n[0][1])+")]\n"
    result+="[("+str(m[1][0])+","+str(n[1][0])+"), ("
    result+=str(m[1][1])+","+str(n[1][1])+")]"
    return result

def play(ctr1, ctr2, m1, m2):
    #compute % chance of oppoents plays (if no dom strat)
    #compute best play for each player

    ctrData1 = getCountryData(ctr1)
    ctrData2 = getCountryData(ctr2) 

    #calc country 1 strategy
    if(m1[0][0]>=m1[1][0] and m1[0][1]>=m1[1][1]):
        c1Dom = "war"
    elif(m1[0][0]<=m1[1][0] and m1[0][1]<=m1[1][1]):
        c1Dom = "peace"
    else:
        c1Dom = "None"

    #calc country 2 strategy
    if(m2[0][0]>=m2[0][1] and m2[1][0]>=m2[1][1]):
        c2Dom = "war"
    elif(m2[0][0]<=m2[0][1] and m2[1][0]<=m2[1][1]):
        c2Dom = "peace"
    else:
        c2Dom = "None"

    if c1Dom=="None":
        #value for c1's evaluation of how likely c2 is to go to war
        c2WarOdds = 0.5 + (0.005)*getDataPoint(ctrData1, 'uai')

        #weighted value for each outcome

    if c2Dom=="None":
        c1WarOdds = 0.5 + (0.005)*getDataPoint(ctrData2, 'uai')
    
    print(ctr1+" strategy: "+c1Dom)
    print(ctr2+" strategy: "+c2Dom)

    


def main():
    #default matrix w-- cost of going to war, v: value of land at stake
    #[(-w,-w), (v,0)]
    #[(0,v), (0,0)]
    w=100
    v=50
    country1 = "India"
    country2 = "Pakistan"

    #load the initial game matrix
    matrix1 = [[-w, v], [0, 0]]
    matrix2 = [[-w, 0], [v, 0]]

    modAttributes(country1, country2, matrix1, matrix2)
    print(formatMatrix(matrix1, matrix2))

    play(country1, country2, matrix1, matrix2)


main()

