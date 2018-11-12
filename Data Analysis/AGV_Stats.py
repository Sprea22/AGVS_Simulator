import os
import sys
import pylab
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
from PIL import Image
from pylab import rcParams

rcParams['figure.figsize'] = 15, 10
# Graphic's different design
pyplot.style.use('ggplot')

# Reading the dataset about the current input for each year from 2005 to 2016
series2 = pd.read_csv("Elaborated_Datasets/AGV_Dataset.csv")

# Set the x axis tick
series2_temp = pd.DataFrame()
count = 0
configurations = ["BT1_A3", "BT2_A3", "BT3_A3", "BT1_A6", "BT2_A6", "BT3_A6", "BT1_A9", "BT2_A9", "BT3_A9", "BT1_A12", "BT2_A12", "BT3_A12"]
configurations_order = ["BT1_A3", "BT1_A6", "BT1_A9", "BT1_A12", "BT2_A3", "BT2_A6", "BT2_A9", "BT2_A12", "BT3_A3", "BT3_A6", "BT3_A9", "BT3_A12"]
parameters = ["Conflicts","Conflict_Wait","Conflict_Path","Waiting_Gate","Articles","Moving_Steps","Time_Steps"]

for conf in configurations:
    series2_temp = series2_temp.append(series2[series2["Conf"] == conf])

series2_temp = series2_temp.drop(["Unnamed: 0"], axis=1)

for param in parameters:
    series2_temp.pivot(index = "Conf", columns="AGV", values=param).reindex(configurations_order).plot(kind='bar', align="edge")
    pyplot.xticks(rotation='horizontal', horizontalalignment='left')
    pyplot.legend(ncol=1, fancybox=True, shadow=True)
    name_fig = "Output_Graphics/AGV/AGV_" + param + ".jpg"
    pyplot.title(param + " : configurations comparison over timesteps")
    pyplot.savefig(name_fig, format="jpg")
    #pyplot.show()
