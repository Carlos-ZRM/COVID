import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, mpld3
import itertools as it
import math 

class datos:
    def __init__(self):
        self.total_nc = []
        self.total_nca = []
        self.total_def = []
        dataframe = pd.read_csv('Casos_Diarios_Estado_Nacional_Confirmados-act.csv')
        fila = dataframe.iloc[0]
        self.total_nc = fila.values.tolist()[3:]
        self.total_nca = list(it.accumulate(self.total_nc))
        dataframe = pd.read_csv('Casos_Diarios_Estado_Nacional_Defunciones-act.csv')
        fila = dataframe.iloc[0]
        self.total_def = fila.values.tolist()[3:]
        
    def graficas_datos(self, opc =1 , dias=1):
        if dias  > len(self.total_nc):
            dias = len(self.total_nc)
         
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        if opc==2 :
            #axis.plot(self.total_s , label = "Suceptibles")
            #axis.plot(self.total_r, label = "Recuperados")
            axis.plot(self.total_nca, label = "Acumulado de casos") 
        else :
            axis.plot(self.total_r, label = "Recuperados", dashes=[2, 1,8,2])    
            axis.plot(self.total_i, label = "Casos activos" )   
            axis.plot(self.total_nc, label = "Nuevos casos", dashes=[1, 1 ] ) 
        
         
        


class interpolacion :
    
    def __init__(self):
        self.datos = []
        self.datos_inter = []
        #dataframe = pd.read_csv('Casos_Diarios_Estado_Nacional_Confirmados.csv')
        dataframe = pd.read_csv('Casos_Diarios_Estado_Nacional_Confirmados-act.csv')
        #dataframe = pd.read_csv('Casos_Diarios_Estado_Nacional_Defunciones.csv')
    
        print(dataframe.head(10))
        ser = dataframe.iloc[0]
        self.datos = ser.values.tolist()[3:]
        self.diarios = self.datos
        self.datos= list(it.accumulate(self.datos))
        
        print(self.datos, len(self.datos), self.datos[15], self.datos[30])
        #a = list(dataframe[dataframe["nombre"] == "Nacional"])
        #a = dataframe.groupby('FECHA_ACTUALIZACION')['FECHA_INGRESO'].value_counts()

       #a = dataframe.groupby('FECHA_INGRESO').count()
        #print(a)
    def get_interpolacion(self):
        x = 0
        self.datos_inter.append(0)
        self.datos_inter.append(0)
        self.datos_inter.append(0)
        while x < (len(self.datos)-2):
            y0 = self.datos[x]
            y1 = self.datos[x+1]
            y2 = self.datos[x+2]
            x0 = x
            x1 = x+1
            x2 = x+2
            #y  = self.lineal(x+2, p0_x, p0_y, p1_x, p1_y)
            y = self.lagrange(x+3,  x0, y0, x1, y1,  x2, y2 )
            self.datos_inter.append(y)
            x = x +1 
        dd = 70
        x = 50
        while x < dd:
            #print("y",p0_y,x)
            y0 = self.datos[x]
            y1 = self.datos[x+1]
            y2 = self.datos[x+2]
            x0 = x
            x1 = x+1
            x2 = x+2
            #y  = self.lineal(x1+1, x0, y0, x1, y1)
            y = self.lagrange(x+3,  x0, y0, x1, y1,  x2, y2 )
            self.datos.append(y)
            
            x = x +1

    def get_interpolacion_lagrange(self, datosMuestra):
        #datosMuestra = 12
        datosTotales = len(self.datos) + 25
        x0 = 1*datosMuestra // 3
        #x0 = datosMuestra - 3
        x1 = 2*datosMuestra // 3
        #x1 =  datosMuestra - 2
        #x2 =  datosMuestra - 1
        x2 = 3*datosMuestra // 3
        # x es el tercer punto 3//3
        x2 = x2-1
        x = datosMuestra 
        # agrega los primeros elementos
        self.datos_inter = self.datos[:datosMuestra]
        while x < datosTotales :
            """
            y0 = self.datos[x0]
            y1 = self.datos[x1]
            y2 = self.datos[x2]
            
            """
            y0 = self.datos_inter[x0]
            y1 = self.datos_inter[x1]
            y2 = self.datos_inter[x2]
            
            y = self.lagrange(x, x0,y0, x1, y1, x2, y2)
            if x < (len(self.datos)):
                self.datos_inter.append(y)
            else : 
                #self.datos.append(y)
                self.datos_inter.append(y)
            x = x +1
            x0 = x0+1
            x1 = x1 +1 
            x2 = x2 +1 
   
        return self.datos_inter
    def get_interpolacion_lineal(self):
        datosMuestra = 53
        datosTotales = len(self.datos)+25
        x0 = datosMuestra //3
        x0 = datosMuestra - 32
        x1 = x0*2
        x1 =  datosMuestra - 4
        # x es el tercer punto 3//3
        x = datosMuestra
        # agrega los primeros elementos
        self.datos_inter = self.datos[:datosMuestra]
        while x < datosTotales :
            y0 = self.datos[x0]
            y1 = self.datos[x1]
            y  = self.lineal(x, x0,y0, x1, y1)
            if x < (len(self.datos)-1):
                self.datos_inter.append(y)
            else : 
                self.datos.append(y)
                self.datos_inter.append(y)
            x = x +1
            x0 = x0+1
            x1 = x1 +1 
   
        
    def lineal (self, x,  x0, y0, x1, y1):
        """
        #a0=  (x -x_1 )* y0 / (x_0 - x_1)
        a0 = (x - p1_x)* (p0_y/(p0_x-p1_x))
        #a1= (x -x_1 )* y0 / (x_0 - x_1)
        a1 = (x - p0_x)*(p1_y/(p1_x-p0_x))
        """
        a0 = y0
        a1 = (x - x0)*(y1-y0)/(x1-x0)
        return a0 +  a1
    def lagrange(self, x,  x0, y0, x1, y1,  x2, y2):
        
        try:
           
            a0 = (y0*(x-x1)*(x-x2))/((x0-x1)*(x0-x2))
            a1 = (y1*(x-x0)*(x-x2))/((x1-x0)*(x1-x2))
            a2 = (y2*(x-x0)*(x-x1))/((x2-x0)*(x2-x1))

            return a0 + a1 +a2
        except:
            print("eror:",x)
            return None
    def plot(self):

        x = np.arange(0, 60, 1)
        x = x*0.17017
        y = np.exp(x)
        plt.plot( y , label = "log 50")
        x = np.arange(0, 30, 1)
        x = x*(math.log(self.datos[14])/15)
        y = np.exp(x)
        #plt.plot( y, label = "log 15 ")
        x = np.arange(0, 35, 1)
        x = x*(math.log(self.datos[29])/30)
        y = np.exp(x)
        #plt.plot(y, label = "log 30")
        
        plt.plot(self.datos , label = "Contagios covid")
        plt.scatter( range(len(self.datos_inter)) , self.datos_inter, label = "Interpolados covid", s = 1)
        #plt.plot(y  , label = "Interpolados covid")
        plt.ylabel('Individuos')
        plt.xlabel('Días')
        plt.legend()
        plt.title(' Datos interpolados ')
        plt.savefig('books_read.png')
        plt.show()
        #mpld3.show()
inter = interpolacion()
p12 = inter.get_interpolacion_lagrange(12)

inter = interpolacion()
p24 = inter.get_interpolacion_lagrange(24)

inter = interpolacion()
p36 = inter.get_interpolacion_lagrange(26)

#inter = interpolacion()
#p48 = inter.get_interpolacion_lagrange(48)

x = np.arange(0, 60, 1)
x = x*0.17017
y = np.exp(x)
#plt.plot( y , label = "e**(ln8261/53)")
plt.plot( inter.datos[:58] , label = "acumulado covid")
x = range(len(inter.datos_inter)) 
#plt.scatter( x , p12, label = "Datos 12 x_i[8,10,12]", s = .8)
#plt.scatter( x , p24, label = "Datos 24 x_i[16,20,24]", s = .8)
#plt.scatter( x , p36, label = "Datos 36 x_i[24,30,36]", s = .8)
#plt.scatter( x , p48, label = "Datos 48 x_i[32,40,48]", s = .8)

#plt.clf()
#plt.plot( inter.diarios[:60] , label = "nuevo covid")

plt.ylabel('Individuos')
plt.xlabel('Días')
plt.legend()
plt.title(' Datos interpolados ')
plt.savefig('Datos33.png')
plt.show()        
#inter.plot()
