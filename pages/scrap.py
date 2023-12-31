from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import sqlite3

# Crear la conexión a la base de datos
conn = sqlite3.connect('productos.db')
cursor = conn.cursor()

# Crear la tabla 'productos' si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        Producto TEXT,
        Precio TEXT,
        Vendedor TEXT,
        Imagen TEXT
    )
''')
conn.commit()

# Definir perfiles
perfil_pccomp = {
    'Nombre': 'PcComp',
    'Container': "soup.find_all('div', class_='product-card')",
    'Producto': "div.find('h3', class_='product-card__title').text.strip()",
    'Vendedor': "div.find('span', class_='card-seller-name').text.strip()",
    'Precio':  "div.find('span', class_='sc-dUOoGL') or div.find('span', class_='goySsD')",
    'Imagen': "div.find('img', class_='sc-lpYOg')['src']"
}

perfil_zalando = {
    'Nombre': 'Zalando',
    'Container': "soup.find_all('div', class_='xCblER')",
    'Producto': "div.find('h3', class_='sDq_FX').text.strip()",
    'Vendedor': "div.find('h3', class_='FtrEr_').text.strip()",
    'Precio': "div.find('span', class_='sDq_FX').text.strip()",
    'Imagen': "div.find('img', class_='sDq_FX')['src']"
}

perfil_coolmod = {
    'Nombre': 'CoolMod',
    'Container': "soup.find_all('div', class_='df-card')",
    'Producto': "div.find('div', class_='df-card__title').text.strip()",
    'Vendedor': "''",  # No hay información del vendedor en el fragmento proporcionado
    'Precio':  "div.find('span', class_='df-card__price')",
    'Imagen': "div.find('img', class_='')['src']"
}


perfiles = [perfil_pccomp]  # Agrega otros perfiles según sea necesario
nombres_perfiles = [perfil['Nombre'] for perfil in perfiles]

perfil_seleccionado = st.selectbox('Selecciona un perfil:', nombres_perfiles)
perfil = next((p for p in perfiles if p['Nombre'] == perfil_seleccionado), None)

def obtener_info_producto(div, perfil):
    producto = eval(perfil['Producto'])
    precio_elem = eval(perfil['Precio'])
    precio = precio_elem.text.strip() if precio_elem else None
    vendedor = eval(perfil['Vendedor'])
    imagen = eval(perfil['Imagen'])

    return {'Producto': producto, 'Precio': precio, 'Vendedor': vendedor, 'Imagen': imagen}

def mostrar_datos_almacenados():
    query = "SELECT * FROM productos"
    result = pd.read_sql(query, conn)
    st.write("Datos almacenados en la base de datos:")
    st.dataframe(result)

def main(perfil):
    uploaded_file = st.file_uploader("Selecciona un archivo")

    mostrar_datos_almacenados()
    
    if st.button('Analizar archivo') and uploaded_file is not None:
        content = uploaded_file.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        divs_productos = eval(perfil['Container'])
        productos_info = [obtener_info_producto(div, perfil) for div in divs_productos]
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

        if st.button('Guardar en base de datos'):
            datosproductos.to_sql('productos', conn, if_exists='append', index=False)

        st.write(datosproductos['Precio'].describe())

        st.success('Archivo analizado correctamente.')

# Ejecutar la aplicación
if __name__ == "__main__":
    main(perfil)

# Cierra la conexión al finalizar
conn.close()
