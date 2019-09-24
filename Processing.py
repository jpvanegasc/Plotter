#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math as m

import matplotlib.pyplot as pl
import numpy as np
from scipy import stats

import Editing as E

class DataProcessor:
	"""
	Defines methods for extracting and proccesing data from files
	"""
	def __init__(self, file_path, no_repeat = False):
		self.file_path = file_path
		self.file_name, self.clean_name = self.__get_filename()
		self.path = self.__get_path()
		self.data = self.__get_clean_data(no_repeat = no_repeat)

	def __get_filename(self):
		file = self.file_path.split('/')[-1]
		clean = file.split('.')[0]
		return (file, clean)

	def __get_path(self):
		path = self.file_path.split('/')
		del(path[-1])
		path = '/'.join(path) + '/'
		return path

	def __get_clean_data(self, no_repeat = False):
		"""
		Reads the file containing the data to be plotted, process it, and stores it in
			lists
		__param__ no_repeat:bool ereases repeated data on a file
		__return__ :(x, y, y1, ... , y_n)
		"""
		with open(self.file_path, 'r') as file:
			data = file.read().strip()
		data = data.split('\n')

		if no_repeat: 
			temp = []
			for d in data:
				if d not in temp:
					temp.append(d)
			data = temp
		
		x = []
		y = [[], [], [], [], [], [], [], [], [], []]
		
		for i in range(len(data)):
			line = data[i].split('\t')

			if i==0:
				try:
					line = E.convert_array_to_float(line)
				except:
					print(f'Careful! First line omitted on {self.file_name}')
					continue

			else:
				line = E.convert_array_to_float(line)
			
			for i, value in enumerate(line):
				if i == 0:
					x.append(value)
				else:
					y[i-1].append(value)
			
		return (x, y)