from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

class Scrapper():

    def __init__(self):
        # Definir perfiles como atributos de la clase usando self
        self.perfil_pccomp = {
            'Nombre': 'PcComp',
            'Container': lambda soup: soup.find_all('div', class_='product-card'),
            'Producto': lambda div: div.find('h3', class_='product-card__title').text.strip(),
            'Vendedor': lambda div: div.find('span', class_='card-seller-name').text.strip(),
            'Precio':  lambda div: div.find('span', class_='sc-dUOoGL') or div.find('span', class_='goySsD'),
            'Imagen': lambda div: div.find('img', class_='sc-lpYOg')['src']
        }

        self.perfil_coolmod = {
            'Nombre': 'CoolMod',
            'Container': lambda soup: soup.find_all('div', class_='df-card'),
            'Producto': lambda div: div.find('div', class_='df-card__title').text.strip(),
            'Vendedor': lambda div: '',  # No hay información del vendedor en el fragmento proporcionado
            'Precio':  lambda div: div.find('span', class_='df-card__price'),
            'Imagen': lambda div: div.find('img', class_='')['src']
        }

        self.perfiles = [self.perfil_pccomp, self.perfil_coolmod]

    def define_profile(self, div, perfil):
        producto = perfil['Producto'](div)
        precio_elem = perfil['Precio'](div)
        precio = precio_elem.text.strip() if precio_elem else None
        vendedor = perfil['Vendedor'](div)
        imagen = perfil['Imagen'](div)

        return {'Producto': producto, 'Precio': precio, 'Vendedor': vendedor, 'Imagen': imagen}

    def scrap_info_product(self, perfil):

        # Subir archivo
        uploaded_file = st.file_uploader("Selecciona un archivo")

        # Inicializar productos_info como una lista vacía
        datosproductos = []

        if st.button('Analizar archivo') and uploaded_file is not None:
            content = uploaded_file.read().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            divs_productos = perfil['Container'](soup)
            productos_info = [self.define_profile(div, perfil) for div in divs_productos]

            datosproductos = pd.DataFrame(productos_info)
            datosproductos['Precio'] = datosproductos['Precio'].str.replace('.', '').str.replace(',', '.').str.replace('€', '').astype(float)

            st.data_editor(
                datosproductos,
                column_config={
                    "Imagen": st.column_config.ImageColumn(
                        "Imagen", help="Imagen productos", width='medium'
                    ),
                    "Precio": st.column_config.NumberColumn(
                    "Precio (en EUR)",
                    help="Precio del producto en EUR",
                    format="€%.2f",
                    ),
                },
                hide_index=True,
            )
        
        return datosproductos
