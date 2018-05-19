import numpy as np
import cv2
import time

# #Script con el que grabe los videos para el dataset descartando los 10 primeros frames
# #porque la camara deslumbra al principio

cap = cv2.VideoCapture(0)
fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
out = cv2.VideoWriter('escalera.avi',fourcc, 20.0, (640,480))
cont = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    cont+=1
    if ret==True:
        if(cont>=10):
            out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

