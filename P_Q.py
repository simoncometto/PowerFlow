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
    #theta = np.append([0],theta_v[0:n-1])
    theta = np.concatenate(([0], theta_v[:n-1]))
    v = np.concatenate(([1], theta_v[n-2:]))
    #v = np.append([1], theta_v[n-1:-1])
    print(v)

    for i, j, Y in zip(mat_admitancia.row, mat_admitancia.col, mat_admitancia.data):
        #Saltear el swing_bus

        if (i == swing_bus):
            continue

        B_ij = Y.imag
        G_ij = Y.real

        theta_i = theta[i]
        theta_j = theta_v[j]
        v_j = v[j]
        delta_theta = theta_i - theta_j
        a = v_j * G_ij
        b = v_j * B_ij

        P[i] += a * cos(delta_theta) + b * sin(delta_theta)
        Q[i] += a * sin(delta_theta) - b * cos(delta_theta)

    for i in range(n):
        P = P * v[i]

    # En realidad para lograr que el algoritmo funcione con el swing bus en cualquier lugar se debería modificar los indices y realizar una doble partición
    # Se une la P y Q en un sólo vector, dejando de lado la primer ubicaicón porque es el swing bus.
    P_Q = np.append(P[1:-1], Q[1:-1])

    return P_Q


if __name__ == '__main__':
    import IEEE_cdf as cdf
    n, mat, load, generation, voltage_phase, swing_bus = cdf.read('ieee14cdf.txt')

    v = voltage_phase[1:,0]
    phase = voltage_phase[1:,1]

    phase = np.deg2rad(phase)
    theta_v = np.concatenate((phase,v))
    mat = sparse.coo_matrix(mat)

    print(theta_v)
    PandQ = P_Q(mat, theta_v)

    P = PandQ[0:(n-1)]
    Q = PandQ[(n-1):-1]

    print("Calculated P")
    print(np.around(100*P, 1))

    P = generation.real - load.real
    print("P from the file")
    print(P[1:-1])
    #print(Q)