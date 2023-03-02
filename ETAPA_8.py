import re
# lo tendria que estar trabajando con un parametro mas que sea un default, y que cambie en cada
#funcion donde se usa, pero para practicidad en este momento lo uso asi
def leer_linea(archivo):
    linea = archivo.readline()
    return linea if linea else "asd"

def extraer(linea,diccionario_textos,parametro,pos):
    for palabra in linea:
        palabra_sin_caracteres_especiales_1 = re.sub("[-()^#/@;:<>{}`\]\[\"+=~|.!?«»,_¿¡0-9]", "", palabra).upper()
        if len(palabra_sin_caracteres_especiales_1) == parametro:
            if palabra_sin_caracteres_especiales_1 not in diccionario_textos:
                veces_en_texto = [0,0,0]
                veces_en_texto[pos] = 1
                diccionario_textos[palabra_sin_caracteres_especiales_1] = veces_en_texto
            else:
                diccionario_textos[palabra_sin_caracteres_especiales_1][pos] += 1

def leer_archivo(archivo,linea,diccionario_textos,parametro,pos):
    while linea[0] != "asd":
        extraer(linea,diccionario_textos,parametro,pos)
        linea = leer_linea(archivo).strip("\n").split(" ")

#el parametro te lo da el archivo configuracion
#la funcion toma los tres archivos y te devuelve un diccionario con la palabra como clave y las veces que aparece como valores
def palabras_validas_textos(parametro):
    diccionario_textos = {}
    archivo_1 = open("Cuentos.txt", "r")
    archivo_2 = open("La araña negra - tomo 1.txt", "r")
    archivo_3 = open("Las 1000 Noches y 1 Noche.txt", "r")
    linea_1 = leer_linea(archivo_1).strip("\n").split(" ")
    linea_2 = leer_linea(archivo_2).strip("\n").split(" ")
    linea_3 = leer_linea(archivo_3).strip("\n").split(" ")
    #texto 1
    leer_archivo(archivo_1,linea_1,diccionario_textos,parametro,0)
    #texto 2
    leer_archivo(archivo_2,linea_2,diccionario_textos,parametro,1)
    #texto 3
    leer_archivo(archivo_3,linea_3,diccionario_textos,parametro,2)
    archivo_1.close()
    archivo_2.close()
    archivo_3.close()
    return diccionario_textos

def ordenar_palabras_diccionario(diccionario):
    lista_palabras_ordenadas = []
    lista_palabras_ordenadas = sorted(diccionario, key=lambda x:x)
    return lista_palabras_ordenadas

def agregar_palabras_archivo(diccionario, lista):
    archivo_palabras_ocultas = open("palabras.csv", "w")
    for palabra in lista:
        palabra_a_archivo = "{},{}\n".format(palabra,diccionario[palabra])
        archivo_palabras_ocultas.write(palabra_a_archivo)
    archivo_palabras_ocultas.close()

def obtener_palabras_validas(longitud_palabra):
    diccionario_de_palabras = palabras_validas_textos(longitud_palabra)
    lista_ordenada = ordenar_palabras_diccionario(diccionario_de_palabras)
    agregar_palabras_archivo(diccionario_de_palabras,lista_ordenada)
    return lista_ordenada
