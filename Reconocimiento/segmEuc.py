#Esta subrutina etiqueta la imagen como [0,2,1] #fondo negro, linea azul y marca roja 
import math
import numpy as np
from scipy.spatial import distance

def segmenta(imagen, centros):
    newImg = []
    numeroFila = 0
    for fila in imagen:
        if numeroFila >= 90:
            newFila = []
            for columna in fila:
                newFila.append(etiqueta(columna, centros))
            newImg.append(newFila)
        else: numeroFila += 1
    return np.array(newImg)

def etiqueta(pix,cent):
    distancias = dEuclidea(pix,cent)
    menor = min(float(s) for s in distancias)
    color = [0,2,1] #fondo negro, linea azul y marca roja 
    return color[distancias.index(menor)]
    

def dEuclidea(pixel,centros):
    matRes = (centros - pixel)**2
    fondo = math.sqrt(matRes[0][0]+matRes[0][1]+matRes[0][2])
    linea = math.sqrt(matRes[1][0]+matRes[1][1]+matRes[1][2])
    marca = math.sqrt(matRes[2][0]+matRes[2][1]+matRes[2][2])

    return [fondo,linea,marca]