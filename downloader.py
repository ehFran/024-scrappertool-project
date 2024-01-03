import streamlit as st
from playwright.sync_api import sync_playwright

class Descargador():

    @staticmethod
    def descargar_web(pagina):
        """
        Descarga el contenido de una página web utilizando Playwright.

        Parameters:
        - pagina (str): La URL de la página web que se desea descargar.

        Returns:
        - str: Contenido HTML de la página web.
        """

        # Definir el User-Agent que simula un navegador web
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'

        # Iniciar el contexto de Playwright
        with sync_playwright() as playwright:

            # Lanzar un navegador web (WebKit)
            browser = playwright.webkit.launch(headless=False, slow_mo=1000)

            # Crear una nueva página en el navegador
            page = browser.new_page()

            # Establecer el encabezado User-Agent en la solicitud
            page.set_extra_http_headers({"User-Agent": user_agent})

            # Navegar a la URL proporcionada
            page.goto(pagina)
            # Esperar a que la página cargue completamente
            page.wait_for_load_state('load')

            # Obtener el contenido HTML de la página
            content = page.content()

            # Cerrar el navegador
            browser.close()

            # Devolver el contenido
            return content


