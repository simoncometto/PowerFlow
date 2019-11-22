# coding=utf-8
import numpy as np
from numpy import deg2rad, rad2deg
from math import cos, sin
from scipy import sparse

def P_Q(mat_admitancia, theta_v, swing_bus=0):
    ''' Función para calcular P y Q en el sistema a partir de V y theta del sistema
    :parameter
        -> mat_admitancia: Matriz de n x n compleja G+jB en formato sparse
        -> theta_v: Vector de 2*(n-1) Los primero n-1 elementos tienen angulo, y los siguiente n-1 elementos tienen volts. EXCLUYE EL SWING_BUS!!!
                    theta está en RADIANTES
        -> swing_bus: escalar que indica el bus de referencia. La potencia para este bus no se calcula, y no forma parte del resultado
    :return:
        -> P_Q un vector de 2*(n-1) donde las primeras n-1 entradas son P y las siguiete Q, calculadas a partir de theta_v y del sistema
    '''

    #Si la matriz no está en formato coo se transforma a coo
    #Sólo válido para pasar de un formato sparse a otro... no para pasar de dense a sparse
    if not sparse.isspmatrix_coo(mat_admitancia):
        mat_admitancia = mat_admitancia.tocoo()

    #Se obtiene el número de nodos a parir de las dimensiones de la mat_admitancia
    n, n = mat_admitancia.get_shape()

    #Vector nulo para almacenar P y Q calculado
    P = np.zeros(n, dtype=np.float64)
    Q = np.zeros(n, dtype=np.float64)

    # Se agrega el ángulo y la tensión del swing bus
    theta = np.concatenate(([0], theta_v[:n-1]))
    v = np.concatenate(([1.06], theta_v[n-1:]))

    for i, j, Y in zip(mat_admitancia.row, mat_admitancia.col, mat_admitancia.data):
        #Saltear el swing_bus
        if (i == swing_bus):
            continue

        B_ij = Y.imag
        G_ij = Y.real

        theta_i = theta[i]
        theta_j = theta[j]
        delta_theta = theta_i - theta_j
        v_i = v[i]
        v_j = v[j]
        a = v_i * v_j * G_ij
        b = v_i * v_j * B_ij

        P[i] += a * cos(delta_theta) + b * sin(delta_theta)
        Q[i] += a * sin(delta_theta) - b * cos(delta_theta)

    # En realidad para lograr que el algoritmo funcione con el swing bus en cualquier lugar se debería modificar los indices y realizar una doble partición
    # Se une la P y Q en un sólo vector, dejando de lado la primer ubicaicón porque es el swing bus.
    P_Q = np.hstack((P[1:], Q[1:]))
    return P_Q * 100


if __name__ == '__main__':
    import IEEE_cdf as cdf
    n, mat, load, generation, voltage_phase, swing_bus, PV_buses = cdf.read('ieee14cdf.txt')


    #v = np.ones(n, dtype=float)
    v = voltage_phase[1:,0]
    phase = voltage_phase[1:,1]
    #phase = np.zeros(n, dtype=float)
    phase = np.deg2rad(phase)
    theta_v = np.concatenate((phase,v))
    mat = sparse.coo_matrix(mat)

    PandQ = P_Q(mat, theta_v)

    P = PandQ[:(n-1)]
    Q = PandQ[(n-1):]

    print("Calculated P")
    print(np.around(P, 1))

    P = generation.real - load.real
    print("P from the file")
    print(P[1:])

    print("Calculated Q")
    print(np.around(Q, 1))

    Q = generation.imag - load.imag
    print("Q from the file")
    print(Q[1:])

