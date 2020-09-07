# -*- coding: utf-8 -*-




def ejecutarbacktest(listaDeVelas):
    
   
    from clasesBacktest import añadirATRListaDeVelas
    import os
    os.chdir('')
    import zigZag
        
    
    añadirATRListaDeVelas(listaDeVelas,14)
    listaSetups = []
        
    #recorremos listaDeVelas buscando escenarios de setup:
    setupVigente= False
    for i in range(700,len(listaDeVelas)):
        listaDeVelasProv = listaDeVelas[(i-700):i]
        velaActual = listaDeVelasProv[-1]
        
        if not setupVigente:
            #buscamos un nuevo setup
            nuevosetup = nuevosetupWolsu3(listaDeVelasProv,1,10)
            
            if nuevosetup.activo:
                listaSetups.append(nuevosetup)
                setupVigente = True
        #IMPORTANTE: falta el caso de que la propia vela que genera un setup sea
        #la misma que genera la orden (vuelve a cerrar por debajo dela linea 1-3)
                
        #falta tambien regenerar el setup si surge otro en la misma direccion, con la nueva lt
        #para ello se debe comprobar aun habiendo un setup vigente si ha surgido uno nuevo, con un pun4 diferente
                
        
        
        if setupVigente:
            #estamos ocupados con un setup
            #metemos la vela nueva en el setup
            #si la vela setup se acaba de activar, se esta metiendo repetida
            novedad = listaSetups[-1].actualizarConNuevaVela(velaActual)
            print (novedad)
        
            if novedad == "nueva orden":
                print (listaSetups[-1].direccion)
                print("ala")
            if novedad == "terminado":
                setupVigente = False
            
        print (100*i/len(listaDeVelas), "%")
        print()
    
    if setupVigente:
        if listaSetups[-1].enMercado:
            listaSetups[-1].cierreForzoso(listaDeVelas[-1])
        else:
            listaSetups.pop()

    
    
    # suma=0
    # num=1
    # for i in listaSetups:
    #     print("Fecha ", i.listaDeVelas[0].fecha)
    #     if not i.orden == "na":
    #         import matplotlib.pyplot as plt
    #         plt.figure(num)
    #         i.plotSetup()
    #         num+=1
    #         res = i.resultadoSetup()
    #         suma+=res
    #     print ()
    # print(len(listaSetups))
    # print()
    # print("Resultado final R ", suma)

 
    return (listaSetups)





def nuevosetupWolsu3 (listaDeVelas, porcentajecambio , profundidad):
    #dando por hecho que listaVelas es una lista que contiene las velas pasadas hasta la actual
    #esta función devuelve un objeto Operacion en caso de entrada
    #en caso de no entraa, devuelve False
    import zigZag
    from Wolsu3.setupclase import setupclase
    
    haySetup =False
    zigZag = zigZag.crearZigZag(listaDeVelas, porcentajecambio , profundidad/2)
    
    #calculamos los inds de las velas de listaVelas que coinciden con max/min en zigZag    
    inds =[]
    for ind in zigZag.keys():
        inds.append(ind)
        
    #definimos los puns del ZigZag que importan
    indAct = len(listaDeVelas)-1
    ind4 = inds[-2]
    ind3 = inds[-3]
    ind2 = inds[-4]
    ind1 = inds[-5]
    
    velaAct = listaDeVelas[len(listaDeVelas)-1]
    pun4 = zigZag[ind4]
    pun3 = zigZag[ind3]
    pun2 = zigZag[ind2]
    pun1 = zigZag[ind1]
    
    #creamos los prámetros del setup supuesto:
    
    
    setupprov = setupclase(False,ind1,ind2,ind3,ind4,indAct,pun1,pun2,pun3,pun4,velaAct.cierre,listaDeVelas\
                           ,porcentajecambio,profundidad)
    #calculamos el punto en el que se encuentra la linea 1-3 actualmente:
    linea13 = setupprov.calcularlinea13()
    
    #comprobamos si estamos por encima de la linea 1-3:
    punAct = 0
    if pun3>pun1 and pun4>pun2 and pun4<pun1:
        #Wolsu alcista
        if velaAct.alto >= linea13:
            #Hay setup alcista
            haySetup = True
            punAct = velaAct.alto
    elif pun3<pun1 and pun4<pun2 and pun4>pun1:
        #Wolsu bajista
        if velaAct.bajo <= linea13:
            #Hay setup bajista
            haySetup = True
            punAct = velaAct.bajo
    
        
    #preparamos el return
    if haySetup:
        print ("Hay un setup")
    else:
        print ("No hay setup")
    
    
    setupfinal = setupclase(haySetup,ind1,ind2,ind3,ind4,indAct,pun1,pun2,pun3,pun4,punAct,listaDeVelas,porcentajecambio,profundidad)
    
    return (setupfinal)


















