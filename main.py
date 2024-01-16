import streamlit as st
import pandas as pd
from scrapper import Scrapper
from downloader import Descargador

# Estilos de la página
estilos = """
    <style>
        .st-emotion-cache-1y4p8pa{
        max-width: 75vw !important;
        }
    </style>
"""
st.markdown(estilos, unsafe_allow_html=True)
descargador = Descargador()
# Sección de descargar páginas html
st.subheader('Descargar Página Web')

# Campo de entrada para la URL
pagina = st.text_input('Ingrese la URL de la página web:', '')

contenido = None

# Botón para descargar
if st.button('Recopilar información') and pagina:
    contenido = descargador.descargar_web(pagina)
    st.text('Contenido recopilado:')
    st.text_area('Contenido:', contenido, height=400)
    st.download_button(
            label="Descargar Contenido",
            data=contenido.encode('utf-8'),
            file_name='contenido.html',
            mime='text/html'
        )


st.divider()

# Sección de Scrapper
st.subheader("Generar CSV a partir de HTML:")

# Scrapper
scrap = Scrapper()
# Selector de perfiles
nombres_perfiles = [perfil['Nombre'] for perfil in scrap.perfiles]
# Selectbox
perfil_seleccionado = st.selectbox('Selecciona un perfil:', nombres_perfiles)
# Identifica el prefil seleccionado
perfil = next((p for p in scrap.perfiles if p['Nombre'] == perfil_seleccionado), None)
# Scrappea los datos usando el perfil seleccionado
datoslist = scrap.scrap_info_product(perfil)

st.divider()


# Sección de preguntas frequentes
st.subheader("FAQ:")

with st.expander("¿Cómo funciona la página?"):
    st.write('La herramienta consta de dos partes, la primera desde, main permite descargar el código html de una web y transformarlo a csv. La segunda lee el documento csv y realiza un pequeño analisis de los productos obtenidos.')

with st.expander("¿Qué son los perfiles?"):
    st.write('Los perfiles son diccionarios con las etiquetas y las clases de los productos a scrapear.')

with st.expander("¿Como añado un perfil nuevo?"):
    st.write('De momento la herramienta no soporta la subida de perfiles. Esta feature se introducirá más adelante.')

with st.expander("¿Qué páginas puedo scrapear"):
    st.write('De momento solo hay perfiles disponibles para PCcomponentes y CoolMood.')


