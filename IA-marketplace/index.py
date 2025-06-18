from iniciar_sesion import iniciarSesion
import time
from selenium.common.exceptions import NoSuchElementException
from extraer_datos import extraer_datos
from selenium.webdriver.common.by import By


def scrapear_marketplace():
    driver = iniciarSesion()
    if driver:
      driver.get("https://www.facebook.com/marketplace/category/cell-phones")
      time.sleep(2)   
    # Tiempo de duracion haciendo 20 scrolls 2:16s
      # scroll_hasta_mas_resultados(driver)
      extraer_datos(driver, 4)  
    
def scroll_hasta_mas_resultados(driver):
    while True:
        try:
            # Busca el texto "Más resultados fuera de tu zona"
            driver.find_element(By.XPATH, "//*[contains(text(), 'Más resultados fuera de tu zona')]")
            print("¡Sección encontrada!")
            time.sleep(20)
            break
        except NoSuchElementException:
            # Si no se encuentra, haz scroll hacia abajo
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(5)  # Espera para que cargue el contenido               
      


if __name__ == "__main__":
    scrapear_marketplace()
    

   



