import csv
import xlwt
import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as sst
import statistics as stts
import sympy as sm
import matplotlib
######################################################################################
file = pd.DataFrame(pd.read_excel(io='FPG.xlsx', header=[0], usecols=[1])).fillna(0)

func = file.col2
x1 = list(range(0, len(func)))

diff_secondary = np.gradient(func)
max = len(diff_secondary)
x2 = list(range(0, max))
gradie = diff_secondary
l = []

def stats(data):
    SKO = np.std(data)
    meanValue = stts.mean(data)
    modaValue = stts.mode(data)
    l = [SKO, meanValue, modaValue]
    return l


g = stats(gradie)
for_plot = pd.Series(data = g[0], index =  x2)
for_plot2 = pd.Series(data = g[1], index = x2)
for_plot3 = pd.Series(data = g[2], index = x2)

peak_values = []
peak_index = []
for i in range(1, len(gradie)-2):
    if gradie[i] > g[0]*2.57:
        if gradie[i-1] < gradie[i] and gradie[i] > gradie[i+1]:
            peak_values.append(gradie[i])
            peak_index.append(i)

period_list = []
#period_dict = {start, }
for i in range(0, len(peak_index)-1):
    per_var = peak_index[i+1] - peak_index[i]

    period_list.append(per_var)
period_list.append(0)

#plt.figure(1)
#plt.plot(peak_index, peak_values, 'b')
#plt.grid(True)
  
#plt.figure(2)
#plt.plot(x2, gradie, label = 'Сигнал')
#plt.plot(x2, for_plot, 'r', label = 'Среднее квадратичное отклонение')
##plt.plot(peak_index, for_plot2, 'g', label ='Среднее значение' )
##plt.plot(peak_index, for_plot3, 'y', label = 'Мода')
##plt.legend()
###plt.xlabel('Значения углов') 
###plt.ylabel('Количество повторений')
#plt.grid(True)

#plt.show()

