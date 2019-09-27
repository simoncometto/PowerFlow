
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
        n, mat_admitancia, load, generation, voltage_phase, swing_bus = cdf.read(filename)

        self.n = n
        self.Y = sparse.coo_matrix(mat_admitancia)
        self.swing_bus = swing_bus

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
        ''' Computa la potencia P y Q para un valor de tensión y ángulo dado
        :parameter x un vactor de 2*(n-1) donde n es la cantidad de nodos del sistema
        :returns PQ: una vector de 2(n-1), '''
        self.last_P_Q = P_Q(self.Y, x)
        return self.P_Q_inj - self.last_P_Q

    def solve_newton(self, initial_voltage=1, initial_angle=0):
        theta = initial_angle * np.ones(self.n-1)
        v = initial_voltage * np.ones(self.n-1)

        x = np.append(theta, v)
        #delta_x = convergencia + 1

        #while(delta_x < convergencia):
        for i in range(1):
            f = self.f(x)
            J = self.J(x)

            self.disp_matrix(J)
            self.disp_matrix(self.Y)

            print(np.shape(f))
            print(J.get_shape())
            a = sparse_alg.spsolve(J,-f)
            xn = a - x
            #delta_x = sp.linalg.norm(xn-x)
            x = xn

        return x

    def disp_matrix(self, mat):
        import matplotlib.pyplot as plt
        if sparse.issparse(mat):
            mat = mat.todense()

        mat_plot = mat != 0
        plt.matshow(mat_plot)
        plt.show()




if __name__ == '__main__':
    ieee14bus = powerflow('IEEE14cdf.txt')

    start = time()
    x = ieee14bus.solve_newton()
    end = time()
    print(x)
    print('Tiempo: ', end-start, 's')
