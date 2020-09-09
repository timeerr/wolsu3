# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:45:33 2019

@author: timee
"""
class Backtest:
    
    def __init__(self,listaDeOperaciones):
        self.listaDeOperaciones = listaDeOperaciones
        self.listaAcc = []
        capinicial = int(input("cual es el capital inicial? :  "))
        suma = capinicial
        numOp=0
        draw = 0
        self.listaDraw = []
        for operacion in self.listaDeOperaciones:
            suma= suma + operacion.resultadoPips()
            self.listaAcc.append(suma)
            numOp = numOp + 1
            
            draw = (suma/max(self.listaAcc))-1
            self.listaDraw.append(draw)
        
    def resultados (self):
        suma=0
        numOp=0
        for operacion in self.listaDeOperaciones:
            suma= suma + operacion.resultadoPips()
            numOp += 1
            print()
            print()
            print("Operacion ",numOp)
            print()
            print(" Fecha: ", operacion.velaApertura.fecha)
            print()
            print(" Abierta en " , operacion.velaApertura.cierre)
            print(" Cerrada en ", operacion.velaCierre.cierre)
            print (" Resultado ", operacion.resultadoPips())
    

        print()
        print()
        print("Resultado Total: " , round(suma) , " pips")
    
    def graficoEquidad (self):
        import matplotlib.pyplot as plt 
        #preparamos gráficos resultados
        x= range(len(self.listaAcc))
        y= self.listaAcc
        plt.plot (x,y)
        plt.xlabel("Operaciones")
        plt.ylabel("Acc")
        plt.title("Equidad")
        
        plt.show()
        
    def drawdownMaximo (self):
        import matplotlib.pyplot as plt 
        x= range(len(self.listaDraw))
        y= self.listaDraw
        plt.plot (x,y)
        plt.xlabel("Operaciones")
        plt.ylabel("")
        plt.title("Drawdown")
        print()
        print("El máximo drawdown es de : " , round((100*min(self.listaDraw))) , "%" )










class Vela:
    
    def __init__(self,fecha,apertura,alto,bajo,cierre):
        
        self.fecha=fecha
        self.alto=float(alto)
        self.bajo=float(bajo)
        self.apertura=float(apertura)
        self.cierre=float(cierre)
        self.atr= "na"
        self.bbmedio= "na"
    
    def definirHora (self, numhora, numminuto):
        from datetime import datetime
        self.hora=  datetime(hour=numhora,minute=numminuto)
    def definirEma10 (self,ema10):
        self.ema10=ema10
    def definirEma20 (self,ema20):
        self.ema20=ema20
    def definirRsi (self,rsi):
        self.rsi=rsi
    def definirATR (self,atr):
        self.atr=float(atr)
    def definirBB(self,alto,bajo,medio):
        self.bbalto=alto
        self.bbbajo=bajo
        self.bbmedio= medio
    
    def imprimirVela(self):
        print ("Vela:")
        print ("Fecha: ", self.fecha)
        print ("Apertura: ", self.apertura)
        print ("Alto: ", self.alto)
        print ("Bajo: ", self.bajo)
        print ("Cierre: ", self.cierre)
        print ('ATR: ', self.atr)
        print()
        





#class ListaDeVelas:
#    
#    def __init__(self):
#        self.listadevelas = []
#    
#    def añadirVela (self,vela):
#        self.listadevelas.append()


def crearListaDeVelas (archivocsv):
    listaDeVelas = []
    import csv
   
    
    with open (archivocsv, 'r') as archivo:
        
       lectorLinea = csv.reader(archivo, delimiter = ',', quotechar = "\"")
       
       
       numlinea=-1
       for linea in lectorLinea:
           numlinea+=1
           
           if numlinea==0:
               continue
           
           
#          nuevaVela = Vela(datetime.fromtimestamp(int(linea[0])),float(linea[1]),float(linea[2]),float(linea[3]),float(linea[4]))
           nuevaVela = Vela(linea[0],float(linea[1]),float(linea[2]),float(linea[3]),float(linea[4]))
   
           listaDeVelas.append(nuevaVela)
    
    return listaDeVelas
    print ("Archivo csv procesado")
    

def imprimirlistaDeVelas (listaDeVelas):
    import matplotlib.pyplot as plt
    
    x=[]
    y=[]
    cont=0
    for vela in listaDeVelas:
        # x.append(cont)
        # x.append(vela.fecha.time())
        x.append(vela.fecha)
        # x.append(vela.fecha.isoformat())
        cont+=1
        y.append(vela.cierre)
        
    
    plt.plot (x,y, 'b', label= 'Precio')
    plt.xticks(rotation = 45)
    plt.xlabel("Op")
    plt.ylabel("")
    plt.title("Gráfico")
    #plt.xticks([])
    plt.show()

def imprimirlistaDeVelasBB (listaDeVelas):
    import matplotlib.pyplot as plt
    
    x=[]
    bbsmedio= []
    bbsalto = []
    bbsbajo= []
    y=[]
    cont=0
    for vela in listaDeVelas:
        # x.append(cont)
        # x.append(vela.fecha.time())
        x.append(vela.fecha)
        if vela.bbmedio!= "na":
            bbsmedio.append(vela.bbmedio)
            bbsalto.append(vela.bbalto)
            bbsbajo.append(vela.bbbajo)
        else:
            bbsmedio.append(vela.cierre)
            bbsalto.append(vela.cierre)
            bbsbajo.append(vela.cierre)
        # x.append(vela.fecha.isoformat())
        cont+=1
        y.append(vela.cierre)
        
    
    plt.plot (x,y, 'b', label= 'Precio')
    plt.plot (x,bbsmedio)
    plt.plot (x,bbsalto)
    plt.plot (x,bbsbajo)
    plt.xticks(rotation = 45)
    plt.xlabel("Op")
    plt.ylabel("")
    plt.title("Gráfico")
    #plt.xticks([])
    plt.show()

def añadirATRListaDeVelas (listaDeVelas,valorATR):
    cont=0
    sum=0
    for vela in listaDeVelas:
        #calculamos el rango verdadero
        if cont==0:
            rangoverdadero = abs(vela.alto-vela.bajo)
        else:
            velaAnterior = listaDeVelas[cont-1]
            rangoverdadero = max((vela.alto-vela.bajo),(vela.alto-velaAnterior.cierre),(velaAnterior.cierre-vela.bajo))
        
        
        sum+=rangoverdadero
        
        if cont==valorATR:
            #media de los rangosverdaderos
            atr = float(round(sum/valorATR,5))
            listaDeVelas[cont].definirATR(atr)
        elif cont>valorATR:
            atr = float(round((velaAnterior.atr*13+rangoverdadero)/valorATR,5))
            listaDeVelas[cont].definirATR(atr)
        
        
        cont+=1

def añadirBBListaDeVelas (listaDeVelas,longitud,numdesvest):
    """

    Parameters
    ----------
    listaDeVelas : lista
        lista que contiene todas las velas.
    longitud : int
        longitud de la media móvil.
    desvest : int
        desviación estándar para las bandas.

    Returns
    -------
    modifica listadevelas con un nuevo atributo en las velas, BB con valores de alto bajo y medio.

    """
    from statistics import mean
    from statistics import stdev
    
    cont=0
    ult= []
    for vela in listaDeVelas:
        cont+=1
        if cont<longitud+1:
            ult.append(vela.cierre)
            continue
        
        ma = mean(ult)
        desv = numdesvest*stdev(ult)
        (alto,bajo)= (ma+desv,ma-desv)
        vela.definirBB(alto,bajo,ma)
        
        
        ult= ult[1:]
        ult.append(vela.cierre)
        
        
        
    
    

    



class Operacion:
    
    def __init__ (self, tipo):
        
        
        if tipo in ("buy", "sell"):
            self.tipo = tipo
        else:
            self.tipo = "NaN"
            print("No se ha podido iniciar correctamente la Operación. Especifique si es buy o sell")
    

    def añadirPrecioApertura (self, precioapertura):
        self.precioapertura = precioapertura
    
    def añadirPrecioCierre (self, preciocierre):
        self.preciocierre = preciocierre
    
    def añadirSL (self,sl):
        self.sl = sl
    
    def definirSLinicial(self,slinicial):
        self.slinicial = slinicial
    
    def añadirTP (self,tp):
        self.tp = tp

    def abrirOp (self,vela):
        self.velaApertura = vela
        self.precioapertura = vela.cierre
    def cerrarOp (self, vela):
        self.velaCierre = vela
        self.preciocierre = vela.cierre
        
    def resultadoPips (self):
        resta = float(self.precioapertura - self.preciocierre)
        if self.tipo == "buy":
            resta = (-1)*resta
        
        #comprobamos si es un yen, y lo pasamos a pips
        if self.preciocierre>50:
            res= resta*100
        else:
            res=resta*10000
        return (round(res))
    
    def resultadoR (self):
        if self.preciocierre<50:
            return(round(self.resultadoPips()/(10000*abs(self.precioapertura-self.slinicial)),2))
        else:
           return(round(self.resultadoPips()/(100*abs(self.precioapertura-self.slinicial)),2)) 
       
        
