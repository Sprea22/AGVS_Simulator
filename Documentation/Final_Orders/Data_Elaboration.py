import pandas as pd
import warnings
warnings.filterwarnings("ignore")

to_elab_total_orders = pd.read_csv("Total_Dataset.csv", sep = ';', index_col=0)

categories_list = list(set(to_elab_total_orders["CAT_ART"]))
categories_list = ["id_order"] + ["client"] + ["status"] + categories_list
orders_list = list(set(to_elab_total_orders["MVNUMDOC"]))
single_order = [0] * (len(categories_list))

total_orders = pd.DataFrame(columns=categories_list)
print("----------------------")
print("Total orders columns: ", len(total_orders.columns))
print("Dataset columns name: ", to_elab_total_orders.columns)
print("Numer of orders: ", len(orders_list))
print("Numer of categories: ", len(categories_list))
print("Single order length: ", len(single_order))
print("----------------------")

for i in range(0, len(orders_list)):
    order_rows = to_elab_total_orders[to_elab_total_orders["MVNUMDOC"] == orders_list[i]]
    for index, row in order_rows.iterrows():
        for j in range(0, len(categories_list)):
            if(categories_list[j] != "Order_Number"):
                if(categories_list[j] == row["CAT_ART"]):
                    row["MVQTAMOV"] = int(row["MVQTAMOV"].split(',')[0])
                    single_order[j] += row["MVQTAMOV"]
    total_orders.loc[i] = single_order
    total_orders["status"].iloc[i]= 0
    total_orders["id_order"].iloc[i]= i
    total_orders["client"].iloc[i] = order_rows["MVALFDOC"].iloc[0]

    single_order = [0] * (len(categories_list))

total_orders.set_index("id_order", inplace=True)
total_orders = total_orders.sample(frac=1).reset_index(drop=True)
total_orders.to_csv("Total_Orders.csv")
