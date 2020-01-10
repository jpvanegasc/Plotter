#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math as m

import numpy as np

def convert_array_to_float(array:list):
	"""
	Converts elements from a list to float
	__param__ array:list list to convert
	__author__ : Juan Vanegas
	"""
	array_in_float = []
	
	for element in array:
		array_in_float.append(float(element.replace(',','.')))

	return array_in_float

def convert_array_to_int(array:list):
	"""
	Convierte los elementos de una lista en int
	__param__ array:list lista a convertir
	__autor__ : Juan Vanegas
	"""
	array_in_int = []
	
	for element in array:
		array_in_int.append(int(element))

	return array_in_int

def convert_array_to_log(array:list, base=10.0, base_e=False):
	"""
	Converts a list of numbers into a list of the logarithm of the numbers
	__param__ array:list list to convert
	__param__ base:float log base. By default 10
	__param__ base_e:bool defines if log base is e. Overrides base. By default False
	__author__ Juan Vanegas
	"""
	array_in_log = []
	
	for element in array:
		if base_e:
			array_in_log.append(m.log(element))
		else:
			array_in_log.append(m.log(element, base))

	return np.array(array_in_log, dtype = np.double, order = 'C')

def convert_array_to_radians(array:list):
	"""
	Converts a list of numbers into a list of the numbers in radians
	__param__ array:list list to convert
	__author__ : Juan Vanegas
	"""
	array_in_rad = []
	
	for element in array:
		array_in_rad.append(element*(m.pi/180))

	return np.array(array_in_rad, dtype = np.double, order = 'C')

def convert_array_to_degrees(array:list):
	"""
	Converts a list of numbers into a list of the numbers in degrees
	__param__ array:list list to convert
	__author__ : Juan Vanegas
	"""
	array_in_deg = []

	for element in array:
		array_in_deg.append(element*(180/m.pi))

	return np.array(array_in_deg, dtype = np.double, order = 'C')