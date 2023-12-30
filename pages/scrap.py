from io import BytesIO
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

perfil_pccomp = {
    'Container': "soup.find_all('div', class_='product-card')",
    'Producto': "div.find('h3', class_='product-card__title').text.strip()",
    'Vendedor': "div.find('span', class_='card-seller-name').text.strip()",
    'Precio':  "div.find('span', class_='sc-dUOoGL') or div.find('span', class_='goySsD')",
    'Imagen': "div.find('img', class_='sc-lpYOg')['src']"
}

perfil_zalando = {
    'Container': "soup.find_all('div', class_='_5qdMrS')",
    'Producto': "div.find('h3', class_='sDq_FX').text.strip()",
    'Vendedor': "div.find('h3', class_='FtrEr_').text.strip()",
    'Precio': "div.find('span', class_='sDq_FX').text.strip()",
    'Imagen': "div.find('img', class_='sDq_FX')['src']"
}

perfil_coolmod = {
    'Container': "soup.find_all('div', class_='df-card__content')",
    'Producto': "div.find('div', class_='df-card__title').text.strip()",
    'Vendedor': "''",  # No hay información del vendedor en el fragmento proporcionado
    'Precio':  "div.find('span', class_='df-card__price').text.strip() if div.find('span', class_='df-card__price') else ''",
    'Imagen': "div.find('img', class_='df-card__image')['src']"
}


def obtener_info_producto(div, perfil):
    try:
        producto = eval(perfil['Producto'])
        precio_elem = eval(perfil['Precio'])
        precio = precio_elem.text.strip() if precio_elem else None
        vendedor = eval(perfil['Vendedor'])
        imagen = eval(perfil['Imagen'])

        return {'Producto': producto, 'Precio': precio, 'Vendedor': vendedor, 'Imagen': imagen}
    except Exception as e:
        st.error(f'Ocurrió un error al obtener la información del producto: {str(e)}')
        return None


def mostrar_tabla(datosproductos):
    # Mostrar el DataFrame con la imagen dentro de la tabla
    st.table(datosproductos)

def main(perfil):
    uploaded_file = st.file_uploader("Selecciona un archivo")

    if st.button('Analizar archivo') and uploaded_file is not None:
        try:
            content = uploaded_file.read().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')

            # Obtener la lista de divs que contienen la información del producto
            divs_productos = eval(perfil['Container'])

            # Crear una lista de diccionarios con la información de cada producto
            productos_info = [obtener_info_producto(div, perfil) for div in divs_productos]

            # Crear un DataFrame
            datosproductos = pd.DataFrame(productos_info)

            # Mostrar la tabla
            mostrar_tabla(datosproductos)
            st.success('Archivo analizado correctamente.')

        except Exception as e:
            st.error(f'Ocurrió un error: {str(e)}')

if __name__ == "__main__":
    # Llamada a la función principal con el perfil de pccomp
    main(perfil_coolmod)

# PERFILES


