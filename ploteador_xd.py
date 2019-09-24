from Graphing import Plotter
import os

#path = '/home/juan/Documentos/UN/7_S/Termo_Ex/04_9/diodo.txt'
path = './Example_Files/quadratic.txt'
p = Plotter(path)

#p.y = ('U_L', r'V')

#p.x = ('I_L', r'mA')
#p.y = ('U', r'V')

p.scatter(reg=2)
