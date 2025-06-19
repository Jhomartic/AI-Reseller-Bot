from iniciar_sesion import iniciarSesion
import time
from selenium.common.exceptions import NoSuchElementException
from extraer_datos import extraer_datos
from selenium.webdriver.common.by import By
from obtener_links import obtener_links
from scroll import hacer_scroll


def scrapear_marketplace(max_productos=None, max_scrolls=None):
    driver = iniciarSesion()
    if driver:
      driver.get("https://www.facebook.com/marketplace/category/cell-phones")
      time.sleep(2)   
    links = obtener_links(driver, max_productos, max_scrolls)
    extraer_datos(driver, links)  
    

if __name__ == "__main__":
    scrapear_marketplace(max_productos=None ,max_scrolls=0)
    

   



