import streamlit as st
from playwright.sync_api import sync_playwright
import os

st.header('Web Scraper DEF')

pagina = st.text_input('Seleccione la página a descargar','https://www.pccomponentes.com/' )
producto = st.text_input('Producto', 'laptop')
numero_paginas = st.number_input('Seleccione el número de paginas a descargar', 1)

def download_amazon_products(pagina, query, page_from=1, page_to=numero_paginas, export_location='.', user_agent=None):
    
    os.makedirs(export_location, exist_ok=True)

    with sync_playwright() as playwright:

        browser = playwright.webkit.launch(headless=False, slow_mo=1000)

        page = browser.new_page()

        if user_agent:
            # Set the User-Agent header
            page.set_extra_http_headers({"User-Agent": user_agent})

        for page_num in range(page_from, page_to + 1):
            page.goto(f'{pagina}')
            page.wait_for_load_state('load')

            with open(f'{export_location}/{query}_{page_num}.html', 'w', encoding='utf-8') as f:
                f.write(page.content())

        browser.close()

if __name__ == '__main__':
    query = producto
    export_location = './export' 
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'


if st.button('Descargar'):
    download_amazon_products(pagina, query, page_from=1, page_to=numero_paginas, export_location=export_location, user_agent=user_agent)

