"""
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from numpy import polyfit, poly1d
from scipy.stats import linregress

class PolynomialFit:
    """
    """
    r, r2 = 0., 0.
    polynomial = None

    def __init__(self, x_list, y_list, deg, low=0, up=None, var="x"):
        self.x = x_list[low:up]
        self.y = y_list[low:up]
        self.degree = deg
        self.var_str = var

        self.coef = polyfit(self.x, self.y, self.degree)
        self.polynomial = poly1d(self.coef)

        self.r = linregress(self.x, self.y)[2]
        self.r2 = self.r**2

    def __str__(self):
        deg = self.degree
        string = '$'

        for c in self.coef:
            if deg > 0:
                string += "%.2f" % round(c, 2)
                string += f" {self.var_str}^" + "{" + str(deg) + "}"
                deg -= 1
            else:
                string += "%.2f" % round(c, 2)

        string += "$\n$r² = %.4f$" % round(self.r2, 4)

        return string 
