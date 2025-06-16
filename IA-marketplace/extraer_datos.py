from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
import json

def extraer_datos(driver, max_productos=None):
    productos = driver.find_elements(By.CSS_SELECTOR, ".x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x135b78x.x11lfxj5.x1iorvi4.xjkvuk6.xnpuxes.x1cjf5ee.x17dddeq")
    links = get_links(productos, max_productos)      
    lista_productos = []
    for indx, link in enumerate(links, start=1):
        driver.get(link)
        
        
        time.sleep(4)
        ## enumerar productos
        titulo = get_titulo(driver)
        precio = get_precio(driver)
        descrip = get_descripcion(driver)
        imagenes = get_imagenes(driver)
        
        lista_productos.append({
          "id": indx,  
          "titulo": titulo,
          "precio": precio,
          "descripcion": descrip,
          "imagenes": imagenes,
          "link": link
        })
    lista_productos = json.dumps(lista_productos, ensure_ascii=False, indent=2)    
    with open("productos.json", "w", encoding="utf-8") as f:
       f.write(lista_productos)
        
    return lista_productos    

def get_links(productos, max_productos):
    links = []
    for producto in productos[:max_productos]:
        try:
            link = producto.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            if "facebook.com/marketplace/item/" in link:
              links.append(link)  
        except NoSuchElementException:
            continue 
    return links    

def get_titulo(driver):
    try:
        titulo = driver.find_element(By.CSS_SELECTOR, "h1 span.x193iq5w").text
    except NoSuchElementException:
        titulo = "No hay titulo"
    return titulo 

def get_precio(driver):
    try:
        precio = driver.find_element(By.CSS_SELECTOR, "div.x1xmf6yo span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.xk50ysn.xzsf02u").text
        precio = limpiar_precio(precio)
    except NoSuchElementException:
        precio = "No hay precio"
    return precio   

def limpiar_precio(precio_str):
    precio_str = precio_str.lower()
    if "gratis" in precio_str:
        return "No puso precio"
    # Busca el primer grupo de dígitos y puntos (para miles)
    match = re.search(r'(\d{1,3}(?:[.\s]\d{3})*)', precio_str)
    if not match:
        return None
    # Limpia puntos y espacios, convierte a int
    precio = int(match.group(1).replace('.', '').replace(' ', ''))
    if precio < 1000:
        precio *= 1000
    return precio

def get_descripcion(driver):
    try:
        descrip = driver.find_element(By.CSS_SELECTOR, "div.x9f619.x1n2onr6 div.xz9dl7a.xyri2b div span.xo1l8bm").text
    except NoSuchElementException:
        descrip = "No hay descripcion"
    return descrip

def get_imagenes(driver):
    try:
        imagenes = driver.find_elements(By.CSS_SELECTOR, "img.x1fmog5m.xu25z0z.x140muxe.xo1y3bh.x5yr21d.xl1xv1r.xh8yej3")
        imagenes_urls = []
        for imagen in imagenes:
            src = imagen.get_attribute("src")
            if src and src not in imagenes_urls:
                imagenes_urls.append(src)
    except NoSuchElementException:
        imagenes_urls = []
    return imagenes_urls