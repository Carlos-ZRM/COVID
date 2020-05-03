import pygame, sys
from pygame.locals import *
from time import sleep
import threading
import matplotlib.pyplot as plt
import numpy as np 

class GUI:
    verde = (4,180,4) 
    rosa = (229,70,143)
    rojo = (223,1,1)
    negro = (25,7,11)
    def __init__(self, cell_x, cell_y, size=1):
        size = 7
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.size = size
        pygame.init()
        #self.display=pygame.display.set_mode((self.cell_x*size, self.cell_
        # y*size) )
        self.display=pygame.display.set_mode((self.cell_y*size, self.cell_x*size ) )
        self.display.fill((255,255,255))
        pygame.display.update()
        #self.evolucion(color1=(200,100,10), color2=(32,55,40))

        x = threading.Thread(target=self.thread_function)
        x.start()


    def thread_function(self):
        while True:
            sleep(1)
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
        
    def evolucion_sir(self, data):
        self.display.fill((255,255,255))
        i = 0 
        j = 0
        
        while i < self.cell_x:
            j = 0
            
            while j <  self.cell_y :
                degradado = data[i][j][1]
                #print(degradado, i, j , data[i][j] )
                if degradado == None:
                    color = (0,0,102)
                elif np.isnan(degradado):
                    color = (0,0,102)
                else:
                    #print("deg",degradado)
                    degradado = int( (1-degradado)*255 )
                    
                if degradado == 0:
                    color = (255, 255, 255)
                elif degradado > 255:
                    color = (0, 0, 0)
                elif np.isnan(degradado):
                    color = (0,0,102)
                else:
                    color = (degradado,degradado,degradado)
                #print(i,j,color, data[i][j][4] )
                pygame.draw.rect(self.display,color,(j*self.size,i*self.size,self.size,self.size))
                j = j+1
            i = i +1
        pygame.display.update()
        sleep(0.03)
    
    def evolucion_svh(self, data):
        self.display.fill((255,255,255))
        i = 0 
        j = 0
        x = y = 0
        
        while i < self.cell_x:
            j = 0
            while j < self.cell_y:
                if data[i][j][0] == 0:
                    color = self.verde
                elif data[i][j][0] == 1:
                    color = self.rosa
                elif data[i][j][0] == 2:
                    color = self.rojo
                else:
                    color = self.negro 
                pygame.draw.rect(self.display,color,(i*self.size,j*self.size,self.size,self.size))
                j = j+1
            i = i +1

        pygame.display.update()
        
        #sleep(0.0001)


    def evolucion(self,data=None, color1=None, color2=None ):
        
        
        #(255,255,255)=(255,255,255)
        BLUE=(0,0,255)

        self.display.fill((255,255,255))
        pygame.draw.rect(self.display,(20,55,100),(200,150,100,50))
        i = 0 
        j = 0
        #sleep(2)
        self.display.fill((255,255,255))
        #pygame.draw.rect(self.display,(20,200,255),(x,y,h,g))
        x = y = 0
        
        while i < self.cell_x:
            j = 0
            while j < self.cell_y:
                if (i + j)%2 == 0:
                    color = color1
                else :
                    color = color2 
                pygame.draw.rect(self.display,color,(i*self.size,j*self.size,self.size,self.size))
                j = j+1
            i = i +1
        
        pygame.display.update()
        sleep(5)

        """
            sleep(0.01)
            pygame.draw.rect(self.display,(0,0,255),(x,y,h,g))
            pygame.display.update()
            for event in pygame.event.get():
         
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
            """
    def plot_sir (self, t_s, t_i, t_r):
        #plt.plot(t_s , label = "Suceptibles")
        plt.plot(t_i, label = "Infectados")
        print("\n\n**************\n Maximo y minmo de recuperados \n" , max(t_i), min(t_i)  ,"\n**********************\n\n")
        plt.plot(t_r, label = "Recuperados")
        plt.ylabel('Individuos')
        plt.xlabel('Días')
        plt.title(' Modelo SIR ')
        plt.legend()
        plt.show()

    def plot_svh(self, virus, vivas , elipse , secretoras ,  muertas):
        plt.clf()

        plt.subplot(311)
        plt.plot(virus)
        plt.yscale('log')
        plt.xlabel('Horas')
        plt.ylabel('Individuos')
        plt.title(' Virus')
        plt.grid(True)

        #fig, ax = plt.subplots()

        plt.subplot(312)
        plt.ylabel('Individuos')
        plt.xlabel('Horas')
        plt.title(' Población vivas, muertas')
        plt.yscale('linear')
        plt.plot( vivas[0] , label = "vivas" )
        plt.plot( muertas[0] , label = "muertas" )
        plt.grid(True)

        plt.subplot(313)
        plt.ylabel('Individuos')
        plt.xlabel('Horas')
        plt.title(' Población elipse secretora')
        suma = np.array(elipse[0])+np.array(secretoras[0])
        plt.plot( elipse[0] , label = "elipse" )
        plt.plot( secretoras[0] , label = "muertas" )
        plt.plot( suma , label = "suma" )
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
        
"""
def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((500,400),0,32)
    x = 0 
    y = 0 
    h = 100
    g = 50
    WHITE=(255,255,255)
    BLUE=(0,0,255)

    DISPLAY.fill(WHITE)

    pygame.draw.rect(DISPLAY,BLUE,(200,150,100,50))

    while True:
        xo = x
        x = y
        y = xo
        xo = h
        h = g
        g = xo
        sleep(2)
        DISPLAY.fill((255,255,255))
        pygame.draw.rect(DISPLAY,(0,0,255),(x,y,h,g))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
"""
#g = GUI(100,100,10)
#g.evolucion(color1=(0,100,10), color2=(20,0,40))

