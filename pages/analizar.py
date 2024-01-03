import streamlit as st
import pandas as pd
from graphics import Graphics

def cargar_archivo():
    """
    File Uploader para subir el archivo CSV.

    Returns:
    - pd.DataFrame or None: DataFrame cargado desde el archivo o None si no se carga ningún archivo.
    """
    archivo = st.file_uploader('Subir CSV:')
    if archivo is not None:
        try:
            return pd.read_csv(archivo)
        except pd.errors.EmptyDataError:
            st.error("El archivo CSV está vacío.")
        except pd.errors.ParserError:
            st.error("Error al procesar el archivo CSV.")
    return None

def cargar_estilos():
    """
    Carga estilos adicionales para la página.
    """
    estilos = """
        <style>
            .st-emotion-cache-1y4p8pa{
            max-width: 75vw !important;
            }
        </style>
    """
    st.markdown(estilos, unsafe_allow_html=True)

def main():

    # Instancia de Graphics
    graphics = Graphics()

    # Estilos de la página
    cargar_estilos()

    # Cargamos el data frame
    df = cargar_archivo()

    if df is not None:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.data_editor(
                df,
                column_config={
                    "Imagen": st.column_config.ImageColumn(
                        "Imagen", help="Imagen productos", width='small'
                    ),
                    "Precio": st.column_config.NumberColumn(
                        "Precio (en EUR)",
                        help="Precio del producto en EUR",
                        format="€%.2f",
                    ),
                },
                hide_index=True,
            )

        with col2:
            precio_info = df['Precio'].describe()
            st.write(precio_info)

        # Generar estadísticas
        price_stats, outlier_threshold, lower_bound, upper_bound, outliers = graphics.generar_estadisticas_outliers(df)

        # Sistema de columnas
        col1, col2 = st.columns(2)

        with col1:
            graphics.visualizar_histograma(df)
        with col2:
            graphics.visualizar_densidad(df)

        with col1:
            graphics.visualizar_productos_vendedor(df)
        with col2: 
            graphics.visualizar_precios_vendedor(df)

        graphics.mostrar_estadisticas_outliers(price_stats, outlier_threshold, lower_bound, upper_bound, outliers)
        graphics.visualizar_outliers_productos(df, outliers)

if __name__ == "__main__":
    main()