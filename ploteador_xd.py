from Plotter import Plotter
import os
"""
#path = '/home/juan/Proyectos/Automatas_Sismicos/Resultados/Raw_Files/L32/'
path = '/home/juan/Proyectos/Automatas_Sismicos/Programas/'
docs = sorted(os.listdir(path))
#print(docs)

for i, doc in enumerate(docs):
	if doc.split('.')[-1] != 'txt':
		continue
	#print(doc)
	p = Plotter(path+doc)
	p.log_x = True
	p.log_y = True
	#if i != len(docs)-1:
	#	p.multiple_graphs = True
	p.frequency(no_title = True, label=doc)



"""
p = Plotter('./Example_Files/termo.txt')
p.scatter(reg=1)
"""
"""
