
import pandas as pd
import numpy as np

orders_list = pd.DataFrame(columns=["client", "shoes_R","shoes_G","shoes_B", "tshirt_R","tshirt_G","tshirt_B", "pullover_R","pullover_G","pullover_B", "hat_R","hat_G","hat_B"])

orders_list.loc[0] = ["A", 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
orders_list.loc[1] = ["C", 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
orders_list.loc[2] = ["C", 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
orders_list.loc[3] = ["A", 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]

orders_list.loc[4] = ["B", 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
orders_list.loc[5] = ["A", 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
orders_list.loc[6] = ["A", 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
orders_list.loc[7] = ["C", 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

orders_list.loc[8] = ["B", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
orders_list.loc[9] = ["A", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

orders_list.loc[10] = ["A", 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
orders_list.loc[11] = ["A", 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]

orders_list.to_csv("orders_list.csv")
