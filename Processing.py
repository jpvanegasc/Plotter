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
	__param__ func_x: function that preprocess x data
	__param__ func_y: function that preprocess each y data
	__param__ columns:int number of columns to be saved. By default all
	__param__ no_repeat:bool clean file of repeated rows of data
	"""
	def __init__(self, file_path, f_x = None, f_y = None, columns = None, no_repeat = False):
		self.file_path = file_path
		self.file_name, self.clean_name = self.__get_filename()
		self.path = self.__get_path()
		self.labels = ('', '', '', '')
		self.f_x, self.f_y = f_x, f_y
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

	def __split_line(self, line, index = 1):
		"""Splits a line separated by diferent kinds of withespace"""
		if index == 0:
			pattern = re.compile(r'\ {2,}|\t')
		else:
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
		line = self.__split_line(line, index = 0)
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
		
		if self.f_x:
			x_var, x_unit = '', ''
		if self.f_y:
			y_var, y_unit = '', ''
		
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
		ignore_bool = False
		
		for i in range(len(data)):
			# Ignore single line or a whole block of data
			ignore_line = re.match(r'#|//', data[i])
			if ignore_line:
				continue
			
			if ignore_bool:
				ignore_end = re.match(r'"""|\*/', data[i])
				if ignore_end: ignore_bool = False
				continue
			
			ignore_start = re.match(r'"""|/\*', data[i])
			if ignore_start: 
				ignore_bool = True
				continue
			
			# Proccess data
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
			
			for ii, value in enumerate(line):
				if ii == 0:
					if not self.f_x:
						x.append(value)
					else:
						x.append(self.f_x(value))
				else:
					if bool(columns):
						if ii > columns - 1: continue
					
					if not self.f_y:
						y_list[ii-1].append(value)
					else:
						y_list[ii-1].append(self.f_y(value))
					

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
		if self.labels[0] == '':
			file_string = ''
		else: 
			file_string = f'{self.labels[2]}({self.labels[3]})\t{self.labels[0]}({self.labels[1]})\n'
		
		for i, elem in enumerate(self.data[0]):
			line = str(self.data[1][0][i]) + '\t' + str(elem) + '\n'
			file_string += line
		
		if save:
			with open(self.path + self.clean_name + '_transposed.txt', '+w') as file:
				file.write(file_string)
		else:
			print(file_string)

	def latex_table(self):
		"""Prints the data in LaTex format"""
		l_num = ''
		for i in range(len(self.data[1])+1):
			l_num += '|l'
		
		latex_command = '\\begin{table}\n\t\\centering\n\t\\begin{tabular}{%s|}\n\t\\hline\n' % l_num
		
		if self.labels[0] != '':
			latex_command += f'\t${self.labels[0]}$({self.labels[1]}) & ${self.labels[2]}$({self.labels[3]}) \\\\ \\hline\n'
		else:
			latex_command += '\t x_var(x_unit) & y_var(y_unit) \\\\ \\hline\n'
		
		for i in range(len(self.data[0])):
			x = self.data[0][i]
			y_line = []
			y_lambda = lambda y : y_line.append(' & %f' % y)
			for elem in self.data[1]: y_lambda(elem[i])
			y_str = ''.join(y_line)
			latex_command += '\t %f %s \\\\ \\hline \n'% (x, y_str)

		latex_command += '\t\\end{tabular}\n\t\\caption{table}\n\t\\label{tab: my_table}\n\\end{table}'
		print(latex_command)
