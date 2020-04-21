from cairo import *
class ECA:
    """
        S_ij (healthy susceptible): float
        I_ij infected
        R_ij Recovered
        N-ij Poblacion
        Q(S,I,R)
        DS= [100*S_ij]/100
        s_ij = (DS, DI, DR)

    """
    def __init__(self , cell_x, cell_y, step):
        self.cell_x=cell_x
        self.cell_y=cell_y
        self.step = step
        self.gui = GUI(cell_x,cell_y,5)
        #self.pob_act = np.full( (cell_x,cell_y,4), float)
        #self.pob_sig = np.full( (cell_x,cell_y,4), float)
        self.pob_act = np.empty(shape=[cell_x,cell_y,4 ])
        self.pob_sig = np.empty(shape=[cell_x,cell_y,4 ])
        self.epsilon = 0.4
        self.v = 0.6
        self.N = 100
        self.m = 0.5
        self.c = 1 
        self.mu = self.c*self.m*self.v
        self.vecindad=[(0,-1),(-1,0),(1,0),(0,1)]
        self.total_s = []
        self.total_i = []
        self.total_r = []
        
        print("*")
        self.initializate()
        print("*Configuracion inicial creada*")
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
        
    def simulation(self):
        i = 0 

        self.gui.evolucion_sir(self.pob_act)
        while i < self.step:
            self.evolucion_ti()
            self.gui.evolucion_sir(self.pob_act)
            i = i +1
        self.gui.plot_sir(self.total_s ,self.total_i ,self.total_r  )
    def evolucion_ti(self):

        i = j = t_s = t_i = t_r = 0
        while i < self.cell_x:
            j = 0
            while j < self.cell_y:
                S = self.evoluvion_S(i,j)
                I = self.evolucion_I(i,j)
                R = self.evolucion_R(i,j)
                t_s += int(S*self.N)
                t_i += int(I*self.N)
                t_r += int(R*self.N)
                #print(S,I,R)
                self.pob_sig[i][j]=[S,I,R,self.N]
                
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
        return S-s_1-s_2

    def evolucion_I (self,i,j):
        S = self.pob_act[i][j][0]
        I = self.pob_act[i][j][1]
        
        suma = self.suma(i,j)
        i_0 = (1-self.epsilon)*I 
        i_1 = S*I*self.v
        i_2 = S*suma
        return i_0+i_1+i_2

    def evolucion_R (self,i,j):
        I = self.pob_act[i][j][1]
        R = self.pob_act[i][j][2]

        return R+self.epsilon*I
    def suma(self, i, j):
        Nd = self.pob_act[i][j][3]
        r = 0.
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
            N = self.pob_act[ii][jj][3]/Nd
            I = self.pob_act[ii][jj][1]
            r = r + (  N *self.mu * I)
        return r
            
            
eca = ECA (50,50,100)
eca.simulation()

#solve { x - (ay^2 -2b y+c )/(ac - b^2) = 0 , y - ( r +  (x^.5)* (c-2rb + r^2 *a)^.5 ),  Constants -> {a,b,c} }