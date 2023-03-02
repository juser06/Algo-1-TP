#https://programacionpython80889555.wordpress.com/2018/12/04/creando-login-con-python-y-tkinter/
#https://stackoverflow.com/questions/65630688/open-only-one-tk-toplevel-window

from TP2 import *
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import messagebox
import re

def destroy_all(root, estado):
    for widget in root.winfo_children():
        if isinstance(widget, Toplevel):
            if estado == True:
                widget.destroy()
            else:
                widget.withdraw()
    root.destroy() if estado else root.withdraw()

def Exit(ventana_principal, ventana_componente, dic):
    MsgBox = messagebox.askquestion("TODO PREPARADO", '¿ESTAS LISTO PARA JUGAR?', icon='warning')
    if MsgBox == 'yes':
        destroy_all(ventana_principal, False)
        main(dic)
    destroy_all(ventana_principal, True)


def mensaje_registro_confirmar(etiqueta_resultado, etiqueta_comprobar, estado_registro,
                               entrada_contraseña, entrada_confirmar, ingresar):
    if estado_registro:
        cadena = 'CONTRASEÑA ACEPTADA'
        entrada_contraseña.delete(0, END)
        entrada_confirmar.delete(0, END)
        entrada_contraseña.config(state="disabled")
        entrada_confirmar.config(state="disabled")
        ingresar["state"] = "disabled"
        changeText(etiqueta_comprobar, '')
    else:
        cadena = 'HAY UN ERROR EN LA CONTRASEÑA'
    changeText(etiqueta_resultado, cadena)


def comprobar_registro_confirmar(ventana_principal, ventana_registro_contraseña, contraseña,
                                 confirmar_contraseña, etiqueta_resultado, etiqueta_comprobar,
                                 nombre, dic_jugador, entrada_contraseña, entrada_confirmar,
                                 ingresar, dic_contraseña, cantidad):
    etiqueta_comprobar_texto = etiqueta_comprobar.cget("text")
    dic_contraseña[1] = contraseña == confirmar_contraseña
    estado_registro = (dic_contraseña[0]) and (dic_contraseña[1])
    mensaje_registro_confirmar(etiqueta_resultado, etiqueta_comprobar, estado_registro,
                               entrada_contraseña, entrada_confirmar, ingresar)
    if estado_registro:
        escribir(nombre, contraseña)
        agregar_jugador(dic_jugador, nombre, cantidad)
        salir(ventana_principal, ventana_registro_contraseña, dic_jugador, cantidad)


def mensaje_registro_contraseña(etiqueta_resultado,resultado,contraseña):
    if contraseña == '':
        cadena = ''
    else: 
        if resultado:
            cadena = 'Contraseña válida'
        else:
            cadena = 'Contraseña inválida'
    changeText(etiqueta_resultado, cadena)


def comprobar_registro_contraseña(etiqueta_resultado,contraseña,dic_contraseña):
    if contraseña == '':
        resultado = False
    else:
        resultado =  contraseña_usuario_nuevo(contraseña)
    dic_contraseña[0] = resultado
    mensaje_registro_contraseña(etiqueta_resultado,resultado,contraseña)


def contraseña_usuario_nuevo(contraseña):
    validador_longitud = (len(contraseña) >= 8) and (len(contraseña) <= 12)
    validador_todo = all((char.isalnum()) or (char in ['_',"-"]) for char in contraseña)
    validador_especial = ('_' in contraseña) or ('-' in contraseña)
    validador_mayus = any(char.isupper() for char in contraseña)
    validador_nro = any(char.isnumeric() for char in contraseña)
    validador_minus = any(char.islower() for char in contraseña)
    validador_tilde = not(any(char in ['Á','É','Í','Ó','Ú'] for char in contraseña.upper()))
    return validador_longitud and validador_especial and validador_mayus and validador_nro and\
           validador_minus and validador_tilde and validador_todo


def mensaje_registro_nombre(ventana, resultado, etiqueta_resultado):
    estado, nombre, cadena = resultado
    changeText(etiqueta_resultado, cadena)
    return (estado, nombre)


def nombre_usuario_nuevo(archivo, nombre_nuevo_usuario):
    cadena = ''
    validador_nombre = False
    if len(nombre_nuevo_usuario) >= 4 and len(nombre_nuevo_usuario) <= 15:
        if re.match("^[a-zA-Z0-9_áéíóúÁÉÍÓÚ]+$", nombre_nuevo_usuario):
            estado_nombre = buscar(archivo, nombre_nuevo_usuario, '')[0]
            if estado_nombre:
                cadena = 'el nombre ya existe'
            else:
                validador_nombre = True
        else:
            cadena = 'tiene caracteres no permitido'
    else:
        cadena = 'no cumple con la longitud'
    return (validador_nombre, nombre_nuevo_usuario, cadena)


def escribir(usuario, contraseña):
    archivo = open('usuarios.csv', 'a')
    archivo.write("{},{}\n".format(usuario, contraseña))
    archivo.close()


def comprobar_registro_nombre(ventana_principal, ventana_registro_usuario, nombre,
                              etiqueta_resultado, dic_jugador, cantidad):
    archivo = open("usuarios.csv", "r")
    resultado = nombre_usuario_nuevo(archivo, nombre)
    archivo.close()
    mensaje_registro_nombre(ventana_registro_usuario, resultado, etiqueta_resultado)
    if resultado[0]:
        nombre_nuevo = resultado[1]
        ventana_registro_usuario.destroy()
        registro_contraseña(ventana_principal, nombre_nuevo, dic_jugador, cantidad)


def changeText(etiqueta, cadena):
    etiqueta.configure(text=cadena)


def mensaje_login(ventana, resultado, entrada_usuario, entrada_contraseña,
                  etiqueta_resultado, nombre, dic_jugador):
    entrada_usuario.delete(0, END)
    entrada_contraseña.delete(0, END)
    estado_usuario, estado_contraseña = resultado
    lista_jugador = list(map(lambda tupla: tupla[1][0], dic_jugador.items()))
    estado = False
    if nombre in lista_jugador:
        cadena = 'Ya procesado'
    else:
        if estado_usuario and estado_contraseña:
            estado = True
            cadena = 'Login finalizado'
        else:
            cadena = 'Usuario o contraseña incorrecto'
    changeText(etiqueta_resultado, cadena)
    return estado


def buscar(archivo, nombre, contraseña):
    estado_nombre = False
    estado_contraseña = False
    salir = False
    while salir == False:
        linea = archivo.readline()
        if linea != '':
            nombre_linea, contraseña_linea = linea.strip().split(",")
            if nombre_linea == nombre:
                estado_nombre = True
                if contraseña_linea == contraseña:
                    estado_contraseña = True
                salir = True
        else:
            salir = True
    return (estado_nombre, estado_contraseña)


def comprobar_login(tupla, ventana_principal, ventana_login, entrada_usuario, entrada_contraseña,
                    etiqueta_resultado, dic_jugador, ingresar, cantidad):
    nombre = tupla[0]
    contraseña = tupla[1]
    archivo = open("usuarios.csv", "r")
    resultado = buscar(archivo, nombre, contraseña)
    archivo.close()
    estado = mensaje_login(ventana_login, resultado, entrada_usuario, entrada_contraseña,
                           etiqueta_resultado, nombre, dic_jugador)
    if estado == True:
        entrada_usuario.delete(0, END)
        entrada_contraseña.delete(0, END)
        entrada_usuario.config(state="disabled")
        entrada_contraseña.config(state="disabled")
        ingresar["state"] = "disabled"
        agregar_jugador(dic_jugador, nombre, cantidad)
        salir(ventana_principal, ventana_login, dic_jugador, cantidad)


def salir(ventana_principal, ventana_componente, dic, cantidad_de_jugadores):
    if len(list(dic.keys())) == cantidad_de_jugadores:
        Exit(ventana_principal, ventana_componente, dic)


def agregar_jugador(dic, nombre, cantidad_de_jugadores):
    mayor = -1 if dic == {} else max(dic.keys())
    lista = list(map(lambda tupla: tupla[1][0], dic.items()))
    longitud = len(lista)
    if (nombre not in lista) and (longitud < cantidad_de_jugadores):
        dic[mayor + 1] = [nombre, 0]


def usuario_Y_contraseña(usuario, contraseña):
    valor_usuario = usuario.get()
    valor_contraseña = contraseña.get()
    return (valor_usuario, valor_contraseña)


def principal():
    cantidad = 2
    dic_jugador = {}
    ventana_principal = Tk()
    ventana_principal.title('Principal')
    ventana_principal.geometry('300x250')
    Label(text='Escoja su opción', bg='LightGreen', width='300', height='2', font=('Calibri', 13)).pack()
    Label(text='').pack()
    Button(text='Acceder', height='2', width='30', bg='DarkGrey', command=lambda: login(ventana_principal,
                                                                                        dic_jugador,cantidad)).pack()
    Label(text='').pack()
    Button(text='Registrarse', height='2', width='30', bg='DarkGrey', command=lambda: registro_nombre(ventana_principal,
                                                                                                      dic_jugador,
                                                                                                      cantidad)).pack()
    Label(text='').pack()
    ventana_principal.mainloop()


def registro_contraseña(ventana_principal, nombre_nuevo, dic_jugador, cantidad):
    dic_contraseña = {0:False,1:False}
    ventana_registro_contraseña = Toplevel(ventana_principal)
    ventana_registro_contraseña.title('Registro')
    ventana_registro_contraseña.geometry('300x400')
    contraseña = StringVar(ventana_registro_contraseña)
    confirmar_contraseña = StringVar(ventana_registro_contraseña)
    Label(ventana_registro_contraseña, text='Introduzca contraseña:\nDebe contener al menos\n1 mayuscula, 1 minuscula\n1 numero\nuno de los siguientes caracteres\"-\" o \"_\"\nentre 8 y 12 caracteres', bg='LightGreen').pack()
    Label(ventana_registro_contraseña, text='').pack()
    Label(ventana_registro_contraseña, text='Contraseña').pack()
    entrada_contraseña = Entry(ventana_registro_contraseña, textvariable=contraseña)
    entrada_contraseña.bind("<KeyRelease>", (lambda event: comprobar_registro_contraseña(etiqueta_comprobar,
                                                                                         entrada_contraseña.get(),
                                                                                         dic_contraseña)))
    entrada_contraseña.pack()
    Label(ventana_registro_contraseña, text='Confirmar contraseña').pack()
    entrada_confirmar = Entry(ventana_registro_contraseña, textvariable=confirmar_contraseña)
    entrada_confirmar.pack()
    Label(ventana_registro_contraseña, text='').pack()
    ingresar = Button(ventana_registro_contraseña, text='Ingresar', width=10, height=1, bg='LightGreen',
                      command=lambda: comprobar_registro_confirmar(ventana_principal,
                                                                   ventana_registro_contraseña, contraseña.get(),
                                                                   confirmar_contraseña.get(),
                                                                   etiqueta_resultado, etiqueta_comprobar,
                                                                   nombre_nuevo, dic_jugador, entrada_contraseña,
                                                                   entrada_confirmar, ingresar,
                                                                   dic_contraseña, cantidad))
    ingresar.pack()
    Label(ventana_registro_contraseña, text='').pack()
    etiqueta_comprobar = Label(ventana_registro_contraseña, text='')
    etiqueta_comprobar.pack()
    etiqueta_resultado = Label(ventana_registro_contraseña, text='')
    etiqueta_resultado.pack()


def registro_nombre(ventana_principal, dic_jugador, cantidad):
    if not any(isinstance(x, Toplevel) for x in ventana_principal.winfo_children()):
        ventana_registro_nombre = Toplevel(ventana_principal)
        ventana_registro_nombre.title('Registro')
        ventana_registro_nombre.geometry('300x250')
        nombre = StringVar(ventana_registro_nombre)
        Label(ventana_registro_nombre, text='Introduzca nombre', bg='LightGreen').pack()
        Label(ventana_registro_nombre, text='').pack()
        Label(ventana_registro_nombre, text='Nombre de usuario').pack()
        entrada_usuario = Entry(ventana_registro_nombre, textvariable=nombre)
        entrada_usuario.pack()
        Label(ventana_registro_nombre, text='').pack()
        Button(ventana_registro_nombre, text='Ingresar', width=10, height=1, bg='LightGreen',
               command=lambda: comprobar_registro_nombre(ventana_principal, ventana_registro_nombre, nombre.get(),
                                                         etiqueta_resultado, dic_jugador, cantidad)).pack()
        Label(ventana_registro_nombre, text='').pack()
        etiqueta_resultado = Label(ventana_registro_nombre, text='')
        etiqueta_resultado.pack()


def login(ventana_principal, dic_jugador, cantidad):
    if not any(isinstance(x, Toplevel) for x in ventana_principal.winfo_children()):
        ventana_login = Toplevel(ventana_principal)
        ventana_login.title('Acceso a cuenta')
        ventana_login.geometry('300x250')
        Label(ventana_login, text='').pack()
        usuario = StringVar(ventana_login)
        contraseña = StringVar(ventana_login)
        Label(ventana_login, text='Nombre de usuario').pack()
        entrada_usuario = Entry(ventana_login, textvariable=usuario)
        entrada_usuario.pack()
        Label(ventana_login, text='').pack()
        Label(ventana_login, text='Contraseña').pack()
        entrada_contraseña = Entry(ventana_login, textvariable=contraseña, show='*')
        entrada_contraseña.pack()
        Label(ventana_login, text='').pack()
        ingresar = Button(ventana_login, text='Acceder', width=10, height=1, bg='LightGreen',
                          command=lambda: comprobar_login(usuario_Y_contraseña(usuario, contraseña),
                                                          ventana_principal, ventana_login,
                                                          entrada_usuario, entrada_contraseña,
                                                          etiqueta_resultado, dic_jugador, ingresar, cantidad))
        ingresar.pack()
        Label(ventana_login, text='').pack()
        etiqueta_resultado = Label(ventana_login, text='')
        etiqueta_resultado.pack()

principal()