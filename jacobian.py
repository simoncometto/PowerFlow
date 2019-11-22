# coding=utf-8
import numpy as np
from scipy import sparse
from math import sin, cos


def jacobian(mat_admitancia, theta_v, swing_bus, last_P_Q):
    '''
    :parameter:
        -> mat_admitancia: matriz de n x n con la admitancia G+jB
        -> v
    :return: J Jacobiano de P y Q es una matriz de 2(n-1) x 2(n-1)'''

    #El jacobiano tine la misma forma que la mat de admitancia entonces se hace una copia
    Jn = mat_admitancia.copy()

    #El jacobiano se lo pasa a formato csr para poder asignarle valores
    if not sparse.isspmatrix_csr(Jn):
        Jn = Jn.tocsr()

    J11 = J12 = J21 = J22 = Jn.astype(np.float64)

    #La matriz de admitancia se la pasa a formato coo para poder iterar sobre los elemtnos
    if not sparse.isspmatrix_coo(mat_admitancia):
        mat_admitancia = mat_admitancia.tocoo()

    #Obtengo la cantidad de nodos
    n, n = mat_admitancia.get_shape()

    # Se obtiene cada posicioón del Jacobiano iterando sobre el jacobiano
    # Cuando se itera sobre elementos del swing_bus se pasa por alto.
    for i, j, Y in zip(mat_admitancia.row, mat_admitancia.col, mat_admitancia.data):
        #Saltear el swing_bus
        if (i == swing_bus or j == swing_bus):
            continue

        i_p = i - 1
        j_p = j - 1
        #Elementos que no son de la diagonal
        # ---------------------------------------------------------------------------------------------
        if(i!=j):
            v_i = theta_v[(n-1) + i_p]
            v_j = theta_v[(n-1) + j_p]
            theta_i = theta_v[i_p]
            theta_j = theta_v[j_p]
            delta_theta = theta_i - theta_j
            G_ij = Y.real
            B_ij = Y.imag

            cos_theta = cos(delta_theta)
            sin_theta = sin(delta_theta)

            a = v_i * v_j
            b = a * G_ij
            c = a * B_ij
            # dP/dtheta
            J11[i, j] = b * sin_theta - c * cos_theta

            # dQ/dtheta
            J21[i, j] = -b * cos_theta + c * sin_theta

            d = v_i * G_ij
            e = v_i * B_ij
            # dP/dV
            J12[i, j] = d * cos(delta_theta) + e * sin(delta_theta)
            # dQ/dV
            J22[i, j] = d * sin(delta_theta) - e * cos(delta_theta)

        # Elementos de la diagonal
        # ---------------------------------------------------------------------------------------------
        else:
            v_i = theta_v[(n-1) + i_p]
            G_ii = Y.real
            B_ii = Y.imag

            P_i = last_P_Q[i_p]
            Q_i = last_P_Q[(n-1) + i_p]
            # dP/dtheta
            J11[i, j] = - Q_i - B_ii * (v_i ** 2)
            # dP/dV
            J21[i, j] = P_i / v_i + G_ii * v_i
            # dQ/dtheta
            J21[i, j] = P_i - G_ii * (v_i ** 2)
            # dQ/dV
            J22[i, j] = Q_i / v_i - B_ii * v_i

        # --------------------------------------------------------------------------------
        np.savetxt('jacobiano.txt', J11.todense(), fmt='%+7.2f', delimiter='   ')

        J1 = sparse.hstack([J11[1:,1:],J12[1:,1:]])
        J2 = sparse.hstack([J21[1:,1:],J22[1:,1:]])
        J = sparse.vstack([J1,J2])

        return J


if __name__ == '__main__':
    '''
    import IEEE_cdf as cdf
    n, mat, load, generation, voltage_phase, swing_bus = cdf.read("ieee14cdf.txt")
    # Vector de 2 veces la cantidad de nodos. Una vez para la tension y otra para la fase
    v_and_theta = np.ones((2 * n), dtype=np.float64)

    J = jacobian(mat, theta_v)

    print(J)'''