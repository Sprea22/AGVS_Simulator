import os
import sys
import pylab
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
from PIL import Image

#%%%%%%%%%%%%%%%%%%%%%%%%%
# SAVE GRAPHIC LIKE IMAGE#
#%%%%%%%%%%%%%%%%%%%%%%%%%
def saveFigure(descr):
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, sys.argv[1]+"/")
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    pyplot.savefig(results_dir + sys.argv[1]+descr, format="jpg")


# Graphic's different design
pyplot.style.use('ggplot')

# Reading the dataset about the current input for each year from 2005 to 2016
series2 = pd.read_csv("TOTAL_agv_stats_dataset.csv")

# Set the x axis tick
series2_temp = pd.DataFrame()
count = 0
configurations = ["BT1_A3", "BT3_A3", "BT1_A6", "BT3_A6", "BT1_A9",  "BT3_A9", "BT1_A12", "BT3_A12"]

for conf in configurations:
    series2_temp = series2_temp.append(series2[series2["Conf"] == conf])

print(series2_temp)
series2_temp.pivot(index = "Conf", columns="AGV", values="Conflicts").plot(kind='bar', align="edge")
pyplot.xticks(rotation='horizontal', horizontalalignment='left')
pyplot.show()

#saveFigure("_Years.jpg")
