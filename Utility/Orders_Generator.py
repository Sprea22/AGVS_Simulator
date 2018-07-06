import pandas as pd
import numpy as np

orders_list = pd.DataFrame(columns=["ID", "shoes", "tshirt", "pullover", "hat"])

orders_list.loc[0] = [1, 1, 0, 0, 0]
orders_list.loc[1] = [1, 0, 1, 0, 0]
orders_list.loc[1] = [1, 0, 1, 0, 0]
'''
orders_list.loc[2] = [1, 0, 0, 1, 1]
orders_list.loc[3] = [1, 0, 0, 0, 1]
orders_list.loc[4] = [1, 0, 1, 0, 0]
orders_list.loc[5] = [1, 1, 0, 0, 1]
'''
orders_list.to_csv("orders_list.csv")
