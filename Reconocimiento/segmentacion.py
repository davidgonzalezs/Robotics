import numpy as np
import cv2

def segEuclid(datos):
    return np.mean(datos[0],axis = 0),np.mean(datos[1],axis = 0),np.mean(datos[2],axis = 0)
