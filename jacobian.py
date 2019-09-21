import numpy as np
import IEEE_cdf as cdf
from math import sin, cos

n, mat_admitancia, load, generation, voltage_phase  = cdf.read("ieee14cdf.txt")
#Vector de 2 veces la cantidad de nodos. Una vez para la tension y otra para la fase
v_and_theta = np.ones((2*n), dtype=np.float64)

#Jacobiano de P y Q es una matriz de 2n x 2n
J = np.zeros([2*n,2*n], dtype=np.float64)

#Obtengo cada posicioón del Jacobiano
#dP/dtheta
for i in range(0,n):
    for j in range(0,n):
        #Computo de elementos que no son de la diagonal
        if(i!=j):
            v_i = v_and_theta[i]
            v_j = v_and_theta[j]
            theta_i = v_and_theta[n + i]
            theta_j = v_and_theta[n + j]
            delta_theta = theta_i - theta_j
            G_ij = mat_admitancia[i,j].real
            B_ij = mat_admitancia[i,j].imag

            cos_theta = cos(delta_theta)
            sin_theta = sin(delta_theta)

            a = v_i * v_j
            b = a * G_ij
            c = a * B_ij
            # dP/dtheta
            J[i, j] = b * sin_theta - c * cos_theta
            # dQ/dtheta
            J[n + i, j] = -b * cos_theta + c * sin_theta


            d = v_i * G_ij
            e = v_i * B_ij
            #dP/dV
            J[i,n+j] =  d * cos(delta_theta) + e * sin(delta_theta)
            #dQ/dV
            J[n+i, n+j] = d * sin(delta_theta) - e * cos(delta_theta)

        #Computo de elementos de la diagonal
        else:
            v_i = v_and_theta[i]
            theta_i = v_and_theta[n + i]
            G_ii = mat_admitancia[i,i].real
            B_ii = mat_admitancia[i,i].imag

            P_i = 0
            Q_i = 0
            # dP/dtheta
            J[i, j] = - Q_i - B_ii * (v_i**2)
            # dP/dV
            J[i, n + j] = P_i / v_i + G_ii * v_i
            # dQ/dtheta
            J[n + i, j] = P_i - G_ii * (v_i**2)
            # dQ/dV
            J[n + i, n + j] = Q_i / v_i - B_ii * v_i

print(J)