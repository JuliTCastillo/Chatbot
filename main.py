import streamlit as st #importar la libreria
from groq import Groq

#Le damos un titulo a la pestaña de la web
st.set_page_config(page_title="Mi chat de IA", page_icon="🎮") 

#Titulo de la pagina
st.title("Mi primera aplacación con Streamlit")

#Ingreso de datos
nombre = st.text_input("¿Cuál es tu nombre?")

#Crear un botón con funcionalidad
if st.button("Saludar") :
    st.write(f"¡Hola, {nombre}! Gracias por venir a Talento Tech")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Nos conectamos a API
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #Obtiene la clave de la API
    return Groq(api_key = clave_secreta) #Conectamos con la API

#Configuramos el Modelo que se va a usar
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #Indica el modelo de la IA
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True #Para que el modelo responda a tiempo
    )

#Historial de mensaje
def inicializar_estado():
    #Si no existe una lista llamada "mensajes" -> creamos uno
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Lista vacia (Historial vacio)

def actualizar_historial(rol, contenido, avatar):
    #El metodo apped() agrega un elemento a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar" : avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : 
            st.markdown(mensaje["content"])

#Contenedor del chat
def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    #Agrupamos los mensajes en el area del chat
    with contenedorDelChat : mostrar_historial()

#? CREANDO FUNCIÓN -> con diseño de la pagina
def configurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración")
    seleccion = st.sidebar.selectbox(
        "Elegí un modelo", #Titulo
        MODELO, #Tiene que estar en una lista
        index = 0 #datoDefecto
    )

    return seleccion #Devuelve un dato

def generar_respuestas(chat_completo):
    respuesta_completa = "" #Texto vacio
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa 

def main(): #Función principal
    #INVOCACIÓN DE FUNCIONES
    modelo = configurar_pagina() #llamamos a la función
    clienteUsuario = crear_usuario_groq() #Crea el usuario para usar la API
    inicializar_estado() #Crea el historial vacio de mensaje
    area_chat() #? Creamos el sector para ver los mensajes
    mensaje = st.chat_input("Escribí tu mensaje...")

    #Verificamos si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "👩‍🏫") #Visualizamos el msg del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
            st.rerun()
                
#Indicamos que nuestra función principal es main()
if __name__ == "__main__":
    main()