
                                  
'''
Модуль 8
Сглаживание исходного сигнала
'''

################################################################################################################################################################################################################

#############################################################################################
           ### Пункт 1. Объявление библиотек, загрузка файлов из внешних файлов ###   
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

file = pd.DataFrame(pd.read_excel(io='part_5(2).xlsx', header=[0], usecols=[0, 1])).fillna(0) 
sequence_of_values_of_a_signal = file.col2                                                   #      Исходные данные
abscissa_axis = list(range(0, len(sequence_of_values_of_a_signal)))                          #      Отсчеты(индексы для перебора)

experiment_sequence = sequence_of_values_of_a_signal

var_axis = list(abscissa_axis)
#############################################################################################
                 ### Пункт 1.2. Объявление функций ###   
#############################################################################################

class signal_period:     #   класс разделяет последовательность на отдельные сигналы     
    def __init__(self, line):  #   функция инициализации
        self.values_line = list(line)     #   создает список для записи одного сигнала
        

    def printF(self):  #функция рисует касательную
        xStart = self.values_line[0]
        xFinish = self.values_line[2]
        yStart = self.values_line[1]  
        yFinish = self.values_line[3]
        
        ax = plt.plot([xStart, xFinish], [yStart, yFinish],'r')
        return ax

def angleInclination(data):
    dannye = []
    Y_values = data
    for i in range(0, len(Y_values)):
        y1 = Y_values[i][1]
        x2 = Y_values[i][2] - Y_values[i][0]
        y2 = Y_values[i][3]
        
        index_k = round((((math.atan(((y2-y1)/x2)))*180)/math.pi), 2)
        #index_k = round((((math.atan(((y2-y1)/x2))), 2)
        dannye.append(index_k)
    return dannye

def drawing(line):
    periods = []
    for i in range(0, len(line)):
        periods.append(signal_period(line[i]))
    return periods

def period(data1):                               #### Находится величина периода 
    var_period_value = []
    var_period_list = []
    for i in range(0, len(data1)-1):
        var_period_value = data1[i+1][0] - data1[i][0]
        var_period_list.append(var_period_value)
        if i == len(data1)-2:
            var_period_value = abs(data1[i][0] - data1[i-1][0])
            var_period_list.append(var_period_value)
    return var_period_list

def stats(data):                                 #### Находятся статистические параметры
    SKO = np.std(data)
    meanValue = stts.mean(data)
    list_table = stts._counts(data)
    len_table = len(list_table)
    if len_table == 1:
        modaValue = stts.mode(data)
    else: 
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        modaValue = max(new_list) # use the max value here
    
    l = [SKO, meanValue, modaValue]
    return l


############################################################################################
####    Нахождение начала и конца прямой  ####
############################################################################################
all_values = []
pointA = []
pointA_index = []
pointB = []
pointB_index = []
count = 0
signal_sequence = []

cut = experiment_sequence[:200]
mini = min(cut)
maxi = max(cut)
differ = (maxi-mini)*0.4

for i in range(0, len(var_axis)-1):
    if count == 0:
        A = experiment_sequence[i]
        A_ind = var_axis[i]
        count += 1
    if i > 0:
        x1 = experiment_sequence[i-1]
        x2 = experiment_sequence[i+1]
        if experiment_sequence[i] <= x1 and experiment_sequence[i] < x2:
            A = experiment_sequence[i]
            A_ind = var_axis[i]
        if experiment_sequence[i] > x1 and experiment_sequence[i] >= x2:
            B = experiment_sequence[i]
            B_ind = var_axis[i]
            if (B-A) >= differ:
                pointA.append(A)
                pointA_index.append(A_ind)
                pointB.append(B)
                pointB_index.append(B_ind)
                X = [A_ind, A, B_ind, B]
                all_values.append(X)

filt_all_values = []
for i in range(0, len(all_values)):
    if (all_values[i][2]-all_values[i][0]) < 150:
        filt_all_values.append(all_values[i])
                
splitting = drawing(filt_all_values)

for p in splitting:
    curX = p.printF()


valueAngles = angleInclination(filt_all_values)
valuePeriod = period(filt_all_values)
print(stats(valueAngles), stats(valuePeriod), len(valuePeriod))


plt.plot(var_axis, experiment_sequence, 'b')
plt.plot(pointA_index, pointA, 'ro')
plt.plot(pointB_index, pointB, 'ko')
plt.grid(True)

plt.figure(2)
plt.title('Зависимость угла наклона "переднего фронта" от ширины периода сигнала')
plt.scatter(valuePeriod, valueAngles, s=25, c='c', alpha=0.7)
plt.ylabel('Значения углов') 
plt.xlabel('Размер периодов')
plt.legend()

plt.grid(True)

plt.show()