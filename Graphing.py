#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math as m

import matplotlib.pyplot as pl
import numpy as np
from scipy import stats

import Editing as E
from Processing import DataProcessor

class Plotter(DataProcessor):
	"""
	Defines methods for graphing files using the pyplot lib
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._x, self._y = None, None
		self._log_x, self._log_y = False, False
		self.x = (self.labels[0], self.labels[1])
		self.y = (self.labels[2], self.labels[3])
		self.multiple_graphs = False
		self.no_title = False
		self.default_title = True
		self.default_labels = True
		self.default_filename = True

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
	def log_x(self, log:bool):
		if type(log) != bool:
			raise ValueError('Please pass a boolean value for log_x')
		
		self._log_x = bool(log)
	
	@log_y.setter
	def log_y(self, log:bool):
		if type(log) != bool:
			raise ValueError('Please pass a boolean value for log_y')
		self._log_y = bool(log)

	# Auxiliary methods
	def _get_title(self, x_var, x_unit, y_var, y_unit):
		"""Generates title in LaTex format"""
		title = r""

		if not self.log_x and not self.log_y:
			
			title = r'${0}\left({1}\right)\;contra\;{2}\left({3}\right)$'.format(
				y_var, y_unit, x_var, x_unit)

			return title

		elif self.log_x and not self.log_y:
			
			title = r'${0}\left({1}\right)\;contra\;log\left({2}\right)$'.format(
				y_var, y_unit, x_var)

			return title

		elif self.log_y and not self.log_x:
			
			title = r'$log\left({0}\right)\;contra\;{1}\left({2}\right)$'.format(
				y_var, x_var, x_unit)

			return title

		elif self.log_x and self.log_y:
			
			title = r'$log\left({0}\right)\;contra\;log\left({1}\right)$'.format(y_var, x_var)

			return title

	def _get_label(self, variable, unit, log = False):
		"""Generates axes names in LaTex format"""
		label = r''

		if not log:
			label = r'${0}\left({1}\right)$'.format(variable, unit)

			return label
		
		else:
			label = r'$log\left({0}\right)$'.format(variable)

			return label
	
	def __regression(self, x_values, y_values, degree):
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
			
			coef = np.polyfit(x_values, y, degree)
			f_fit = np.poly1d(coef)

			r_value = stats.linregress(x_values, y)[2]

			pl.plot(x_values, f_fit(x_values), label=str(f_fit)+'\nr^2 = %.4f' % round(r_value**2, 4))
	
	def __save_fig(self):
		"""Sets title, labels and saves figure"""
		if self.default_title:
			title = self._get_title(self.x['variable'], self.x['unit'], self.y['variable'], 
			self.y['unit'])
		else:
			title = input('What title do you want for the graph?\n')

		if self.default_labels:
			label_x, label_y = self.x['label'], self.y['label']
		else:
			label_x = input('What label do you want for the x-axis?\n')
			label_y = input('What label do you want for the y-axis?\n')

		if not self.no_title: pl.title(title)
		pl.xlabel(label_x)
		pl.ylabel(label_y)
		pl.legend()
		
		if self.default_filename:
			filename = self.clean_name
		else:
			filename = input('What filename do you want for the graph? (No extension)\n')
		
		if not self.multiple_graphs: 
			pl.savefig(self.path + filename +'.png')
			pl.close()

	# Graphing
	def scatter(self, reg:int = 0, **kwargs):
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
		colors = ['#000000', '#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
			'#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabebe', '#469990', '#e6beff',
			'#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#000075']
		pl.gca().set_prop_cycle('color', colors)

		# Plots data and regression
		for y in y_values:
			if len(y) == 0:
				break
			pl.scatter(x_values, y, s=5, **kwargs)
		
		if bool(reg):
			self.__regression(x_values, y_values, reg)

		self.__save_fig()

	def lines(self, reg:int = 0, **kwargs):
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
		colors = ['#000000', '#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
			'#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabebe', '#469990', '#e6beff',
			'#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#000075']
		pl.gca().set_prop_cycle(color = colors)

		# Plots data and regression
		for y in y_values:
			if len(y) == 0:
				break
			pl.plot(x_values, y, linewidth=1, **kwargs)
		
		if bool(reg):
			self.__regression(x_values, y_values, reg)
		
		self.__save_fig()

	def histogram(self, **kwargs):
		"""
		Generates an histogram graph and saves it
		__param__ **kwargs : this gets passed to the pyplot function
		__author__ : Juan Vanegas
		"""
		if len(self.data[1][0]) != 0:
			print('Careful! The file you are plotting contains more than one column\n')
		
		x_values = self.data[0]
			
		# Log graphs
		if self.log_x: x_values = E.convert_array_to_log(x_values)
		
		# Plots data
		pl.hist(x_values, linewidth=1, **kwargs)

		self.__save_fig()

	def frequency(self, scatter=True, **kwargs):
		"""
		if you got a better name for this method, please do change it
		Generates a frequency graph and saves it
		__param__ scatter:bool plots the graph as a scatter plot
		__param__ **kwargs : this gets passed to the pyplot function
		__author__ : Juan Vanegas
		"""
		if len(self.data[1][0]) != 0:
			print('Careful! The file you are plotting contains more than one column\n')

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
			pl.scatter(x_values, freq, color='darkblue', s=5, **kwargs)
		else:
			pl.plot(x_values, freq, color='darkblue', linewidth=1, **kwargs)
		
		self.__save_fig()	
