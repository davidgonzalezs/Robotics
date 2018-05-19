import cv2
import numpy as np

def getVecinosIzq(imagen):
    m,n,ch = np.shape(imagen)
    res = []
    res.append(imagen[(m*3/4)-1][(n/3)-1])
    res.append(imagen[(m*3/4)-1][(n/3)])
    res.append(imagen[(m*3/4)-1][(n/3)+1])

    res.append(imagen[m*3/4][(n/3)-1])
    res.append(imagen[m*3/4][(n/3)+1])

    res.append(imagen[(m*3/4)+1][(n/3)-1])
    res.append(imagen[(m*3/4)+1][(n/3)])
    res.append(imagen[(m*3/4)+1][(n/3)+1])

    return res

def getVecinosDer(imagen):
    m,n,ch = np.shape(imagen)
    res = []
    res.append(imagen[(m*3/4)-1][((2*n)/3)-1])
    res.append(imagen[(m*3/4)-1][((2*n)/3)])
    res.append(imagen[(m*3/4)-1][((2*n)/3)+1])

    res.append(imagen[m*3/4][((2*n)/3)-1])
    res.append(imagen[m*3/4][((2*n)/3)+1])

    res.append(imagen[(m*3/4)+1][((2*n)/3)-1])
    res.append(imagen[(m*3/4)+1][((2*n)/3)])
    res.append(imagen[(m*3/4)+1][((2*n)/3)+1])

    return res