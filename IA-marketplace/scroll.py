import time, random


def hacer_scroll(driver):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        print("Haciendo scroll...")
        time.sleep(random.randint(6, 10))  # Espera para que cargue el contenido
            
            
  