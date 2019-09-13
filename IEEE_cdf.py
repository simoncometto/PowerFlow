import numpy as np
import matplotlib.pyplot as plt


with open('ieee14cdf.txt') as cdf:
        #Leo el archivo hasta llegar a la sección de BUS DATA
        words = ['',]
        while words[0] != 'BUS':
            line = cdf.readline()
            words = line.split(' ')
            words = [item for item in words if item]  #Elimino los elementos vacios

        #Leo la cantidad de nodos en la 4ta columna
        n = int(words[3])
        #Creo la matriz de admitancia nula de n x n numeros complejos
        mat_admitancia = np.zeros((n,n), dtype=np.complex128)

        #Creo los vectores que las variables en cada nodo:
        load = np.zeros(n, dtype=np.complex128)   # P + jQ
        generation = np.zeros(n, dtype=np.complex128)      # P + jQ
        voltage_phase = np.zeros((n,2), dtype=np.float)    # V(por unidad), angulo en grados

        #Leo las siguientes n lineas con la info de cada nodo
        for i in range(n):
            line = cdf.readline()
            words = line.split(' ')
            words = [item for item in words if item]  #Elimino los elementos vacios

            voltage_phase[i, :] = (float(words[7]), float(words[8]))
            load[i] = complex(float(words[9]) , float(words[10]))
            generation[i] = complex(float(words[11]) , float(words[12]))

        #Leo el archivo hasta llegar a la sección de BRANCH DATA
        while words[0] != 'BRANCH':
            line = cdf.readline()
            words = line.split(' ')
            words = [item for item in words if item]  #Elimino los elementos vacios

        #Leo las lineas de la sección Branch
        while True:
            line = cdf.readline()
            words = line.split(' ')
            words = [item for item in words if item]  # Elimino los elementos vacios

            # Si llego al fin de la sección indicado por un -999\n salgo del bucle
            if words[0] == '-999\n':
                break

            i = int(words[0]) - 1
            j = int(words[1]) - 1       # La impedancia entre el nodo i y el nodo j
            mat_admitancia[i,j] = mat_admitancia[j,i] = -1/complex(float(words[6]) , float(words[7]))  #Asigno la impendancia R + jX

        #Recorro la matriz de admitacnia para asignarle a la diagonal la suma de las filas
        for i in range(0,n):
            for j in range(0,n):
                if j != i:
                    mat_admitancia[i,i] = mat_admitancia[i,i] + mat_admitancia[i,j]

if __name__ == '__main__':

    mat_plot = mat_admitancia != 0
    plt.matshow(mat_plot)
    plt.show()