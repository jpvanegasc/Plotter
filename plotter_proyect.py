import math as m

def convert_array_to_float(array:list):
	"""
	Convierte los elementos de una lista en float
	__param__ array:list lista a convertir
	__autor__ : Juan Vanegas
	"""
	array_in_float = []
	
	for element in array:
		#if ',' in element:
		#	array_in_float.append(float(element.replace(',','.')))
		#else:
		array_in_float.append(float(element))

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
	Convierte una lista de números en una lista del logaritmo de los números
	__param__ array:list lista de números a cambiar
	__param__ base:float base del logaritmo. Por default es 10.
	__param__ base_e:bool define si la base a usar es e. Por default no se usa
	__autor__ Juan Vanegas
	"""
	array_in_log = []
	
	for element in array:
		
		#if type(element)!= float:
		#	raise Exception('The elements in the array you are trying to convert must be floats')
		#else:
		if base_e:
			array_in_log.append(m.log(element))
		else:
			array_in_log.append(m.log(element, base))

	return array_in_log


def generar_titulo_labels(variable_x:str, unit_x:str, variable_y:str, unit_y:str, log_x=False, log_y=False, dimensionless=False):
	""" 
	Genera el título y los nombres de los ejes en formato LaTex
	__param__ variable_x:str nombre del eje x
	__param__ unit_x:str unidades del eje x
	__param__ variable_y:str nombre del eje y
	__param__ unit_y:str unidades del eje y
	__param__ log_x:bool define si es una gráfica con el eje x como log(x)
	__param__ log_y:bool define si es una gráfica con el eje y como log(y)
	__autor__ : Juan Vanegas
	"""
	titulo_grafica, label_x, label_y, = r'', r'', r''
	
	if type(variable_x)!=str or type(variable_y)!=str:
		raise Exception('The names of the variables must be strings')

	if not log_x and not log_y:
		
		titulo_grafica = r'${0}\left({1}\right)\;contra\;{2}\left({3}\right)$'.format(variable_y, unit_y, 
			variable_x, unit_x)
		label_x = r'${0}\left({1}\right)$'.format(variable_x, unit_x)
		label_y = r'${0}\left({1}\right)$'.format(variable_y, unit_y)

		return titulo_grafica, label_x, label_y

	elif log_x and not log_y:
		
		titulo_grafica = r'$log\left({0}\right)\;contra\;{1}$'.format(variable_y,variable_x)
		label_x = r'$log\left({0}\right)$'.format(variable_x)
		label_y = r'${0}$'.format(variable_y)

		return titulo_grafica, label_x, label_y

	elif log_x and log_y:
		
		titulo_grafica = r'$log\left({0}\right)\;contra\;log\left({1}\right)$'.format(variable_y,variable_x)
		label_x = r'$log\left({0}\right)$'.format(variable_x)
		label_y = r'$log\left({0}\right)$'.format(variable_y)

		return titulo_grafica, label_x, label_y

def convert_array_to_radians(array:list):
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


def convert_array_to_degrees(array:list):
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


def latex_table(array_1:list, array_2:list):
	pass
