import numpy as np

def pintaCentroLinea(imagen):
    m,n,ch = np.shape(imagen)
    imagen[(m-2)/2] = pintaPixel(imagen[(m-2)/2])
    return imagen

def pintaSalidas(imagen):
    #Pinta primera y ultima filas
    m,n,ch = np.shape(imagen)
    imagen[0] = pintaPixel(imagen[0])
    imagen[m-1] = pintaPixel(imagen[m-1])
    #Pinta primera y ultima columnas
    colIzdaPint = pintaPixel(imagen[:,0])
    colDerPint = pintaPixel(imagen[:,n-1])
    cnt = 0
    for fila in imagen:
        fila[0] = colIzdaPint[cnt]
        fila[n-1] = colDerPint[cnt]
        cnt+=1
    return imagen

def pintaPixel(fila):
    cont = 0
    linea = False
    lastLinePix = 0
    for pixel in range(len(fila)-1):
        if np.all(fila[pixel] == [255,0,0]):
            linea = True
            cont+=1
        elif linea == True and np.all(fila[pixel] == [0,0,0]) and cont > 10:
            fila[int(pixel-(cont/2))] = [0,255,0]
            break
    return fila

def pintaSensores(imagen):
    m,n,ch = np.shape(imagen)
    cont = 0
    for i in range(n):
        if cont == n/3 or cont == (2*n)/3:
            imagen[m*3/4][i] = [0,255,0]
        cont += 1
    return imagen



    