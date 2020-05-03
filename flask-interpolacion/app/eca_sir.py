from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import csv

class ECA:

    mx= {1:['BC Norte',87257,38,3315766,10],
    2:['BC Sur',17801,40,712029,10],
    3:['Sonora',29385,97,2850330,10],
    4:['Chihuahua',26345,135,3556574,10],
    5:['Sinaloa',98877,30,2966321,10],
    6:['Durango',26996,65,1754754,10],
    7:['Nayarit',78737,15,1181050,10],
    8:['Coahuila',33579,88,2954915,10],
    9:['Nuevo Leon',165145,31,5119504,10],
    10:['Tamaulipas',76482,45,3441698,10],
    11:['Zacatecas',39480,40,1579209,10],
    12:['San Luis Potosi',84932,32,2717820,10],
    13:['Aguascalientes',656272,2,1312544,10],
    14:['Jalisco',182438,43,7844830,10],
    15:['Colima',177809,4,711235,10],
    16:['Guanajuato',325204,18,5853677,10],
    17:['Queretaro',291196,7,2038372,10],
    18:['Veracruz',193155,42,8112505,10],
    19:['Hidalgo',238197,12,2858359,10],
    20:['Michoacan',152816,30,4584471,10],
    21:['Puebla',342716,18,6168883,10],
    22:['Estado de Mexico',1348967,12,16187608,10],
    23:['Tlaxcala',424282,3,1272847,10],
    24:['CDMX',8918653,1,8918653,10],
    25:['Morelos',951906,2,1903811,10],
    26:['Guerrero',98146,36,3533251,10],
    27:['Oaxaca',84423,47,3967889,10],
    28:['Tabasco',184252,13,2395272,10],
    29:['Chiapas',127266,41,5217908,10],
    30:['Campeche',31032,29,899931,10],
    31:['Yucatan',99865,21,2097175,10],
    32:['Quintana Roo',57752,26,1501562,10]} 

    """
        S_ij (healthy susceptible): float
        I_ij infected
        R_ij Recovered
        N-ij Poblacion
        Q(S,I,R)
        DS= [100*S_ij]/100
        s_ij = (DS, DI, DR)

    """

    def __init__(self , cell_x=10, cell_y=10, step=10, flask=None, epsilon=None, v=None, N=None, m=None ,c=None ):

        self.cell_x=cell_x
        self.cell_y=cell_y
        self.step = step
        self.flask = flask
        
        #self.pob_act = np.full( (cell_x,cell_y,4), float)
        #self.pob_sig = np.full( (cell_x,cell_y,4), float)
        self.pob_act = np.empty(shape=[cell_x,cell_y,4 ])
        self.pob_sig = np.empty(shape=[cell_x,cell_y,4 ])
        
        if epsilon ==None:
            self.epsilon = 0.02
        else:
            self.epsilon = epsilon
        
        if v==None:
            self.v = 0.7
        else : 
            self.v = v
        
        if N ==None:
            self.N = 100
        else:
            self.N = N

        if m == m : 
            self.m = 0.1
        else : 
            self.m = m
        
        if c ==None:
            self.c = 1 
        else :
            self.c = c 
        
        self.mu = self.c*self.m*self.v
        self.vecindad=[(0,-1),(-1,0),(1,0),(0,1)]
        self.total_s = []
        self.total_i = []
        self.total_r = []
        
        print("*")
        #self.initializate()
        print("*Configuracion inicial creada*")
    
    def init_json(self, cell_x, cell_y, step ):
        with open('mapa.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

    def iniciar_mexico(self , inf = 10 ):
        #print(self.mx)
        self.cell_x = 45
        self.cell_y = 72
        
        #self.cell_x = 72
        #self.cell_y = 45
        
        self.pob_act = np.empty(shape=[self.cell_x,self.cell_y,5 ])
        self.pob_sig = np.empty(shape=[self.cell_x,self.cell_y,5 ])
        i = j = 0
        t_s = 0

        with open('mapa.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                j = 0
                for e in row:

                    if e == '':
                        self.pob_act[i][j]=[ None , None , None, None, None ]
                        self.pob_sig[i][j]=[ None , None , None, None, None ]
                    else:

                        e = int(e)
                        N = self.mx[e][1]
                        S = (N - inf)/N
                        I  = 1 - S
                        self.pob_act[i][j]=[ S , I , 0., N, e ]
                        self.pob_sig[i][j]=[ S , I , 0., N, e ]
                        t_s += N
                    j = j +1
                   #print(e)
                i = i +1    
                #print(len(reader),len(row))
                #print(row)
        self.total_s.append(t_s)
        self.total_i.append(0)
        self.total_r.append(0)
       
        
    def initializate (self):
        i = 0 
        j = 0
        t_s = 0
        while i < self.cell_x:
            j = 0
            while j < self.cell_y:
                self.pob_act[i][j]=[1.,0., 0., self.N ]
                self.pob_sig[i][j]=[1.,0., 0., self.N ]
                t_s +=self.N
                j = j +1
            i = i +1
        self.total_s.append(t_s)
        self.total_i.append(0)
        self.total_r.append(0)
        self.pob_act[i//2][j//2]=[.7,0.3, 0., self.N ]
        #self.pob_act[i//4][j//4]=[.7,0.3, 0., self.N ]
    
    def simulacion_flask(self , esc = 5 ):
        self.evolucion_ti()
        img  = Image.new( 'RGB',[self.cell_y*esc , self.cell_x*esc ] )
        result = []
        i = 0 
        j = 0
        while i < self.cell_x:
            j = 0
            fila = []
            while j < self.cell_y:
                
                a = self.pob_act[i][j][1]
               
                if a is None or np.isnan(a):
                    fila.extend( [ (0,0,102) ]*esc )
                else :
                    a = int( (1-a)*255 )
                    fila.extend( [(a,a,a)]*esc )

                j = j +1
            result.extend(fila*esc)
            i = i +1

        img.putdata(result)
        #img.show()
        img.save("nono.png")
        #return self.pob_act
        return img

    
    def simulation(self):
        i = 0 
        while i < self.step:
            self.evolucion_ti()
            #print("Dia: ", i)
            i = i +1
        print("Dia ",i)
   
    def evolucion_ti(self):

        i = j = t_s = t_i = t_r = 0
        while i < self.cell_x:
            j = 0
            while j < self.cell_y:
                if np.isnan(self.pob_act[i][j][0] ):
                    j = j+1
                    continue
                N = self.pob_act[i][j][3]
                S = self.evoluvion_S(i,j)
                I = self.evolucion_I(i,j)
                R = self.evolucion_R(i,j)
                #print(i,j, self.pob_act[i][j], " ** " , S, N)
                t_s += int(S*N)
                t_i += int(I*N)
                t_r += int(R*N)
                #print(S,I,R)
                
                self.pob_sig[i][j][0]= S
                self.pob_sig[i][j][1]= I
                self.pob_sig[i][j][2]= R
                
                #[S,I,R,self.N]
                #self.pob_sig[i][j]=[S,I,R,self.N]
                
                j = j+1
            i = i + 1
        aux = self.pob_act
        self.pob_act = self.pob_sig
        self.pob_sig = aux
        
        self.total_s.append(t_s)
        self.total_i.append(t_i)
        self.total_r.append(t_r)

        

    def evoluvion_S(self, i, j):
        S = self.pob_act[i][j][0]
        I = self.pob_act[i][j][1]
        suma = self.suma(i,j)
        s_1 = self.v*S*I
        s_2 = S*suma
        #print("SS", suma )
        if (S-s_1-s_2) < 0:
            #print("S < 0 ", S, I, suma, "// ", s_1, s_2)
            return 0
        return S-s_1-s_2

    def evolucion_I (self,i,j):
        S = self.pob_act[i][j][0]
        I = self.pob_act[i][j][1]
        
        suma = self.suma(i,j)
        i_0 = (1-self.epsilon)*I 
        i_1 = S*I*self.v
        i_2 = S*suma
        if (i_0+i_1+i_2) < 0:
            print(" I < 0",S,I,"--",suma, i_0 , i_1 , i_2)
        return i_0+i_1+i_2

    def evolucion_R (self,i,j):
        I = self.pob_act[i][j][1]
        R = self.pob_act[i][j][2]
        return R+self.epsilon*I
    def suma(self, i, j):
        Nd = self.pob_act[i][j][3]
        
        r = 0.0
        #print("r",r)
        """
            -   (i,j-1)
        (i-1,j) (i, j )   (i+1,j)
                (i,j+1)
        """
        for v_ij in self.vecindad:
            ii = i+ v_ij[0]
            jj = j +v_ij[1]
            if ii == -1:
                ii = self.cell_x -1
            if ii == self.cell_x :
                ii = 0
            if jj == -1 :
                jj = self.cell_y - 1
            if jj == self.cell_y : 
                jj = 0
            if np.isnan( self.pob_act[ii][jj][3] ):
                pass
            else :
                N = self.pob_act[ii][jj][3]/Nd
                I = self.pob_act[ii][jj][1]
                r = r + (  N *self.mu * I)
                #print( "--", ii, jj , ( N *self.mu * I), N, I)
        #print("\n suma",N, I ,r ,self.mu ," *\n")
        return r
            
    def graficas_flask(self):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        
        axis.plot(self.total_s , label = "Suceptibles")
        axis.plot(self.total_i, label = "Infectados")
        axis.plot(self.total_r, label = "Recuperados")
        
        return fig 
        """
        plt.ylabel('Individuos')
        plt.xlabel('Días')
        plt.title(' Modelo SIR ')
        plt.show()
        """
if __name__ == "__main__":
    epsilon=.4
    v=.9
    m=1
    c=.9

    eca = ECA (45,72,15,epsilon=epsilon, v=v, m=m ,c=c)
    eca.iniciar_mexico()
    for a in range(15):
        img = eca.simulacion_flask()
        #img.show()
        img.save("hola.png")
        img.close()
    
    eca.graficas_flask()


    #eca.simulation()

#solve { x - (ay^2 -2b y+c )/(ac - b^2) = 0 , y - ( r +  (x^.5)* (c-2rb + r^2 *a)^.5 ),  Constants -> {a,b,c} }