import os.path
from os.path import exists

def leer_linea(archivo):
    linea = archivo.readline()
    return linea if linea else "asd,0"

def creacion_archivo():
    archivo = open("configuracion.csv", "w")
    long = 7
    max_part = 5
    rein_part = False
    archivo.write("LONGITUD_PALABRA_SECRETA,{}\nMAXIMO_PARTIDAS,{}\nREINICIAR_ARCHIV0_PARTIDAS,{}".format(long,max_part,rein_part))
    archivo.close()

#devuelve el valor numerico de cantidad de letras, cantidad de partidas, reiniciar archivo
def parametros_juego():
    datos_conf_partida = []
    if os.path.exists("configuracion.csv"):
        archivo = open("configuracion.csv", "r")
        parametro, cantidad = leer_linea(archivo).strip("\n").split(",")
        while parametro != "asd":
            datos_conf_partida.append(cantidad)
            parametro, cantidad = leer_linea(archivo).strip("\n").split(",")
        archivo.close()
    else:
        creacion_archivo()
        parametros_juego()
    return (datos_conf_partida)

parametros_juego()
