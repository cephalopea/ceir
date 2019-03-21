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

#creates an outcome formatted as a dictionary
def createOutcome(pdi, idv, mas, uai, ltowvs, ivr):
    return {'pdi': pdi, 'idv': idv 'mas': mas 'uai': uai, 'ltowvs': ltowvs, 'ivr': ivr}

#finds the average distance between a country's attributes and an outcome's attributes
def getDistance(ctr, outcome):
    ctrData = getCountryData(ctr) #dataframe of just the input country
    ctrDistance = {}
    attributes = ['pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    dist = 0
    for attribute in attributes:
        ctrDistance[attribute] = abs(getDataPoint(ctrData, attribute) - outcome[attribute])
    for attribute in attributes:
        dist += ctrDistance[attribute]
    dist /= 6
    print(dist)
    return dist

getDistance('IND', sampleOutcome)
