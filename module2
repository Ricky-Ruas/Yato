



#############################################################################################
                    #Модуль2
                    #Предназначен для исправления алгоритма по разбиению 
                    #сигнала на периоды и построение углов наклона ВЕРСИЯ 1.1 - сначало
                    #фильтруем исходный сигнал кубическим сплайном
#############################################################################################

import csv
import xlwt
import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as sst
import statistics as stts
import matplotlib

####
file = pd.DataFrame(pd.read_excel(io='FPG.xlsx', header=[0], usecols=[0, 1])).fillna(0) 

sequence_of_values_of_a_signal = file.col2          ######## ВОООТ!!! ВОТ ОН МАССИВ, КОТОРЫЙ НУЖНО ИСПОЛЬЗОВАТЬ ПРИ РИСОВАНИИ ЛИНИЙ!!!!!!

abscissa_axis = list(range(0, len(sequence_of_values_of_a_signal)))
abscissa_axis0 = list(range(0, len(sequence_of_values_of_a_signal)-2))

#############################################################################################
                        ### Нахождение второй производной от сигнала ###   
#############################################################################################
diff_secondary = np.gradient(sequence_of_values_of_a_signal, edge_order = 2)

#############################################################################################
    ### Разбиение сигнала для рисования прямой на начало сигнала и на пиковое значение ###   
#############################################################################################

count_period = diff_secondary
dif_index1 = []
val_dif1 = []

for i in range(1, len(diff_secondary)-1):
    if count_period[i-1] < 0 and count_period[i+1] > 0 : ## Началo периода(возрастание прямой)
        dif_index1.append(i)
        val_dif1.append(count_period[i])
     
############################################################################################
####  Удаление лишних значений (второго рядом стоящего значения) из выбранных точек возрастания функции   ####
############################################################################################

def filtr_values(data1, data2):
    value_signal_index = []
    value_signal = []
    for i in range(0, len(data1)-1, 2):
        disparity_value = data1[i] - data1[i+1]
        if disparity_value < 2:
            value_signal_index.append(data1[i])
            value_signal.append(data2[i])
    return value_signal_index, value_signal

start_signal = filtr_values(dif_index1, val_dif1)

start_value_period_signal = start_signal[1]
start_value_index_period_signal = start_signal[0]

############################################################################################
####  Нахождение периода сигнала (так, на всякий случай - чтобы убрать значения-"некондицию")   ####
############################################################################################

def period(data1):
    var_period_value = []
    var_period_list = []
    for i in range(0, len(data1)-1):
        var_period_value = data1[i+1] - data1[i]
        var_period_list.append(var_period_value)
    return var_period_list

def stats(data):
    SKO = np.std(data)
    meanValue = stts.mean(data)
    modaValue = stts.mode(data)
    l = [SKO, meanValue, modaValue]
    return l

initial_value_index_period = period(start_value_index_period_signal)
initial_value_stats = stats(initial_value_index_period)

############################################################################################
####  Нахождение периода для наклонa прямой с удалением некондиции   ####
############################################################################################

filt_values_index = []
for i in range(0, len(start_value_index_period_signal)-1):
    const0_plus = initial_value_stats[2] + initial_value_stats[0]
    const0_minus = initial_value_stats[2] - initial_value_stats[0]
    const1 = start_value_index_period_signal[i+1] - start_value_index_period_signal[i]
    if const1 <= const0_plus and const1 >= const0_minus:
        filt_values_index.append(start_value_index_period_signal[i])
        
  
############################################################################################
####    Нахождение максимума (конечной точки для наклонной прямой) в периодах_"кондициях"  ####
############################################################################################
end_point_line = []
end_point_line_index = []
init_point_line = []
init_point_line_index = []
signal_sequence = []
raa = []
sss = []
for i in range(0, len(filt_values_index)-1):
    start = filt_values_index[i]
    end = filt_values_index[i+1]
    single_period = list(sequence_of_values_of_a_signal [start : end])
    maxi = max(single_period)
    mini = min(single_period)
    index_max = single_period.index(maxi)+start

    signal_sequence.append(single_period)
    end_point_line.append(maxi)                                 #---- Конечное значение прямой    
    end_point_line_index.append(index_max)                      #---- Конечный индекс прямой    
    init_point_line.append(single_period[0])                    #---- Начальное значение прямой    
    init_point_line_index.append(start)                         #---- Начальный индекс прямой
    raa.append(diff_secondary[start])
    sss.append(np.max(diff_secondary[start:end]))
############################################################################################
####   Рисование прямой по начальной и конечной точкам   ####
############################################################################################  
all_values = []
for i in range(0, len(end_point_line)):
    X = [init_point_line_index[i], init_point_line[i], end_point_line_index[i], end_point_line[i]]
    all_values.append(X)

class signal_period:     #   класс разделяет последовательность на отдельные сигналы     
    def __init__(self, line, signal):  #   функция инициализации
        self.values_line = list(line)     #   создает список для записи одного сигнала
        self.values_signal = list(signal)

    def printTangent(self, V):  #функция рисует касательную
        xStart = self.values_line[0]
        xFinish = self.values_line[2]
        yStart = self.values_line[1]  
        yFinish = self.values_line[3]
        
        plt.plot([xStart, xFinish], [yStart, yFinish],'r')

    def printe(self):  #функция рисует касательную вместе с сигналом(или наоборот)
        max = self.values_line[0]+len(self.values_signal)
        X = range(self.values_line[0], max)
        plt.plot(X, self.values_signal, 'b')
        self.printTangent(X)
        return max

def drawing(line, signal):
    periods = []
    for i in range(0, len(line)):
        periods.append(signal_period(line[i], signal[i]))
    return periods

splitting = drawing(all_values, signal_sequence)
for p in splitting:
    curX = p.printe()


#############################################################################################
                        ###  Отрисовка графиков   ###
#############################################################################################
plt.figure(1)
plt.plot(abscissa_axis, sequence_of_values_of_a_signal, 'b')
#plt.plot(X_Y_values.X, X_Y_values.Y, 'r')

plt.grid(True)

plt.figure(2)
plt.plot(abscissa_axis, diff_secondary, 'r')
plt.grid(True)

#plt.figure(3)
#plt.plot(abscissa_axis, diff_secondary, 'r')
#plt.grid(True)

plt.show()

