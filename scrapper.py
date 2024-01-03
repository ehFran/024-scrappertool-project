
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

    def define_perfiles(self, div, perfil):
        """
        Define el perfil del producto a partir de un fragmento HTML.

        Parameters:
        - div (bs4.element.Tag): Fragmento HTML que contiene información del producto.
        - perfil (dict): Perfil de scraping que define cómo extraer información del fragmento.

        Returns:
        - dict: Información del producto.
        """
        producto = perfil['Producto'](div)
        precio_elem = perfil['Precio'](div)
        precio = precio_elem.text.strip() if precio_elem else None
        vendedor = perfil['Vendedor'](div)
        imagen = perfil['Imagen'](div)

        return {'Producto': producto, 'Precio': precio, 'Vendedor': vendedor, 'Imagen': imagen}

    def scrap_info_product(self, perfil):
        """
        Scrap información de productos desde un archivo HTML.

        Parameters:
        - perfil (dict): Perfil de scraping que define cómo extraer información del fragmento.

        Returns:
        - pd.DataFrame: DataFrame con la información de los productos.
        """
        uploaded_file = st.file_uploader("Selecciona un archivo")

        datosproductos = []

        if uploaded_file is not None:
            try:
                content = uploaded_file.read().decode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')
                divs_productos = perfil['Container'](soup)
                productos_info = [self.define_perfiles(div, perfil) for div in divs_productos]

                datosproductos = pd.DataFrame(productos_info)
                datosproductos['Precio'] = datosproductos['Precio'].str.replace('.', '').str.replace(',', '.').str.replace('€', '').astype(float)

                nuevo_orden_columnas = ["Imagen", "Producto", "Precio", "Vendedor"]
                datosproductos = datosproductos[nuevo_orden_columnas]
                
                with st.expander('Mostrar tabla de productos'):
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

                    st.download_button(
                        label="Descargar como CSV",
                        data=datosproductos.to_csv(index=False).encode('utf-8'),
                        file_name='productos.csv',
                        mime='text/csv'
                    )

            except Exception as e:
                st.error(f"Error al procesar el archivo: {str(e)}")

        return datosproductos