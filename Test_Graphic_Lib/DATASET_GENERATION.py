import pandas as pd
import glob

# To generate total stats about each AGV dataset
path = "Total/*.csv"
db = pd.DataFrame()
for name in glob.glob(path):
    file = pd.read_csv(name)
    file = file.iloc[0:len(file)-1]
    file_length = len(file["Conflicts"])
    BT_name = name[6:9]
    N_AGV_name = name[10:][:-10]
    file["Conf"] = [BT_name+"_"+N_AGV_name] * file_length
    file["N_AGV"] = N_AGV_name
    db = db.append(file)

db.to_csv("TOTAL_agv_stats_dataset.csv")


# To generate total stats dataset

path = "Total/*.csv"
db = pd.DataFrame()
for name in glob.glob(path):
    file = pd.read_csv(name).iloc[-1].drop("AGV")
    BT_name = name[6:9]
    N_AGV_name = name[10:][:-10]
    file["Conf"] = BT_name+"_"+N_AGV_name
    file["N_AGV"] = N_AGV_name
    db = db.append(file)

db.to_csv("TOTAL_stats_dataset.csv", index=False)


# To generate total timesteps dataset
path = "Timesteps/*.csv"
db = pd.DataFrame()
for name in glob.glob(path):
    file = pd.read_csv(name)
    file_length = len(file["Conflicts"])
    BT_name = name[20:23]
    N_AGV_name = name[24:][:-10]
    file["Conf"] = [BT_name+"_"+N_AGV_name] * file_length
    file["time"] = list(range(0,file_length))
    db = db.append(file)

db.to_csv("TOTAL_timesteps_dataset.csv", index=False)
