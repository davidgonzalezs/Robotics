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
import vecinos as vec
from pyrobot.brain import Brain  
   
class prac_run(Brain):
    
    tiempo_inicial = time()

    # Leo las imagenes de entrenamiento
    imNp = imread('Escritorio/imagenes/imgSinColorear.png')
    markImg = imread('Escritorio/imagenes/imagenColoreada.png')

    imNp2 = imread('Escritorio/imagenes/imgSinColorear2.png')
    markImg2 = imread('Escritorio/imagenes/imagenColoreada2.png')

    imNp3 = imread('Escritorio/imagenes/imgSinColorear3.png')
    markImg3 = imread('Escritorio/imagenes/imagenColoreada3.png')


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
    #fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
    #height, width, channels = imNp.shape
    #out = cv2.VideoWriter('videos/segmentV3-2017.avi',fourcc, 5.0, (width,height))

    while (capture.isOpened()):
        ret, imNp = capture.read()
        cv2.imshow("Imagen",imNp)
        #rgb = cv2.cvtColor(imNp,cv2.COLOR_BGR2RGB) # La pongo en formato numpy
        if cont%15 == 0:  # voy a segmentar solo una de cada 25 imagenes y la muestra
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
            imSalidas = ps.pintaSensores(imSalidas)

            #Clasificar Escena (recta, curva, cruce...)
            tipoEscena = clasEsc.analizarImagen(imSalidas,labelsEu)
            
            escena = tipoEscena.split(".")

            # front = min([s.distance() for s in self.robot.range["front"]])
            # left = min([s.distance() for s in self.robot.range["left-front"]])
            # right = min([s.distance() for s in self.robot.range["right-front"]])
            translation = 0
            rotate = 0
            if escena[0] == "Curva a derecha" or escena[0] == "Curva a izquierda" or escena[0] == "Linea recta":
                vecinosSensorIzdo = np.asarray(vec.getVecinosIzq(imSalidas))
                vecinosSensorDer = np.asarray(vec.getVecinosDer(imSalidas))
                print vecinosSensorDer
                cont1 = 0
                for i in vecinosSensorIzdo:
                    if np.any(i!= [0,0,0]):
                        cont1+=1
                cont2 = 0
                for i in vecinosSensorDer:
                    if np.any(i != [0,0,0]):
                        cont2+=1

                if cont1>0:
                    #print "me moveria izq"
                    self.robot.move(0.3, 0.4)
                elif cont2>0:
                    #print "me moveria der"
                    self.robot.move(0.3,-0.4)

            # # Pintar texto en una imagen
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(imSalidas,tipoEscena,(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(imSalidas,tipoEscena.format(len(imSalidas)),(7,10),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255))

            # # Pintar un circulo en el centro de la imagen
            cv2.circle(imSalidas, (imSalidas.shape[1]/2,imSalidas.shape[0]/2), 2, (0,255,0), -1)
            cv2.imshow("Salidas",imSalidas)
            # # Guardo esta imagen para luego con todas ellas generar un video
         #   out.write(imSalidas)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cont += 1


    capture.release()
    #out.release()
    cv2.destroyAllWindows()

    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print tiempo_ejecucion

def INIT(engine):  
    print "ey"
    assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
    return prac_run('prac_run', engine)  