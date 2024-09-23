import serial, time, sys, glob                    # Importaciones
import tkinter as tk                              
from tkinter import ttk
from ttkthemes import ThemedTk                   # Permite aplicar temas visuales 
from PIL import Image, ImageTk                   # Permite manipular imagenes

root = ThemedTk(theme='elegance')
root.config(width=600, height=500)               # Tamaño de la Ventana
root.title("Comunicacion con puerto serial")     # Título de la Ventana 
tabControl = ttk.Notebook(root)                  # Contenedor para las pestañas 

tab1 = ttk.Frame(tabControl)                     # Creamos las pestañas
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='TAB1')                # Se añaden las pestañas al contenedor, nombre y posicion 
tabControl.add(tab2, text='TAB2')
tabControl.add(tab3, text='TAB3')

tabControl.grid(row=0, column=0, sticky="nsew")  # sticky: controla el como se estira y se alinea 

#TAB1_____________________________________________________________________________________________________________

# Imagenes para mostrar el estado de la conexión con Arduino
ImagenOriginal = Image.open(r"C:\Users\mario\Pictures\Screenshots\LedVerde.png").resize((150, 150)) 
ImagenConectado = ImageTk.PhotoImage(ImagenOriginal)       # Imagen de conexión exitosa

ImagenOriginal2 = Image.open(r"C:\Users\mario\Pictures\Screenshots\LedRojo.png").resize((150, 150)) 
ImagenDesconectado = ImageTk.PhotoImage(ImagenOriginal2)   # Imagen de conexión fallida/desconectada

label_imagen = tk.Label(tab1, image=ImagenDesconectado)    # Mostrar LED rojo (desconectado) por defecto
label_imagen.grid(column=0, row=4, padx=3, pady=3)

#Puertos COM
result = []                                                     #Lista Vacia 
def serial_ports():
    if sys.platform.startswith('win'):                     #Windows 
        ports = ['COM%s' % (i + 1) for i in range(256)]    #Se genera una lista de puertos COM, desde COM1 hasta COM256
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'): #Linux
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):   #IOS
        ports = glob.glob('/dev/tty.*')  
    else:
        raise EnvironmentError('Unsupported platform') #Si el sistema operativo no es uno de los anteriores
    global result                                      
    for port in ports:      #Intenta abrir un puerto, si puede lo cierra y lo agrega a la lista 
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Seleccionar Puertos
current_value = tk.StringVar()  #se utilizará para almacenar el valor seleccionado en el combo box (lista desplegable).
puerto = ttk.Combobox(tab1, textvariable=current_value)
print(serial_ports())    #Llama a la funcion 
puerto['values'] = result    #Lista de Puertos 
puerto.grid(column=0, row=1, padx=3, pady=3)

# Velocidad de conexión
velocidad = ttk.Combobox(tab1, text="Velocidad de Transmision",
                         state="readonly",
                         values=["9600", "115200"])
velocidad.grid(column=1, row=1, padx=3, pady=3)

# RECONFIGURACIÓN DE PUERTOS COM
arduino = None  #Sin conexion
def config():   #Establecer conexion 
    global arduino
    global puerto_seleccionado, velocidad_seleccionada 
    puerto_seleccionado = puerto.get()
    velocidad_seleccionada = velocidad.get()
    
    print(f"Intentando conectar a {puerto_seleccionado} con velocidad {velocidad_seleccionada}")
    
    try:
        arduino = serial.Serial(puerto_seleccionado, int(velocidad_seleccionada), timeout=1) #Realiza la conexion
        print(f"Conectado a {puerto_seleccionado}")
        label_imagen.config(image=ImagenConectado)  # Muestra la imagen de conexión exitosa (verde)
    except serial.SerialException as e:
        print(f"Error al conectar: {e}")
        label_imagen.config(image=ImagenDesconectado)  # Muestra la imagen de desconexión (rojo)

# Funciones para encender y apagar el LED
def Encender():
    if arduino:
        print('Encendiendo LED')
        arduino.write(b'1')
        time.sleep(0.05)

def Apagar():
    if arduino:
        print('Apagando LED')
        arduino.write(b'0')
        time.sleep(0.05)

# Botones
Texto1 = ttk.Label(tab1, text="Selecciona el Puerto", font=("Helvetica", 10, "bold"))
Texto1.grid(column=0, row=0, padx=3, pady=3)
Texto2 = ttk.Label(tab1, text="Selecciona la Velocidad", font=("Helvetica", 10, "bold"))
Texto2.grid(column=1, row=0, padx=3, pady=3)

# Botones para encender y apagar el LED (funcionan solo si está conectado)
Valor1 = ttk.Button(tab1, text="Led OFF", command=Apagar)
Valor1.grid(column=0, row=5, padx=3, pady=3)
Valor2 = ttk.Button(tab1, text="Led ON", command=Encender)
Valor2.grid(column=1, row=5, padx=3, pady=3)

# Botón de conectar
conectar = tk.Button(tab1, text="Conectar", command=config)
conectar.grid(column=1, row=2, padx=3, pady=3)

#TAB2_____________________________________________________________________________________________________________
def Operaciones():
    var = int(seleccion.get())
    print(var)
    if var == 1:
        print('Operacion 1: Suma')
        Valor1.config(state='normal')
        BottonAccion.config(state='normal')                                                       
        button2.config(state="disabled")        #seleccion 2
        mostrar.config(state="disabled")      
        pwm_inten.config(state="disabled")          #seleccion 3
        button3.config(state="disabled")     
    elif var == 2:
        print('Operacion 2: Voltaje Variable')
        Valor1.config(state='disabled')          #seleccion 1
        BottonAccion.config(state='disabled')                                                                
        button2.config(state="normal")          #seleccion 2
        mostrar.config(state="normal")     
        pwm_inten.config(state="disabled")          #seleccion 3
        button3.config(state="disabled")  
        
    elif var == 3:
        print('Operacion 3: PWM')
        Valor1.config(state='disabled')          #seleccion 1
        BottonAccion.config(state='disabled')                                                               
        button2.config(state="disabled")        #seleccion 2
        mostrar.config(state="disabled")      
        pwm_inten.config(state="normal")        #seleccion 3
        button3.config(state="normal")  

def suma():
    if arduino:
        selec_value = Valor1.get()  # Obtén el valor del Entry
        if selec_value.isdigit():   # Asegúrate de que sea un número
           print(f"Enviando para suma: S{selec_value}")
           arduino.write(f'S{selec_value}\n'.encode())  # Enviar comando "S" seguido del número
           time.sleep(0.05)
           data = arduino.readline().decode().strip()   # Leer la respuesta de Arduino
           print(f"Resultado recibido: {data}")
           # Mostrar el resultado en consola o interfaz
        else:
           print("Por favor, ingresa un número válido.")
         
def convercion():
    if arduino:
        print("Leyendo voltaje...")
        arduino.write(b'LEER\n')  # Envía el comando para leer el voltaje
        time.sleep(0.05)
        data = arduino.readline().decode().strip()  # Leer la respuesta de Arduino
        mostrar.delete(0, tk.END)  # Limpia el campo de entrada antes de mostrar el nuevo valor
        mostrar.insert(0, data)    # Muestra el voltaje en el campo de entrada
        print(f"Voltaje recibido: {data}")

def Pwm():
    if arduino:
        pwm_value = pwm_inten.get()  # Obtener el valor de PWM
        if pwm_value.isdigit() and 0 <= int(pwm_value) <= 255:  # Asegúrate de que esté en rango
            print(f"Enviando intensidad PWM: P{pwm_value}")
            arduino.write(f'P{pwm_value}\n'.encode())  # Enviar comando "P" seguido del valor PWM
            time.sleep(0.05)
            data = arduino.readline().decode().strip()  # Leer la respuesta de Arduino
            print(f"Respuesta recibida: {data}")
        else:
            print("Por favor, ingresa un valor entre 0 y 255.")
      
#Control de las Opciones   
ins0 = ttk.Label(tab2, text="Seleccione una opcion para habilitarla",font=("Helvetica", 10, "bold"))
ins0.grid(column=0, row=0, padx=3, pady=3)
seleccion = ttk.Spinbox(tab2, from_=1, to=3, increment=1, state="readonly")
seleccion.grid(column=0, row=1, padx=3, pady=3)
BottonSeleccion = ttk.Button(tab2, text='Iniciar', command=Operaciones)
BottonSeleccion.grid(column=1, row=1, padx=3, pady=3)

#Operacion 1 
ins1 = ttk.Label(tab2, text="1) Ingrese un valor y su valor se le sumara una unidad",font=("Helvetica", 10, "bold"))
ins1.grid(column=0, row=2, padx=3, pady=3)
Valor1 = ttk.Entry(tab2, state="disabled")
Valor1.grid(column=0, row=3, padx=3, pady=3)
BottonAccion = ttk.Button(tab2, text='SUMA', state="disabled", command=suma)
BottonAccion.grid(column=1, row=3, padx=3, pady=3)

#Operacion 2
ins2 = ttk.Label(tab2, text="2) Muestra el voltaje de una resistencia variable",font=("Helvetica", 10, "bold"))
ins2.grid(column=0, row=4, padx=3, pady=3)
button2 = ttk.Button(tab2, text='Convertir', state="disabled", command=convercion)
button2.grid(column=0, row=5, padx=3, pady=3)
mostrar = ttk.Entry(tab2, state="disabled")
mostrar.grid(column=1, row=5, padx=3, pady=3)

#Operacion3
ins2 = ttk.Label(tab2, text="3) Modifica la intencidad del led ingresando un valor de 0 a 255",font=("Helvetica", 10, "bold"))
ins2.grid(column=0, row=6, padx=3, pady=3)
pwm_inten = ttk.Entry(tab2, state="disabled")
pwm_inten.grid(column=0, row=7, padx=3, pady=3)
button3 = ttk.Button(tab2, text='Intensidad', state="disabled", command=Pwm)        
button3.grid(column=1, row=7, padx=3, pady=3)
     
#TAB3_______________________________________________________________________________________________________________                   
DATO = ttk.Label(tab3, text="Integrantes de Equipo:",font=("Helvetica", 15, "bold"))
DATO.grid(column=0, row=0, padx=3, pady=3) 
DATO1 = ttk.Label(tab3, text="Mario Cruz Romero, Azael Beltran Marcial Y Dulce Maria Corte Tepale",font=("Helvetica", 10, "bold"))
DATO1.grid(column=0, row=1, padx=3, pady=3)  

Logo = Image.open(r"C:\Users\mario\Pictures\Screenshots\Logo.png").resize((150, 150)) 
Logo1 = ImageTk.PhotoImage(Logo)       
Logo2 = tk.Label(tab3, image=Logo1)    
Logo2.grid(column=0, row=3, padx=3, pady=3)

root.mainloop()