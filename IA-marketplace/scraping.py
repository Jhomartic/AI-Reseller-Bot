from iniciar_sesion import iniciarSesion
import time
from extraer_datos import extraer_datos

def scrapear_marketplace():
    driver = iniciarSesion()
    if driver:
      driver.get("https://www.facebook.com/marketplace/category/cell-phones")
      time.sleep(3)   
    #   hacer scroll para cargar mas productos
    #     # for _ in range(1):
    #     #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     #     time.sleep(6)
      productos = extraer_datos(driver)  
      print(productos)
            
      


if __name__ == "__main__":
    scrapear_marketplace()
    

   



