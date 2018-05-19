Este directorio contiene código para ayudaros a segmentar una imagen.

Archivos:

select_pixels.py    Funciones para pintar encima de una imagen

pinta_colores.py    Ejemplo para mostrar la distribución de color de los píxeles marcados

principal.py	    Obtiene una imagen de un video ejemplo y la colorea para usarla posteriormente en el entrenamiento

pract_run.py	    Esqueleto de programa para ejecutar el algoritmo de segmentación.
		    Este programa primero entrena el clasificador con los datos de
 		    entrenamiento y luego segmenta el vídeo.

segmentacion.py	    Halla los centros de las diferentes clases (fondo, linea y marca) a partir de los datos de los pixeles reales obtenidos de la imagen coloreada.

segmEuc.py	    Es el clasificador que mediante el calculo de las distancias euclideas etiqueta los pixeles de la imagen a segmentar.


No me ha dado tiempo a terminar todo analisis.
