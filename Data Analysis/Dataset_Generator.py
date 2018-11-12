import pandas as pd
import glob

# To generate total stats about each AGV dataset
path = "Source_Datasets/Total/*.csv"
db = pd.DataFrame()
for name in glob.glob(path):
    file = pd.read_csv(name, sep=';')
    file = file.iloc[0:len(file)-1]
    file_length = len(file["Conflicts"])
    BT_name = name[22:25]
    N_AGV_name = name[26:][:-10]
    file["Conf"] = [BT_name+"_"+N_AGV_name] * file_length
    file["N_AGV"] = N_AGV_name
    db = db.append(file)

db.to_csv("Elaborated_Datasets/AGV_Dataset.csv")


# To generate total stats dataset

path = "Source_Datasets/Total/*.csv"
db = pd.DataFrame()
for name in glob.glob(path):
    file = pd.read_csv(name, sep=";").iloc[-1].drop("AGV")
    BT_name = name[22:25]
    N_AGV_name = name[26:][:-10]
    file["Conf"] = BT_name+"_"+N_AGV_name
    file["N_AGV"] = N_AGV_name
    db = db.append(file)

db.to_csv("Elaborated_Datasets/Stats_Dataset.csv", index=False)


# To generate total timesteps dataset
path = "Source_Datasets/Timesteps/*.csv"
db = pd.DataFrame()
for name in glob.glob(path):
    file = pd.read_csv(name, sep=";")
    file_length = len(file["Conflicts"])
    BT_name = name[36:39]
    N_AGV_name = name[40:][:-10]
    file["Conf"] = [BT_name+"_"+N_AGV_name] * file_length
    file["time"] = list(range(0,file_length))
    db = db.append(file)

db.to_csv("Elaborated_Datasets/Timesteps_Dataset.csv", index=False)
