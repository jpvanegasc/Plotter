#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math as m
import re

import matplotlib.pyplot as pl
import numpy as np
from scipy import stats
import scipy.optimize as opt

import Editing as E
from Processing import DataProcessor

class Plotter(DataProcessor):
    """
    Defines methods for graphing files using the pyplot lib
    """
    colors = ['#000000', '#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4', 
            '#42d4f4', '#f032e6', '#fabebe', '#469990', '#e6beff', '#9A6324', 
            '#fffac8', '#800000', '#aaffc3', '#808000', '#000075', "#ffe119", "#bfef45"]
    multiple_graphs = False
    no_title = True
    default_title = True
    default_labels = True
    default_filename = True
    grid = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._x, self._y = None, None
        self._log_x, self._log_y = False, False
        self._color = None

        self.x = (self.labels[0], self.labels[1])
        self.y = (self.labels[2], self.labels[3])
        self.color = 0

    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y

    @property
    def log_x(self):
        return self._log_x
    
    @property
    def log_y(self):
        return self._log_y

    @property
    def color(self):
        return self._color

    @x.setter
    def x(self, x_value):
        try:
            x_variable, x_unit = x_value
        except ValueError:
            raise ValueError(
                "Please pass an iterable with two items: x_variable, x_unit")
        else:
            label = self._get_label(x_variable, x_unit, log = self.log_x)
            self._x = {'variable':x_variable, 'unit':x_unit, 'label':label}

    @y.setter
    def y(self, y_value):
        try:
            y_variable, y_unit = y_value
        except ValueError:
            raise ValueError(
                "Please pass an iterable with two items: y_variable, y_unit")
        else:
            label = self._get_label(y_variable, y_unit, log = self.log_y)
            self._y = {'variable':y_variable, 'unit':y_unit, 'label':label}
    
    @log_x.setter
    def log_x(self, log):
        self._log_x = bool(log)
        self.x = (self.x['variable'], self.x['unit'])
    
    @log_y.setter
    def log_y(self, log):
        self._log_y = bool(log)
        self.y = (self.y['variable'], self.y['unit'])

    @color.setter
    def color(self, num:int):
        if type(num) != int:
            raise ValueError("Color must be an int")
        self._color = self.colors[num]
        

    # Auxiliary methods
    def _get_label(self, variable, unit, log=False):
        """Generates axes names in LaTex format"""
        flag = re.search(r'd\w*_less', unit)
        label = r''

        if not log:
            if not flag:
                label = r'$%s\left(\mathrm{%s}\right)$' % (variable, unit)
            else:
                label = r'${0}$'.format(variable)

            return label
        
        else:
            label = r'$log\left({0}\right)$'.format(variable)

            return label
    
    def __regression(self, x_values, y_values, degree, low = 0, up=None, reg_label=None):
        """
        Plots a polynomial fit for each pair (x, y_n) on y values
        __param__ x_values:list fixed x values for each individual y value group
        __param__ y_values:list group oof all the y values found on the file
        __param__ degree:int degree of the polynomial to be fitted
        __author__ : Juan Vanegas
        """
        for y in y_values:
            if len(y) == 0:
                break
            
            x_values = x_values[low:up]
            y = y[low:up]

            coef = np.polyfit(x_values, y, degree)
            f_fit = np.poly1d(coef)

            r_value = stats.linregress(x_values, y)[2]
            
            if reg_label: label= '\n'+ reg_label
            else: label = ''
            
            pl.plot(x_values, f_fit(x_values), c=self.color, 
                label=str(f_fit)+'\n$r² = %.4f$' % round(r_value**2, 4)+label)
    
    def __function_fit(self, x_values, y_values, function):
        """
        Plots a curve fit -for a given curve-, for each pair 
        """
        for y in y_values:
            if len(y) == 0:
                break
            
            optimizedParameters = opt.curve_fit(function, x_values, y)[0]
            
            r_value = stats.linregress(x_values, y)[2]

            pl.plot(x_values, function(x_values, *optimizedParameters), c=self.color, 
                label=str(function)+'\nr² = %.4f' % round(r_value**2, 4))

    def __save_fig(self):
        """Sets title, labels and saves figure"""
        if self.default_title:
            title = r'{0} contra {1}'.format(self.y['label'], self.x['label'])
        else:
            title = input('What title do you want for the graph?\n')

        if self.log_x:
            self.x['label'] = self._get_label(self.x['variable'], self.x['unit'], log = True)
        if self.log_y:
            self.y['label'] = self._get_label(self.y['variable'], self.y['unit'], log = True)

        if self.default_labels:
            label_x, label_y = self.x['label'], self.y['label']
        else:
            label_x = input('What label do you want for the x-axis?\n')
            label_y = input('What label do you want for the y-axis?\n')

        if not self.no_title: pl.title(title)
        pl.xlabel(label_x)
        pl.ylabel(label_y)
        pl.legend()
        if self.grid: pl.grid(b=True, which='both')

        if self.default_filename:
            filename = self.clean_name
        else:
            filename = input('What filename do you want for the graph? (No extension)\n')
        
        if not self.multiple_graphs: 
            pl.savefig(self.path + filename +'.png')
            pl.close()

    # Graphing
    def scatter(self, reg:int=0, fit=None, reg_l=None, ms=5, **kwargs):
        """
        Generates a scatter graph and saves it
        __param__ reg:int degree of the polynomial used for adjusting ALL data. Default 0
            means no regression is plotted
        __param__ **kwargs : this gets passed to the pyplot function
        __author__ : Juan Vanegas
        """
        x_values, y_values = self.data

        if self.log_x: x_values = E.convert_array_to_log(x_values)
        if self.log_y:
            temp_y = []
            for y in y_values:
                temp_y.append(E.convert_array_to_log(y))
            y_values = temp_y
        
        # Set color cycle
        pl.gca().set_prop_cycle('color', self.colors)

        # Plots data and regression
        for y in y_values:
            if len(y) == 0:
                break
            pl.scatter(x_values, y, c=self.color, s=ms, **kwargs)
        
        if bool(reg):
            self.__regression(x_values, y_values, reg, reg_label=reg_l)
        
        if bool(fit):
            self.__function_fit(x_values, y_values, fit)

        self.__save_fig()

    def lines(self, reg:int=0, fit=None, reg_l=None, lw=1, **kwargs):
        """
        Generates a graph with lines and saves it
        __param__ reg:int degree of the polynomial used for adjusting ALL data. Default 0
            means no regression is plotted
        __param__ **kwargs : this gets passed to the pyplot function
        __author__ : Juan Vanegas
        """
        x_values, y_values = self.data

        if self.log_x: x_values = E.convert_array_to_log(x_values)
        if self.log_y:
            temp_y = []
            for y in y_values:
                temp_y.append(E.convert_array_to_log(y))
            y_values = temp_y
        
        # Set color cycle
        pl.gca().set_prop_cycle('color', self.colors)

        # Plots data and regressions
        for y in y_values:
            if len(y) == 0:
                break
            pl.plot(x_values, y, c=self.color, linewidth=lw, **kwargs)
        
        if bool(reg):
            self.__regression(x_values, y_values, reg, reg_label=reg_l)

        if bool(fit):
            self.__function_fit(x_values, y_values, fit)
        
        self.__save_fig()

    def histogram(self, lw=1, **kwargs):
        """
        Generates an histogram graph and saves it
        __param__ **kwargs : this gets passed to the pyplot function
        __author__ : Juan Vanegas
        """
        if len(self.data[1][0]) != 0:
            print('Warning: The file you are plotting contains more than one column\n')
        
        x_values = self.data[0]
            
        # Log graphs
        if self.log_x: x_values = E.convert_array_to_log(x_values)
        
        # Plots data
        pl.hist(x_values, linewidth=lw, **kwargs)

        self.__save_fig()

    def frequency(self, scatter=True, reg:int=0, fit=None, reg_l=None, ms=5, lw=1, **kwargs):
        """
        if you got a better name for this method, please do change it
        Generates a frequency graph and saves it
        __param__ scatter:bool plots the graph as a scatter plot
        __param__ **kwargs : this gets passed to the pyplot function
        __author__ : Juan Vanegas
        """
        if len(self.data[1][0]) != 0:
            print('Warning: The file you are plotting contains more than one column\n')

        # Generates the y values
        sorted_data = sorted(self.data[0])
        x_values, freq = [], []

        for dat in sorted_data:
            if dat not in x_values:
                x_values.append(float(dat))
                freq.append(1.0)
            else:
                freq[-1] += 1.0

        # Log graphs
        if self.log_x: x_values = E.convert_array_to_log(x_values)
        if self.log_y: freq = E.convert_array_to_log(freq)
        
        # Plots data
        if scatter:
            pl.scatter(x_values, freq, color='darkblue', s=ms, **kwargs)
        else:
            pl.plot(x_values, freq, color='darkblue', linewidth=lw, **kwargs)

        if bool(reg):
            self.__regression(x_values, freq, reg, reg_label=reg_l)

        if bool(fit):
            self.__function_fit(x_values, freq, fit)
        
        self.__save_fig()
