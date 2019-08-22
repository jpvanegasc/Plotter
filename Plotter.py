#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math as m
import pylab as pl
import numpy as np

class Editor:
	"""
	Defines methods for data manipulation
	"""
	def convert_array_to_float(self, array:list):
		"""
		Converts elements from a list to float
		__param__ array:list list to convert
		__author__ : Juan Vanegas
		"""
		array_in_float = []
		
		for element in array:
			array_in_float.append(float(element.replace(',','.')))

		return array_in_float
	
	def convert_array_to_int(self, array:list):
		"""
		Convierte los elementos de una lista en int
		__param__ array:list lista a convertir
		__autor__ : Juan Vanegas
		"""
		array_in_int = []
		
		for element in array:
			array_in_int.append(int(element))

		return array_in_int

	def convert_array_to_log(self, array:list, base=10.0, base_e=False):
		"""
		Converts a list of numbers into a list of the logarithm of the numbers
		__param__ array:list list to convert
		__param__ base:float log base. By default 10
		__param__ base_e:bool defines if log base is e. Overrides base. By default False
		__author__ Juan Vanegas
		"""
		array_in_log = []
		
		for element in array:
			
			if type(element)!= float:
				raise Exception(
					"The elements in the array you are trying to convert aren't floats")
			else:
				if base_e:
					array_in_log.append(m.log(element))
				else:
					array_in_log.append(m.log(element, base))

		return array_in_log

	def convert_array_to_radians(self, array:list):
		"""
		Converts a list of numbers into a list of the numbers in radians
		__param__ array:list list to convert
		__author__ : Juan Vanegas
		"""
		array_in_rad = []
		
		for element in array:
			if type(element) != float:
				raise Exception(
					'The elements in the array you are trying to convert must be floats')
			else:
				array_in_rad.append(element*(m.pi/180))

		return array_in_rad

	def convert_array_to_degrees(self, array:list):
		"""
		Converts a list of numbers into a list of the numbers in degrees
		__param__ array:list list to convert
		__author__ : Juan Vanegas
		"""
		array_in_deg = []

		for element in array:
			if type(element) != float:
				raise Exception(
					'The elements in the array you are trying to convert must be floats')
			else:
				array_in_deg.append(element*(180/m.pi))

		return array_in_deg

#-----------------------------------------------------------------------------------------

class Plotter(Editor):
	"""
	Defines methods for graphing files using the pyplot lib
	"""
	def __init__(self, file_path, no_repeat = False):
		self.file_path = file_path
		self.file_name, self.clean_name = self.__get_filename()
		self.path = self.__get_path()
		self.data = self.__get_clean_data(no_repeat = no_repeat)
		self._x = {'variable':'', 'unit':''}
		self._y = {'variable':'', 'unit':''}
		self._log_x, self._log_y = False, False
		self._multiple_graphs = False
		self.take_dir = False

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
	def multiple_graphs(self):
		return self._multiple_graphs
	
	@x.setter
	def x(self, x_value):
		try:
			x_variable, x_unit = x_value
		except ValueError:
			raise ValueError(
				"Please pass an iterable with two items: x_variable, x_unit")
		else:
			self._x = {'variable':x_variable, 'unit':x_unit}

	@y.setter
	def y(self, y_value):
		try:
			y_variable, y_unit = y_value
		except ValueError:
			raise ValueError(
				"Please pass an iterable with two items: y_variable, y_unit")
		else:
			self._y = {'variable':y_variable, 'unit':y_unit}
	
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

	@multiple_graphs.setter
	def multiple_graphs(self, multi:bool):
		if type(multi) != bool:
			raise ValueError('Please pass a boolean value for multiple_graphs')

		self._multiple_graphs = bool(multi)

	# Paths
	def __get_filename(self):
		file = self.file_path.split('/')[-1]
		clean = file.split('.')[0]
		return (file, clean)

	def __get_path(self):
		path = self.file_path.split('/')
		del(path[-1])
		path = '/'.join(path) + '/'
		return path

	# Data
	def __get_clean_data(self, no_repeat:bool = False):
		"""
		Comment coming soon in a theater near you
		__param__ no_repeat:bool esto es lo que debería hacer para que limpie datos repetidos
		"""
		with open(self.file_path, 'r') as file:
			data = file.read().strip()
		data = data.split('\n')
		
		x, x1, x2, x3, x4, x5, x6, x7, x8, x9 = [], [], [], [], [], [], [], [], [], []
		y, y1, y2, y3, y4, y5, y6, y7, y8, y9 = [], [], [], [], [], [], [], [], [], []
		
		for i in range(len(data)):
			i_v = data[i].split('\t')

			if i==0:
				try:
					i_v = self.convert_array_to_float(i_v)
				except:
					print(f'Careful! First line omitted on {self.file_name}')
					continue

			else:
				i_v = self.convert_array_to_float(i_v)
			
			if len(i_v) != 1:
				x.append(i_v[0])
				y.append(i_v[1])
			
			elif len(i_v) == 1:
				x.append(i_v[0])

		if len(y) != 0:
			return (x,y)
			
		elif len(y) == 0:
			return (x, 0)
		

	# Titles
	def get_title_labels(self):
		""" 
		Generates title and axes names in LaTex format
		__author__ : Juan Vanegas
		"""
		titulo_grafica, label_x, label_y, = r'', r'', r''

		if not self.log_x and not self.log_y:
			
			titulo_grafica = r'${0}\left({1}\right)\;contra\;{2}\left({3}\right)$'.format(
				self.y['variable'], self.y['unit'], self.x['variable'], self.x['unit'])
			label_x = r'${0}\left({1}\right)$'.format(self.x['variable'], self.x['unit'])
			label_y = r'${0}\left({1}\right)$'.format(self.y['variable'], self.y['unit'])

			return titulo_grafica, label_x, label_y

		elif self.log_x and not self.log_y:
			
			titulo_grafica = r'${0}\left({1}\right)\;contra\;log\left({2}\right)$'.format(
				self.y['variable'], self.y['unit'], self.x['variable'])
			label_x = r'$log\left({0}\right)$'.format(self.x['variable'])
			label_y = r'${0}\left({1}\right)$'.format(self.y['variable'], self.y['unit'])

			return titulo_grafica, label_x, label_y

		elif self.log_y and not self.log_x:
			
			titulo_grafica = r'$log\left({0}\right)\;contra\;{1}\left({2}\right)$'.format(
				self.y['variable'], self.x['variable'], self.x['unit'])
			label_x = r'${0}\left({1}\right)$'.format(self.x['variable'], self.x['unit'])
			label_y = r'$log\left({0}\right)$'.format(self.y['variable'])

			return titulo_grafica, label_x, label_y

		elif self.log_x and self.log_y:
			
			titulo_grafica = r'$log\left({0}\right)\;contra\;log\left({1}\right)$'.format(
				self.y['variable'], self.x['variable'])
			label_x = r'$log\left({0}\right)$'.format(self.x['variable'])
			label_y = r'$log\left({0}\right)$'.format(self.y['variable'])

			return titulo_grafica, label_x, label_y

	# Graphing
	def scatter(self, default_title:bool = True, regression:bool = False, no_title:bool = False):
		"""
		"""
		if default_title:
			title, label_x, label_y = self.get_title_labels()
		else:
			label_x, label_y = self.get_title_labels()[1], self.get_title_labels()[2]
			title = input('¿Qué título desea para la gráfica?\n')
		
		if self.data[1] == 0:
			raise Exception('The file you are trying to plot contains only one column')

		x_values, y_values = self.data
			
		# Log graphs
		if self.log_x: x_values = self.convert_array_to_log(x_values)
		if self.log_y: y_values = self.convert_array_to_log(y_values)

		pl.scatter(x_values, y_values, color='darkblue', s=5)
		
		if regression:
			a = np.polyfit(x_values, y_values, 1)
			b = np.poly1d(a)
			pl.plot(x_values,b(y_values),color='darkblue', label=str(b))
		
		# Title and labels
		if not no_title: pl.title(title)
		pl.xlabel(label_x)
		pl.ylabel(label_y)
		if not self.multiple_graphs: pl.savefig(self.path + self.clean_name +'.png')
		if not self.multiple_graphs: pl.close()

	def lines(self, default_title:bool = True, regression:bool = False, no_title:bool = False):
		"""
		"""
		if default_title:
			title, label_x, label_y = self.get_title_labels()
		else:
			label_x, label_y = self.get_title_labels()[1], self.get_title_labels()[2]
			title = input('Please write the title you wish for the graph:\n')

		if self.data[1] == 0:
			raise Exception('The file you are trying to plot contains only one column')

		x_values, y_values = self.data
			
		# Log graphs
		if self.log_x: x_values = self.convert_array_to_log(x_values)
		if self.log_y: y_values = self.convert_array_to_log(y_values)

		pl.plot(x_values, y_values, color='darkblue', linewidth=1)
		color_list = ['darkblue', 'darkgreen', 'darkred', ]
		
		if regression:
			a=np.polyfit(x_values, y_values, 1)
			b=np.poly1d(a)
			pl.plot(x_values,b(y_values),color='darkblue', label=str(b))
		
		# Title and labels
		if not no_title: pl.title(title)
		pl.xlabel(label_x)
		pl.ylabel(label_y)
		if not self.multiple_graphs: pl.savefig(self.path + self.clean_name +'.png')
		if not self.multiple_graphs: pl.close()

	def histogram(self, default_title:bool = True, no_title:bool = False):
		"""
		"""
		if default_title:
			title, label_x, label_y = self.get_title_labels()
		else:
			label_x, label_y = self.get_title_labels()[1], self.get_title_labels()[2] 
			title = input('Please write the title you wish for the graph:\n')

		if self.data[1] != 0:
			raise Exception('The file you are trying to plot contains more than one column')

		x_values = self.data[0]
			
		# Log graphs
		if self.log_x: x_values = self.convert_array_to_log(x_values)

		pl.hist(x_values, color='darkblue', linewidth=1)
		color_list = ['darkblue', 'darkgreen', 'darkred', ]

		# Title and labels
		if not no_title: pl.title(title)
		pl.xlabel(label_x)
		pl.ylabel(label_y)
		pl.savefig(self.path + self.clean_name +'.png')
		pl.close()

	def frequency(self, scatter=True, default_title:bool = True, no_title:bool = False):
		"""
		if you got a better name for this method, please do change it
		"""
		if default_title:
			title, label_x, label_y = self.get_title_labels()
		else:
			label_x, label_y = self.get_title_labels()[1], self.get_title_labels()[2] 
			title = input('Please write the title you wish for the graph:\n')

		if self.data[1] != 0:
			raise Exception('The file you are trying to plot contains more than one column')

		sorted_data = sorted(self.data[0])
		x_values, freq = [], []

		for dat in sorted_data:
			if dat not in x_values:
				x_values.append(float(dat))
				freq.append(1.0)
			else:
				freq[-1] += 1.0

		if self.log_x: x_values = self.convert_array_to_log(x_values)
		if self.log_y: freq = self.convert_array_to_log(freq)

		if scatter:
			pl.scatter(x_values, freq, color='darkblue', s=5)
		else:
			pl.plot(x_values, freq, color='darkblue', linewidth=1)
		
		if not no_title: pl.title(title)
		pl.xlabel(label_x)
		pl.ylabel(label_y)
		if not self.multiple_graphs: pl.savefig(self.path + self.clean_name +'.png')
		if not self.multiple_graphs: pl.close()		