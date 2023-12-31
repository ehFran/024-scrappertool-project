import sqlite3
import pandas as pd

class ConectaDB():

    def __init__(self):

        # Crear la conexión a la base de datos
        self.conn = sqlite3.connect('productos.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla 'productos' si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                Producto TEXT,
                Precio TEXT,
                Vendedor TEXT,
                Imagen TEXT
            )
        ''')
        self.conn.commit()

    def save_dataframe(self, dataframe):
        # Guarda el dataframe en la tabla productos
        dataframe.to_sql('productos', self.conn, if_exists='append', index=False)

    def get_all_data(self):
        # Consulta para obtener todos los datos de la tabla 'productos'
        query = 'SELECT * FROM productos'
        
        # Ejecutar la consulta y recuperar los resultados como un DataFrame
        result = pd.read_sql_query(query, self.conn)
        
        return result