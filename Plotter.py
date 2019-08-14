#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math as m
import pylab as pl
import numpy as np

class Editor:
	"""
	Define métodos para la manipulación de datos
	"""
	def convert_array_to_float(self, array:list):
		"""
		Convierte los elementos de una lista en float
		__param__ array:list lista a convertir
		__autor__ : Juan Vanegas
		"""
		array_in_float = []
		
		for element in array:
			array_in_float.append(float(element.replace(',','.')))

		return array_in_float


	def convert_array_to_log(self, array:list, base=10.0, base_e=False):
		"""
		Convierte una lista de números en una lista del logaritmo de los números
		__param__ array:list lista de números a cambiar
		__param__ base:float base del logaritmo. Por default es 10.
		__param__ base_e:bool define si la base a usar es e. Por default no se usa
		__autor__ Juan Vanegas
		"""
		array_in_log = []
		
		for element in array:
			
			if type(element)!= float:
				raise Exception("The elements in the array you are trying to convert aren't floats")
			else:
				if base_e:
					array_in_log.append(m.log(element))
				else:
					array_in_log.append(m.log(element, base))

		return array_in_log

	def convert_array_to_radians(self, array:list):
		"""
		Convierte una lista de números en una lista de los números en radianes
		__param__ array:list lista de números a convertir
		__autor__ : Juan Vanegas
		"""
		array_in_rad = []
		
		for element in array:
			if type(element) != float:
				raise Exception('The elements in the array you are trying to convert must be floats')
			else:
				array_in_rad.append(element*(m.pi/180))

		return array_in_rad


	def convert_array_to_degrees(self, array:list):
		"""
		Convierte una lista de números en una lista de los números en grados
		__param__ array:list lista de números a convertir
		__autor__ : Juan Vanegas
		"""
		array_in_deg = []

		for element in array:
			if type(element) != float:
				raise Exception('The elements in the array you are trying to convert must be floats')
			else:
				array_in_deg.append(element*(180/m.pi))

		return array_in_deg

#--------------------------------------------------------------------------------------------------

class Plotter(Editor):
	"""
	Define métodos para graficar archivos utilizando la librería pyplot
	"""
	def __init__(self, file_path):
		self._file_path = file_path
		self._file_name, self._clean_name = self.__get_filename()
		self._path = self.__get_path()
		self._data = self.__get_clean_data()
		self.x , self.y = ['', ''], ['', '']
		self.log_x, self.log_y = False, False
		self.take_dir = False

	@property
	def file_path(self):
		return self._file_path
	
	@property
	def file_name(self):
		return self._file_name

	@property
	def clean_name(self):
		return self._clean_name
	
	@property
	def path(self):
		return self._path

	@property
	def data(self):
		return self._data
	
	
	#haz una funcion que elimine datos repetidos en un archivo generico x, y
	#mejor, pasalo como argumento de clean data

	def __get_filename(self):
		file = self.file_path.split('/')[-1]
		clean = file.split('.')[0]
		return (file, clean)

	def __get_path(self):
		path = self.file_path.split('/')
		del(path[-1])
		path = '/'.join(path) + '/'
		return path

	def set_x(self, x_variable, x_unit):
		self.x = []
		self.x.append(x_variable)
		self.x.append(x_unit)
		self.x = tuple(self.x)

	def set_y(self, y_variable, y_unit):
		self.y = []
		self.y.append(y_variable)
		self.y.append(y_unit)
		self.y = tuple(self.y)

	def set_log(self, log_x:bool, log_y:bool):
		self.log_x = log_x
		self.log_y = log_y

	def __get_clean_data(self, no_repeat:bool = False):
		"""
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
			
			x.append(i_v[0])
			y.append(i_v[1])

		return (x,y)

	def get_title_labels(self):
		""" 
		Genera el título y los nombres de los ejes en formato LaTex
		__autor__ : Juan Vanegas
		"""
		titulo_grafica, label_x, label_y, = r'', r'', r''

		if not self.log_x and not self.log_y:
			
			titulo_grafica = r'${0}\left({1}\right)\;contra\;{2}\left({3}\right)$'.format(
				self.y[0], self.y[1], self.x[0], self.x[1])
			label_x = r'${0}\left({1}\right)$'.format(self.x[0], self.x[1])
			label_y = r'${0}\left({1}\right)$'.format(self.y[0], self.y[1])

			return titulo_grafica, label_x, label_y

		elif self.log_x and not self.log_y:
			
			titulo_grafica = r'${0}\left({1}\right)\;contra\;log\left({2}\right)$'.format(
				self.y[0], self.y[1], self.x[0])
			label_x = r'$log\left({0}\right)$'.format(self.x[0])
			label_y = r'${0}\left({1}\right)$'.format(self.y[0], self.y[1])

			return titulo_grafica, label_x, label_y

		elif self.log_y and not self.log_x:
			
			titulo_grafica = r'$log\left({0}\right)\;contra\;{1}\left({2}\right)$'.format(
				self.y[0], self.x[0], self.x[1])
			label_x = r'${0}\left({1}\right)$'.format(self.x[0], self.x[1])
			label_y = r'$log\left({0}\right)$'.format(self.y[0])

			return titulo_grafica, label_x, label_y

		elif self.log_x and self.log_y:
			
			titulo_grafica = r'$log\left({0}\right)\;contra\;log\left({1}\right)$'.format(
				self.y[0], self.x[0])
			label_x = r'$log\left({0}\right)$'.format(self.x[0])
			label_y = r'$log\left({0}\right)$'.format(self.y[0])

			return titulo_grafica, label_x, label_y


	def scatter(self, default_title:bool = True, regression:bool = False, no_title:bool = False):
		"""
		"""
		if default_title:
			title, label_x, label_y = self.get_title_labels()
		else:
			def_tit, label_x, label_y = self.get_title_labels()
			title = input('¿Qué título desea para la gráfica?\n')

		x_values, y_values = self.data
			
		# Log graphs
		if self.log_x: x_values = convert_array_to_log(x_values)
		if self.log_y: y_values = convert_array_to_log(y_values)

		pl.scatter(x_values, y_values, color='darkblue', s=5)
		
		if regression:
			a=np.polyfit(x_values, y_values, 1)
			b=np.poly1d(a)
			pl.plot(x_values,b(y_values),color='darkblue', label=str(b).replace())
		
		# Title and labels
		if not no_title: pl.title(title)
		pl.xlabel(label_x)
		pl.ylabel(label_y)
		pl.savefig(self.path + self.clean_name +'.png')
		pl.close()

	def lines(self, default_title:bool = True, regression:bool = False, no_title:bool = False):
		"""
		"""
		if default_title:
			title, label_x, label_y = self.get_title_labels()
		else:
			def_tit, label_x, label_y = self.get_title_labels()
			title = input('¿Qué título desea para la gráfica?\n')

		x_values, y_values = self.data
			
		# Log graphs
		if self.log_x: x_values = convert_array_to_log(x_values)
		if self.log_y: y_values = convert_array_to_log(y_values)

		pl.plot(x_values, y_values, color='darkblue', linewidth=1)
		color_list = ['darkblue', 'darkgreen', 'darkred', ]
		
		if regression:
			a=np.polyfit(x_values, y_values, 1)
			b=np.poly1d(a)
			pl.plot(x_values,b(y_values),color='darkblue', label=str(b).replace())
		
		# Title and labels
		if not no_title: pl.title(title)
		pl.xlabel(label_x)
		pl.ylabel(label_y)
		pl.savefig(self.path + self.clean_name +'.png')
		pl.close()

	def histogram(self):
		pass

p = Plotter('/home/juan/Documentos/UN/6_S/Moderna/4-07-2019-jpvanegasc/V0-0.txt')
#p = Plotter('./test.txt')