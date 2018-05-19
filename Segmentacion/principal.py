#coding=utf-8
#!/usr/bin/python
import pygame
import numpy as np
import cv2
from select_pixels import select_fg_bg
from select_pixels import roundline
from scipy.misc import imread, imsave
from matplotlib import pyplot as plt
import select_pixels as sel
from time import time
tiempo_inicial = time()
def segmentarImagen(imagen,strn):
	#Colorear Imagen
	i = cv2.imread(imagen)
	imgColoreada = select_fg_bg(i)
	imsave("imagenes/imagenColoreada" + strn + ".png",imgColoreada)


cap = cv2.VideoCapture("videos/video2017-3.avi")
n = 0
while (cap.isOpened()):
	ret, frame = cap.read()
	if ret==True:						#ret es true si el frame se ha leido correctamente
		#frame = cv2.flip(frame,0)    #Dar la vuelta al video
		rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

		cv2.imshow('frame',frame)

		if cv2.waitKey(10) & 0xFF == ord('q'):
			break
		if cv2.waitKey(10) & 0xFF == ord('c'):
			n+=1
			imsave("imagenes/imgSinColorearParam" + str(n) + ".png",frame)
			imsave("imagenes/imgSinColorear" + str(n) + ".png",rgb)
			segmentarImagen("imagenes/imgSinColorearParam" + str(n) + ".png",str(n))
			if n==3:
				break
	else:
		break
cap.release()
cv2.destroyAllWindows()

tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print "El tiempo de ejecución de principal.py fue: " + str(tiempo_ejecucion)