#coding=utf-8
import numpy as np
import cv2

## Este script genera el dataset del icono que se introduzca por consola 
## leyendo y almacenando una de cada 5 imagenes de dicho video para observar
# mas perspectivas

icono = raw_input('Introduce un icono (telefono, botiquin, servicio o escalera): ')
while icono!="botiquin" and icono!="telefono" and icono!="servicio" and icono!="escalera":
    icono = raw_input('Icono no reconocido, escoge uno de estos -> (telefono, botiquin, servicio o escalera): ')

cap = cv2.VideoCapture(icono+".avi")
cont = 0
numFile = 0

while(numFile<100):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if cont%5 == 0:
        nombreArchivo = icono + "/" + icono + str(numFile) + ".jpg"
        cv2.imwrite(nombreArchivo,frame)
        cont +=1 
        numFile+=1
    else: cont+=1
cap.release