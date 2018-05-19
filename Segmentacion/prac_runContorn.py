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
import segmentacion as seg
import segmEuc as sE
import marcaSalida as ms
#import clasif as cl

# Leo las imagenes de entrenamiento
imNp = imread('imagenes/imgSinColorear.png')
markImg = imread('imagenes/imagenColoreada.png')


# saco todos los puntos marcados en rojo/verde/azul
data_marca=imNp[np.where(np.all(np.equal(markImg,(255,0,0)),2))]
data_fondo=imNp[np.where(np.all(np.equal(markImg,(0,255,0)),2))]
data_linea=imNp[np.where(np.all(np.equal(markImg,(0,0,255)),2))]

# Creo y entreno los segmentadores euclideos
segmEuc = seg.segEuclid([data_fondo, data_linea, data_marca]) 

# Inicio la captura de imagenes
capture = cv2.VideoCapture("videos/video2017-3.avi")

# Ahora clasifico el video
cont = 1
while (capture.isOpened()):
    ret, imNp = capture.read()
    cv2.imshow("Imagen",imNp)
    rgb = cv2.cvtColor(imNp,cv2.COLOR_BGR2RGB) # La pongo en formato numpy
    if cont%25 == 0:  # voy a segmentar solo una de cada 25 imagenes y la muestra
        # Segmento la imagen.
        # Compute rgb normalization
        imrgbn=np.rollaxis((np.rollaxis(imNp,2)+0.0)/np.sum(imNp,2),0,3)[:,:,:2] #normaliza
        labelsEu=sE.segmenta(imNp,segmEuc)
        # Vuelvo a pintar la imagen
        # genero la paleta de colores
        paleta = np.array([[255,255,255],[0,0,255],[255,0,0],[0,255,0]],dtype=np.uint8)
        #print labelsEu
        # ahora pinto la imagen
        imColor = cv2.cvtColor(paleta[labelsEu],cv2.COLOR_RGB2BGR)
        imDraw = cv2.imshow("Segmentacion Euclid",imColor)
        imgray = cv2.cvtColor(imColor,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        im2, conts, hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        imgDest = cv2.drawContours(imColor, conts, -1, (0,255,0))
        imCont = cv2.imshow("Imagen Contorneada",imColor)

        imPuntos = ms.marcar_Salida(imColor)
        # # Para pintar texto en una imagen
        # cv2.putText(imDraw,'Lineas: {0}'.format(len(convDefsLarge)),(15,20),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0))
        # # Para pintar un circulo en el centro de la imagen
        # cv2.circle(imDraw, (imDraw.shape[1]/2,imDraw.shape[0]/2), 2, (0,255,0), -1)
        # # Guardo esta imagen para luego con todas ellas generar un video
        #cv2.imwrite()
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cont += 1

capture.release()
cv2.destroyAllWindows()

    

