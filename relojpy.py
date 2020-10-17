#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import pygame, sys, time, os
from pygame.locals import *




def apagar():
    pygame.quit()
    sys.exit()
    
def eventos():
    for evento in pygame.event.get():
        if evento.type == QUIT:
            apagar()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                apagar()


class Segmento(pygame.Surface):
    """Segmento para formar el caracter"""
    def __init__(self, rect):
        self.pos = (int(rect[0]), int(rect[1]))

        # verifico cual es el ancho y cual el largo
        if rect[2] < rect[3]:
            self.orientacion = "V"
            self.largo = rect[3]
            self.ancho = rect[2]
            self.ptos = [(0                   ,int(self.ancho/2)),
                         (int(self.ancho/2)   ,0),
                         (self.ancho          ,int(self.ancho/2)),
                         (self.ancho          ,int(self.largo-self.ancho/2)),
                         (int(self.ancho/2)   ,self.largo),
                         (0                   ,int(self.largo-self.ancho/2))]
        else:
            self.orientacion = "H"
            self.largo = rect[2]
            self.ancho = rect[3]
            self.ptos = [(0                            ,int(self.ancho/2)),
                         (int(self.ancho/2)            ,0),
                         (int(self.largo-self.ancho/2) ,0),
                         (self.largo                   ,int(self.ancho/2)),
                         (int(self.largo-self.ancho/2) ,self.ancho),
                         (int(self.ancho/2)            ,self.ancho)]

        self.borde = 0  # Con 0 hago un segmento relleno
        self.color = pygame.Color(255,255,255)  # Blanco por defecto
        self.fondo = pygame.Color(0,0,0,0)  # Transparente por defecto
        self.visible = True

        super(Segmento, self).__init__((rect[2]+1, rect[3]+1), pygame.HWSURFACE|pygame.SRCALPHA)

    def update(self):
        self.fill(self.fondo)

        pygame.draw.polygon(self, self.color, self.ptos, self.borde)
       
    def render(self, sup):
        if self.visible:
            sup.blit(self, self.pos)

        
class Puntos(pygame.Surface):
    """Puntos de separacion entre horas y minutos y entre minutos y segundos"""

    def __init__(self, pos, r=10, e=50, a=122):
        '''pos es la posicion, r el radio, e es la separacion entre los puntos, a es la altura del caracter'''
        self.pos = pos
        self.r = r
        self.e = e
        self.a = a
        self.color = pygame.Color(255,255,255)  # Blanco por defcecto
        self.fondo = pygame.Color(0,0,0,0)  # Transparente por defecto
        self.visible = True

        super(Puntos, self).__init__((2*r, a), pygame.HWSURFACE|pygame.SRCALPHA)

    def update(self ):
        self.fill(self.fondo)
        pygame.draw.circle(self, self.color, (self.r, int(self.a/2-self.e/2)), self.r)
        pygame.draw.circle(self, self.color, (self.r, int(self.a/2+self.e/2)), self.r)

    def render(self, val, sup):
        if self.visible:
            if val==':':
                sup.blit(self, self.pos)

class Caracter(pygame.Surface):
    '''Caracter de 7 segmentos'''

    digitos = {
               '0':[True, True, True, True, True, True, False],
               '1':[False, False, True, True, False, False, False],
               '2':[False, True, True, False, True, True, True],
               '3':[False, True, True, True, True, False, True],
               '4':[True, False, True, True, False, False, True],
               '5':[True, True, False, True, True, False, True],
               '6':[True, True, False, True, True, True, True],
               '7':[False, True, True, True, False, False, False],
               '8':[True, True, True, True, True, True, True],
               '9':[True, True, True, True, True, False, True]
              }

    def __init__(self, pos, a=10, l=50, e=3):
        '''pos es la posicion del caracter, a y l son el ancho y largo de los segmentos, e es el espacio entre segmentos'''

        self.pos = pos
        self.a = a
        self.l = l
        self.esp = e
        self.fondo = pygame.Color(0,0,0,0)  # Fondo transparente por defecto

        #   Segmentos
        #
        #       b
        #     XXXXX
        #    X     X
        #  a X     X c
        #    X  g  X
        #     XXXXX
        #    X     X
        #  f X     X d
        #    X     X
        #     XXXXX
        #       e         

        self.a = Segmento((0, a/2+e, a, l))
        self.b = Segmento((a/2+e, 0, l, a))
        self.c = Segmento((l+2*e, a/2+e, a, l))
        self.d = Segmento((l+2*e, a/2+l+3*e, a, l))
        self.e = Segmento((a/2+e, 2*l+4*e, l, a))
        self.f = Segmento((0, a/2+l+3*e, a, l))
        self.g = Segmento((a/2+e, l+2*e, l, a))

        self.dictSegmentos = {'a':self.a, 
                              'b':self.b,
                              'c':self.c,
                              'd':self.d,
                              'e':self.e,
                              'f':self.f,
                              'g':self.g
                             }

        self.segmentos = [self.a, 
                          self.b,
                          self.c,
                          self.d,
                          self.e,
                          self.f,
                          self.g
                         ]

        super(Caracter, self).__init__((l+a+2*e+1, 2*l+a+4*e+1), pygame.HWSURFACE|pygame.SRCALPHA)

    def update(self):

        for s in self.segmentos:
            s.update()
        
    def render(self, val, sup):
        '''Digito a renderizar'''


        segVis = Caracter.digitos[val]  # Segmentos visibles para el digito pasado

        self.fill(self.fondo)

        for indice in range(0,7):
            self.segmentos[indice].visible = segVis[indice]
            self.segmentos[indice].render(self)
        
        sup.blit(self, self.pos)


class Reloj(pygame.Surface):
    '''Reloj digital con display de 7 segmentos'''

    def __init__(self, pos):

        #ancho de los caracteres: l+a+2*e ==> 50+10+2*3 = 66 ==> uso 70
        self.pos = pos
        self.ancho = 66
        self.dosPuntos = 20
        self.esp = 10
        self.fondo = pygame.Color(0,0,0,0)  # Transparente por defecto
        self.h1 = Caracter((0,0))
        self.h2 = Caracter((self.ancho + self.esp,0))
        self.p1 = Puntos(  (2*self.ancho + 2*self.esp,0))
        self.m1 = Caracter((2*self.ancho + 3*self.esp + self.dosPuntos,0))
        self.m2 = Caracter((3*self.ancho + 4*self.esp + self.dosPuntos,0))
        self.p2 = Puntos(  (4*self.ancho + 5*self.esp + self.dosPuntos,0))
        self.s1 = Caracter((4*self.ancho + 6*self.esp + 2*self.dosPuntos,0))
        self.s2 = Caracter((5*self.ancho + 7*self.esp + 2*self.dosPuntos,0))
    
        self.hora = [self.h1, self.h2, self.p1, self.m1, self.m2, self.p2, self.s1, self.s2]

        super(Reloj, self).__init__((6*self.ancho + 7*self.esp + 2*self.dosPuntos, self.h1.get_height()), pygame.HWSURFACE|pygame.SRCALPHA)

    # def get_size(self):
    #     '''Devuelve el ancho y alto del reloj'''

    #     ancho = 0
    #     alto = 0
    #     for car in self.hora:
    #         ancho = ancho + car.get_width()
    #         if car.get_height > alto:
    #             alto = car.get_height

    #     return (ancho, alto)

    def render(self, sup, strhora=""):
        self.fill(self.fondo)

        if strhora == "":  # Si strhora esta vacio muestro la hora actual
            strhora = time.strftime('%H:%M:%S')


        for i in range(8):

            self.hora[i].update()  # Actualizo cada caracter
            self.hora[i].render(strhora[i], self)  # Dibujo cada caracter con el valor que le corresponde

        sup.blit(self, self.pos)

#        print valor
def main(args):

    #print args

    # Posicion de la ventana. (opcion '-p' en la linea de comandos, con parametros X e Y)
    # Se establece la posicion de la ventana indicando la distancia en pixeles del borde izquierdo
    # y del borde superior de la pantalla.
    #
    # Ejemplo: Establecer la posicion a 100 pixeles de distancia horizontal y 150 pixeles del borde superior
    #        python relojpy.py -p 100 150
    #
    # Si se omite, el sistema decidira donde dibujar la ventana. Tener en cuenta que si se establece NOFRAME
    # y la ventana se dibuja en un lugar no deseado no se podra mover.

    if '-p' in args:
        Indice_p = args.index('-p')
        posVentanaX = int(args[Indice_p + 1])
        posVentanaY = int(args[Indice_p + 2])
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (posVentanaX, posVentanaY)


    # Color de fondo. (opcion -f en la linea de comandos con un parametro indicando el color elegido)
    # Se puede establecer el color con el nombre, formato HTML (un string de tipo "#rrggbbaa", donde los valores rr, gg bb y aa son 
    # hexadecimales y el valor de alpha puede ser opcional), formato hexadecimal (similar al HTML, pero el string es de tipo 
    # "0xrrggbbaa"), o un valor entero.
    #
    # Ejemplo: Distintas formas de establecer el fondo azul.
    #        python relojpy.py -f blue
    #        python relojpy.py -f "#0000ff"
    #        python relojpy.py -f 0x0000ff
    #        python relojpy.py -f 324567
    #
    # Si se omite el parametro -f se stablece el color negro como color predeterminado
    #

    if '-f' in args:
        Indice_f = args.index('-f')
        valParam = args[Indice_f + 1]
        if valParam.isdigit():
            fondo = pygame.Color(int(valParam))
        else:
            fondo = pygame.Color(valParam)

    else:
        fondo = pygame.Color(0)



    reloj = Reloj((0,0))

    # Icono. (opcion '-i' en la linea de comandos, con un parametro indicando el icono a emplear)
    # Los iconos disponibles se encuentran en la carpeta imagenes, y son archivos de tipo .png con un
    # tamano de 32x32 y cuyo nombre es de la forma "icon-###.png", donde ### representan un numero de 
    # icono. Este numero es el que se debe indicar en el parametro para seleccionarlo. 
    # Se puede utilizar cualquier imagen con estas caracteristicas, respetando el formato del nombre
    # de archivo. Si las imagenes tienen un tamano distinto al indicado no se garantiza la correcta 
    # visualizacion del icono.
    #
    # Ejemplo: Seleccion del icono numero 16 (el nombre de archivo es "icon-016.png")
    #        python relojpy.py -i 016
    #
    # Si se omite la opcion -i se establece el icono 003 como predeterminado
    # Para modificar el icono que se ubica junto a la barra de titulo ver la opcion '-t'
    #

    rutaRelojpy = "/".join(args[0].split("/")[:-1]) + "/"
    ruta_icono = rutaRelojpy + "imagenes/icon-003.png"


    if '-i' in args:
        Indice_i = args.index('-i')
        ruta_icono = rutaRelojpy + "imagenes/icon-" + args[Indice_i + 1] + ".png"

    icono = pygame.image.load(ruta_icono)
    pygame.display.set_icon(icono)
    del icono
    
    # Titulo. (opcion '-t' en la linea de comandos, con dos parametros. El primero es el titulo de la 
    # ventana mostrado en la barra de titulo y el segundo el numero de icono que debe mostrar la barra
    # de titulo)
    # Los iconos disponibles son los mismos que los indicados para la opcion '-i' y se encuentran en 
    # la carpeta imagenes. Si se desea que el icono de la barra de titulo sea el mismo que el usado 
    # por el sistema para representar la ventana se omite el segundo parametro. Algunos sistemas no 
    # soportan un icono distinto en la barra de titulo, en este caso se ignora el segundo parametro.
    #
    # Ejemplo: Personalizacion del titulo y seleccion del icono numero 16 
    #        python relojpy.py -t "Titulo del reloj" 016
    #
    # Ejemplo 2: Personalizacion solo del titulo. El icono es el mismo que el que identifica a la ventana
    #        python relojpy.py -t "Titulo del reloj"
    #
    # Si se omite la opcion '-t' se establece el titulo "Relojpy" y el icono es el mismo del de la ventana
    #
    titulo = "Relojpy"
    if '-t' in args:
        Indice_t = args.index('-t')
        titulo = args[Indice_t + 1]
        if (Indice_t + 2) <= (len(args) - 1):
            if args[Indice_t + 2].isdigit():
                ruta_icono = rutaRelojpy + "imagenes/icon-" + args[Indice_t + 2] + ".png"

            
    pygame.display.set_caption(titulo, ruta_icono)
    

    # Sin marco de la ventana. (Opcion 'NOFRAME' en la linea de comandos)
    # Si se encuentra la opcion 'NOFRAME' la ventana se dibujara sin el marco. Para cerrar la ventana
    # en este caso se debe presionar Esc cuando la ventana tiene el foco del teclado. Por defecto se 
    # dibuja con marco.
    if 'NOFRAME' in args:
        ventana = pygame.display.set_mode(reloj.get_size(), pygame.NOFRAME)
    else:
        ventana = pygame.display.set_mode(reloj.get_size())
    

    # Ayuda del programa. (Opcion '-h' en la linea de comandos)
    # Si se llama al programa con la opcion '-h' se muestra por el terminal la ayuda, con todas
    # las opciones disponibles y su uso.
    #
    if '-h' in args:
        print("Relojpy")
        print ("-------")
        print("")
        print("Reloj digital con display de 7 segmentos")
        print("")
        print("Opciones de la linea de comandos:")
        print("")
        print("  -p X Y   ---------------->   Se establece la posicion de la ventana indicando la distancia en")
        print("                               pixeles del borde izquierdo y del borde superior de la pantalla.")
        print("")
        print("                               Ejemplo: Establecer la posicion a 100 pixeles de distancia horizontal")
        print("                               y 150 pixeles del borde superior")
        print(""  )
        print("                                   python relojpy.py -p 100 150")
        print("")
        print("                               Si se omite, el sistema decidira donde dibujar la ventana. Tener en")
        print("                               cuenta que si se establece NOFRAME y la ventana se dibuja en un lugar")
        print("                               no deseado no se podra mover.")
        print("")
        print("")
        print("  -f color   -------------->   Se puede establecer el color con el nombre, formato HTML (un string")
        print("                               de tipo '#rrggbb', donde los valores rr, gg y bb hexadecimales), ")
        print("                               formato hexadecimal (similar al HTML, pero el string es de tipo")
        print("                               '0xrrggbbaa'), o un valor entero que defina un color.")
        print("")
        print("                               Ejemplo: Distintas formas de establecer el fondo azul.")
        print("")
        print("                                   python relojpy.py -f blue")
        print('                                   python relojpy.py -f "#0000ff"')
        print("                                   python relojpy.py -f 0x0000ff")
        print("                                   python relojpy.py -f 324567")
        print("")
        print("                               Si se omite el parametro '-f' se stablece el color negro como color")
        print("                               predeterminado.")
        print("")
        print("")
        print("  -i numIcono   ----------->   Establece el icono que se utilizara el sistema para representar la")
        print("                               ventana. Los iconos disponibles se encuentran en la carpeta")
        print("                               imagenes, y son archivos de tipo .png con un tamano de 32x32 y")
        print("                               cuyo nombre es de la forma 'icon-###.png', donde ### representan")
        print("                               un numero de icono. Este numero es el que se debe indicar en el")
        print("                               parametro para seleccionarlo. Se puede utilizar cualquier imagen")
        print("                               con estas caracteristicas, respetando el formato del nombre de")
        print("                               archivo. Si las imagenes tienen un tamano distinto al indicado no")
        print("                               se garantiza la correcta visualizacion del icono.")
        print("")
        print("                               Ejemplo: Seleccion del icono numero 16 (el nombre de archivo es ")
        print('                               "icon-016.png")')
        print("")
        print("                                   python relojpy.py -i 016")
        print("")
        print("                               Si se omite la opcion '-i' se establece el icono 003 como")
        print("                               predeterminado. Para modificar el icono que se ubica junto a la")
        print("                               barra de titulo ver la opcion '-t'.")
        print("")
        print("")
        print('  -t "Tiulo" [numIcono]  --->  Los iconos disponibles son los mismos que los indicados ')
        print("                               para la opcion '-i' y se encuentran en la carpeta imagenes.")
        print("                               Si se desea que el icono de la barra de titulo sea el mismo")
        print("                               que el usado por el sistema para representar la ventana se")
        print("                               omite el segundo parametro.  Algunos sistemas no soportan")
        print("                               un icono distinto en la barra de titulo, en este caso se ")
        print("                               ignora el segundo parametro.")
        print("")
        print("                               Ejemplo 1: Personalizacion del titulo y seleccion del icono")
        print("                               numero 16.")
        print("")
        print('                                   python relojpy.py -t "Titulo del reloj" 016')
        print("")
        print("                               Ejemplo 2: Personalizacion solo del titulo. El icono es")
        print("                               el mismo que el que identifica a la ventana.")
        print("")
        print('                                   python relojpy.py -t "Titulo del reloj"')
        print("")
        print("                               Si se omite la opcion '-t' se establece el titulo ")
        print('                               "Relojpy" y el icono es el mismo del de la ventana.')
        print("")
        print("")
        print("  -h   -------------------->   Muestra esta ayuda")
        print("")
        print("")
        print("  NOFRAME   --------------->   Si se encuentra la opcion 'NOFRAME' la ventana se dibujara ")
        print("                               sin el marco. Para cerrar la ventana en este caso se debe ")
        print("                               presionar Esc cuando la ventana tiene el foco del teclado.")
        print("                               Por defecto se dibuja con marco.")
        print("")

        return 0



    pygame.init()
    isRunning = True

    while isRunning:

        
        
        ventana.fill(fondo)

#        hora = time.strftime('%H:%M:%S')
        reloj.render(ventana)

        eventos()
        pygame.display.update()

    return 0



if __name__ == '__main__':
    #print sys.argv, "en main"
    for argumento in sys.argv:
        print argumento

    sys.exit(main(sys.argv))

