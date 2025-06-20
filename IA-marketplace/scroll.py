from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time, random


def hacer_scroll(driver):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        print("Haciendo scroll...")
        time.sleep(random.uniform(6, 12))  # Espera para que cargue el contenido
            
            
  