# -*- coding: utf-8 -*-

class setupclase:
    
    from clasesBacktest import Operacion
    
    def __init__(self,activo,ind1,ind2,ind3,ind4,indAct,pun1,pun2,pun3,pun4,punAct,listaDeVelas,porcentajecambio,profundidad):
        
        self.ind1 = ind1
        self.ind2 = ind2
        self.ind3 = ind3
        self.ind4 = ind4
        self.ind5 = indAct
        self.indAct = indAct
        
        self.pun1 = pun1
        self.pun2 = pun2
        self.pun3 = pun3
        self.pun4 = pun4
        self.pun5 = punAct
        self.punAct = punAct
        
        self.activo = activo
        
        self.listaDeVelas = listaDeVelas
        self.porcentajecambio = porcentajecambio
        self.profundidad= profundidad
        
        self.orden = "na"
        self.ordenVigente = False
        self.enMercado = False
        self.slabe = False
        self.preciocierre = "NA"
        
        if pun1<pun3:
            self.direccion = "alcista"
        else:
            self.direccion = "bajista"
    
    def calcularlinea13(self):
        
        return((((self.indAct-self.ind1)*(self.pun3-self.pun1))/(self.ind3-self.ind1))+self.pun1)

    def hayOrden(self):
        hayOrden = False
        if self.direccion == "alcista":
            if self.listaDeVelas[-1].cierre < self.calcularlinea13():
                #tenemos orden
                hayOrden = True
        if self.direccion == "bajista":
            if self.listaDeVelas[-1].cierre > self.calcularlinea13():
                hayOrden = True
        
        return (hayOrden)
    
    def calcularOrdenWolsu3(self):
        #crea la clase operacion asociada al setup, junto con los parámetros de entrada
        from clasesBacktest import Operacion
        
        if self.direccion == "alcista":
            self.orden = Operacion("sell")
            precioapertura = (self.listaDeVelas[-1].cierre)-(2*(float(self.listaDeVelas[-1].atr)))
            
            precioSL = (abs(self.pun5-precioapertura)*0.786)+precioapertura
            self.orden.añadirSL(precioSL)
            self.orden.definirSLinicial(precioSL)
            
            precioTP = precioapertura-(abs(precioSL-precioapertura)*2)
            self.orden.añadirTP(precioTP)
            
            self.orden.añadirPrecioApertura(precioapertura)
        
        
        elif self.direccion == "bajista":
            self.orden = Operacion ("buy")
            precioapertura = self.listaDeVelas[-1].cierre+(2*self.listaDeVelas[-1].atr)
            
            precioSL = precioapertura-(abs(self.pun5-precioapertura)*0.786)
            self.orden.añadirSL(precioSL)
            self.orden.definirSLinicial(precioSL)
            
            precioTP = precioapertura +(abs(precioSL-precioapertura)*2)
            self.orden.añadirTP(precioTP)
            
            self.orden.añadirPrecioApertura(precioapertura)
        
        else:
            print ("No se ha podido calcular la orden, ya que el setup no está bien definido")
        
        
            
    def calcularPrecio1RWolsu3(self):
        if self.orden.tipo == "buy":
            precio1R = self.orden.precioapertura+(abs(self.orden.slinicial-self.orden.precioapertura))
        if self.orden.tipo == "sell":
            precio1R = self.orden.precioapertura-(abs(self.orden.precioapertura-self.orden.slinicial))
        
        return (precio1R)

    def calcularPrecioBEWolsu3(self):
        if self.orden.tipo == "buy":
            preciobe = self.orden.precioapertura+(abs(self.orden.sl-self.orden.precioapertura)*0.2)
        if self.orden.tipo == "sell":
            preciobe = self.orden.precioapertura-(abs(self.orden.precioapertura-self.orden.sl)*0.2)
        
        return (preciobe)
    
    def hayPunto5(self):
        if self.direccion == "alcista" and self.listaDeVelas[-1].alto > self.pun5:
            return (True)
        if self.direccion == "bajista" and self.listaDeVelas[-1].bajo < self.pun5:
            return (True)
        return (False)
    
    def actualizarPunto5(self):
        if self.direccion=="alcista":
            self.pun5=self.listaDeVelas[-1].alto
            self.ind5=len(self.listaDeVelas)-1
        elif self.direccion=="bajista":
            self.pun5=self.listaDeVelas[-1].bajo
            self.ind5=len(self.listaDeVelas)-1
        
    def actualizarConNuevaVela(self,vela):
        from zigZag import crearZigZag
        
        self.listaDeVelas.append(vela)
        self.indAct = len(self.listaDeVelas)-1
        
        zigzagdesdeelsetup = crearZigZag(self.listaDeVelas[self.ind5:], self.porcentajecambio, self.profundidad/2)
        if not self.ordenVigente and len(zigzagdesdeelsetup)>=7:
            self.activo= False
            print ("orden cancelada, ha pasado demasiado tiempo desde el setup")
            return ("terminado")
        
        if not self.enMercado:
            #no estamos en mercado
            if self.ordenVigente:
                #si hay orden, buscamos si hemos de entrar o de actualizarla
                if self.hayPunto5():
                    #nuevo punto 5
                    self.orden = "na"
                    self.ordenVigente = False
                    self.actualizarPunto5()
                    return("nuevo punto 5 para la orden")
                elif self.orden.precioapertura >= vela.bajo and self.orden.precioapertura <=vela.alto:
                    #estamos dentro:
                    self.enMercado = True
                    return("estamos dentro")
                
                
            #Sin orden vigente, buscamos cierre linea13    
            else:  
                hayOrden = self.hayOrden()
                
                if hayOrden:
                    self.ordenVigente =  True
                    self.calcularOrdenWolsu3()
                    return("nueva orden")
                
                
                elif self.hayPunto5():
                    self.actualizarPunto5()
                    return ("nuevo punto 5 para el setup")
                    print()
                    
        if self.enMercado:
            #estamos en mercado
            if self.orden.sl>= vela.bajo and self.orden.sl<=vela.alto:
                #se tocó el sl
                self.orden.añadirPrecioCierre(self.orden.sl)
                self.activo = False
                self.ordenVigente = False
                if self.slabe:
                    print("Cerrado BE")
                else:
                    print("Cerrado SL")
                
                return ("terminado")
            
            
            #sl a be
            precio1R = self.calcularPrecio1RWolsu3()
            if precio1R>=vela.bajo and precio1R<=vela.alto and self.slabe==False:
                #mover SL a BE
                preciobe = self.calcularPrecioBEWolsu3()
                self.orden.añadirSL(preciobe)
                self.slabe = True
                
            #tp
            if self.orden.tp<=vela.alto and self.orden.tp>=vela.bajo:
                #se tocó el tp
                self.orden.añadirPrecioCierre(self.orden.tp)
                self.activo = False
                self.ordenVigente = False
                print("Cerrado TP")
                
                return ("terminado")
         
      
    def plotSetup (self):
        import zigZag
        import matplotlib.pyplot as plt
        import os
        os.chdir('C:\\Users\\timee\\Google Drive\\Development\\Trading')
        
        
        if not self.orden=="na":
            plt.text(self.indAct-10, self.orden.tp, "-------"+str(self.orden.tp)+"---------", color= 'g')
            plt.text(self.indAct-10, self.orden.slinicial, "------"+str(self.orden.slinicial)+"----------", color= 'r')
            plt.text(self.indAct-10, self.orden.precioapertura, "-------"+str(self.orden.precioapertura)+"---------", color= 'y')
            if self.slabe:
                plt.text(self.indAct-10,self.orden.sl, "-----------be--------------")
            
            #imprimir zona 1R
            plt.text(self.indAct-10,self.calcularPrecio1RWolsu3(), "-----------1R--------------")
            
            plt.text(self.ind1,self.pun1,'1: '+str(self.pun1))
            plt.text(self.ind2,self.pun2,'2: '+str(self.pun2))
            plt.text(self.ind3,self.pun3,'3: '+str(self.pun3))
            plt.text(self.ind4,self.pun4,'4: '+str(self.pun4))
            plt.text(self.ind5,self.pun5,'5: '+str(self.pun5))
            
            plt.text(self.indAct*0.98,self.pun5*1.015,"Resultado"+ str(self.orden.resultadoR()),fontsize=12)
            
        
        linea13lt = []
        for i in range(self.ind1,self.indAct):
            pun = (((i-self.ind1)*(self.pun3-self.pun1))/(self.ind3-self.ind1))+self.pun1
            linea13lt.append(pun)
        plt.plot(range(self.ind1,self.indAct), linea13lt)
        
        
        zigzag = zigZag.crearZigZag(self.listaDeVelas,1,10)
        zigZag.plotZigZag(zigzag, self.listaDeVelas) 
        
        print ("El setup tiene las siguientes carácterísticas")
        print (self.orden.tipo)
        print ("Cerrado en el dia : ", self.listaDeVelas[-1].fecha)
        print()
        print("Precio de entrada: ", self.orden.precioapertura)
        print("Precio de SL: ", self.orden.sl)
        print()
        print ("Punto 1 en vela : ",self.ind1," a precio ", self.pun1)
        print ("Punto 2 en vela : ",self.ind2, " a precio ", self.pun2)
        print ("Punto 3 en vela : ",self.ind3, " a precio ", self.pun3)
        print ("Punto 4 en vela : ",self.ind4, " a precio ", self.pun4)
        print ("Punto 5 en vela : ",self.ind5, " a precio ", self.pun5)
    
    def cierreForzoso(self,vela):
        self.orden.añadirPrecioCierre(vela.cierre)
    
    def resultadoSetup(self):
        if self.orden=="na":
            return (0.00)
        else:
            return (self.orden.resultadoR())
        