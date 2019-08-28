from time import sleep

def multiplica_linha_coluna(i, j, matrizA, matrizB):
    valor = 0
    i, j
    for k in range(len(matrizB)):
       valor = valor + matrizA[i][k] * matrizB[k][j]
    return valor, i, j