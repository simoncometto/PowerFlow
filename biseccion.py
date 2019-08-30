# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:36:39 2019

@author: Simón Cometto
"""

import numpy as np

f = lambda x: (x+2)**3-1    #np.cos(x)


a = float(input("Ingrese a: "))
b = float(input("Ingrese b: "))
tolerancia = float(input("Ingrese la tolerancia: ")) 

print(f(a))
print(f(b))


if (f(a)*f(b))<0: #Hay un cero en el medio
    print("Comienzo el algoritmo")
    
    #Mientras el intérvalo es mayor a la tolerancia
    while(abs(a-b)>tolerancia):
        #Encuentro el punto medio entre a y b
        c =  a + (abs(b-a)*0.5)
        print(a," | ",c, " | ",b)
        #Si f(a) y f(c) tienen signo distinto, entonces hubo un cruce por cero entre a y b
        if(f(a)*f(c)<0):
            b = c
        #Sino el cero se encuentra entre b y c
        else:
            a = c
    print("El cero se encuentra en :", c)        
    
else:             #No se sabe si hay cero en el medio
    print("Inicie el algoritmo de nuevo con otro valor de a y b")