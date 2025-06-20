from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, re, json, os, datetime, random
from obtener_links import cargar_links_json 

def get_products(driver, max_productos=None):
    links = cargar_links_json()
    productos_guardados = cargar_productos_json()
    links_guardados = set(p["link"] for p in productos_guardados)  
    
    # Filtra los links para que solo queden los que NO están guardados
    links_nuevos = [link for link in links if link not in links_guardados]
    
      # Si max_productos está definido, solo toma esa cantidad
    if max_productos is not None:
        links_nuevos = links_nuevos[:max_productos]
    
    
    productos_nuevos = []
    for link in links_nuevos:
        if link in links_guardados: continue
        productos_nuevos.append(get_producto(link, driver))
           
    lista_productos = productos_guardados + productos_nuevos
    guardar_productos_json(lista_productos)
    ## imprimir cantidad de prodcutos nuevos
    if productos_nuevos:
        print(f"Se encontraron {len(productos_nuevos)} productos nuevos.")
    else:
        print("No se encontraron productos nuevos.")
    
    print(f"Total de productos guardados: {len(lista_productos)}")  
    
    return productos_nuevos   



def get_producto(link, driver):
    driver.get(link)
    time.sleep(random.uniform(4, 7)) 
        
    producto = {
        "titulo": get_titulo(driver),
        "precio": get_precio(driver),
        "descripcion": get_descripcion(driver),
        "imagenes": get_imagenes(driver),
        "link": link,
        "fecha_scraping": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    return producto
        
        
       
        

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

def cargar_productos_json():
    if os.path.exists("productos.json"):
        with open("productos.json", "r", encoding="utf-8") as f:
            productos = json.load(f)
    else:
      productos = []
      
    return productos

def guardar_productos_json(productos):
    with open("productos.json", "w", encoding="utf-8") as f:
      json.dump(productos, f, ensure_ascii=False, indent=2)