from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, re, json, os, datetime


def extraer_datos(driver, max_productos=None):
    productos = driver.find_elements(By.CSS_SELECTOR, ".x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x135b78x.x11lfxj5.x1iorvi4.xjkvuk6.xnpuxes.x1cjf5ee.x17dddeq")
    links = get_links(productos, max_productos) 
    lista_productos = get_products(driver, links)  

    return lista_productos 
      

def get_links(productos, max_productos=None):
    # Lee los links existentes desde links.json (si existe)
    if os.path.exists("links.json"):
        with open("links.json", "r", encoding="utf-8") as f:
            links_guardados = json.load(f)
    else:
        links_guardados = []

    links = []
    productos_a_procesar = productos if max_productos is None else productos[:max_productos]
    for producto in productos_a_procesar:
        try:
            link = producto.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            if link and "facebook.com/marketplace/item/" in link and link not in links_guardados and link not in links:
                link = limpiar_link(link)
                links.append(link)
        except NoSuchElementException:
            continue

    # Une los links antiguos y los nuevos, sin duplicados
    todos_los_links = links_guardados + [l for l in links if l not in links_guardados]

    # Guarda la lista actualizada en links.json
    with open("links.json", "w", encoding="utf-8") as f:
        json.dump(todos_los_links, f, ensure_ascii=False, indent=2)

    return links

def limpiar_link(link):
    match = re.search(r"(https://www\.facebook\.com/marketplace/item/\d+)", link)
    if match:
        return match.group(1)
    return link

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

def get_products(driver, links):
    
    if os.path.exists("productos.json"):
        with open("productos.json", "r", encoding="utf-8") as f:
            productos_guardados = json.load(f)
    else:
      productos_guardados = []
      
    links_guardados = set(p["link"] for p in productos_guardados)  
        
    productos_nuevos = []
    for link in links:
        if link in links_guardados:
            continue
        driver.get(link)
        time.sleep(5)  # Espera a que la página cargue
        
        producto = {
            "titulo": get_titulo(driver),
            "precio": get_precio(driver),
            "descripcion": get_descripcion(driver),
            "imagenes": get_imagenes(driver),
            "link": link,
            "fecha_scraping": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        productos_nuevos.append(producto)
        
    lista_productos = productos_guardados + productos_nuevos
    ## imprimir cantidad de prodcutos nuevos
    if productos_nuevos:
        print(f"Se encontraron {len(productos_nuevos)} productos nuevos.")
    else:
        print("No se encontraron productos nuevos.")
    
    print(f"Total de productos guardados: {len(lista_productos)}")    
    
    with open("productos.json", "w", encoding="utf-8") as f:
      json.dump(lista_productos, f, ensure_ascii=False, indent=2)
      
    return lista_productos