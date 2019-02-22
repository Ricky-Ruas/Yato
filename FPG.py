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
SKIP_FIRST_POINTS = 59
dannye = []
disp = 0
class signal_period:     #   класс разделяет последовательность на отдельные сигналы     
    def __init__(self, points):  #   функция инициализации
        self.Y_values = list(points)     #   создает список для записи одного сигнала
       

    def printTangent(self, xRange):  #функция рисует касательную
        yStart = self.Y_values[0]   #по начальным х,у и максимальным х,у в массиве одного сигнала
        yFinish = max(self.Y_values) 
         
        xStart = xRange[0]
        xFinish = xRange[np.argmax(self.Y_values)]
        #self.index_k = self.index_k.append(math.atan(yFinish))
        plt.plot([xStart, xFinish], [yStart, yFinish],'r')
    def printe(self, startX):  #функция рисует касательную вместе с сигналом(или наоборот)
        finishX = startX + len(self.Y_values)
        X = range(startX,finishX)
        plt.plot(X, self.Y_values, 'b')
        self.printTangent(X)
        return finishX+1

class Angle:
    def __init__(self, points):
        self.Y_values = list(points)
        self.index_k = list()

    def angle(self):
        y1 = self.Y_values[0]
        y2 = max(self.Y_values)
        x2 = np.argmax(self.Y_values)
        self.index_k = round((((math.atan(((y2-y1)/x2)))*180)/math.pi), 2)
        
        dannye.append(self.index_k)
        return dannye

   
def split(allPoints):
    periods = []
    curPointInd  = 0   
    while(True):
        skipPointsCount = curPointInd+SKIP_FIRST_POINTS
        isLastPeriod = False
        if(skipPointsCount > len(file.col2)):
            skipPointsCount = len(file.col2)
            isLastPeriod = True
        periodPoints = file.col2[curPointInd:skipPointsCount]
        currentPoints = periodPoints.values.tolist()
        curPointInd = skipPointsCount
        while(True):
            #print(str(curPointInd) +'\t' + str(len(file.col2)))
            if(isLastPeriod):
                break;
            if file.col2[curPointInd] > file.col2[curPointInd+1]:
                currentPoints.append(file.col2[curPointInd])
                curPointInd+=1
            else:
                break
        periods.append(signal_period(periodPoints))
               
        if(isLastPeriod):
            break;
   

    return periods

def angles(allPoints):
    curPointInd  = 0
    angle_mass = []
    while(True):
        skipPointsCount = curPointInd+SKIP_FIRST_POINTS
        isLastPeriod = False
        if(skipPointsCount > len(file.col2)):
            skipPointsCount = len(file.col2)
            isLastPeriod = True
        periodPoints = file.col2[curPointInd:skipPointsCount]
        currentPoints = periodPoints.values.tolist()
        curPointInd = skipPointsCount
        while(True):
            #print(str(curPointInd) +'\t' + str(len(file.col2)))
            if(isLastPeriod):
                break;
            if file.col2[curPointInd] > file.col2[curPointInd+1]:
                currentPoints.append(file.col2[curPointInd])
                curPointInd+=1
            else:
                break
        angle_mass.append(Angle(periodPoints))
        if(isLastPeriod):
            break;
    return angle_mass


splitPeriods = split(file)
curX = 0
for p in splitPeriods:
    curX = p.printe(curX)

angleLines = angles(file)

for an in angleLines:
    an = an.angle()
######
dispersionValue = np.var(an)
SKO = math.sqrt(dispersionValue)
meanValue = stts.mean(an)
modaValue = stts.mode(an)

norm_distrib = []
norm_distrib_highquality = []

for i in range(0, len(an)):
    three_sigma, two_sigma = SKO*3, SKO
    min_limit, max_limit = modaValue-three_sigma, modaValue+three_sigma
    min_limit_qual, max_limit_qual = modaValue-two_sigma, modaValue+two_sigma
    if an[i] >= min_limit and an[i] <= max_limit:
        norm_distrib.append(an[i])
    if an[i] >= min_limit_qual and an[i] <= max_limit_qual:
        norm_distrib_highquality.append(an[i])

print(len(dannye)) 

###################################
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
#    if 
    period_list.append(per_var)

period_list.append(1)
###################################
##########
#plt.grid(True)
plt.figure(2)
plt.plot(peak_index, dannye, 'b')
plt.xlabel('Значения углов') 
plt.ylabel('Массив значений')
plt.grid(True)

plt.figure(3)
plt.scatter(period_list, dannye)
plt.ylabel('Значения углов') 
plt.xlabel('Размер периодов')
plt.xticks([0, 50, 63, 100, 130, 200, 300])
plt.grid(True)

#plt.figure(2)
#y1 = plt.hist(norm_distrib, bins=35, label = 'Экпериментальные данные')
#y2 = plt.hist(norm_distrib_highquality, bins=30, alpha = 0.7, label = 'Экпериментальные данные. Высокая добростность')
#plt.legend()
#plt.xlabel('Значения углов') 
#plt.ylabel('Количество повторений')
#plt.grid(True)

#plt.figure(3)
#sst.probplot(norm_distrib, dist="norm", plot = plt)
#plt.title('Экпериментальные данные')
#plt.grid(True)

#plt.figure(4)
#sst.probplot(norm_distrib_highquality, dist="norm", plot = plt)
#plt.title('Экпериментальные данные. Высокая добротность')
#plt.grid(True) 

plt.show()


