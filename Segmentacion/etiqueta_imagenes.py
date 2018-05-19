import cv2
from scipy.misc import imread, imsave
from matplotlib import pyplot as plt
import select_pixels as sel

def segmentarImagen(imagen):
	#Colorear Imagen
	i = cv2.imread(imagen)
	imgColoreada = select_fg_bg(i, 2)
	cv2.imwrite("imagenes/imagenColoreada.jpg",imgColoreada)



# Abres el video / camara con

capture = cv2.VideoCapture("videos/video2017-3.avi")

# Lees las imagenes y las muestras para elegir la(s) de entrenamiento
# posibles funciones a usar
ret, frame = cap.read()
if cv2.waitKey(10) & 0xFF == ord('q'):
	break
if cv2.waitKey(10) & 0xFF == ord('c'):
    imsave("imagenes/imgSinColorear.png",frame)
    cv2.imwrite("imagenes/imgSinColorear.jpg",frame)
	cv2.imwrite("imagenes/imgSinColorearParam.jpg",rgb)
	segmentarImagen('imagenes/imgSinColorearParam.jpg')
	break
else:
    break

cv2.waitKey()
capture.read()
cv2.imshow()

capture.release()
cv2.destroyWindow("Captura")

# Si deseas mostrar la imagen con funciones de matplotlib posiblemente haya que cambiar
# el formato, con
cv2.cvtColor(<img>, ...)

# Esta funcion del paquete "select_pixels" pinta los pixeles en la imagen 
# Puede ser util para el entrenamiento

markImg = sel.select_fg_bg(imNp)

# Tambien puedes mostrar imagenes con las funciones de matplotlib
plt.imshow(markImg)
plt.show()

# Si deseas guardar alguna imagen ....

imsave('lineaMarcada.png',markImg)

