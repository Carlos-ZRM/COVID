import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
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
        zeros =  len(self.total_nc) - len(self.total_def)
        zeros = [0]*zeros
        self.total_def= zeros+self.total_def
        #print("len",len(self.total_def), len(self.total_nc))
        
    def graficas_datos(self, opc =1 , dias=1):
        if dias  > len(self.total_nc):
            dias = len(self.total_nc)
        
        fig = Figure(figsize=(16.8 , 6.4),  dpi=60)
        axi = fig.add_subplot(1, 2, 1)
        axi.plot(self.total_def[:dias], label = "Defunciones", dashes=[2, 1,8,2])    
        axi.plot(self.total_nc[:dias], label = "Nuevos casos", dashes=[1, 1 ] ) 
        
        axi.set_xlabel('Días', fontsize=20)
        axi.set_ylabel('Número de casos', fontsize='medium')  
        axi.legend(fontsize=18) 
        
        axis = fig.add_subplot(1, 2, 2)
        axis.plot(self.total_nca[:dias], label = "Acumulado de casos") 
        axis.set_xlabel('Días', fontsize=20)
        axis.set_ylabel('Número de casos', fontsize='medium')  
        axis.legend(fontsize=18) 
        

        return fig 
    def get_datos(self, dias):
        if dias  > len(self.total_nc):
            dias = len(self.total_nc)
        nc = self.total_nc[dias-1]
        nca = self.total_nca[dias-1]
        defu = self.total_def[dias-1]
        return int(nc), int(nca), int(defu)

class interpolacion :
    
    def __init__(self , csv_file ):
        self.datos = []
        self.datos_inter = []
        #dataframe = pd.read_csv('Casos_Diarios_Estado_Nacional_Confirmados.csv')
        #dataframe = pd.read_csv('Casos_Diarios_Estado_Nacional_Defunciones.csv')
        dataframe = pd.read_csv(csv_file)
        print(dataframe.head(10))
        ser = dataframe.iloc[0]
        self.datos = ser.values.tolist()[3:]
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
def flask( numDatos):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    inter = interpolacion('Casos_Diarios_Estado_Nacional_Confirmados.csv')
    pdia = inter.get_interpolacion_lagrange(int(numDatos))

    inter = interpolacion('Casos_Diarios_Estado_Nacional_Confirmados.csv')
    p12 = inter.get_interpolacion_lagrange(12)

    inter = interpolacion('Casos_Diarios_Estado_Nacional_Confirmados.csv')
    p24 = inter.get_interpolacion_lagrange(24)

    inter = interpolacion('Casos_Diarios_Estado_Nacional_Confirmados.csv')
    p36 = inter.get_interpolacion_lagrange(26)

    inter = interpolacion('Casos_Diarios_Estado_Nacional_Confirmados.csv')
    p48 = inter.get_interpolacion_lagrange(48)


    x = np.arange(0, 60, 1)
    x = x*0.17017
    y = np.exp(x)
    axis.plot( y , label = "e**(ln8261/53)")
    axis.plot( inter.datos , label = "Muertos covid")
    x = range(len(inter.datos_inter)) 
    axis.scatter( x , pdia, label = "Datos "+numDatos, s = .8)
    
    """
    axis.scatter( x , p12, label = "Datos 12 x_i[8,10,12]", s = .8)
    axis.scatter( x , p24, label = "Datos 24 x_i[16,20,24]", s = .8)
    axis.scatter( x , p36, label = "Datos 36 x_i[24,30,36]", s = .8)
    axis.scatter( x , p48, label = "Datos 48 x_i[32,40,48]", s = .8)
    """
    #fig.ylabel('Individuos')
    #fig.xlabel('Días')
    #fig.legend()
    #fig.title('Interpolación de los datos confirmados')
    #plt.savefig('Datos33.png')
    #plt.show()
    return fig        
#inter.plot()

"""
csv = datos()
nc_csv, nca_csv, defu_csv = csv.get_datos( dias=50)
print(nc_csv, nca_csv, defu_csv)
plt.show()

"""