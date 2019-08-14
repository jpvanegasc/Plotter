import math as m
import pylab as pl
import numpy as np

def convert_array_to_float(array:list):
	"""
	Convierte los elementos de una lista en float
	__param__ array:list lista a convertir
	__autor__ : Juan Vanegas
	"""
	array_in_float = []
	
	for element in array:
		array_in_float.append(float(element.replace(',','.')))

	return array_in_float


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
		
		if type(element)!= float:
			raise Exception('The elements in the array you are trying to convert must be floats')
		else:
			if base_e:
				array_in_log.append(m.log(element))
			else:
				array_in_log.append(m.log(element, base))

	return array_in_log


def generar_titulo_labels(variable_x:str, unit_x:str, variable_y:str, unit_y:str, log_x=False, log_y=False):
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
		
		titulo_grafica = r'${0}\left({1}\right)\;contra\;log\left({2}\right)$'.format(variable_y,unit_y,variable_x)
		label_x = r'$log\left({0}\right)$'.format(variable_x)
		label_y = r'${0}$'.format(variable_y)

		return titulo_grafica, label_x, label_y

	elif log_y and not log_x:
		
		titulo_grafica = r'$log\left({0}\right)\;contra\;{1}\left({2}\right)$'.format(variable_y,variable_x,unit_x)
		label_x = r'${0}$'.format(variable_x)
		label_y = r'$log\left({0}\right)$'.format(variable_y)

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


def plot_file(path_to_file:str, v_x:str, u_x:str, v_y:str, u_y:str, result_name:str,na,
			scatter=False, regression=False, log_x=False, log_y=False, 
			local_file=False, default_title=True, y_graphs:int = 1):
	"""
	Generar la gráfica usando pylab de un archivo de datos
	
	__param__ path_to_file:str dirección al archivo de datos
	__param__ v_x:str nombre de la variable x
	__param__ u_x:str unidades de la variable x
	__param__ v_y:str nombre de la variable x
	__param__ u_y:str unidades de la variable y
	__param__ result_name:str dirección a la imagen generada
	__param__ scatter:bool define si se grafica con una dispersión de puntos. Default=False
	__param__ regression:bool define si a la dispersión se le añade una línea de tendencia. Default=False
	__param__ log_x:bool define si se debe graficar utilizando el logaritmo de los valores x. Default=False
	__param__ log_y:bool define si se debe graficar utilizando el logaritmo de los valores y. Default=False
	__param__ local_file:bool el archivo a guardar y el archivo a generar están en la misma carpeta que
		el programa que va a graficar. Default=True
	__param__ default_title:bool
	__param__ y_graphs:int define el número de graficas a realizar en una misma imagen. 
		Se toma para todos el mismo conjunto de valores x. Default=1

	__autor__ : Juan Vanegas
	"""
	# Abrir archivo y dividir por líneas
	if local_file: file_path = './' + path_to_file
	else: file_path = path_to_file

	with open(file_path, 'r') as file:
		data=file.read().strip()

	data=data.split('\n')

	# Generar el título y los nombres de los ejes
	if default_title: titulo, label_x, label_y = generar_titulo_labels(v_x, u_x, v_y, u_y, log_x=log_x, log_y=log_y)
	else:
		def_tit, label_x, label_y = generar_titulo_labels(v_x, u_x, v_y, u_y, log_x=log_x, log_y=log_y)
		titulo=input('¿Qué título desea para la gráfica?\n')


	# Generar las listas de los valores x y y a graficar
	x_values, y_values1 = [], []

	for i in range(0,len(data)):
		i_v = data[i].split('\t')
		flag=False
		
		if i==0:
			try:
				i_v = convert_array_to_float(i_v)
				flag = True
			except:
				print('¡Cuidado! Se omitió la primera línea')
				continue
				flag = False
		else:
			i_v = convert_array_to_float(i_v)
			flag = True
		
		if flag:
			x_values.append(i_v[0])
			y_values1.append(i_v[1])

	# Gráficas logarítmicas
	if log_x: x_values = convert_array_to_log(x_values)
	if log_y: y_values1 = convert_array_to_log(y_values1)

	if scatter:
		# Graficar con puntos y una regresión
		pl.scatter(x_values, y_values1, color='darkblue', s=5)
		if regression:
			a=np.polyfit(x_values, y_values1, 1)
			b=np.poly1d(a)
			pl.plot(x_values,b(y_values1),color='darkblue', label=str(b).replace())
	else:
		# Graficar con líneas
		if y_graphs==1: pl.plot(x_values, y_values1, color='darkblue', linewidth=1, label=na)
		else:
			color_list = ['darkblue', 'darkgreen', 'darkred', ]

	# Graficar título, nombres de ejes, ajustar comentarios y guardar
	pl.title(titulo)
	pl.xlabel(label_x)
	pl.ylabel(label_y)
	if y_graphs!= 1: pl.legend(loc='upper right')
	pl.savefig(result_name)
	pl.close()
