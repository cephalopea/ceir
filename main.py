"""
@author: Caiti, Logan, Ian, and Michael
"""

import pandas as pd
import numpy as np

ntlData = pd.read_csv("./datasets/geert-hofstede.csv")
ntlData.fillna(60, inplace=True) #center val as placeholder for missing vals

sampleOutcome = {'pdi': 0, 'idv': 10, 'mas': 20, 'uai': 30, 'ltowvs': 40, 'ivr': 50}

WAR="war"
PEACE="peace"
BLANK="None"

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
    result+='{:^7}'.format(str(round(m[0][0], 1)))+","+'{:^7}'.format(str(round(n[0][0], 1)))
    result+="), ("
    result+='{:^7}'.format(str(round(m[0][1],1)))+","+'{:^7}'.format(str(round(n[0][1],1)))
    result+=")]\n"
    result+="[("
    result+='{:^7}'.format(str(round(m[1][0], 1)))+","+'{:^7}'.format(str(round(n[1][0],1)))
    result+="), ("
    result+='{:^7}'.format(str(round(m[1][1],1)))+","+'{:^7}'.format(str(round(n[1][1],1)))
    result+=")]"
    return result

#compute and print each country's strategy, assuming they don't know the other's payoffs
def play(ctr1, ctr2, m1, m2, c1LastPlay, c2LastPlay):
    
    ctrData1 = getCountryData(ctr1)
    ctrData2 = getCountryData(ctr2) 

    #calc country 1 strategy
    if(m1[0][0]>=m1[1][0] and m1[0][1]>=m1[1][1]):
        c1Dom = WAR
    elif(m1[0][0]<=m1[1][0] and m1[0][1]<=m1[1][1]):
        c1Dom = PEACE
    else:
        c1Dom = BLANK

    #calc country 2 strategy
    if(m2[0][0]>=m2[0][1] and m2[1][0]>=m2[1][1]):
        c2Dom = WAR
    elif(m2[0][0]<=m2[0][1] and m2[1][0]<=m2[1][1]):
        c2Dom = PEACE
    else:
        c2Dom = BLANK

    if c1Dom==BLANK:
        #value for c1's evaluation of how likely c2 is to go to war
        c2WarOdds = 0.5 + (0.005)*getDataPoint(ctrData1, 'uai')

        if c2LastPlay==WAR:
            c2WarOdds+=0.3
        elif c2LastPlay==PEACE:
            c2WarOdds-=0.1

        #account for bias towards last play
        bonus=(70-getDataPoint(ctrData1, 'ltowvs'))*0.3
        if c1LastPlay==PEACE:
            bonus=bonus*-1
        elif c1LastPlay==BLANK:
            bonus=0
        
        #weighted value for each outcome
        warPayoff1 = m1[0][0]*c2WarOdds + m1[0][1]*(1-c2WarOdds)+bonus
        peacePayoff1 = m1[1][0]*c2WarOdds + m1[1][1]*(1-c2WarOdds)-bonus

        if(peacePayoff1>warPayoff1):
            c1Dom=PEACE
        else:
            c1Dom=WAR

    if c2Dom==BLANK:
        c1WarOdds = 0.5 + (0.005)*getDataPoint(ctrData2, 'uai')

        if c1LastPlay==WAR:
            c1WarOdds+=0.3
        elif c1LastPlay==PEACE:
            c1WarOdds-=0.1

        bonus=(70-getDataPoint(ctrData2, 'ltowvs'))*0.3
        if c2LastPlay==PEACE:
            bonus=bonus*-1
        elif c2LastPlay==BLANK:
            bonus=0
        
        warPayoff2 = m2[0][0]*c1WarOdds + m2[1][0]*(1-c1WarOdds)+bonus
        peacePayoff2 = m2[0][1]*c1WarOdds + m2[1][1]*(1-c1WarOdds)-bonus

        if(peacePayoff2>warPayoff2):
            c2Dom=PEACE
        else:
            c2Dom=WAR

    
    print(ctr1+" strategy: "+c1Dom)
    print(ctr2+" strategy: "+c2Dom)

    return c1Dom, c2Dom


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

    #modify matrix according to countrys gf values
    modAttributes(country1, country2, matrix1, matrix2)
    print(formatMatrix(matrix1, matrix2))

    c1Strat=BLANK
    c2Strat=BLANK

    for i in range(10):
        print("\nround " + str(i)+":")
        strategies=play(country1, country2, matrix1, matrix2, c1Strat, c2Strat)
        c1Strat=strategies[0]
        c2Strat=strategies[1]


main()
