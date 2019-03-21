#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:49:38 2019

@author: Logan
"""

import pandas as pd

ntlData = pd.read_csv("geert-hofstede.csv")
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

#and load the initial game matrix
game_matrix = [[(-w,-w), (v,0)], [(0,v), (0,0)]]

#modify game mx according to values

#play game with complete info--print results

#play game w limited info--print results

#FOR LATER: play game in multiple rounds
