# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:36:39 2019

@author: Simón Cometto
"""

import numpy as np


def biseccion(f, a, b, tolerancia=False, iteraciones=False):
    ''' Encuentra el cero de f entre a y b mediante el método bisección
        Parámetros: 
            ->  f: una función que, dado x, devuelve el valor de f(x)
            ->  a y b: números reales iniciales para el método
            ->  tolerancia: el menor intérvalo entre el cual se encuentra el cero
            ->  iteraciones: la cantidad de iteraciones a realizar en el algoritmo'''

    #Si a la función no se le pasa un parámetro para detener las iteraciones devuelve False
    if not (tolerancia or iteraciones):
        return False

    if (f(a)*f(b))<0: #Hay un cero en el medio
        #El algoritmo se ejecuta hasta llegar a un intervalo de tolerancia menor o igual a "tolerancia"
        if(tolerancia):
            #Mientras el intérvalo es mayor a la tolerancia
            while(abs(a-b)>tolerancia):
                #Encuentro el punto medio entre a y b
                c =  a + (abs(b-a)*0.5)

                #Si f(a) y f(c) tienen signo distinto, entonces hubo un cruce por cero entre a y b
                if(f(a)*f(c)<0):
                    b = c
                #Sino el cero se encuentra entre b y c
                else:
                    a = c
            return c
        elif iteraciones:
            for i in range(iteraciones):
                c = a + (abs(b - a) * 0.5)

                # Si f(a) y f(c) tienen signo distinto, entonces hubo un cruce por cero entre a y b
                if (f(a) * f(c) < 0):
                    b = c
                # Sino el cero se encuentra entre b y c
                else:
                    a = c
            return c
    else:    #No se sabe si hay cero en el medio
        pass
        #Ver que devolver en caso de que no haya un cero en el medio, o como implementarlo

def punto_fijo(g, x_i, n):
    ''' Encuentra el cero de f a partir de g.
        Parámetros:
            ->  g: surge de despejar x de f
            ->  n: la cantidad de iteraciones'''
    for i in range(n):
        x_i = g(x_i)
    return x_i

if __name__ == "__main__":
    f = lambda x: (x + 2) ** 3 - 1  # np.cos(x)

    a = float(input("Ingrese a: "))
    b = float(input("Ingrese b: "))
    t = float(input("Ingrese la tolerancia: "))
    i = int(input("Ingrese la cantidad de iteraciones: "))

    cero = biseccion(f, a, b, tolerancia=t)
    cero2 = biseccion(f, a, b, iteraciones=i)
    print("Un cero se encuentra en: ", cero)
    print("Luego de: ", i, " iteraciones el cero es: ", cero2)
