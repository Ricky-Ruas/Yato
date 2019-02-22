



#############################################################################################
                    #Модуль4
                    #Предназначен для исправления алгоритма по разбиению 
                    #сигнала на периоды и построение углов наклона. ВЕРСИЯ 1.3
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
                        ### Фильтрация кубическим сплаином ###   
#############################################################################################

import math


class Spline:
    def __init__(self, coefficients, horizontal_knots, spline_degree=3):
        self.k = spline_degree
        self.k_fact = math.factorial(self.k)
        self.coefficients = coefficients
        horizontal_knots.sort()
        self.g = len(horizontal_knots) - 2
        self.a = horizontal_knots[0]
        self.b = horizontal_knots[self.g + 1]
        self.knots = [self.a] * (self.k + 1) + [0] * self.g + [self.b] * (self.k + 1)
        for i in range(self.g):
            self.knots[i + self.k + 1] = horizontal_knots[i + 1]

    def get_left_node_index(self, point, min_id=0):
        if point < self.a or point > self.b:
            return -1

        l = min_id
        while l < self.g + self.k and (self.knots[l] > point or self.knots[l + 1] <= point):
            l += 1
        return l

    # evaluate B-spline of degree deg on interval [λ_{knot_id}, λ_{knot_id+deg+1}) at given point
    def b_spline(self, point, deg, knot_id):
        if point < self.knots[knot_id] or point > self.knots[knot_id + deg + 1]:
            return 0

        if deg == 0:
            return point != self.knots[knot_id + deg + 1]

        # if there are k + 1 coincident points on the left side
        if self.knots[knot_id + deg] < self.knots[knot_id + deg + 1]:
            j = 0
            while j < deg and self.knots[knot_id + j] == self.knots[knot_id + j + 1]:
                j += 1
            if j == deg:
                return pow((self.knots[knot_id + deg + 1] - point) /
                           (self.knots[knot_id + deg + 1] - self.knots[knot_id]), deg)

        # if there are k + 1 coincident points on the right side
        if self.knots[knot_id] < self.knots[knot_id + 1]:
            j = 1
            while j <= deg and self.knots[knot_id + j] == self.knots[knot_id + j + 1]:
                j += 1
            if j == deg + 1:
                return pow((point - self.knots[knot_id]) /
                           (self.knots[knot_id + deg + 1] - self.knots[knot_id]), deg)

        l = self.get_left_node_index(point, knot_id)
        buff = [0] * (deg + 1)
        buff[knot_id - l + deg] = 1

        for j in range(1, deg + 1):
            for i in reversed(range(l - deg + j, l + 1)):
                alpha = (point - self.knots[i]) / (self.knots[i + 1 + deg - j] - self.knots[i])
                buff[i - l + deg] = alpha * buff[i - l + deg] + (1 - alpha) * buff[i - 1 - l + deg]

        return buff[deg]
