"""
@author: Caiti
"""

import pandas as pd
import numpy as np

ntlData = pd.read_csv("geert-hofstede.csv")
ntlData.fillna(60, inplace=True) #center val as placeholder for missing vals

sampleOutcome = {'pdi': 0, 'idv': 10, 'mas': 20, 'uai': 30, 'ltowvs': 40, 'ivr': 50}

#next two functions are unnecessary, but convenient for clarity

#creates a dataframe of just the relevant country's data
def getCountryData(ctr):
    return ntlData.loc[ntlData['ctr'] == ctr]

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
def attributeModify(ctr1, ctr2, util):
    ctrData1 = getCountryData(ctr1)
    ctrData2 = getCountryData(ctr2)
    ctrDifference = getDistance(ctr1, ctr2)
    
