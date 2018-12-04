# Relojpy
Reloj en python para escritorio 

Este es un sencillo reloj, a modo de display de 7 segmentos escrito en python y que hace uso de la librería gráfica pygame.
También puede importarse el paquete pudiendo utilizar el display en un proyecto distinto.
Para salir de la aplicación se puede utilizar la X en la esquina de la ventana o la tecla ESC.

Opciones de línea de comando

-p  X   Y   ------->    La opción '-p' sirve para posicionar la ventana en un lugar determinado. Recibe 2 parámetros, los valores X e
                        Y de la esquina superior izquierda de la ventana, los cuales deben ser enteros válidos.

NOFRAME     ------->    La constante 'NOFRAME' permite dibujar la ventana sin el marco decorativo. En caso de omitirla la ventana se
                        dibujará con el marco habitual del sistema operativo. Para salir de la aplicación cuando no se encuentra el
                        marco (por lo tanto tampoco el botón para cerrar la ventana) se utiliza la tecla ESC.

-i  Num     ------->    La opción '-i' permite elegir un ícono para representar la aplicación. Recibe un parámetro que identifica el 
                        ícono a utilizar. Los íconos deben estar ubicados en la carpeta "imagenes" en el mismo directorio que la 
                        aplicación, y deben tener obligadamente el nombre "icon-XXX.png" donde XXX es el número que identifica al 
                        ícono. El tamaño recomendado para las imágenes a utilizar como ícono debe ser de 32x32 píxeles, aunque otros
                        tamaños también podrían ser válidos no se garantiza su funcionamiento.

                        El paquete de íconos incluidos en la aplicación fué creado por Freepik y está disponible en www.flaticon.com 
