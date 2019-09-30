#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math as m
import re

import matplotlib.pyplot as pl
import numpy as np
from scipy import stats

import Editing as E

class DataProcessor:
	"""
	Defines methods for extracting and proccesing data from files

	__param__ file_path:str path to file to be unpacked
	__param__ columns:int number of columns to be saved. By default all
	__param__ no_repeat:bool clean file of repeated rows of data
	"""
	def __init__(self, file_path, columns = None, no_repeat = False):
		self.file_path = file_path
		self.file_name, self.clean_name = self.__get_filename()
		self.path = self.__get_path()
		self.labels = ()
		self.data = self.__get_clean_data(columns = columns, no_repeat = no_repeat)

	def __get_filename(self):
		file = self.file_path.split('/')[-1]
		clean = file.split('.')[0]
		return (file, clean)

	def __get_path(self):
		path = self.file_path.split('/')
		del(path[-1])
		path = '/'.join(path) + '/'
		return path
	
	# Auxiliary methods
	def __get_data_from_file(self, no_repeat):
		"""Extracts data from a file and divides it into rows"""
		with open(self.file_path, 'r') as file:
			data = file.read().strip()
		data = data.split('\n')

		if no_repeat: 
			temp = []
			for d in data:
				if d not in temp:
					temp.append(d)
			data = temp

		return data

	def __split_line(self, line):
		"""Splits a line separated by diferent kinds of withespace"""
		pattern = re.compile(r'\ +|\t')
		edited_line = pattern.split(line)
		temp_line = []

		for elem in edited_line:
			if elem != '':
				temp_line.append(elem)

		return temp_line

	def __get_first_line(self, line):
		"""
		Reads a line and, if possible, extracts axis names
		__param__ line:str
		"""
		pattern = re.compile(r'[\w\\\{\}]+\([\w^\\ \{\}]+\)')
		line = self.__split_line(line)
		srch_x, srch_y = False, False
		if len(line) >= 2:
			srch_x = pattern.search(line[0])
			srch_y = pattern.search(line[1])
		x_var, x_unit, y_var, y_unit = '', '', '', ''

		if srch_x:
			x = srch_x.group().replace(')', '').split('(')
			x_var = x[0].strip()
			x_unit = x[1].strip()
		
		if srch_y:
			y = srch_y.group().replace(')', '').split('(')
			y_var = y[0].strip()
			y_unit = y[1].strip()
		
		return (x_var, x_unit, y_var, y_unit)

	# Process file
	def __get_clean_data(self, columns = None, no_repeat = False):
		"""
		Reads the file containing the data to be plotted, process it, and stores it in
			lists
		__param__ no_repeat:bool ereases repeated data on a file
		__return__ :(x, y, y1, ... , y_n)
		"""
		data = self.__get_data_from_file(no_repeat)
		
		x = []
		y_list = [[], [], [], [], [], [], [], [], [], []]
		
		for i in range(len(data)):
			line = self.__split_line(data[i])

			if i==0:
				try:
					line = E.convert_array_to_float(line)
				except:
					self.labels = self.__get_first_line(data[i]) 
					print(f'Careful! First line omitted on {self.file_name}')
					continue

			else:
				line = E.convert_array_to_float(line)
			
			for i, value in enumerate(line):
				if i == 0:
					x.append(value)
				else:
					if bool(columns):
						if i > columns - 1: continue

					y_list[i-1].append(value)

		# Numpy arrays		
		temp_y = []
		for y in y_list:
			if len(y) != 0:
				temp_y.append(np.array(y, dtype = np.double, order = 'C'))
			else:
				break
		
		y_list = temp_y
		x = np.array(x, dtype = np.double, order = 'C')

		return (x, y_list)

	# Other stuff
	def transpose_data(self, save = True):
		"""Transpose x and y1 only"""
		file_string = ''

		for i, elem in enumerate(self.data[0]):
			line = str(self.data[1][0][i]) + '\t' + str(elem) + '\n'
			file_string += line
		
		if save:
			with open(self.path + self.clean_name + '_transposed.txt', '+w') as file:
				file.write(file_string)
		else:
			print(file_string)
