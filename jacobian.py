import numpy as np
from scipy import sparse
from math import sin, cos


def jacobian(mat_admitancia, v_and_theta, swing_bus):
    '''

    :return: J Jacobiano de P y Q es una matriz de 2(n-1) x 2(n-1)'''

    n, n = mat_admitancia.get_shape()
    J = sparse.coo_matrix([2*(n-1),2*(n-1)])

    #Se obtiene cada posicioón del Jacobiano iterando sobre el jacobiano
    # cuando se itera sobre elementos del swing_bus se pasa por alto.

    already_pass_swing_bus = False

    for i, j, Y in zip(mat_admitancia.row, mat_admitancia.col, mat_admitancia.data):
        #Saltear el swing_bus
        if (i == swing_bus || j == swing_bus):
            already_pass_swing_bus = True
            continue

        i_J = i
        j_J = j

        if already_pass_swing_bus:
            i_J = i - 1
            j_J = j - 1

        #Elementos que no son de la diagonal
        # ---------------------------------------------------------------------------------------------
        if(i!=j):
            v_i = v_and_theta[i, 0]
            v_j = v_and_theta[j, 0]
            theta_i = v_and_theta[n, 1]
            theta_j = v_and_theta[n, 1]
            delta_theta = theta_i - theta_j
            G_ij = mat_admitancia[i, j].real
            B_ij = mat_admitancia[i, j].imag

            cos_theta = cos(delta_theta)
            sin_theta = sin(delta_theta)

            a = v_i * v_j
            b = a * G_ij
            c = a * B_ij
            # dP/dtheta
            J[i_J, j_J] = b * sin_theta - c * cos_theta
            # dQ/dtheta
            J[(n - 1) + i_J, j_J] = -b * cos_theta + c * sin_theta

            d = v_i * G_ij
            e = v_i * B_ij
            # dP/dV
            J[i_J, (n - 1) + j_J] = d * cos(delta_theta) + e * sin(delta_theta)
            # dQ/dV
            J[(n - 1) + i_J, (n - 1) + j_J] = d * sin(delta_theta) - e * cos(delta_theta)

        # Elementos de la diagonal
        # ---------------------------------------------------------------------------------------------
        else:
            v_i = v_and_theta[i, 0]
            G_ii = mat_admitancia[i, i].real
            B_ii = mat_admitancia[i, i].imag

            P_i = P_Q[i_J]
            Q_i = P_Q[(n - 1) + i_J]
            # dP/dtheta
            J[i_J, j_J] = - Q_i - B_ii * (v_i ** 2)
            # dP/dV
            J[i_J, (n - 1) + j_J] = P_i / v_i + G_ii * v_i
            # dQ/dtheta
            J[(n - 1 + i_J, j_J] = P_i - G_ii * (v_i ** 2)
            # dQ/dV
            J[(n - 1) + i_J, (n - 1) + j_J] = Q_i / v_i - B_ii * v_i



if __name__ == '__main__':
    import IEEE_cdf as cdf
    n, mat, load, generation, voltage_phase = cdf.read("ieee14cdf.txt")
    # Vector de 2 veces la cantidad de nodos. Una vez para la tension y otra para la fase
    v_and_theta = np.ones((2 * n), dtype=np.float64)

    J = jacobian(mat, v_and_theta)

    print(J)