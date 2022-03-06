#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 10:37:03 2022

@author: cati
"""
from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
import random

NPROD = 3
NCONS = 1
N = 5


def productor(l_semaforos,buffer, idx):
    v = 0 
    for i in range(N):
        v += random.randint(0,5)
        l_semaforos[2*idx].acquire()# wait empty
        buffer[idx] = v
        l_semaforos[2*idx+1].release()  # signal nonEmpty
    v = -1
    l_semaforos[2*idx].acquire()# wait empty
    buffer[idx] = v
    l_semaforos[2*idx+1].release() # signal nonEmpty
    
    
    
def minimo(lista):
    otro = [0]*len(lista)
    maximo = max(lista)
    for i in range(len(lista)):
        if lista[i] == -1:
            otro[i] = maximo + 1
        else:
            otro[i] = lista[i]
    minimo = otro[0]
    index = 0
    for i in range(1, len(otro)):
        if otro[i] < minimo and otro[i] != -1:
            minimo = otro[i]
            index = i
    return minimo, index
    
def consumidor(lista, buffer):  
    
    numeros = []
    
    for i in range(NPROD):
        lista[2*i+1].acquire() # wait nonEmpty
        
    while [-1]*NPROD != list(buffer):
        
        v, index = minimo(buffer)
        print('anade:', v, 'de Prod', index)
        numeros.append(v)
        print (f"numeros: {numeros}")
        lista[2*index].release() # signal empty
        lista[2*index + 1].acquire() # wait nonEmpty
    
    print ('Valor final de la lista:', numeros)



def main():
    buffer = Array('i',NPROD)
    
    l_semaforos = []
    for i in range(0,NPROD):
        non_empty = Semaphore(0)
        empty = BoundedSemaphore(1)
        l_semaforos.append(empty)
        l_semaforos.append(non_empty)
    l_prod = [ Process(target = productor, 
                       name=f'prod_{i}', 
                       args=(l_semaforos,buffer,i))
                    for i in range (NPROD)]
    cons = Process(target = consumidor, args = (l_semaforos,buffer))
    
    
    for p in l_prod:
         p.start()
    cons.start()
    for p in l_prod:
        p.join()
    cons.join()


if __name__ == "__main__":
 main()    
           
         
    
    


