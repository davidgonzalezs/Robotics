#coding=utf-8
####################################################
# Esqueleto de programa para ejecutar el algoritmo de segmentacion.
# Este programa primero entrena el clasificador con los datos de
#  entrenamiento y luego segmenta el video (este entrenamiento podria
#  hacerse en "prac_ent.py" y aqui recuperar los parametros del clasificador
###################################################
import cv2
from scipy.misc import imread, imsave
from matplotlib import pyplot as plt
import numpy as np
import segmEuc as sE
import clasifEscenas as clasEsc
from time import time
import pintaSalidas as ps
tiempo_inicial = time()

# Leo las imagenes de entrenamiento
imNp = imread('imagenes/imgSinColorear.png')
markImg = imread('imagenes/imagenColoreada.png')

imNp2 = imread('imagenes/imgSinColorear2.png')
markImg2 = imread('imagenes/imagenColoreada2.png')

imNp3 = imread('imagenes/imgSinColorear3.png')
markImg3 = imread('imagenes/imagenColoreada3.png')


# saco todos los puntos marcados en rojo/verde/azul
data_marca=imNp[np.where(np.all(np.equal(markImg,(255,0,0)),2))]
data_fondo=imNp[np.where(np.all(np.equal(markImg,(0,255,0)),2))]
data_linea=imNp[np.where(np.all(np.equal(markImg,(0,0,255)),2))]

np.append(data_marca,imNp2[np.where(np.all(np.equal(markImg,(255,0,0)),2))])
np.append(data_fondo,imNp2[np.where(np.all(np.equal(markImg,(0,255,0)),2))])
np.append(data_linea,imNp2[np.where(np.all(np.equal(markImg,(0,0,255)),2))])

np.append(data_marca,imNp3[np.where(np.all(np.equal(markImg,(255,0,0)),2))])
np.append(data_fondo,imNp3[np.where(np.all(np.equal(markImg,(0,255,0)),2))])
np.append(data_linea,imNp3[np.where(np.all(np.equal(markImg,(0,0,255)),2))])

# Creo y entreno los segmentadores euclideos
segmEuc = sE.segEuclid([data_fondo, data_linea, data_marca]) 



# Inicio la captura de imagenes
capture = cv2.VideoCapture("videos/video2017-3.avi")

# Ahora clasifico el video
cont = 1
fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
height, width, channels = imNp.shape
out = cv2.VideoWriter('videos/segmentV3-2017.avi',fourcc, 5.0, (width,height))

while (capture.isOpened()):
    ret, imNp = capture.read()
    cv2.imshow("Imagen",imNp)
    #rgb = cv2.cvtColor(imNp,cv2.COLOR_BGR2RGB) # La pongo en formato numpy
    if cont%25 == 0:  # voy a segmentar solo una de cada 25 imagenes y la muestra
        # Segmento la imagen.
        # Compute rgb normalization
        #imrgbn=np.rollaxis((np.rollaxis(imNp,2)+0.0)/np.sum(imNp,2),0,3)[:,:,:2] #normaliza
        labelsEu=sE.segmenta(imNp,segmEuc)
        # Vuelvo a pintar la imagen
        # genero la paleta de colores
        paleta = np.array([[0,0,0],[0,0,255],[255,0,0],[0,255,0]],dtype=np.uint8)
    
        # ahora pinto la imagen
        imColor = cv2.cvtColor(paleta[labelsEu],cv2.COLOR_RGB2BGR)
        dimgDest =  cv2.medianBlur(imColor, 3)

        #pinto las salidas de la imagen
        imSalidas = ps.pintaSalidas(dimgDest)
        imSalidas = ps.pintaCentroLinea(imSalidas)
        cv2.imshow("Salidas",imSalidas)

        #Clasificar Escena (recta, curva, cruce...)
        tipoEscena = clasEsc.analizarImagen(imSalidas,labelsEu)

        # # Pintar texto en una imagen
        # cv2.putText(imSalidas,tipoEscena.format(len(imSalidas)),(15,20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255))

        # # Pintar un circulo en el centro de la imagen
        cv2.circle(imSalidas, (imSalidas.shape[1]/2,imSalidas.shape[0]/2), 2, (0,255,0), -1)
        cv2.imshow("Salidas",imSalidas)
        # # Guardo esta imagen para luego con todas ellas generar un video
        out.write(imSalidas)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cont += 1


capture.release()
out.release()
cv2.destroyAllWindows()

tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print tiempo_ejecucion

