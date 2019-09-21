from Plotter import Plotter
import os

path = '/home/juan/Documentos/UN/7_S/Termo_Ex/04_9/datos_termopar_2.txt'

p = Plotter(path)

#p.log_y = True
p.y = ('N', r'a.u.')
p.x = ('R', r'\Omega')
p.scatter(reg=1)