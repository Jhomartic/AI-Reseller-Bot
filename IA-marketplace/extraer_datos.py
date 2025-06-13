from selenium.webdriver.common.by import By

def extraer_datos(driver):
    productos = driver.find_elements(By.CSS_SELECTOR, ".x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x135b78x.x11lfxj5.x1iorvi4.xjkvuk6.xnpuxes.x1cjf5ee.x17dddeq")
    lista_productos = []
    for producto in productos[:8]:
          try:
               datos = producto.find_element(By.CSS_SELECTOR, "[class*='xdj266r']").text
               link = producto.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
               lista_productos.append([*datos.splitlines(), link]) 
               
          except: 
              continue
             
           
    productos_filtrados = [item for item in lista_productos if len(item) == 4]     
    return productos_filtrados