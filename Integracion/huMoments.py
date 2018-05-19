#coding=utf-8
import cv2
import csv

## Funcion getHuMoments(image)
## Obtiene los momentos de Hu de una imagen pasada como parametro usando la libreria de python cv2
def getHuMoments(image):
    print "Hola"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY) #59%
    ret, final = cv2.threshold(thresh,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #74%
    filtrada = cv2.medianBlur(final,5)
   # print filtrada
    cv2.imshow("Imagen Binarizada", filtrada)
    #cv2.imwrite("segmentacion/img.jpg", filtrada)
    return cv2.HuMoments(cv2.moments(filtrada)).flatten()


## Funcion createCSV
## Crea un fichero CSV con los momentos de Hu extraidos de las imagenes del dataset
## en el csv se guarda con el formato:  etiquetaIcono momentoImg0 momentoImg1 momentoImg2 ... momentoImg99
def createCSV(lista):
    
    with open('dataset.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        writer.writerow(["botiquin"] + lista[0]) 
        writer.writerow(["telefono"] + lista[1])
        writer.writerow(["escalera"] + lista[2])
        writer.writerow(["servicio"] + lista[3])

## Funcion classCenters
## Funcion principal que obtiene los momentos de Hu de las imagenes del dataset 
## llamando reiteradamente a getHuMoments(imagen) y lod guarda en una lista.
## Despues llama a la funcion createCSV(lista) para crear el csv.
def classCenters():
    iconos = ["botiquin","telefono","escalera","servicio"]
    finalList = []                        # 0-> datosbotiquin, 1-> datostelefono, 2-> datos escalera, 3-> datos servicio
    for icono in iconos:
        iconList = []
        for numImg in range(100):
            img = cv2.imread(icono + "/" + icono + str(numImg) + ".jpg")
            iconList.append(getHuMoments(img))
        finalList.append(iconList)
    createCSV(finalList)
  

#Llamada para ejecutar el script
#classCenters()