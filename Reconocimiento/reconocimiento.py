#coding=utf-8
import numpy as np
import cv2
import math
from scipy.spatial import distance

## La funcion getMins(huImagen, bbdd) haya las distancias euclideas entre los momentos de Hu de una imagen
## y los de las imagenes del dataset usando la libreria de python scipy.spatial (distance).
## Finalmente devuelve las distancias mínimas medidas de cada icono.
def getMins (huImagen, bbdd):
    resultado = []
    for i in bbdd:
        listaAux = []
        for k in i:
            listaAux.append(distance.euclidean(k,huImagen)) 
        resultado.append(min(listaAux))
    return resultado
        
## La funcion reconocer(imageMoments, dataSetMoments) llama a la funcion getMins(huImagen,bbdd)
## de la que obtiene las distancias euclideas minimas de los momentos de hu de la imagen a analizar
## con los momentos de Hu de las imagenes del dataset. La menor de las distancias es la que establece
## el icono reconocido.
def reconocer(imageMoments,dataSetMoments):
    minDistances = getMins(imageMoments,dataSetMoments)
    indice = minDistances.index(min(minDistances))
    icono = "icono no reconocido"
    if indice == 0:
        icono = "botiquin"
    elif indice == 1:
        icono = "telefono"
    elif indice == 2:
        icono = "escalera"
    elif indice == 3:
        icono = "servicio"
    else: "Ningun icono reconocido"

    return icono
