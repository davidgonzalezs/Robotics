import cv2
import numpy as np
#import testReconocimiento as testRec
#import createDataSet as crDtSet
import pintaSalidas as ps
def getCloseHoles(contList,img):

    cnt = contList[0]
    hole = False
    hull = cv2.convexHull(cnt,returnPoints = False)
    if (len(hull)>3):
        defects = cv2.convexityDefects(cnt,hull)
        if defects!= None:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                if(d>1000):
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    cv2.line(img,start,end,[0,255,0],2)
                    # print start
                    # print end
                    cv2.circle(img,far,5,[0,0,255],-1)
                    hole = True
            cv2.imshow("HOLES",img)
    return hole

def contourImg(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
    conts, hier = cv2.findContours(image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, conts, -1, (255,255,255))
    return conts

def getSalidas(marco):
    salidas = 0
    for i in marco:
        if(np.all(i==[0,255,0])): #punto de la salida
            salidas+=1
    return salidas

def analizarMarca(image,imgCompleta):
    cnt = contourImg(image)
    if len(cnt)!=0:
        rect = cv2.minAreaRect(cnt[0])
        x,y,w,h = cv2.boundingRect(cnt[0])
        roi = image[y:y+h, x:x+w]
        cv2.imshow("roi",roi)
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2)
        cv2.imshow("cuadrado",image)
        #Ahora establezco direccion flecha
        if w > 20 and h > 20:
            conMarca = 0
            for i in range((w-1)/2):
                for j in roi[:,i]:
                    if j == 1:
                        conMarca +=1
            print conMarca
            for i in range(((w-1)/2), w-1):
                for j in roi[:,i]:
                    if j ==1:
                        conMarca -=1
            if conMarca>0:
                return "Flecha a la izquierda"
            else: 
                return "Flecha a la derecha"
            

def analizarImagen(image,labels):
    imageLine = (labels==1).astype(np.uint8)
    imageForm = (labels==2).astype(np.uint8)
    np.set_printoptions(threshold=np.nan)

    contoursLine = contourImg(imageLine)
    m,n,ch = np.shape(image)
    salSuperiores = getSalidas(image[0])
    salIzquierda = getSalidas(image[:,0])
    salDerecha = getSalidas(image[:,n-1])
    entradas = getSalidas(image[m-1])

    
    #dataSetMoments = crDtSet.createDataSet()

    if(salSuperiores==1 and entradas == 2 and salIzquierda==0 and salDerecha==0):
        print "Cruce / incorporacion con salida junto a la entrada. Flecha: " + str(analizarMarca(imageForm,image))
        return "Cruce / incorporacion con salida junto a la entrada. Flecha: " + str(analizarMarca(imageForm,image))
        
    elif(salSuperiores==2 and entradas==1 and salIzquierda==0 and salDerecha==0):
        print "Cruce / bifurcacion 2 salidas. Flecha: " + str(analizarMarca(imageForm,image))
        return "Cruce / bifurcacion 2 salidas. Flecha: " + str(analizarMarca(imageForm,image))
        
    elif(salSuperiores==0 and entradas==1 and salIzquierda==1 and salDerecha==0):
        hole = getCloseHoles(contoursLine,image)
        if(hole==True):
            print "Curva a izquierda. Flecha: " + str(analizarMarca(imageForm,image))
            return "Curva a izquierda. Flecha: " + str(analizarMarca(imageForm,image))
        else:
            #print "Linea recta. Simbolo: " + str(testRec.pruebaDinamica(dataSetMoments,labels))
            return "Linea recta. Simbolo: "# + str(testRec.pruebaDinamica(dataSetMoments,labels))
    elif(salSuperiores==0 and entradas==1 and salIzquierda==0 and salDerecha==1):
        hole = getCloseHoles(contoursLine,image)
        if(hole==True):
            print "Curva a derecha. Flecha: " + str(analizarMarca(imageForm,image))
            return "Curva a derecha. Flecha: " + str(analizarMarca(imageForm,image))
        else:
            #print "Linea recta. Simbolo: " + str(testRec.pruebaDinamica(dataSetMoments,labels))
            return "Linea recta. Simbolo: " #+ str(testRec.pruebaDinamica(dataSetMoments,labels))
    elif(salSuperiores==1 and entradas==1 and salIzquierda==0 and salDerecha==0):
        hole = getCloseHoles(contoursLine,image)
        if(hole==True):
            conti = 0
            for i in image[0]:
                if np.all(i!=[0,255,0]):
                    conti+=1
            contj = 0
            for j in image[len(image)-1]:
                if np.all(j!=[0,255,0]):
                    contj+=1
            if conti>contj:
                print "Curva a derecha. Flecha: " + str(analizarMarca(imageForm,image))
                return "Curva a derecha. Flecha: " + str(analizarMarca(imageForm,image))
            else:
                print "Curva a izquierda. Flecha: " + str(analizarMarca(imageForm,image))
                return "Curva a izquierda. Flecha: " + str(analizarMarca(imageForm,image))
        else:
            return "Linea recta. Simbolo: " #+ str(testRec.pruebaDinamica(dataSetMoments,labels))
    elif( entradas==1 and salIzquierda==1 and salDerecha==1):
        if(salSuperiores == 1):
            print "Cruce en X con 3 salidas. Flecha: " + str(analizarMarca(imageForm,image))
            return "Cruce en X con 3 salidas. Flecha: " + str(analizarMarca(imageForm,image))
        else:
            print "Cruce en T con 2 salidas. Flecha: " + str(analizarMarca(imageForm,image))
            return "Cruce en T con 2 salidas. Flecha: " + str(analizarMarca(imageForm,image))
    elif( entradas==1 and salIzquierda==1 and salDerecha==0 and salSuperiores==1):
        print "Cruce en T con 2 salidas. Flecha: " + str(analizarMarca(imageForm,image))
        return "Cruce en T con 2 salidas. Flecha: " + str(analizarMarca(imageForm,image))
    else:
        print "Forma no conocida. Flecha: " + str(analizarMarca(imageForm,image))
        return "Forma no conocida. Flecha: " + str(analizarMarca(imageForm,image))






