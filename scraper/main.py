import streamlit as st
import pandas as pd
from conecta_db import ConectaDB
from scrapper import Scrapper


scrap = Scrapper()

nombres_perfiles = [perfil['Nombre'] for perfil in scrap.perfiles]

# Crear el selectbox
perfil_seleccionado = st.selectbox('Selecciona un perfil:', nombres_perfiles)

perfil = next((p for p in scrap.perfiles if p['Nombre'] == perfil_seleccionado), None)


scrap.scrap_info_product(perfil)






