import cv2
import numpy as np



def getCloseHoles(contList,img):

    # chullList = [cv2.convexHull(cont, returnPoints=False) for cont in contList ]
    # convDefs = [cv2.convexityDefects(cont, chull) for (cont,chull) in zip(contList,chullList)]
    # cont = contList[0]
    # cnvDef = convDefs[0]
    # # Saco la lista de agujeros del contorno
    # listConvDefs=cnvDef[:,0,:].tolist()
    # # Devuelvo la lista de agujeros mayores de 4 pixeles, aproximadamente
    # print listConvDefs
    # holes = False
    # for init,end,mid,length in listConvDefs:
    #     if length>1000:
    #         resultado = [init,end,mid,length]
    #         holes = True
    # cv2.imshow("Holes",img)
    # return holes
    cnt = contList[0]
    hole = False
    hull = cv2.convexHull(cnt,returnPoints = False)
    if (len(hull)>3):
        defects = cv2.convexityDefects(cnt,hull)
        # tam = defects.shape
        # print tam
        
        # if tam[1]>1:
        #     t = 1
        # else: t = 0
        # print t
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
    cv2.imshow("imcont",image)
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
    centroLinea = getSalidas(image[m/2])
    analizarMarca(imageForm,image)

    if(salSuperiores==1 and entradas == 2 and salIzquierda==0 and salDerecha==0):
        return "Cruce / incorporacion con salida junto a la entrada"
        
    elif(salSuperiores==2 and entradas==1 and salIzquierda==0 and salDerecha==0):
        
        return "Cruce / bifurcacion 2 salidas"
        
    elif(salSuperiores==0 and entradas==1 and salIzquierda==1 and salDerecha==0):
        hole = getCloseHoles(contoursLine,image)
        #print hole
        if(hole==True):
            return "Curva a izquierda."
        else: return "Linea recta."
    elif(salSuperiores==0 and entradas==1 and salIzquierda==0 and salDerecha==1):
        hole = getCloseHoles(contoursLine,image)
        #print hole
        if(hole==True):
            return "Curva a derecha."
        else: return "Linea recta."
    elif(salSuperiores==1 and entradas==1 and salIzquierda==0 and salDerecha==0):
        hole = getCloseHoles(contoursLine,image)
        #print hole
        if(hole==True):
            for i in image[0]:
                if np.all(i==[0,255,0]):
                    return "Curva a izquierda."
            for j in image[len(image)-1]:
                if np.all(j==[0,255,0]):
                    return "Curva a derecha."
        else: return "Linea recta."
    elif( entradas==1 and salIzquierda==1 and salDerecha==1):
        if(salSuperiores == 1):
            return "Cruce en X con 3 salidas."
        else:
            return "Cruce en T con 2 salidas."
    elif( entradas==1 and salIzquierda==1 and salDerecha==0 and salSuperiores==1):
        return "Cruce en T con 2 salidas."
    else: return "Forma no conocida"






