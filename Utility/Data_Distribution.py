from scipy.stats import truncnorm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

'''
orders_list = pd.read_csv("Utility/Total_Orders.csv", index_col=0)

testing_orders_list = pd.DataFrame(columns = orders_list.columns)

for col in orders_list.columns[2:].values:
    article_values = orders_list[col].values
    article_mean = np.mean(article_values)
    article_std = np.std(article_values)
    lower = np.min(article_values)
    upper = np.max(article_values)
    mu, sigma = np.mean(article_values), np.std(article_values)
    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    #fig, ax = plt.subplots(1, sharex=True)
    #plt.title(str(col))
    #ax.hist(X.rvs(1), normed=True)
    pred_values = X.rvs(200)
    for i in range(0, len(pred_values)):
        pred_values[i] = int(pred_values[i])
    testing_orders_list[col] = pred_values.T

DB = orders_list
DB_Dist = []
for x in DB.columns.values:
    if(x != 'client' and x != 'status' and x != 'Unnamed: 0'):
        DB_Dist.append(DB[x].sum())
s1 = float(sum(DB_Dist))
DB_Dist = np.divide(DB_Dist, s1)

DB_Dist_Test = []
for x in testing_orders_list.columns.values:
    if(x != 'client' and x != 'status' and x != 'Unnamed: 0'):
        DB_Dist_Test.append(testing_orders_list[x].sum())
s2 = float(sum(DB_Dist_Test))
DB_Dist_Test = np.divide(DB_Dist_Test, s2)

plt.plot(DB_Dist)
plt.plot(DB_Dist_Test)
plt.title(str(np.corrcoef(DB_Dist, DB_Dist_Test)[0][1]))
plt.show()

testing_orders_list.to_csv("Testing_Orders_List.csv")
'''

import random

orders_list = pd.read_csv("Utility/orders_list_generated.csv", index_col=0)

COs = ["CO"]*136
MIs = ["MI"]*10
FIs = ["FI"]*54


destinations = COs + MIs + FIs
status = [0]*200

random.shuffle(destinations)

orders_list["client"] = destinations
orders_list["status"] = status

orders_list.to_csv("orders_list_generated_final.csv")
