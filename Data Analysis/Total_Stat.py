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
series2 = pd.read_csv("Elaborated_Datasets/Stats_Dataset.csv")
# Initialize the graphic's figure

# Set the x axis tick
series2_origin = series2[:]
count = 0
configurations = ["BT1_A3", "BT2_A3", "BT3_A3", "BT1_A6", "BT2_A6", "BT3_A6", "BT1_A9", "BT2_A9", "BT3_A9", "BT1_A12", "BT2_A12", "BT3_A12"]
configurations_order = ["BT1_A3", "BT1_A6", "BT1_A9", "BT1_A12", "BT2_A3", "BT2_A6", "BT2_A9", "BT2_A12", "BT3_A3", "BT3_A6", "BT3_A9", "BT3_A12"]
parameters = ["Conflicts","Conflict_Wait","Conflict_Path","Waiting_Gate","Articles","Moving_Steps","Time_Steps"]

series2 = series2.set_index(["Conf"]).reindex(configurations_order)

for param in parameters:
    series2[param].plot(kind='bar', align="edge")
    pyplot.xticks(rotation='horizontal', horizontalalignment='left')
    name_fig = "Output_Graphics/Total/Total_" + param + ".jpg"
    pyplot.title(param + ": Total stats of different configurations")
    pyplot.savefig(name_fig, format="jpg")
    #pyplot.show()
