



#############################################################################################
                    #Модуль3
                    #Предназначен для исправления алгоритма по разбиению 
                    #сигнала на периоды и построение углов наклона. ВЕРСИЯ 1.2
#############################################################################################

import csv
import xlwt
import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as sst
import scipy.interpolate as sint
import scipy.signal as ssig
import scipy as sp
import statistics as stts
import matplotlib

####
file = pd.DataFrame(pd.read_excel(io='FPG.xlsx', header=[0], usecols=[0, 1])).fillna(0) 

kol = file.col2     ######## ВОООТ!!! ВОТ ОН МАССИВ, КОТОРЫЙ НУЖНО ИСПОЛЬЗОВАТЬ ПРИ РИСОВАНИИ ЛИНИЙ!!!!!!
leng = len(kol)
abscissa_axis = pd.Series(range(0, leng))
abscissa_axis0 = list(range(0, leng-2))

#############################################################################################
                        ### Интерполяция кубическим сплаином ###   
#############################################################################################
sequence_of_values_of_a_signal = kol
for i in range(0, leng):
    sequence_of_values_of_a_signal[i] = round(kol[i])
                                                                                                                    ##cubic = ssig.cspline1d(sequence_of_values_of_a_signal, 0.0)
                                                                                                                    #filt_mass1 = []
                                                                                                                    #filt_mass2 = []
                                                                                                                    #filt_mass3 = []
                                                                                                                    #filt_mass4 = []
                                                                                                                    #filt_mass5 = []
                                                                                                                    #filt_mass6 = []
                                                                                                                    #k = leng//10   
                                                                                                                    #filt_mass1.extend(sequence_of_values_of_a_signal[0:k])
                                                                                                                    #filt_mass2.extend(sequence_of_values_of_a_signal[k*1:k*2])
                                                                                                                    #filt_mass3.extend(sequence_of_values_of_a_signal[k*2:k*3])
                                                                                                                    #filt_mass4.extend(sequence_of_values_of_a_signal[k*3:k*4])
                                                                                                                    #filt_mass5.extend(sequence_of_values_of_a_signal[k*4:k*5])
                                                                                                                    #filt_mass6.extend(sequence_of_values_of_a_signal[k*5:k*6])
                                                                                                                    #a = sp.array([filt_mass1, filt_mass2, filt_mass3, filt_mass4, filt_mass5, filt_mass6])
                                                                                                                    #cub_filt = ssig.spline_filter(a, 5.0)

##m = ssig.savgol_filter(kol, 29, 3)        ###ФИльтрация Савичкого-Голея
mm = ssig.savgol_filter(kol, 21, 3)

m = ssig.resample(mm, leng*2)              ###Увеличенная в 2 раза частота дискретизации
xnew = np.linspace(0, leng, leng*2, endpoint=False)
value_list = []
#print(m)              
diff_secondary = np.gradient(m, edge_order = 2)
for i in range(0, len(diff_secondary)):
    if diff_secondary[i] >= -2.5 and diff_secondary[i] <= 3.5:
        value_list.append(diff_secondary[i])
    if diff_secondary[i] < -2.5:
        value_list.append(-2)
    if diff_secondary[i] > 3.5:
        value_list.append(3)

x = list(range(0, len(value_list)))
plt.figure(1)
plt.plot(x, value_list, 'r')
plt.grid(True)

plt.figure(2)
plt.plot(abscissa_axis, sequence_of_values_of_a_signal, 'b')
plt.plot(xnew, m, 'r')
#plt.plot(abscissa_axis, cub_filt, 'r--')
plt.grid(True)
plt.show()

