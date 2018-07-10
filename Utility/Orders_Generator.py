import pandas as pd
import numpy as np

orders_list = pd.DataFrame(columns=["ID", "shoes", "tshirt", "pullover", "hat"])

<<<<<<< HEAD
orders_list.loc[0] = [1, 1, 0, 0, 0]
orders_list.loc[1] = [1, 0, 1, 0, 0]
orders_list.loc[2] = [1, 0, 1, 0, 0]
'''
orders_list.loc[2] = [1, 0, 0, 1, 1]
orders_list.loc[3] = [1, 0, 0, 0, 1]
orders_list.loc[4] = [1, 0, 1, 0, 0]
orders_list.loc[5] = [1, 1, 0, 0, 1]
'''
=======
orders_list.loc[0] = [0, 1, 0, 0, 0]
orders_list.loc[1] = [1, 0, 1, 0, 0]
orders_list.loc[2] = [2, 0, 0, 1, 0]
orders_list.loc[3] = [3, 0, 0, 0, 1]
orders_list.loc[4] = [4, 0, 0, 1, 1]
orders_list.loc[5] = [5, 1, 1, 0, 0]
orders_list.loc[6] = [1, 0, 1, 1, 0]
orders_list.loc[7] = [2, 1, 1, 0, 1]
orders_list.loc[8] = [3, 1, 1, 1, 0]
orders_list.loc[9] = [3, 0, 1, 1, 1]

>>>>>>> 2e9287af9e667092178c536f26b668c1ebcab826
orders_list.to_csv("orders_list.csv")
