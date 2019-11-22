# coding=utf-8
import numpy as np

def read(archivo):
    '''Lee un archivo de texto con el formato establecido por la IEEE.

        :return:
        ->  n: un escalar indicando la cantidad de nodos del sistema
        ->  mat_admitancia: una matriz de nxn compleza
        ->  load: un vector de dim=n complejo P+jQ. La carga de cada nodo.
        ->  generation: un vector de dim=n complejo P+jQ. La generación de cada nodo
        ->  voltage_phase: Un vector de pares (nx2) .La tensión y fase(¡¡¡EN GRADOS!!!) en cada nodo (según lo calculado)

        Ejemplo:
         -> n, mat_admitancia, load, generation, voltage_phase, swing_bus  = cdf.read("ieee14cdf.txt")'''

    with open(archivo) as cdf:
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

            PV_buses = np.array([], dtype=int)

            #Leo las siguientes n lineas con la info de cada nodo
            for i in range(n):
                line = cdf.readline()
                words = line.split(' ')
                words = [item for item in words if item]  #Elimino los elementos vacios

                voltage_phase[i, :] = (float(words[7]), float(words[8]))
                load[i] = complex(float(words[9]) , float(words[10]))
                generation[i] = complex(float(words[11]) , float(words[12]))



                #Asigno el swing_bus
                if(int(words[6])==3):
                    swing_bus = i

                #PV buses
                if (int(words[6]) == 2):
                    PV_buses = np.hstack((PV_buses,[i]))

            #Leo el archivo hasta llegar a la sección de BRANCH DATA
            while words[0] != 'BRANCH':
                line = cdf.readline()
                words = line.split(' ')
                words = [item for item in words if item]  #Elimino los elementos vacios

            #Leo las lineas de la sección Branch
            while True:         #Salgo con un break en el próximo if
                line = cdf.readline()
                words = line.split(' ')
                words = [item for item in words if item]  # Elimino los elementos vacios

                # Si llego al fin de la sección indicado por un -999\n salgo del bucle
                if words[0] == '-999\n':
                    break

                i = int(words[0]) - 1
                j = int(words[1]) - 1       # La impedancia entre el nodo i y el nodo j
                mat_admitancia[i,j] = mat_admitancia[j,i] = -1/complex(float(words[6]) , float(words[7]))  #Asigno la impendancia R + jX
                mat_admitancia[i,i] = mat_admitancia[j,j] = complex(0,float(words[8]))  #En la diagonal sumo Charging B ''la impedancia paralelo del equivalente pi''

            #Recorro la matriz de admitacnia para asignarle a la diagonal la suma de las filas
            for i in range(0,n):
                for j in range(0,n):
                    if j != i:
                        mat_admitancia[i,i] += -mat_admitancia[i,j]
                        #mat_admitancia[j,j] += -mat_admitancia[i,j]

            np.savetxt('Ybus.txt', mat_admitancia, fmt='%+9.4f', delimiter='  ')

            return n, mat_admitancia, load, generation, voltage_phase, swing_bus, PV_buses

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    n, mat, load, generation, voltage_phase, swing_bus, PV_buses = read("ieee14cdf.txt")

    print(n, ' nodos')
    print('PV buses: ', PV_buses)
    print(mat)
    mat_plot = mat != 0
    plt.matshow(mat_plot)
    plt.show()
