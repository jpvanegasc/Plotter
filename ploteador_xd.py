from Plotter import Plotter
import os

path = '/home/juan/Documentos/UN/7_S/Termo_Ex/04_9/datos_termistor.txt'

p = Plotter(path)

p.log_y = True
p.x = ('T', r'C^o')
p.y = ('U', r'V')
p.scatter(reg=1)

