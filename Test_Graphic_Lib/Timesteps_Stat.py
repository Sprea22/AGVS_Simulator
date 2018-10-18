import os
import sys
import pylab
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
from PIL import Image

# Graphic's different design
pyplot.style.use('ggplot')

# Reading the dataset about the current input for each year from 2005 to 2016
series2 = pd.read_csv("TOTAL_timesteps_dataset.csv")
# Initialize the graphic's figure
fig2 = pyplot.figure()
ax = fig2.add_subplot(111)

# Set the x axis tick
series2_origin = series2[:]

parameters = series2.columns.values.tolist()
parameters = parameters[1:len(parameters)-2]
print(parameters)
cont = 0
configurations = ["BT1_A3", "BT1_A6", "BT1_A9", "BT1_A12", "BT2_A3", "BT2_A6", "BT2_A9", "BT2_A12", "BT3_A3",  "BT3_A6", "BT3_A9", "BT3_A12"]

for param in parameters:
    for conf in configurations:
        series_temp = series2[series2["Conf"] == conf]
        pyplot.plot(series_temp["time"], series_temp[param], linewidth=2, alpha=0.8, label = series_temp["Conf"].iloc[0])
    pyplot.legend(ncol=1, fancybox=True, shadow=True)
    pyplot.legend(ncol=1, fancybox=True, shadow=True)
    name_fig = "Graphics Images/Timesteps" + param + ".jpg"
    pyplot.title(param + " : configurations comparison over timesteps")
    pyplot.savefig(name_fig, format="jpg")
    ax.clear()

#pyplot.show()
#saveFigure("_Years.jpg")
