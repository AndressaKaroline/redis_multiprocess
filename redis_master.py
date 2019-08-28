import numpy
import random
import time
import logging
from time import sleep
from redis import Redis
from rq import Queue
from redis_modules import multiplica_linha_coluna

def cria_matriz(linhas, colunas):
  A = []
  for i in range(linhas):
    linha = []
    for j in range(colunas):
      linha = linha + [random.randint(1, 10)]
    A = A + [linha]
  return A

if __name__ == '__main__':
    print "Initializing redis master"
    redis_conn = Redis(host='127.0.0.1',port=6379)
    queue_jobs = Queue('my_queue', connection=redis_conn)
    jobs = []

    linhas, colunas = 3, 3

    print "Gerando matrizes"
    matrizA = [[1, 2, 3],[1, 2, 3],[1, 2, 3]] 
    matrizB = [[1, 2, 3],[1, 2, 3],[1, 2, 3]] 
    # matrizA = cria_matriz(linhas, colunas)
    # matrizB = cria_matriz(linhas, colunas)
    matrizC = numpy.zeros(shape=(linhas,colunas))

    print "Multiplicando matrizes"
    for i in range(len(matrizA)):
        for j in range(len(matrizA[0])):
            job = queue_jobs.enqueue(multiplica_linha_coluna, i, j, matrizA, matrizB)
            jobs.append(job)

    for job in jobs:
      print "Trabalhos enfileirados {0}".format(len(queue_jobs))
      while job.result is None:
        print "O trabalho {0} ainda nao foi concluido".format(job.id)
        sleep(2)
        print "Resultado {0}".format(job.result[0])
      print job.result[0]
      matrizC[job.result[1]][job.result[2]] = job.result[0]

    print("{}: Resultado: \n{}".format(time.strftime('%c'), matrizC))