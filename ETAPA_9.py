import time

def texto_archivo(dic_archivo_partidas,archivo):
    tiempo = time.time()
    fecha = fecha_dmy(tiempo)
    hora = time.strftime("%T", time.localtime(tiempo))
    lista_texto = dic_archivo_partidas.items()
    lista_texto = sorted(lista_texto, key=lambda aciertos:aciertos[1][0], reverse=True)
    for jugador in lista_texto:
        texto = "{},{},{},{},{}\n".format(fecha,hora,jugador[0],jugador[1][0],jugador[1][1])
        archivo.write(texto)

def fecha_dmy(tiempo):
    mes = time.strftime("%b", time.gmtime(tiempo))
    dia = time.strftime("%d", time.gmtime(tiempo))
    año = time.strftime("%Y", time.gmtime(tiempo))
    fecha = "{} {} {}".format(dia, mes, año)
    return fecha


def actualizacion_dic_archivo_partidas(resultado,jugador_referencia,intentos,dic_archivo_partidas):
    if resultado:
        dic_archivo_partidas[jugador_referencia][0] += 1
        dic_archivo_partidas[jugador_referencia][1] += intentos


def archivo_partidas(opcion_reinicio, dic_archivo_partidas):
    if opcion_reinicio == True:
        archivo = open("partidas.csv", "w")
    else:
        archivo = open("partidas.csv", "a")
    texto_archivo(dic_archivo_partidas,archivo)
    archivo.close()
