from cairo import *
import numpy as np
class ECA:
    """
        S Estatus de la celula (sana,eclipse, secretora, muerta)
        V virus free
        Hours numero de horas infectada
        ti: Tasa de infeccion (cantidad necesaria de virus free para que una celula se infecte eclipse)
        tt : tasa de transmision 


    """
    def __init__(self , cell_x, cell_y, step, ti, tt):
        self.cell_x=cell_x
        self.cell_y=cell_y
        self.step=step
        self.nun_sana = []
        self.num_eclipse = []
        self.num_secretora = []
        self.num_muerta = []
        self.num_virus = []
        self.pob_act = np.full((cell_x,cell_y), np.array)
        self.pob_sig = np.full((cell_x,cell_y), np.array)
        self.ti = ti
        self.tt = tt
        self.configuracion_inicial()
        self.gui = GUI(cell_x,cell_y,1)
        self.evolucion()
    def configuracion_inicial(self):
        # Iniciamos la poblacion inicial
        i = j = 0
        while i < self.cell_x:
            j = 0
            while j < self.cell_y:
                # cada ceula tiene las tres propiedades  SVH (int, float, int)
                self.pob_act[i][j]=[0,(0.2025),0]
                j = j+1
            i = i +1
        # Se agrega la celula inicial en estado eclipse 
        #self.pob_act[self.cell_x//2][self.cell_y//2]=[1,self.ti,0]

    def evolucion(self):
        i = 0 
        # Se evoluciona la cantidad de horas o ticks

        self.gui.evolucion_svh(self.pob_act)
        while i < self.step:
            self.evolucion_ti()
            self.gui.evolucion_svh(self.pob_act)
            i = i +1
            if i%100==0:
                print("t",i//100)
            
        self.gui.plot_svh(self.num_virus,[self.nun_sana, 'celulas sanas'],
                        [self.num_eclipse, 'celulas en eclipse'],
                        [self.num_secretora, 'celulas secretoras'],
                        [self.num_muerta, 'celulas muertas'])
    def evolucion_ti(self):

        i = j = 0
        num_san = num_ecl = num_sec = num_mu = num_vi = 0
        # creamos la poblacion t_i+1
        while i < self.cell_x:
            j = 0
            # Hacemos la evolucion de cada caracteristica de la celula
            while j < self.cell_y:
                s = self.evoluvion_S(i,j)
                v = self.evolucion_V(i,j)
                h = self.evolucion_H(i,j)
                self.pob_sig[i][j]=[s,v,h]
                if s == 0:
                    num_san = num_san +1
                elif s ==1:
                    num_ecl = num_ecl+1
                elif s == 2:
                    num_sec = num_sec +1
                else :
                    num_mu = num_mu +1 
                num_vi = num_vi + v
                j = j+1
            i = i + 1
        self.nun_sana.append(num_san)
        self.num_eclipse.append(num_ecl)
        self.num_secretora.append(num_sec)
        self.num_muerta.append(num_mu)
        self.num_virus.append(num_vi)

        # La poblacion actual t_i sera t_i+1    
        aux = self.pob_act
        self.pob_act = self.pob_sig
        self.pob_sig = aux
        

    def evoluvion_S(self, i, j):
        celula = self.pob_act[i][j]
        status = 0
        # Si han pasado 31 horas despues del contagio la celula se muere
        if celula[2]>31:
            status =3
        # Si han pasado 8 horas despues del contagio la celula es secretora
        elif celula[2]>8:
            status = 2
         
        # Si ha pasado una hora despues del contagio la celula esta en eclipse
        elif (0.0333325 * celula[1])  > np.random.random_sample():
            status = 1
        # en cualquier otro caso la celula esta sana 

        elif celula[0]==0:
            status = 0
        else :
            status = celula[0]
        return status
    
        

    def evolucion_V (self,i,j):
        # Virus free es el valor actual mas el transmitido por todas las celulas secretoras de la vecindad
        # Se deben verificar las condicioens de frontera 
        # Se utilizo la vecindad de moore
        virus= self.pob_act[i][j][1]
        """
        (i-1,j-1)  ( i ,j-1)  (i+1,j-1)
        (i-1, j )  ( - , - )  (i+1, j )
        (i-i,j+1)  ( i ,j+1)  (i+1,j+1)
        """
        #------------------------
        #(i-1,j-1) 
        if i-1 < 0 :
            ii = self.cell_x - 1
        else :
            ii = i
        if j-i < 0 :
            jj = self.cell_y - 1 
        else : 
            jj = j
        # Si el status es secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt
        #-------------------------
         #(i,j-1) 
        ii = i
        if j-i < 0 :
            jj = self.cell_y - 1 
        else : 
            jj = j
        # Si el status es  secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt     
        #-------------------------
         #(i+1,j-1)
        if i+1 == self.cell_x :
            ii = 
        else :
            ii = i
        if j-i < 0 :
            jj = self.cell_y - 1 
        else : 
            jj = j
        # Si el status es secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt
        
        #---------------------------
         #(i-1,j)
        if i-1 < 0 :
            ii = self.cell_x - 1
        else :
            ii = i
        jj = j
        # Si el status es secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt


         #-------------------------
         #(i+1,j)
        if i+1 == self.cell_x :
            ii = 0
        else :
            ii = i
        jj = j
        # Si el status es secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt


         #-------------------------
         #(i-1,j+1)
        if i - 1 < 0 :
            ii = self.cell_x -1
        else :
            ii = i
        if j+i == self.cell_y :
            jj = 0 
        else : 
            jj = j
        # Si el status es secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt
        
        
         #-------------------------
         #(i,j+1)
        ii = i
        if j+i == self.cell_y :
            jj = 0 
        else : 
            jj = j
        # Si el status es secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt
        #---------------------------
         #-------------------------
         #(i+1,j+1)
        if i+1 == self.cell_x :
            ii = 0
        else :
            ii = i
        if j+i == self.cell_y :
            jj = 0 
        else : 
            jj = j
        # Si el status es secretor
        if self.pob_act[ii][jj][0]==2:
            virus = virus + self.tt
        #---------------------------
        # Factor de difusion constante  cada celula
        virus = virus + ((4 * (3.18 * 10 ** -15) * 2 ) / (11 ** 2) )
        return virus
    def evolucion_H (self,i,j):
        celula = self.pob_act[i][j]
        # Verificamos que la celula esta en un status no sano 
        if celula[0]>0:
            return celula[2]+1
        else  :
            return 0

e = ECA (633,633,120,0.2,tt=(0.20250))