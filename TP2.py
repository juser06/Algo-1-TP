"""en la etapa 2 se agrego el validador de palabra que tiene el input dentro del mismo, con lo cual ahora palabra de usuario
se pide por def para que asi se puede pedir varias veces. Jose"""
"""para la etapa 4 saque de aca el tema del reloj https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/"""

import random
import os
import time
import datetime
from ETAPA_8 import *
from ETAPA_10 import *
from ETAPA_9 import *

# ------------------------funciones que estaban en el TP para usar --------------------------------

# funcion con el codigo para cada color de la letra
def obtener_color(color):
    colores = {
        "Verde": "\x1b[32m",
        "Amarillo": "\x1b[33m",
        "GrisOscuro": "\x1b[90m",
        "Defecto": "\x1b[39m"
    }
    return colores[color]

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------Codigo de la Etapa 1------------------------------------------------------

def verde(letra_usuario, contador, lista_pos, lista_color):
    if contador in lista_pos:
        pos = list(map(lambda lista: lista[2], lista_color)).index(contador)
        lista_color[pos][1] = 'GrisOscuro'
        lista_color[pos][2] = None
    else:
        lista_pos.append(contador)
    lista_color.append([letra_usuario, 'Verde', contador])

def amarillo_Y_gris(palabra_juego, letra_usuario, lista_pos, lista_color):
    pos_juego = None
    color_usuario = 'GrisOscuro'
    contador = 0
    longitud_juego = len(palabra_juego)
    while contador < longitud_juego:
        letra_juego = palabra_juego[contador]
        if (letra_usuario == letra_juego) and (contador not in lista_pos):
            pos_juego = contador
            color_usuario = 'Amarillo'
            lista_pos.append(pos_juego)
            contador = longitud_juego
        else:
            contador = contador + 1
    lista_color.append([letra_usuario, color_usuario, pos_juego])

# funcion que toma la palabra de juego y la del jugador y las compara dando el valor del color
# ENTRADA: ('SALTA', 'PLUMA')
# SALIDA: [('P', 'GrisOscuro'), ('L', 'Amarillo'), ('U', 'GrisOscuro'), ('M', 'GrisOscuro'), ('A', 'Verde')]
def validador_de_letras(palabra_del_juego, palabra_del_usuario):
    lista_color = []
    lista_pos = []
    contador = -1
    for letra in palabra_del_usuario:
        contador += 1
        if letra == palabra_del_juego[contador]:
            verde(letra, contador, lista_pos, lista_color)
        else:
            amarillo_Y_gris(palabra_del_juego, letra, lista_pos, lista_color)
    return list(map(lambda lista: (lista[0], lista[1]), lista_color))

# toma la palabra con codigo de color y lo muestra en pantalla con su respectivo color
def imprimir_letra_color(lista_letra_color):
    cadena = ''
    for tupla in lista_letra_color:
        letra = tupla[0]
        color = obtener_color(tupla[1])
        cadena = cadena + color + letra + ' '
    print(' ' + cadena + obtener_color("Defecto"))

# dependiendo de la cantidad de letras verdes te da el color
#ENTRADA: ([('P', 'GrisOscuro'), ('L', 'Amarillo'), ('U', 'GrisOscuro'), ('M', 'GrisOscuro'), ('A', 'Verde')], 'Verde')
#SALIDA: False
def controlar_victoria(resultado_de_validador_de_letras,color_sustituir):
    validador = True
    contador = 0
    while contador < len(resultado_de_validador_de_letras):
        if resultado_de_validador_de_letras[contador][1] != color_sustituir:
            validador = False
            contador = len(resultado_de_validador_de_letras)
        else:
            contador += 1
    return validador

def mostrar_perdedores(dic_jugadores,jugador_referencia,puntaje_resto):
    for clave in dic_jugadores:
        if clave != jugador_referencia:
            print("{} perdiste {} puntos y tenés acumulado {} puntos".format(dic_jugadores[clave][0],abs(puntaje_resto),
                                                                             dic_jugadores[clave][1]))

# desde la etapa 4 muestra tambien el tiempo que se tardo en adivinar
def mensaje_partida(tiempo,resultado,dic_jugadores,jugador_referencia,puntaje_referencia,puntaje_resto):
    if resultado:
        minutos = time.strftime("%M", time.gmtime(time.time() - tiempo))
        segundos = time.strftime("%S", time.gmtime(time.time() - tiempo))
        print("{} Ganaste! Tardaste {} minutos y {} segundos en adivinar la palabra"
              .format(dic_jugadores[jugador_referencia][0],minutos, segundos))
        print("Obtuviste un total de {} puntos, tenes acumulados {} puntos"
              .format(puntaje_referencia,dic_jugadores[jugador_referencia][1]))
    else:
        print("Perdieron!\n")
        print("{} Perdiste un total de {} puntos, tenes acumulados {} puntos"
              .format(dic_jugadores[jugador_referencia][0],puntaje_referencia,dic_jugadores[jugador_referencia][1]))
    mostrar_perdedores(dic_jugadores,jugador_referencia,puntaje_resto)

def mensaje_fin(lista_ganadores):
    limpiar()
    if len(lista_ganadores) == 1:
        print("El ganador es {} con un total de {} puntos".format(lista_ganadores[0][0],lista_ganadores[0][1]))
    else:
        print("Fue un empate")

# ------------------------Codigo de la etapa 2------------------------------------------------------

def entrada(jugador_activo, dic_jugadores):
    dic = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    print("Es el turno de: {}".format(dic_jugadores[jugador_activo][0]))
    cadena = input("Arriesgo: ").upper()
    for letra_CON_tilde in dic:
        letra_SIN_tilde = dic[letra_CON_tilde]
        cadena = cadena.replace(letra_CON_tilde, letra_SIN_tilde)
    return cadena


# revisa que la palabra que ingreso el usuario respete las reglas
def control_de_validez_palabra(longitud_palabra, lista, jugador_activo, dic_jugadores):
    validador = 0
    while validador == 0:
        palabra_del_usuario = entrada(jugador_activo, dic_jugadores)
        if len(palabra_del_usuario) < longitud_palabra:
            print(
                "La palabra ingresada es muy corta, acordate que tiene que tener {} letras. Volve a ingresarla.\n".format(
                    longitud_palabra))
        elif len(palabra_del_usuario) > longitud_palabra:
            print(
                "La palabra ingresada es muy larga, acordate que tiene que tener {} letras. Volve a ingresarla.\n".format(
                    longitud_palabra))
        elif not palabra_del_usuario.isalnum():
            print("Ingresaste caracteres especiales, acordate que solo debe contener letras. Volve a ingresarla.\n")
        elif not palabra_del_usuario.isalpha():
            print("Ingresaste numeros, acordate que solo debe contener letras. Volve a ingresarla.\n")
        elif palabra_del_usuario in lista:
            print("La palabra ingresada ya fue utilizada. Ingresa una nueva.\n")
        else:
            validador = 1
    return palabra_del_usuario


# ------------------------Codigo de la etapa 3------------------------------------------------------

#ENTRADA: (' ? ? ? ? ?', 2)
#SALIDA: [(False, ' ? ? ? ? ?'), (False, ' ? ? ? ? ?')]
def insertar_lista_intentos(palabra_oculta, cantidad_mayor_intentos):
    lista = []
    for elemento in range(0, cantidad_mayor_intentos):
        lista.append((False, palabra_oculta))
    return lista

#ENTRADA: 'SALTA'
#SALIDA: ' S A L T A'
def insertar_espacio_cadena(cadena):
    return ''.join(list(map(lambda elemento:' '+elemento,cadena)))

def imprimir_resultado_acumulado(oculta, lista_intentos):
    limpiar()
    print("Palabra a adivinar:", oculta)
    for tupla in lista_intentos:
        intento = tupla[1]
        if tupla[0] == True:
            imprimir_letra_color(intento)
        else:
            print(intento)

#ENTRADA: (5, '?')
#SALIDA: ' ? ? ? ? ?'
def crear_palabra_oculta(longitud_palabra, char):
    return (' ' + char)*longitud_palabra

#ENTRADA: ('?',' ? ? ? ? ?',[('P', 'GrisOscuro'),('L', 'Amarillo'),('U', 'GrisOscuro'),('M', 'GrisOscuro'),('A', 'Verde')],'Verde')
#SALIDA: ' ? ? ? ? A'
def sustituir_palabra_oculta(char, palabra_oculta, palabra_con_color,color_sustituir):
    enumerar_palabra_con_color = enumerate(palabra_con_color)
    for tupla in enumerar_palabra_con_color:
        pos = tupla[0]*2 + 1
        letra_usuario = tupla[1][0]
        color_usuario = tupla[1][1]
        if (palabra_oculta[pos] == char) and (color_usuario == color_sustituir):
            palabra_oculta = modificar_elemento_de_cadena(letra_usuario,pos,palabra_oculta)
    return palabra_oculta

#ENTRADA: ('Z', 1, ' ? ? ? ? ?')
#SALIDA: ' Z ? ? ? ?'
def modificar_elemento_de_cadena(char,pos,cadena):
    lista = list(cadena)
    lista[pos] = char
    return ''.join(lista)

def modificar_palabra_oculta(char, palabra_oculta, palabra_con_color, palabra_del_juego, resultado, estado_FIN,
                     color_sustituir):
    if (resultado == False) and (estado_FIN):
        cadena_imprimir = insertar_espacio_cadena(palabra_del_juego)
    else:
        cadena_imprimir = sustituir_palabra_oculta(char, palabra_oculta, palabra_con_color,color_sustituir)
    return cadena_imprimir

def ciclo_partida(char, color_sustituir, longitud_palabra, palabra_oculta, palabra_del_juego, cantidad_mayor_intentos,
                  lista_intentos_con_color, dic_jugadores, cantidad_de_jugadores, jugador_inicial):
    lista_intentos_sin_color = []
    contador = 0
    while contador < cantidad_mayor_intentos:
        intento = contador + 1
        estado_FIN = contador == cantidad_mayor_intentos - 1
        jugador_activo = (contador+jugador_inicial) % (cantidad_de_jugadores)
        palabra_del_usuario = control_de_validez_palabra(longitud_palabra, lista_intentos_sin_color, jugador_activo, dic_jugadores)
        palabra_con_color = validador_de_letras(palabra_del_juego, palabra_del_usuario)
        resultado = controlar_victoria(palabra_con_color,color_sustituir)
        palabra_oculta = modificar_palabra_oculta(char, palabra_oculta, palabra_con_color, palabra_del_juego, resultado,
                         estado_FIN, color_sustituir)
        lista_intentos_sin_color.append(palabra_del_usuario)
        lista_intentos_con_color[contador] = (True, palabra_con_color)
        imprimir_resultado_acumulado(palabra_oculta, lista_intentos_con_color)
        if resultado:
            contador = cantidad_mayor_intentos
        else:
            contador = contador + 1
    return (resultado,intento,jugador_activo)

# ----------------------------------Etapa 4--------------------------------------------------

def validar_continuar(lista,contador_de_partidas,cant_max_partidas):
    estado = False
    while estado == False:
        continuar_jugando = input("\nDesea continuar jugando (S/N)\n").upper()
        if continuar_jugando in lista:
            estado = True
        else:
            print("\nLa opcion ingresada no es correcta, Desea continuar jugando (S/N)")
    return contador_de_partidas + 1 if continuar_jugando == lista[0] else cant_max_partidas

#ENTRADA: (5, 10)
#SALIDA: {1:50, 2:40, 3:30, 4:20, 5:10}
def crear_dic_puntaje(cantidad_mayor_intentos,entero):
    dic = {}
    contador = cantidad_mayor_intentos + 1
    for intento in range(1,cantidad_mayor_intentos + 1):
        contador = contador - 1
        dic[intento] = entero*contador
    return dic

#CASO 1
#ENTRADA: (True, 2, 0, 1, {1:50, 2:40, 3:30, 4:20, 5:10})
#SALIDA: (0, 40, -40)
#CASO 2
#ENTRADA: (False, 5, 1, 1, {1:50, 2:40, 3:30, 4:20, 5:10})
#SALIDA: (1, -100, -50)
def puntaje_partida(resultado,intento,jugador_activo,jugador_inicial,dic_puntaje):
    if resultado:
        jugador_referencia = jugador_activo
        puntaje_referencia = dic_puntaje[intento]
        puntaje_resto = -puntaje_referencia
    else:
        jugador_referencia = jugador_inicial
        puntaje_referencia = -100
        puntaje_resto = -50
    return (jugador_referencia,puntaje_referencia,puntaje_resto)

#ENTRADA: ({0:['A',50], 1:['B',-50]}, 0, 40, -40)
#SALIDA: {0:['A',90], 1:['B',-90]}
def puntaje_acumulado(dic_jugadores,jugador_referencia,puntaje_referencia,puntaje_resto):
    for clave in dic_jugadores:
        if clave == jugador_referencia:
            puntaje = puntaje_referencia
        else:
            puntaje = puntaje_resto
        dic_jugadores[clave][1] = dic_jugadores[clave][1] + puntaje

#SALIDA: ('SALTA', 5)
def seleccionar_palabra_del_juego(longitud_palabra):
    palabra_del_juego = random.choice(obtener_palabras_validas(longitud_palabra)).upper()
    return (palabra_del_juego)

#ENTRADA: {0:['A',100], 1:['B',100]}
#SALIDA: [['A',100], ['B',100]]
def ganadores(dic_jugadores):
    mayor_puntaje = max(map(lambda lista:lista[1],dic_jugadores.values()))
    return [dic_jugadores[clave] for clave in dic_jugadores if dic_jugadores[clave][1] == mayor_puntaje]

def crear_dic_archivo_partidas(dic_jugadores):
    dic_archivo_partidas = {}
    for jugador in dic_jugadores.values():
        dic_archivo_partidas[jugador[0]] = [0,0]
    return dic_archivo_partidas

def resultado_partida(char,color_sustituir,cantidad_mayor_intentos,tiempo,dic_jugadores,cantidad_de_jugadores,jugador_inicial,
                dic_puntaje,longitud_palabra):
    palabra_del_juego = seleccionar_palabra_del_juego(longitud_palabra)
    #palabra_del_juego = "ESPEJOS"
    palabra_oculta = crear_palabra_oculta(longitud_palabra, char)
    lista_intentos_con_color = insertar_lista_intentos(palabra_oculta, cantidad_mayor_intentos)
    imprimir_resultado_acumulado(palabra_oculta, lista_intentos_con_color)
    resultado,intento,jugador_activo = ciclo_partida(char, color_sustituir, longitud_palabra, palabra_oculta, palabra_del_juego,
                                                     cantidad_mayor_intentos, lista_intentos_con_color, dic_jugadores,
                                                     cantidad_de_jugadores, jugador_inicial)
    jugador_referencia,puntaje_referencia,puntaje_resto = puntaje_partida(resultado,intento,jugador_activo,jugador_inicial,
                                                                          dic_puntaje)
    return (resultado,jugador_referencia,puntaje_referencia,puntaje_resto,intento)

def ciclo_continuar(char,color_sustituir,cantidad_mayor_intentos,dic_jugadores,cantidad_de_jugadores,primer_turno,
                    dic_puntaje,cant_max_partidas,longitud_palabra,opcion_reinicio):
    lista = ["S", "N"]
    contador_de_partidas = 0
    dic_archivo_partidas = crear_dic_archivo_partidas(dic_jugadores)
    while contador_de_partidas < cant_max_partidas:
        tiempo = time.time()
        jugador_inicial = (contador_de_partidas+primer_turno) % (cantidad_de_jugadores)
        resultado,jugador_referencia,puntaje_referencia,puntaje_resto,intentos = resultado_partida(char,color_sustituir, cantidad_mayor_intentos,
                                                                                    tiempo,dic_jugadores,cantidad_de_jugadores,
                                                                                    jugador_inicial,dic_puntaje,longitud_palabra)
        puntaje_acumulado(dic_jugadores,jugador_referencia,puntaje_referencia,puntaje_resto)
        mensaje_partida(tiempo,resultado,dic_jugadores,jugador_referencia,puntaje_referencia,puntaje_resto)
        actualizacion_dic_archivo_partidas(resultado,dic_jugadores[jugador_referencia][0],intentos,dic_archivo_partidas)
        if contador_de_partidas != cant_max_partidas - 1:
            contador_de_partidas = validar_continuar(lista,contador_de_partidas,cant_max_partidas)
        else:
            input('\nFIN\n')
            contador_de_partidas += 1
    archivo_partidas(opcion_reinicio, dic_archivo_partidas)

#-------------------------------------Etapa 5---------------------------------------------
#ENTRADA: 2
#SALIDA: {0:['A',0], 1:['B',0]}
def ingresar_nombre_jugador(cantidad):
    limpiar()
    dic = {}
    for elemento in range(0,cantidad):
        nombre = input("Ingrese el nombre del jugador {}: ".format(elemento+1))
        dic[elemento] = [nombre,0]
    return dic

#ENTRADA: 2
#SALIDA: ({0:['A',0], 1:['B',0]}, 1)
def orden(cantidad):
    return random.choice(range(0,cantidad))

def defecto(longitud_palabra,cant_max_partidas,reinicio_archivo):
    if longitud_palabra == None or longitud_palabra == "":
        longitud_palabra = 7
    if cant_max_partidas == None or cant_max_partidas == "":
        cant_max_partidas = 5
    if reinicio_archivo == None or reinicio_archivo == "":
        reinicio_archivo = False
    return (longitud_palabra,cant_max_partidas,reinicio_archivo)

def main(dic):
    dic_jugadores = dic
    char = '?'
    color_sustituir = 'Verde'
    longitud_palabra, cant_max_partidas, reinicio_archivo = parametros_juego()
    longitud_palabra, cant_max_partidas, reinicio_archivo = defecto(longitud_palabra,cant_max_partidas,reinicio_archivo)
    cantidad_mayor_intentos = 5
    cantidad_de_jugadores = len(list(dic_jugadores.keys()))
    puntaje = 10
    dic_puntaje = crear_dic_puntaje(cantidad_mayor_intentos,puntaje)
    primer_turno = orden(cantidad_de_jugadores)
    ciclo_continuar(char,color_sustituir,cantidad_mayor_intentos,dic_jugadores,cantidad_de_jugadores,primer_turno,
                    dic_puntaje,int(cant_max_partidas),int(longitud_palabra),reinicio_archivo)
    lista_ganadores = ganadores(dic_jugadores)
    mensaje_fin(lista_ganadores)
    input()
