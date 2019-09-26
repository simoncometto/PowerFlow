
import numpy as np
import scipy as sp
import scipy.sparse as sparse
from time import time
import IEEE_cdf as cdf
from jacobian import jacobian
from P_Q import P_Q

class powerflow:
    '''

    '''
    def __init__(self, filename=''):
        n, mat_admitancia, load, generation, voltage_phase, swing_bus = cdf.read(filename)

        self.Y = sparse.coo_matrix(mat_admitancia)

    def J(self, x):
        '''Computa el jacobiano para un valor de tensión y ángulo dado
        :parameter x: un vactor de 2*(n-1) donde n es la cantidad de nodos del sistema
        :returns jacobiano: una matriz de 2(n-1) x 2(n-1)
        '''
        jacobian = 1
        return jacobian

    def f(self, x):
        ''' Computa la potencia P y Q para un valor de tensión y ángulo dado
        :parameter x un vactor de 2*(n-1) donde n es la cantidad de nodos del sistema
        :returns PQ: una vector de 2(n-1), '''
        PQ = 6
        return PQ

    def solve_newton(self, convergencia, initial_voltage=np.ones(self.n - 1), initial_angle=np.zeros(self.n - 1)):

        x = np.append(initial_voltage, initial_angle)
        delta_x = convergencia + 1

        while(delta_x < convergencia):
            a = sparse.linalg.spsolve(J(x),-f(x))
            xn = a - x
            delta_x = sp.linalg.norm(xn-x)
            x = xn



if __name__ == '__main__':
    ieee14bus = powerflow('IEEE14cdf.txt')

    start = time()
    x = ieee14bus.solve_newton()
    end = time()
    print(x)
    print('Tiempo: ', end-start, 's')

    ieee14bus.f()
