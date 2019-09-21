import numpy as np
import IEEE_cdf as cdf
from math import cos, sin

P_Q = np.zeros(2*n, dtype=np.float64)

n, mat_admitancia, _* = cdf.read('ieee14cdf.txt')

v_theta = np.ones()

for i in range(n):
    for j in range(n):
        v_j = v[j]
        B_ij = mat_admitancia[i,j].imag
        G_ij = mat_admitancia[i,j].real
        a = v_j * G_ij
        b = v_j * B_ij

        P_Q[i] = P_Q[i] + a * cos() + b * sin()
        P_Q[n+i] = P_Q[n+i] + a * sin() - b * cos()

    P_Q[i] = v[i] * P[i]
    P_Q[i] = v[i] * P[i]