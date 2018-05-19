#coding=utf-8
import numpy as np
import cv2
import csv
import reconocimiento as rec
import huMoments as hu
import segmEuc as sE
from scipy.misc import imread, imsave

def pruebaDinamica(dataSetMoments):
    capture = cv2.VideoCapture("video2017-3.avi")
    cont = 0
    while(capture.isOpened()):
        cont += 1
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Video",frame)
        if cont%20 == 0:
            labels=sE.segmenta(frame,segmEuc)
            imageForm = (labels==2).astype(np.uint8)
            paleta = np.array([[255,255,255],[0,0,255],[255,0,0],[0,255,0]],dtype=np.uint8)
            imColor = cv2.cvtColor(paleta[imageForm],cv2.COLOR_RGB2BGR)
            cv2.imshow("sss",imColor)
            momentosHu = hu.getHuMoments(imColor)
            print "Hu Moments: "
            print momentosHu
            print "Etiqueta: " + rec.reconocer(momentosHu,dataSetMoments)
            print "----------------------------------------------"
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    capture.release()
    out.release()
    cv2.destroyAllWindows()

#Prueba en directo despacho Dario
# Captura imagen en directo y llama al modulo reconocer para reconocer el icono capturado
def enDirecto(dataSetMoments):
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):   
        ret, imagen = cap.read()
        cv2.imshow("img",imagen)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
    cv2.imshow("Imagen Captada", imagen)        
    momentosHu = hu.getHuMoments(imagen)
    print momentosHu
    while(1):
        if cv2.waitKey(10) & 0xFF == ord('p'):
            return rec.reconocer(momentosHu,dataSetMoments)
            break
    return "fallo"
    
def perCent(x,max):
    return (100*x)/max

#Porcentaje de acierto de reconocimiento 1-NN
#Sacar un elemento de la bbdd en cada iteracion y reconocerlo, ver si da la etiq correcta
def pruebaEstadistica(dataSetMoments):
    dataSetCopia = list(dataSetMoments)
    total = 400
    correctos = 0
    cont = 0
    for fila in dataSetMoments:
        for k in range(100):
            aux = fila[k]
            dataSetCopia[cont].pop(dataSetCopia[cont].index(aux))
            reconocido = rec.reconocer(aux,dataSetCopia)
            if (cont == 0 and reconocido=="botiquin") or (cont == 1 and reconocido=="telefono") or (cont == 2 and reconocido=="escalera") or (cont == 3 and reconocido=="servicio"):
                correctos+=1
            dataSetCopia[cont].append(aux)
        cont+=1
    return perCent(correctos,400)

#Abrimos el csv y nos hacemos el dataset en forma de listas de python
with open('dataset.csv', mode='r') as dataset:
    data = csv.reader(dataset)  
    bot = next(data)
    tel = next(data)
    esc = next(data)
    ser = next(data)
dataset.close()
botiquin = []
telefono = []
escalera = []
servicio = []

for i in bot:
    if i != "botiquin":
        elems = i.replace("[","").replace("]","").split()
        elems2 = []
        for k in elems:
            elems2.append(float(k))
        botiquin.append(elems2)
for i in tel:
    if i != "telefono":
        elems = i.replace("[","").replace("]","").split()
        elems2 = []
        for k in elems:
            elems2.append(float(k))
        telefono.append(elems2)
for i in esc:
    if i != "escalera":
        elems = i.replace("[","").replace("]","").split()
        elems2 = []
        for k in elems:
            elems2.append(float(k))
        escalera.append(elems2)
for i in ser:
    if i != "servicio":
        elems = i.replace("[","").replace("]","").split()
        elems2 = []
        for k in elems:
            elems2.append(float(k))
        servicio.append(elems2)

dataSetMoments = [botiquin,telefono,escalera,servicio]


# Llamamos a la funcion que deseemos o en directo o la fiabilidad de nuestro dataset
#print enDirecto(dataSetMoments)
#print "Hay una fiabilidad del " + str(pruebaEstadistica(dataSetMoments)) + "%"
imNp = imread('../Segmentacion/imagenes/imgSinColorear.png')
markImg = imread('../Segmentacion/imagenes/imagenColoreada.png')

imNp2 = imread('../Segmentacion/imagenes/imgSinColorear2.png')
markImg2 = imread('../Segmentacion/imagenes/imagenColoreada2.png')

imNp3 = imread('../Segmentacion/imagenes/imgSinColorear3.png')
markImg3 = imread('../Segmentacion/imagenes/imagenColoreada3.png')

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

pruebaDinamica(dataSetMoments)