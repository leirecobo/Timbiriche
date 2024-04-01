###########################################################
###########################################################

# FUNCIONES AUXILIARES


def acabado(Tablero):
    MH=Tablero[0]
    MV= Tablero[1]
    for matriz in [MH,MV]:
        for lista in matriz:
            for elemento in lista:
                if elemento==0:
                    
                    return False
    return True

def existe(Matriz, indice):
    i=indice[0]
    j=indice[1]
    n=len(Matriz)
    m=len(Matriz[0])
    if 0<= i<= n-1 and 0<=j<=m-1:
        return True
    else:
        return False

def PuntoGanado(Nodo, Tablero):
    (k,x,y)=Nodo
    MH =Tablero[0]
    MV = Tablero[1]
    Cerrados=[]
    Punto=False
   
    if k==0: #horizontalak, goiko karratua
        if existe(MH,(x-1,y)) and existe(MV, (y,x-1)) and existe(MV, (y+1,x-1)):
            if MH[x-1][y]>0 and MV[y][x-1]>0 and MV[y+1][x-1]>0:
                Punto=True
                Cerrados.append((x-1,y))
            #horizontalak, beheko karratua
        if existe(MH, (x+1,y)) and existe(MV, (y,x)) and existe(MV, (y+1,x)):
            if MH[x+1][y]>0 and MV[y][x]>0 and MV[y+1][x]>0:
                Punto=True
                Cerrados.append((x,y))
    else:
            #bertikala, eskumako karratua
        if existe(MH, (y,x-1)) and existe(MH, (y+1, x-1)) and existe(MV, (x-1,y)):
            if MH[y][x-1]>0 and MH[y+1][x-1]>0 and MV[x-1][y]>0:
                Punto=True
                Cerrados.append((y,x-1))
            #bertikala, ezkerreko karratua
        if existe(MH, (y,x)) and existe(MH, (y+1,x)) and existe(MV, (x+1,y)):
            if MH[y][x]>0 and MH[y+1][x]>0 and MV[x+1][y]>0:
                Punto=True
                Cerrados.append((y,x))
    return (Punto, Cerrados)
        
def MovimientosPosibles(Tablero):

    solucion = []
    for k in [0,1]:
        Matriz = Tablero[k]
        for i in range(len(Matriz)):
            for j in range(len(Matriz[0])):
                if Matriz[i][j]==0:
                    solucion.append((k,i,j))
    return solucion
                    

###########################################################
###########################################################

# FUNCIONES DE EVALUACION


def eval1(Tablero):
    MatrizPuntos = Tablero[2]
    Punto1=0
    for lista in MatrizPuntos:
        for elemento in lista:
            if elemento == 1:
                Punto1 += 1
    return Punto1

def eval2(Tablero):
    MatrizPuntos = Tablero[2]
    Punto2=0
    for lista in MatrizPuntos:
        for elemento in lista:
            if elemento == 2:
                Punto2 -= 1
    return Punto2

def eval3(Tablero):
    MatrizPuntos= Tablero[2]
    Punto1=0
    Punto2=0
    for lista in MatrizPuntos:
        for elemento in lista:
            if elemento==1:
                Punto1+=1
            elif elemento ==2:
                Punto2+=1
                
    return Punto1-Punto2


###########################################################
###########################################################

# FUNCION PRINCIPAL: MINIMAX

def GeneralMax(Tablero, N, neval):
    if N==0 or acabado(Tablero)==True:
        #print("\n\n")
        if neval == 1:
            return None, eval1(Tablero)
        elif neval == 2:
            return None,eval2(Tablero)
        else: 
            return None,eval3(Tablero)
    else:
        maximo=float("-inf")
        for sucesor in MovimientosPosibles(Tablero):
            (k,i,j)=sucesor
            (Punto,Cerrados)=PuntoGanado(sucesor,Tablero)
            
            if Punto:
                for celda in Cerrados:
                    Tablero[2][celda[0]][celda[1]]=1
                Tablero[k][i][j]=1
                valor=GeneralMax(Tablero,N-1,neval)[1]
                #print(sucesor,valor,"\n",tablero_a_str(Tablero))
                for celda in Cerrados:
                    Tablero[2][celda[0]][celda[1]]=0
                Tablero[k][i][j]=0

            else:
                Tablero[k][i][j]=1
                valor=GeneralMin(Tablero,N-1,neval)[1]
                #print(sucesor,valor,"\n",tablero_a_str(Tablero))
                Tablero[k][i][j]=0
                
            if valor>maximo:
                maximo=valor
                jugada=sucesor
                
        return (jugada,maximo)



def GeneralMin(Tablero, N,neval):
    if N==0 or acabado(Tablero)==True:
        #print("\n\n")
        if neval == 1:
            return None, eval1(Tablero)
        elif neval == 2:
            return None,eval2(Tablero)
        else: 
            return None,eval3(Tablero)
    else:
        minimo=float("inf")
        for sucesor in MovimientosPosibles(Tablero):
            (k,i,j)=sucesor
            (Punto,Cerrados)=PuntoGanado(sucesor,Tablero)
            if Punto:
                for celda in Cerrados:
                    Tablero[2][celda[0]][celda[1]]=2
                Tablero[k][i][j]=2
                valor=GeneralMin(Tablero,N-1,eval)[1]
                #print(sucesor,valor,"\n",tablero_a_str(Tablero))
                for celda in Cerrados:
                    Tablero[2][celda[0]][celda[1]]=0
                Tablero[k][i][j]=0
            else:
                Tablero[k][i][j]=2
                valor=GeneralMax(Tablero,N-1,neval)[1]
                #print(sucesor,valor,"\n",tablero_a_str(Tablero))
                Tablero[k][i][j]=0
            if valor<minimo:
                minimo=valor
                jugada=sucesor
        return (jugada,minimo)


###########################################################
###########################################################

# FUNCION PRINCIPAL: AlphaBeta

def AlphaBeta(tablero, N,neval, Turno=1, alpha=float("-inf"), beta=float("inf")):
    if N==0 or acabado(tablero)==True:
        if neval == 1:
            return None, eval1(tablero)
        elif neval == 2:
            return None,eval2(tablero)
        else: 
            return None,eval3(tablero)
    else:
        
        if Turno==1:
            alpha=float("-inf")
            for sucesor in MovimientosPosibles(tablero):
                (k,i,j) = sucesor
                (Punto,Cerrados)=PuntoGanado(sucesor,tablero)
                tablero[k][i][j]=1
                if Punto==True:
                    for celda in Cerrados:
                        tablero[2][celda[0]][celda[1]]=1
                    jugada,a = AlphaBeta(tablero,N-1,neval,1,alpha,beta)
                    if a > alpha:
                        alpha=a
                        mjugada = sucesor
                    for celda in Cerrados:
                        tablero[2][celda[0]][celda[1]]=0
                else:
                    jugada,a = AlphaBeta(tablero,N-1,neval,0,alpha,beta)
                    if a > alpha:
                        alpha=a
                        mjugada = sucesor
                tablero[k][i][j]=0
                if beta<=alpha:
                    break
            return mjugada,alpha
        else:
            beta=float("inf")
            for sucesor in MovimientosPosibles(tablero):
                (k,i,j) = sucesor
                (Punto,Cerrados)=PuntoGanado(sucesor,tablero)
                tablero[k][i][j]=2
                if Punto==True:
                    for celda in Cerrados:
                        tablero[2][celda[0]][celda[1]]=2
                    jugada,b = AlphaBeta(tablero,N-1,neval,0,alpha,beta)
                    if b < beta:
                        beta=b
                        mjugada = sucesor
                    for celda in Cerrados:
                        tablero[2][celda[0]][celda[1]]=0
                else:
                    jugada,b = AlphaBeta(tablero,N-1,neval,1,alpha,beta)
                    if b < beta:
                        beta=b
                        mjugada = sucesor
                tablero[k][i][j]=0
                if beta<=alpha:
                    break
            return mjugada,beta


###########################################################
###########################################################

# PROGRAMAS PARA ESCRIBIR



from colorama import Fore

def tablero_a_str(tablero):
    n = len(tablero[0][0])
    # n da gelaxka kopurua. nx(n+1)-eko matrizeak dira MH eta MV
    MH = tablero[0]
    MV = tablero[1]
    X = tablero[2]
    string = Fore.BLACK+"_"*(8*n+5)+"\n"
    string += "|"+" "*(8*n+3)+"|\n"
    for i in range(n):
        # Hacer línea de asteriscos
        linea1 = Fore.BLACK+"| "
        linea2 = Fore.BLACK+"| "
        linea3 = Fore.BLACK+"| "
        for j in range(n):
            # Creamos la linea de asteriscos
            linea1 += Fore.WHITE+"#"
            arista = MH[i][j]
            if arista == 1:
                linea1 += Fore.RED+" * * * "
            elif arista == 2:
                linea1 += Fore.BLUE+" * * * "
            else:
                linea1 +="       "
                
            # Creamos las lineas de columnas de asteriscos
            relleno = X[i][j]
            arista = MV[j][i]
            if arista == 1:
                linea2 += Fore.RED+"*       "
                if relleno == 1:
                    linea3 += Fore.RED+"*   X   "
                elif relleno == 2:
                    linea3 += Fore.RED+"*   "+Fore.BLUE+"X   "
                else:
                    linea3 += Fore.RED+"*       "
            elif arista == 2:
                linea2 += Fore.BLUE+"*       "
                if relleno == 1:
                    linea3 += Fore.BLUE+"*   "+Fore.RED+"X   "
                elif relleno == 2:
                    linea3 += Fore.BLUE+"*   X   "
                else:
                    linea3 += Fore.BLUE+"*       "
            else:
                linea2 += "        "
                if relleno == 1:
                    linea3 += Fore.RED+"    X   "
                elif relleno == 2:
                    linea3 += Fore.BLUE+"    X   "
                else:
                    linea3 += "        "
        # ultimo caracter de cada liena
        linea1 += Fore.WHITE+"#"+Fore.BLACK+" |"+"\n"
        arista = MV[-1][i]
        if arista == 1:
            linea2 += Fore.RED+"*"+Fore.BLACK+" |"+"\n"
            linea3 += Fore.RED+"*"+Fore.BLACK+" |"+"\n"
        elif arista == 2:
            linea2 += Fore.BLUE+"*"+Fore.BLACK+" |"+"\n"
            linea3 += Fore.BLUE+"*"+Fore.BLACK+" |"+"\n"
        else:
            linea2 += Fore.BLACK+"  |"+"\n"
            linea3 += Fore.BLACK+"  |"+"\n"
        string += linea1 + linea2 + linea3 + linea2
    # Creamos ultima linea
    string += Fore.BLACK+"| "
    for j in range(n):
        string += Fore.WHITE+"#"
        arista = tablero[0][-1][j]
        if arista == 1:
            string += Fore.RED+" * * * "
        elif arista == 2:
            string += Fore.BLUE+" * * * "
        else:
            string += "       "
    string += Fore.WHITE+"#"+Fore.BLACK+" |"+"\n"
    string += Fore.BLACK+"|"+"_"*(8*n+3)+"|\n"
    return string


def escribir_coordenadas(n):
    print("Escribimos las coordenadas en el orden k, i, j; en horizontal de izquierda a derecha y en vertical de arriba abajo.\n")
    
    string = ""
    for i in range(n):
        # Hacer línea de asteriscos
        linea1 = ""
        linea2 = ""
        linea3 = ""
        linea4 = ""
        for j in range(n):
            # Creamos la linea de asteriscos
            linea1 += Fore.WHITE+"#"
            linea1 += Fore.BLACK+' 0'+","+str(i)+","+str(j)+" "
            linea2 += Fore.BLACK+'1'+"       "
            linea3 += Fore.BLACK+str(j)+"       "
            linea4 += Fore.BLACK+str(i)+"       "
        # ultimo caracter de cada liena
        linea1 += Fore.WHITE+"#"+"\n"
        linea2 += Fore.BLACK+"1"+"\n"
        linea3 += Fore.BLACK+str(n)+"\n"
        linea4 += Fore.BLACK+str(i)+"\n"
        string += linea1 + linea2 + linea3 + linea4
    # Creamos ultima linea
    for j in range(n):
        string += Fore.WHITE+"#"
        string += Fore.BLACK+' 0'+","+str(n)+","+str(j)+" "
    string += Fore.WHITE+"#"
    print(string)


###########################################################
###########################################################

# FUNCIONES AUXILIARES PARA JUGAR

def pedir_coordenadas(n,tablero):
    k = input("k:\t")
    while k!='0' and k!='1':
        print("El caracter insertado debe ser 0 o 1. Vuelve a intentarlo.")
        k = input("k:\t")
    k = int(k)
    valido = False
    while not(valido):
        i = input("i:\t")
        if i.isnumeric():
            i = int(i)
            if i>=0 and i<=n-1:
                valido = True
                continue
        print("Para obtener un índice válido insertar un número entre 0 y ",n-1)
    valido = False
    while not(valido):
        j = input("j:\t")
        if j.isnumeric():
            j = int(j)
            if j>=0 and j<=n-2:
                valido = True
                continue
        print("Para obtener un índice válido insertar un número entre 0 y ",n-2)

    while tablero[k][i][j]>0:
        print("Esa arista ya está ocupada. Vuelve a intentarlo.")
        k = input("k:\t")
        while k!='0' and k!='1':
            print("El caracter insertado debe ser 0 o 1. Vuelve a intentarlo.")
            k = input("k:\t")
        k = int(k)
        valido = False
        while not(valido):
            i = input("i:\t")
            if i.isnumeric():
                i = int(i)
                if i>=0 and i<=n-1:
                    valido = True
                    continue
            print("Para obtener un índice válido insertar un número entre 0 y ",n-1)
        valido = False
        while not(valido):
            j = input("j:\t")
            if j.isnumeric():
                j = int(j)
                if j>=0 and j<=n-2:
                    valido = True
                    continue
            print("Para obtener un índice válido insertar un número entre 0 y ",n-2)
    return k,i,j

def inicializar_parametros_mVSj():
    print("A continuación, escribe un número del 1 al 5 para ajustar la dificultad:")
    print("\t1: principiante")
    print("\t2: fácil")
    print("\t3: intermedio")
    print("\t4: difícil")
    print("\t5: experto")
    print()
    
    valido = False
    while not(valido):
        difi = input("Selecciona un número:\t")
        if difi.isnumeric():
            difi = int(difi)
            if difi>=1 and difi<=5:
                valido = True
                continue
        print("Para seleccionar una opción válida escibe un número del 1 al 5.")

    print()
    print("Has seleccionado dificultad ", end="")
    if difi == 1:
        print("'principiante'")
    elif difi == 2:
        print("'fácil'")
    elif difi == 3:
        print("'intermedio'")
    elif difi == 4:
        print("'difícil'")
    else:
        print("'experto'")
        
    # podemos hacer difi = difi * k para q sea más jodido, difi = difi + k
    difi = difi*2
    
    print()
    
    print("A continuación, escribe un número del 3 al 10 para ajustar el tamaño de la cuadrícula:")
    
    valido = False
    while not(valido):
        n = input("Selecciona un número:\t")
        if n.isnumeric():
            n = int(n)
            if n>=3 and n<=10:
                valido = True
                continue
        print("Para seleccionar una opción válida escibe un número del 3 al 10.")
    
    print()
    print("Selecciona según qué criterio va a jugar la máquina.\n")
    print("Las funciones de evaluación son las siguientes:")
    print("\t1: mira el caso en el que haga más puntos.")
    print("\t2: busca que el otro haga el menos número de puntos posibles.")
    print("\t3: busca que tu puntuación diste de la de tu rival.")
    neval = input("\nSelecciona un número:\t")
    while not(neval in {"1","2","3"}):
        neval = input("El número introducido no es 1, 2 o 3. Prueba de nuevo:\t")
    return difi,n,int(neval)



def inicializar_parametros_mVSm():
    print("Escribe un número del 3 al 10 para ajustar el tamaño de la cuadrícula:")
    valido = False
    while not(valido):
        n = input("Selecciona un número:\t")
        if n.isnumeric():
            n = int(n)
            if n>=3 and n<=10:
                valido = True
                continue
        print("Para seleccionar una opción válida escibe un número del 3 al 10.")
    print()
    print("Selecciona el nivel de dificultad según el que se va a regir Máquina1")
    print("\t1: principiante")
    print("\t2: fácil")
    print("\t3: intermedio")
    print("\t4: difícil")
    print("\t5: experto")
    print()
    valido = False
    while not(valido):
        difi1 = input("Selecciona un número:\t")
        if difi1.isnumeric():
            difi1 = int(difi1)
            if difi1>=1 and difi1<=5:
                valido = True
                continue
        print("Para seleccionar una opción válida escibe un número del 1 al 5.")
    print()
    print("Selecciona el nivel de dificultad según el que se va a regir Máquina2")
    valido = False
    while not(valido):
        difi2 = input("Selecciona un número:\t")
        if difi2.isnumeric():
            difi2 = int(difi2)
            if difi2>=1 and difi2<=5:
                valido = True
                continue
        print("Para seleccionar una opción válida escibe un número del 1 al 5.")
    print()
    print("Las funciones de evaluación son las siguientes:")
    print("\t1: mira el caso en el que haga más puntos.")
    print("\t2: busca que el otro haga el menos número de puntos posibles.")
    print("\t3: busca que tu puntuación diste de la de tu rival.")
    neval1 = input("\nSelecciona un número para Máquina1:\t")
    while not(neval1 in {"1","2","3"}):
        neval1 = input("El número introducido no es 1, 2 o 3. Prueba de nuevo:\t")
    neval2 = input("\nSelecciona un número para Máquina2:\t")
    while not(neval2 in {"1","2","3"}):
        neval2 = input("El número introducido no es 1, 2 o 3. Prueba de nuevo:\t")
    
    return n,difi1,difi2,int(neval1),int(neval2)


###########################################################
###########################################################

# FUNCIONES PRINCIPALES PARA JUGAR, minimax

#import time

def maquinaVSjugador_minimax():
    # n número de puntos
    # la máquina juega con 1, y el jugador juega con 2
    
    print()
    print("\t"*5+"_"*20+"\n"+"\t"*5+"|"+" "*18+"|")
    print("\t"*5+"|"+" "*4+"TIMBIRICHE"+" "*4+"|")
    print("\t"*5+"|"+"_"*18+"|\n")
    
    difi,n,neval = inicializar_parametros_mVSj()
    
    print("\n")
    
    PuntosJugador = 0
    PuntosMaquina = 0
    MH = [[0 for j in range(n-1)] for i in range(n)]
    MV = [[0 for j in range(n-1)] for i in range(n)]
    X =  [[0 for j in range(n-1)] for i in range(n-1)]
    tablero = [MH,MV,X]
    
    print("Instrucciones para el usuario. Cuándo sea tu turno:")
    print("\tEscribe junto a 'k' 0 aristas horizontales, y  1 verticales.")
    print("\tInserta junto a 'i' la primera coordenada de la arista que deseas poner.")
    print("\tInserta junto a 'j' la segunda coordenada de la arista que deseas poner.")
    print()
    #time.sleep(4)
    print("Las coordenadas de las aristas son las siguientes:\n")
    escribir_coordenadas(n-1)
    print(Fore.BLACK+"\n¡Comencemos a jugar!\n")
    text = input(Fore.BLACK+"¿Quién empieza? Escibe 'Jugador' o 'Máquina' y presiona enter:\t")
    while text!='Jugador' and text != 'jugador' and text != 'máquina' and text != "maquina" and text != 'Máquina' and text != "Maquina":
        text = input("No se ha reconocido la entrada. Vuelve a intentarlo:\t")
    print()
    if text == 'Jugador' or text == 'jugador':
        print(Fore.BLACK+"Está bien, empieza jugando.")
        print("\n"+tablero_a_str(tablero)+"\n")
        print(Fore.BLACK+"Escoje tu movimiento:")
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=2
        print(tablero_a_str(tablero))
        #time.sleep(2)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a la máquina\n")
    else:
        print(Fore.BLACK+"Está bien, empezaré yo.")
    
    while not(acabado(tablero)):
        (k,i,j)=GeneralMax(tablero,difi,neval)[0]
        tablero[k][i][j]=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                PuntosMaquina += 1
                tablero[2][punto[0]][punto[1]]=1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina, "\n\n")
                if PuntosJugador > PuntosMaquina:
                    print("¡Enhorabuena! Has conseguido ganarme.")
                elif PuntosJugador < PuntosMaquina:
                    print("¡Te he vencido! Tendrás que practicar más para ganarme.")
                else:
                    print("¡Vaya! Hemos empatado. Otra vez será.")
                return
            (k,i,j)=GeneralMax(tablero,difi,neval)[0]
            #time.sleep(2)
            tablero[k][i][j]=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca al jugador\n")
        print("Escoje tu próximo movimiento: ")
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=2
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                tablero[2][punto[0]][punto[1]]=2
                PuntosJugador += 1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina, "\n\n")
                if PuntosJugador > PuntosMaquina:
                    print("¡Enhorabuena! Has conseguido ganarme.")
                elif PuntosJugador < PuntosMaquina:
                    print("¡Te he vencido! Tendrás que practicar más para ganarme.")
                else:
                    print("¡Vaya! Hemos empatado. Otra vez será.")
                return
            print(Fore.BLACK+"¡Vuelves a jugar! Escoje tu próximo movimiento: ")
            k,i,j=pedir_coordenadas(n,tablero)
            print()
            tablero[k][i][j]=2
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a la máquina\n")

def maquinaVSmaquina_minimax():
    # n número de puntos
    # la máquina juega con 1, y el jugador juega con 2
    
    print()
    print("\t"*5+"_"*20+"\n"+"\t"*5+"|"+" "*18+"|")
    print("\t"*5+"|"+" "*4+"TIMBIRICHE"+" "*4+"|")
    print("\t"*5+"|"+"_"*18+"|\n")
    
    n,difi1,difi2,neval1,neval2=inicializar_parametros_mVSm()
    

    MH = [[0 for j in range(n-1)] for i in range(n)]
    MV = [[0 for j in range(n-1)] for i in range(n)]
    X =  [[0 for j in range(n-1)] for i in range(n-1)]
    tablero = [MH,MV,X]
    
    P1 = 0
    P2 = 0
    print("\n\nEmpieza jugando Máquina1:")
    while not(acabado(tablero)):
        (k,i,j)=GeneralMax(tablero,difi1,neval1)[0]
        tablero[k][i][j]=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                P1 += 1
                tablero[2][punto[0]][punto[1]]=1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tMáquina1: ",P1,"\n\tMáquina: ",P2, "\n\n")
                if P1 > P2:
                    print("Ha ganado Máquina1")
                elif P1 < P2:
                    print("Ha ganado Máquina2")
                else:
                    print("¡Vaya! Ha habido un empate.")
                return
            (k,i,j)=GeneralMax(tablero,difi1,neval1)[0]
            #time.sleep(1)
            tablero[k][i][j]=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",P1,"\n\tMáquina: ",P2)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Máquina2\n")
        (k,i,j)=GeneralMin(tablero,difi2,neval2)[0]
        tablero[k][i][j]=2
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                P2 += 1
                tablero[2][punto[0]][punto[1]]=2
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tMáquina1: ",P1,"\n\tMáquina: ",P2, "\n\n")
                if P1 > P2:
                    print("Ha ganado Máquina1")
                elif P1 < P2:
                    print("Ha ganado Máquina2")
                else:
                    print("¡Vaya! Ha habido un empate.")
                return
            (k,i,j)=GeneralMax(tablero,difi2,neval2)[0]
            #time.sleep(1)
            tablero[k][i][j]=2
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",P1,"\n\tMáquina: ",P2)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Máquina1\n")


###########################################################
###########################################################

# FUNCIONES PRINCIPALES PARA JUGAR, AlphaBeta

def maquinaVSjugador_alphabeta():
    # n número de puntos
    # la máquina juega con 1, y el jugador juega con 2
    
    print()
    print("\t"*5+"_"*20+"\n"+"\t"*5+"|"+" "*18+"|")
    print("\t"*5+"|"+" "*4+"TIMBIRICHE"+" "*4+"|")
    print("\t"*5+"|"+"_"*18+"|\n")
    
    difi,n,neval = inicializar_parametros_mVSj()
    
    print("\n")
    
    PuntosJugador = 0
    PuntosMaquina = 0
    MH = [[0 for j in range(n-1)] for i in range(n)]
    MV = [[0 for j in range(n-1)] for i in range(n)]
    X =  [[0 for j in range(n-1)] for i in range(n-1)]
    tablero = [MH,MV,X]
    
    print("Instrucciones para el usuario. Cuándo sea tu turno:")
    print("\tEscribe junto a 'k' 0 aristas horizontales, y  1 verticales.")
    print("\tInserta junto a 'i' la primera coordenada de la arista que deseas poner.")
    print("\tInserta junto a 'j' la segunda coordenada de la arista que deseas poner.")
    print()
    #time.sleep(4)
    print("Las coordenadas de las aristas son las siguientes:\n")
    escribir_coordenadas(n-1)
    print(Fore.BLACK+"\n¡Comencemos a jugar!\n")
    text = input(Fore.BLACK+"¿Quién empieza? Escibe 'Jugador' o 'Máquina' y presiona enter:\t")
    while text!='Jugador' and text != 'jugador' and text != 'máquina' and text != "maquina" and text != 'Máquina' and text != "Maquina":
        text = input("No se ha reconocido la entrada. Vuelve a intentarlo:\t")
    print()
    if text == 'Jugador' or text == 'jugador':
        print(Fore.BLACK+"Está bien, empieza jugando.")
        print("\n"+tablero_a_str(tablero)+"\n")
        print(Fore.BLACK+"Escoje tu movimiento:")
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=2
        print(tablero_a_str(tablero))
        #time.sleep(2)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a la máquina\n")
    else:
        print(Fore.BLACK+"Está bien, empezaré yo.")
    
    while not(acabado(tablero)):
        (k,i,j)=AlphaBeta(tablero,difi,neval)[0]
        tablero[k][i][j]=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                PuntosMaquina += 1
                tablero[2][punto[0]][punto[1]]=1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina, "\n\n")
                if PuntosJugador > PuntosMaquina:
                    print("¡Enhorabuena! Has conseguido ganarme.")
                elif PuntosJugador < PuntosMaquina:
                    print("¡Te he vencido! Tendrás que practicar más para ganarme.")
                else:
                    print("¡Vaya! Hemos empatado. Otra vez será.")
                return
            (k,i,j)=AlphaBeta(tablero,difi,neval)[0]
            #time.sleep(2)
            tablero[k][i][j]=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca al jugador\n")
        print("Escoje tu próximo movimiento: ")
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=2
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                tablero[2][punto[0]][punto[1]]=2
                PuntosJugador += 1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina, "\n\n")
                if PuntosJugador > PuntosMaquina:
                    print("¡Enhorabuena! Has conseguido ganarme.")
                elif PuntosJugador < PuntosMaquina:
                    print("¡Te he vencido! Tendrás que practicar más para ganarme.")
                else:
                    print("¡Vaya! Hemos empatado. Otra vez será.")
                return
            print(Fore.BLACK+"¡Vuelves a jugar! Escoje tu próximo movimiento: ")
            k,i,j=pedir_coordenadas(n,tablero)
            print()
            tablero[k][i][j]=2
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a la máquina\n")

def maquinaVSmaquina_alphabeta():
    # n número de puntos
    # la máquina juega con 1, y el jugador juega con 2
    
    print()
    print("\t"*5+"_"*20+"\n"+"\t"*5+"|"+" "*18+"|")
    print("\t"*5+"|"+" "*4+"TIMBIRICHE"+" "*4+"|")
    print("\t"*5+"|"+"_"*18+"|\n")
    
    n,difi1,difi2,neval1,neval2=inicializar_parametros_mVSm()
    

    MH = [[0 for j in range(n-1)] for i in range(n)]
    MV = [[0 for j in range(n-1)] for i in range(n)]
    X =  [[0 for j in range(n-1)] for i in range(n-1)]
    tablero = [MH,MV,X]
    
    P1 = 0
    P2 = 0
    print("\n\nEmpieza jugando Máquina1:")
    while not(acabado(tablero)):
        (k,i,j)=AlphaBeta(tablero,difi1,neval1)[0]
        tablero[k][i][j]=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                P1 += 1
                tablero[2][punto[0]][punto[1]]=1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tMáquina1: ",P1,"\n\tMáquina: ",P2, "\n\n")
                if P1 > P2:
                    print("Ha ganado Máquina1")
                elif P1 < P2:
                    print("Ha ganado Máquina2")
                else:
                    print("¡Vaya! Ha habido un empate.")
                return
            (k,i,j)=AlphaBeta(tablero,difi1,neval1)[0]
            #time.sleep(1)
            tablero[k][i][j]=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",P1,"\n\tMáquina: ",P2)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Máquina2\n")
        (k,i,j)=AlphaBeta(tablero,difi2,neval2,2)[0]
        tablero[k][i][j]=2
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                P2 += 1
                tablero[2][punto[0]][punto[1]]=2
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tMáquina1: ",P1,"\n\tMáquina: ",P2, "\n\n")
                if P1 > P2:
                    print("Ha ganado Máquina1")
                elif P1 < P2:
                    print("Ha ganado Máquina2")
                else:
                    print("¡Vaya! Ha habido un empate.")
                return
            (k,i,j)=AlphaBeta(tablero,difi2,neval2,2)[0]
            #time.sleep(1)
            tablero[k][i][j]=2
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",P1,"\n\tMáquina: ",P2)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Máquina1\n")

###########################################################
###########################################################

# FUNCIONES PRINCIPALES PARA JUGAR, Jugador VS Jugador

def jugadorVSjugador():
    # n número de puntos
    # la máquina juega con 1, y el jugador juega con 2
    
    print()
    print("\t"*5+"_"*20+"\n"+"\t"*5+"|"+" "*18+"|")
    print("\t"*5+"|"+" "*4+"TIMBIRICHE"+" "*4+"|")
    print("\t"*5+"|"+"_"*18+"|\n")
    
    print("A continuación, escribe un número del 3 al 10 para ajustar el tamaño de la cuadrícula:")
    
    valido = False
    while not(valido):
        n = input("Selecciona un número:\t")
        if n.isnumeric():
            n = int(n)
            if n>=3 and n<=10:
                valido = True
                continue
        print("Para seleccionar una opción válida escibe un número del 3 al 10.")
    
    
    P1 = 0
    P2 = 0
    MH = [[0 for j in range(n-1)] for i in range(n)]
    MV = [[0 for j in range(n-1)] for i in range(n)]
    X =  [[0 for j in range(n-1)] for i in range(n-1)]
    tablero = [MH,MV,X]
    
    print("Instrucciones para el usuario. Cuándo sea tu turno:")
    print("\tEscribe junto a 'k' 0 aristas horizontales, y  1 verticales.")
    print("\tInserta junto a 'i' la primera coordenada de la arista que deseas poner.")
    print("\tInserta junto a 'j' la segunda coordenada de la arista que deseas poner.")
    print()
    #time.sleep(4)
    print("Las coordenadas de las aristas son las siguientes:\n")
    escribir_coordenadas(n-1)
    print(Fore.BLACK+"\n¡Comencemos a jugar! Empieza Jugador1.\n")
    
    while not(acabado(tablero)):
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                tablero[2][punto[0]][punto[1]]=1
                P1 += 1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador1: ",P1,"\n\tJugador2: ",P2, "\n\n")
                if P1 > P2:
                    print("¡Enhorabuena! Ha ganado Jugador1")
                elif P1 < P2:
                    print("¡Enhorabuena! Ha ganado Jugador1")
                else:
                    print("¡Vaya! Ha habido un empate")
                return
            print(Fore.BLACK+"¡Vuelves a jugar! Escoje tu próximo movimiento: ")
            k,i,j=pedir_coordenadas(n,tablero)
            print()
            tablero[k][i][j]=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        
        print("\nRecuento de puntos:\n\tJugador1: ",P1,"\n\tJugador2: ",P2)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Jugador2.\n")
        
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=2
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                tablero[2][punto[0]][punto[1]]=2
                P2 += 1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador1: ",P1,"\n\tJugador2: ",P2, "\n\n")
                if P1 > P2:
                    print("¡Enhorabuena! Ha ganado Jugador1")
                elif P1 < P2:
                    print("¡Enhorabuena! Ha ganado Jugador1")
                else:
                    print("¡Vaya! Ha habido un empate")
                return
            print(Fore.BLACK+"¡Vuelves a jugar! Escoje tu próximo movimiento: ")
            k,i,j=pedir_coordenadas(n,tablero)
            print()
            tablero[k][i][j]=2
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador1: ",P1,"\n\tJugador2: ",P2)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Jugador1.\n")

###########################################################
###########################################################

# FUNCIONES PRINCIPALES PARA JUGAR, AlphaBeta optimizado

# Las primeras decisiones que se toman no son de gran importancia, 
# pero las opciones finales si que tienen un mayor peso. Es por ello
# que para agilizar el programa podemos cambiar la dificultad en 
# las ejecuciones.

# Por lo menos será 2, y en las últimas ejecuciones llegará a la
# dificultad dada

def maquinaVSjugador_alphabeta_optim():
    # n número de puntos
    # la máquina juega con 1, y el jugador juega con 2
    
    print()
    print("\t"*5+"_"*20+"\n"+"\t"*5+"|"+" "*18+"|")
    print("\t"*5+"|"+" "*4+"TIMBIRICHE"+" "*4+"|")
    print("\t"*5+"|"+"_"*18+"|\n")
    
    difi,n,neval = inicializar_parametros_mVSj()
    
    print("\n")
    
    PuntosJugador = 0
    PuntosMaquina = 0
    MH = [[0 for j in range(n-1)] for i in range(n)]
    MV = [[0 for j in range(n-1)] for i in range(n)]
    X =  [[0 for j in range(n-1)] for i in range(n-1)]
    tablero = [MH,MV,X]
    
    print("Instrucciones para el usuario. Cuándo sea tu turno:")
    print("\tEscribe junto a 'k' 0 aristas horizontales, y  1 verticales.")
    print("\tInserta junto a 'i' la primera coordenada de la arista que deseas poner.")
    print("\tInserta junto a 'j' la segunda coordenada de la arista que deseas poner.")
    print()
    #time.sleep(4)
    print("Las coordenadas de las aristas son las siguientes:\n")
    escribir_coordenadas(n-1)
    print(Fore.BLACK+"\n¡Comencemos a jugar!\n")
    text = input(Fore.BLACK+"¿Quién empieza? Escibe 'Jugador' o 'Máquina' y presiona enter:\t")
    while text!='Jugador' and text != 'jugador' and text != 'máquina' and text != "maquina" and text != 'Máquina' and text != "Maquina":
        text = input("No se ha reconocido la entrada. Vuelve a intentarlo:\t")
    print()
    if text == 'Jugador' or text == 'jugador':
        print(Fore.BLACK+"Está bien, empieza jugando.")
        print("\n"+tablero_a_str(tablero)+"\n")
        print(Fore.BLACK+"Escoje tu movimiento:")
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=2
        print(tablero_a_str(tablero))
        #time.sleep(2)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a la máquina\n")
    else:
        print(Fore.BLACK+"Está bien, empezaré yo.")
    
    aristas_ocupadas = 1
    total_aristas = (2*((n-1)**2))+(2*(n-1))
    
    while not(acabado(tablero)):
        if aristas_ocupadas > (total_aristas/3):
            N = difi
        else: 
            N = int(((difi-2)/(total_aristas/3))*aristas_ocupadas+2)
        
        (k,i,j)=AlphaBeta(tablero,N,neval)[0]
        tablero[k][i][j]=1
        aristas_ocupadas+=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                PuntosMaquina += 1
                tablero[2][punto[0]][punto[1]]=1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina, "\n\n")
                if PuntosJugador > PuntosMaquina:
                    print("¡Enhorabuena! Has conseguido ganarme.")
                elif PuntosJugador < PuntosMaquina:
                    print("¡Te he vencido! Tendrás que practicar más para ganarme.")
                else:
                    print("¡Vaya! Hemos empatado. Otra vez será.")
                return
            (k,i,j)=AlphaBeta(tablero,N,neval)[0]
            #time.sleep(2)
            tablero[k][i][j]=1
            aristas_ocupadas+=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca al jugador\n")
        print("Escoje tu próximo movimiento: ")
        k,i,j=pedir_coordenadas(n,tablero)
        print()
        tablero[k][i][j]=2
        aristas_ocupadas+=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                tablero[2][punto[0]][punto[1]]=2
                PuntosJugador += 1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina, "\n\n")
                if PuntosJugador > PuntosMaquina:
                    print("¡Enhorabuena! Has conseguido ganarme.")
                elif PuntosJugador < PuntosMaquina:
                    print("¡Te he vencido! Tendrás que practicar más para ganarme.")
                else:
                    print("¡Vaya! Hemos empatado. Otra vez será.")
                return
            print(Fore.BLACK+"¡Vuelves a jugar! Escoje tu próximo movimiento: ")
            k,i,j=pedir_coordenadas(n,tablero)
            print()
            tablero[k][i][j]=2
            aristas_ocupadas+=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",PuntosJugador,"\n\tMáquina: ",PuntosMaquina)
        print("\n\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a la máquina\n")

def maquinaVSmaquina_alphabeta_optim():
    # n número de puntos
    # la máquina juega con 1, y el jugador juega con 2
    
    print()
    print("\t"*5+"_"*20+"\n"+"\t"*5+"|"+" "*18+"|")
    print("\t"*5+"|"+" "*4+"TIMBIRICHE"+" "*4+"|")
    print("\t"*5+"|"+"_"*18+"|\n")
    
    n,difi1,difi2,neval1,neval2=inicializar_parametros_mVSm()
    

    MH = [[0 for j in range(n-1)] for i in range(n)]
    MV = [[0 for j in range(n-1)] for i in range(n)]
    X =  [[0 for j in range(n-1)] for i in range(n-1)]
    tablero = [MH,MV,X]
    
    P1 = 0
    P2 = 0
    
    aristas_ocupadas = 1
    total_aristas = (2*((n-1)**2))+(2*(n-1))
    
    print("\n\nEmpieza jugando Máquina1:")
    while not(acabado(tablero)):
        if aristas_ocupadas > (total_aristas/3):
            N1 = difi1
        else: 
            N1 = int(((difi1-2)/(total_aristas/3))*aristas_ocupadas+2)
        
        (k,i,j)=AlphaBeta(tablero,N1,neval1)[0]
        tablero[k][i][j]=1
        aristas_ocupadas+=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                P1 += 1
                tablero[2][punto[0]][punto[1]]=1
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tMáquina1: ",P1,"\n\tMáquina: ",P2, "\n\n")
                if P1 > P2:
                    print("Ha ganado Máquina1")
                elif P1 < P2:
                    print("Ha ganado Máquina2")
                else:
                    print("¡Vaya! Ha habido un empate.")
                return
            (k,i,j)=AlphaBeta(tablero,N1,neval1)[0]
            #time.sleep(1)
            tablero[k][i][j]=1
            aristas_ocupadas+=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",P1,"\n\tMáquina: ",P2)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Máquina2\n")
        
        if aristas_ocupadas > (total_aristas/3):
            N2 = difi2
        else: 
            N2 = int(((difi2-2)/(total_aristas/3))*aristas_ocupadas+2)
        
        (k,i,j)=AlphaBeta(tablero,N2,neval2,2)[0]
        tablero[k][i][j]=2
        aristas_ocupadas+=1
        (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        while ganado:
            for punto in puntos:
                P2 += 1
                tablero[2][punto[0]][punto[1]]=2
            print(tablero_a_str(tablero),"\n")
            if acabado(tablero):
                print("\nRecuento de puntos:\n\tMáquina1: ",P1,"\n\tMáquina: ",P2, "\n\n")
                if P1 > P2:
                    print("Ha ganado Máquina1")
                elif P1 < P2:
                    print("Ha ganado Máquina2")
                else:
                    print("¡Vaya! Ha habido un empate.")
                return
            (k,i,j)=AlphaBeta(tablero,N2,neval2,2)[0]
            #time.sleep(1)
            tablero[k][i][j]=2
            aristas_ocupadas+=1
            (ganado,puntos) = PuntoGanado((k,i,j), tablero)
        print(tablero_a_str(tablero))
        print("\nRecuento de puntos:\n\tJugador: ",P1,"\n\tMáquina: ",P2)
        print("\n"+Fore.BLACK+"_"*50+"\n"+"Cambio de turno, le toca a Máquina1\n")

###########################################################
###########################################################

# EJECUCION PRINCIPAL:
    
def principal():
    while True:
        print("\nA continuación selecciona un modo de juego entre los siguientes:")
        print("\t1. Jugador VS jugador")
        print("\t2. Jugador VS máquina")
        print("\t3. Máquina VS máquina")
        n = input("\nSelecciona un número:\t")
        while not(n in {"1","2","3"}):
            n = input("El número introducido no es 1, 2 o 3. Prueba de nuevo:\t")
        n = int(n)
        print()
        if n == 1:
            jugadorVSjugador()
        else:
            print("Selecciona una de las siguientes opciones:")
            print("\t1. MiniMax")
            print("\t2. AlphaBeta")
            print("\t3. AlphaBeta optimiziado")
            k = input("\nSelecciona un número:\t")
            while not(k in {"1","2","3"}):
                k = input("El número introducido no es 1, 2 o 3. Prueba de nuevo:\t")
            k = int(k)
            if n == 2:
                if k == 1:
                    maquinaVSjugador_minimax()
                elif k == 2:
                    maquinaVSjugador_alphabeta()
                else:
                    maquinaVSjugador_alphabeta_optim()
            else:
                if k == 1:
                    maquinaVSmaquina_minimax()
                elif k == 2:
                    maquinaVSmaquina_alphabeta()
                else:
                    maquinaVSmaquina_alphabeta_optim()
        print("\n\n¿Quieres volver a jugar?")
        txt = input("Escribe sí o no:\t")
        while not(txt in {"si","Si","sí","Sí","no","No","SI","NO"}):
            txt = input("El texto introducido no es válido. Prueba de nuevo:\t")
        if txt in {"no","No","NO"}:
            break
principal() 



#tablero = [[[1, 1], [2, 0], [0, 2]], [[2, 0], [0, 0], [1, 1]], [[0, 0], [0, 0]]]
# tablero = [[[0, 0], [0, 0], [0, 0]], [[0, 0],[0,0],[0,0]],[[0,0],[0,0]]]
# tablero=[[[2, 0], [0, 1], [1, 0]], [[2, 0],[0,1],[1,0]],[[0,0],[0,0]]]
# tablero = [[[1,1],[1,1],[1,1]],[[0,0],[0,1],[0,0]],[[0,0],[0,0],[0,0]]]
#print(tablero_a_str(tablero))
#print(GeneralMax(tablero,15))

#maquinaVSjugador()

# Cosas que faltan:
# Algoritmo con la poda
            
                


