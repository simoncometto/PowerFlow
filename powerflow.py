# coding=utf-8
import numpy as np
import scipy as sp
import scipy.sparse as sparse
import scipy.sparse.linalg as sparse_alg
from time import time
import IEEE_cdf as cdf
from jacobian import jacobian
from P_Q import P_Q

class powerflow:
    '''

    '''
    def __init__(self, filename=''):
        n, mat_admitancia, load, generation, voltage_phase, swing_bus, PV_buses = cdf.read(filename)

        self.n = n
        self.Y = sparse.coo_matrix(mat_admitancia)
        self.swing_bus = swing_bus
        self.PV_buses = PV_buses

        delta_PQ = generation-load
        self.P = delta_PQ.real
        self.Q = delta_PQ.imag

        self.P_Q_inj = delta_PQ[1:].real
        self.P_Q_inj = np.append(self.P_Q_inj, delta_PQ[1:].imag)

    def J(self, x):
        '''Computa el jacobiano para un valor de tensión y ángulo dado
        :parameter x: un vactor de 2*(n-1) donde n es la cantidad de nodos del sistema
        :returns jacobiano: una matriz de 2(n-1) x 2(n-1)
        '''
        return jacobian(self.Y, x, self.swing_bus, self.last_P_Q)

    def f(self, x):
        ''' Computa deltaP y deltaQ para un valor de tensión y ángulo dado
        :parameter x un vactor de 2*(n-1) donde n es la cantidad de nodos del sistema
        :returns delta_PQ: una vector de 2(n-1)'''
        self.last_P_Q = P_Q(self.Y, x)
        return (self.P_Q_inj - self.last_P_Q)

    def solve_newton(self, initial_voltage=1, initial_angle=0):
        theta = initial_angle * np.ones(self.n-1)
        v = initial_voltage * np.ones(self.n-1)

        x = np.append(theta, v)

        #while(delta_x < convergencia):
        for i in range(1):
            func = self.f(x)
            #self.disp_matrix(np.vstack([func, func]))

            jaco = self.J(x)
            J_to_disp = jaco.todense()
            #self.disp_matrix(J_to_disp[:self.n-1,:self.n-1])

            #Jacobiano reducido
            rJ = jaco.todense()
            #Las filas a eliminar son aquellas que corresponden a la dQ/dtheta de un PV bus
            filas_a_eliminar = self.PV_buses- 1 + self.n-1
            #Las columas a eliminar son aquellas que corresponden a la dP/dV de un PV bus
            columnas_a_eliminar = filas_a_eliminar
            rJ = np.delete(rJ, filas_a_eliminar, 0)
            rJ = np.delete(rJ, columnas_a_eliminar, 1)

            #self.disp_matrix(rJ)
            #a = sparse_alg.spsolve(jaco,-func)
            func_reducido = np.delete(func, columnas_a_eliminar)
            a = np.linalg.solve(rJ, -func_reducido)
            xn = a - x
            x = xn

        return x

    def disp_matrix(self, mat):
        import matplotlib.pyplot as plt
        if sparse.issparse(mat):
            mat = mat.todense()

        mat_plot = mat != 0.0
        plt.matshow(mat_plot)
        plt.show()


#---------------------------------------------------------------------------------------------

if __name__ == '__main__':
    ieee14bus = powerflow('IEEE14cdf.txt')

    start = time()
    x = ieee14bus.solve_newton()
    end = time()
    #print(x)
    print('Tiempo: ', end-start, 's')
