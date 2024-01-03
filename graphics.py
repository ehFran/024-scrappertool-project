import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Graphics():

    @staticmethod
    def generar_estadisticas_outliers(data_frame):
        """
        Genera estadísticas outliers.

        Parameters:
        - data_frame (pd.DataFrame): DataFrame de entrada.

        Returns:
        - Tuple: Estadísticas de precios, umbral de outliers, límite inferior, límite superior, outliers.
        """
        if data_frame is not None:
            price_stats = data_frame['Precio'].describe()
            outlier_threshold = 1.5
            lower_bound = price_stats['25%'] - outlier_threshold * (price_stats['75%'] - price_stats['25%'])
            upper_bound = price_stats['75%'] + outlier_threshold * (price_stats['75%'] - price_stats['25%'])
            outliers = data_frame[(data_frame['Precio'] < lower_bound) | (data_frame['Precio'] > upper_bound)]

            return price_stats, outlier_threshold, lower_bound, upper_bound, outliers
        else:
            return pd.Series(), 0, 0, 0, pd.DataFrame()

    # Funciones de visualización de datos

    @staticmethod
    def visualizar_histograma(data_frame):
        """
        Visualiza el histograma de precios.

        Parameters:
        - data_frame (pd.DataFrame): DataFrame de entrada.
        """
        st.subheader('Histograma de Precios')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data_frame['Precio'], kde=True, ax=ax)
        plt.title('Distribución de Precios')
        plt.xlabel('Precio')
        plt.ylabel('Frecuencia')
        st.pyplot(fig)

    @staticmethod
    def visualizar_densidad(data_frame):
        """
        Visualiza el gráfico de densidad de precios.

        Parameters:
        - data_frame (pd.DataFrame): DataFrame de entrada.
        """
        st.subheader('Gráfico de Densidad')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.kdeplot(data_frame['Precio'], fill=True, ax=ax)
        plt.title('Gráfico de Densidad de Precios')
        plt.xlabel('Precio')
        plt.ylabel('Densidad')
        st.pyplot(fig)

    @staticmethod
    def visualizar_productos_vendedor(data_frame):
        """
        Visualiza el gráfico de barras de productos por vendedor.

        Parameters:
        - data_frame (pd.DataFrame): DataFrame de entrada.
        """
        vendedor_counts = data_frame['Vendedor'].value_counts()

        st.subheader('Productos por vendedor')
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=vendedor_counts.index, y=vendedor_counts.values, ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.title('Cantidad de Productos por Vendedor')
        plt.xlabel('Vendedor')
        plt.ylabel('Cantidad de Productos')
        st.pyplot(fig)

    @staticmethod
    def visualizar_precios_vendedor(data_frame):
        """
        Visualiza el gráfico de barras de la media de precios por vendedor.

        Parameters:
        - data_frame (pd.DataFrame): DataFrame de entrada.
        """
        mean_prices_by_vendedor = data_frame.groupby('Vendedor')['Precio'].mean().sort_values()

        st.subheader('Media de Precios por Vendedor')
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=mean_prices_by_vendedor.index, y=mean_prices_by_vendedor.values, ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.title('Media de Precios por Vendedor')
        plt.xlabel('Vendedor')
        plt.ylabel('Media de Precios')
        st.pyplot(fig)

    @staticmethod
    def visualizar_outliners_boxplot(data_frame):
        """
        Visualiza el diagrama de caja (boxplot) para identificar outliers.

        Parameters:
        - data_frame (pd.DataFrame): DataFrame de entrada.
        """
        st.subheader('Análisis de Outliers en Precios')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x=data_frame['Precio'], ax=ax)
        plt.title('Diagrama de Caja: Precios')
        plt.xlabel('Precio')
        st.pyplot(fig)

    @staticmethod
    def mostrar_estadisticas_outliers(price_stats, outlier_threshold, lower_bound, upper_bound, outliers):
        """
        Muestra información sobre los outliers.

        Parameters:
        - price_stats (pd.Series): Estadísticas de precios.
        - outlier_threshold (float): Umbral para outliers.
        - lower_bound (float): Límite inferior.
        - upper_bound (float): Límite superior.
        - outliers (pd.DataFrame): DataFrame que contiene los outliers.
        """
        st.subheader('Información sobre Outliers:')
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Outliers", len(outliers))
        with col2:
            st.metric("Valor Mínimo", price_stats["min"])
        with col3:
            st.metric("Valor Máximo", price_stats["max"])
        with col4:
            st.metric("Rango Intercuartílico (IQR)", round(price_stats["75%"] - price_stats["25%"], 3))
        with col5:
            st.metric("Umbral para Outliers", outlier_threshold)
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.metric("Límite Inferior", round(lower_bound, 3))
        with col3:
            st.metric("Límite Superior", round(upper_bound, 3))
        st.write('Outliers:')
        st.write(outliers)

    @staticmethod
    def visualizar_outliers_productos(data_frame, outliers):
        """
        Visualiza los outliers en el conjunto de datos.

        Parameters:
        - data_frame (pd.DataFrame): DataFrame de entrada.
        - outliers (pd.DataFrame): DataFrame que contiene los outliers.
        """
        st.subheader('Visualización de Outliers en Precios')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x=data_frame.index, y=data_frame['Precio'], ax=ax)
        sns.scatterplot(x=outliers.index, y=outliers['Precio'], color='red', label='Outliers', ax=ax)
        plt.title('Visualización de Outliers en Precios')
        plt.xlabel('Índice del Producto')
        plt.ylabel('Precio')
        st.pyplot(fig)