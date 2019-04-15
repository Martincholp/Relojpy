# Relojpy
  -------
Reloj digital de 7 segmentos, en python para escritorio 

Este es un sencillo reloj, a modo de display de 7 segmentos escrito en python y 
que hace uso de la librería gráfica pygame.
También puede importarse el paquete pudiendo utilizar el display en un proyecto 
distinto. (Aun no implementado)
Para salir de la aplicación se puede utilizar la X en la esquina de la ventana o
la tecla ESC.

Opciones de línea de comando

-p X Y   ---------------->  Se establece la posicion de la ventana indicando la
                            distancia en pixeles del borde izquierdo y del borde
                            superior de la pantalla.
                   
                            Ejemplo: Establecer la posicion a 100 pixeles de 
                            distancia horizontal y 150 pixeles del borde 
                            superior.

                                python relojpy.py -p 100 150

                            Si se omite, el sistema decidira donde dibujar la 
                            ventana. Tener en cuenta que si se establece NOFRAME
                            y la ventana se dibuja en un lugar no deseado no se 
                            podra mover.
  

-f color   -------------->  Se puede establecer el color del fondo con el nombre
                            del mismo, con formato HTML (un string de tipo 
                            '#rrggbb' donde los valores rr, gg y bb son 
                            hexadecimales), formato hexadecimal (similar al HTML,
                            pero no es necesario un string y la sintaxis es de 
                            tipo 0xrrggbb), o un valor entero que defina un color.

                            Ejemplo: Distintas formas de establecer el fondo 
                            azul.

                                python relojpy.py -f blue
                                python relojpy.py -f "#0000ff"
                                python relojpy.py -f 0x0000ff
                                python relojpy.py -f 324567

                            Si se omite el parametro '-f' se stablece el color 
                            negro como color predeterminado.


-i numIcono   ----------->  Establece el icono que se utilizara el sistema para
                            representar la ventana. Los iconos disponibles se 
                            encuentran en la carpeta imagenes, y son archivos de
                            tipo .png con un tamano de 32x32 y cuyo nombre es de
                            la forma 'icon-###.png', donde ### representan un 
                            numero de icono. Este numero es el que se debe 
                            indicar en el parametro para seleccionarlo. Se puede
                            utilizar cualquier imagen con estas caracteristicas,
                            respetando el formato del nombre de archivo. Si las 
                            imagenes tienen un tamano distinto al indicado no se
                            garantiza la correcta visualizacion del icono.

                            Ejemplo: Seleccion del icono numero 16 (el nombre de
                            archivo es "icon-016.png")

                                python relojpy.py -i 016
        
                            Si se omite la opcion '-i' se establece el icono 003
                            como predeterminado. Para modificar el icono que se 
                            ubica junto a la barra de titulo ver la opcion '-t'.

                            El paquete de íconos incluidos en la aplicación fué 
                            creado por Freepik y está disponible en
                            www.flaticon.com 

-t "Tiulo" [numIcono]  -->  Los iconos disponibles son los mismos que los 
                            indicados para la opcion '-i' y se encuentran en la 
                            carpeta imagenes. Si se desea que el icono de la 
                            barra de titulo sea el mismo que el usado por el 
                            sistema para representar la ventana se omite el 
                            segundo parametro.  Algunos sistemas no soportan un 
                            icono distinto en la barra de titulo, en este caso 
                            se ignora el segundo parametro.
 
                            Ejemplo 1: Personalizacion del titulo y seleccion 
                            del icono numero 16.

                                python relojpy.py -t "Titulo del reloj" 016

                            Ejemplo 2: Personalizacion solo del titulo. El icono
                            es el mismo que el que identifica a la ventana.

                                python relojpy.py -t "Titulo del reloj"
      
                            Si se omite la opcion '-t' se establece el titulo 
                            "Relojpy" y el icono es el mismo del de la ventana.


-h   -------------------->  Muestra esta ayuda

NOFRAME   --------------->  Si se encuentra la opcion 'NOFRAME' la ventana se 
                            dibujara sin el marco. Para cerrar la ventana en 
                            este caso se debe presionar Esc cuando la ventana 
                            tiene el foco del teclado. Por defecto se dibuja con
                            marco.

                            Ejemplo: Eliminar el marco de la ventana del reloj

                                python relojpy.py NOFRAME
