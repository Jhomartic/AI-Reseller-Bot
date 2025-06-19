from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time


def hacer_scroll(driver):
        contador += 1
        print(f"Scroll número: {contador}")
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(7)  # Espera para que cargue el contenido
            
            
            
    # while True:
    #     contador += 1
    #     print(f"Scroll número: {contador}")
    #     try:
    #         # Busca el texto "Más resultados fuera de tu zona"
    #         driver.find_element(By.XPATH, "//*[contains(text(), 'Más resultados fuera de tu zona')]")
    #         print("¡Sección encontrada!")
    #         time.sleep(20)
    #         break
    #     except NoSuchElementException:
    #         # Si no se encuentra, haz scroll hacia abajo
    #         driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    #         time.sleep(5)  # Espera para que cargue el contenido                              
      