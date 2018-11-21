#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import pygame, sys, time
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
        self.pos = (rect[0], rect[1])

        # verifico cual es el ancho y cual el largo
        if rect[2] < rect[3]:
            self.orientacion = "V"
            self.largo = rect[3]
            self.ancho = rect[2]
            self.ptos = [(0              ,self.ancho/2),
                         (self.ancho/2   ,0),
                         (self.ancho     ,self.ancho/2),
                         (self.ancho     ,self.largo-self.ancho/2),
                         (self.ancho/2   ,self.largo),
                         (0              ,self.largo-self.ancho/2)]
        else:
            self.orientacion = "H"
            self.largo = rect[2]
            self.ancho = rect[3]
            self.ptos = [(0 ,self.ancho/2),(self.ancho/2 ,0),(self.largo-self.ancho/2 ,0),(self.largo ,self.ancho/2),(self.largo-self.ancho/2 ,self.ancho),(self.ancho/2,self.ancho)]

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
        pygame.draw.circle(self, self.color, (self.r,self.a/2-self.e/2), self.r, 0)
        pygame.draw.circle(self, self.color, (self.r,self.a/2+self.e/2), self.r, 0)

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



    pygame.init()
#r = pygame.Rect((70,70),(170,150))

    negro = pygame.Color(0,0,0)
    reloj = Reloj((0,0))
    ventana = pygame.display.set_mode(reloj.get_size(), pygame.NOFRAME)
    isRunning = True

    while isRunning:

    	
        
        ventana.fill(negro)

#        hora = time.strftime('%H:%M:%S')
        reloj.render(ventana)

        eventos()
        pygame.display.update()

    return 0



if __name__ == '__main__':
    sys.exit(main(sys.argv))

