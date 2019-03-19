import pandas as pd
import numpy as np

ntlData = pd.read_csv("geert-hofstede.csv")
ntlData = ntlData.replace('#NULL!', 'NaN')
print(ntlData)

