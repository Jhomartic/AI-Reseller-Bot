from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import  re, json, os
import time
from scroll import hacer_scroll



def obtener_links(driver, max_productos=None, max_scrolls=None):
   scroll_count = 0
   while True:
       links = filtrar_links(driver, max_productos)
       guardar_links_json(links)  # Esta función debe actualizar links.json sin duplicados
       if max_scrolls == 0:
        print("max_scrolls es 0, no se hace scroll.")
        break
        # Condición para max_scrolls > 0
       if max_scrolls is not None and max_scrolls > 0:
          if scroll_count >= max_scrolls:
            print("Se alcanzó el máximo de scrolls.")
            break
       try:
            # Busca el texto "Más resultados fuera de tu zona"
            driver.find_element(By.XPATH, "//*[contains(text(), 'Más resultados fuera de tu zona')]")
            print("¡Sección encontrada!")
            time.sleep(20)
            break
       except NoSuchElementException:
            hacer_scroll(driver)
            scroll_count += 1
            time.sleep(2) 
                       
   return links    




def filtrar_links(driver, max_productos=None):
    
    producto = driver.find_elements(By.CSS_SELECTOR, ".x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x135b78x.x11lfxj5.x1iorvi4.xjkvuk6.xnpuxes.x1cjf5ee.x17dddeq")
    # Lee los links existentes desde links.json (si existe)
    links_guardados = cargar_links_json()
    
    links = []
    productos_a_procesar = producto if max_productos is None else producto[:max_productos]
    for producto in productos_a_procesar:
        try:
             # Ajusta el selector según el HTML real de la ubicación
            ubicacion = producto.find_element(By.CSS_SELECTOR, "div.x1gslohp.xkh6y0r div.x1iorvi4 span.x4zkp8e.x3x7a5m").text.lower()
            print(ubicacion)
            if ubicacion and "cartagena de indias" not in ubicacion:
                print(f"Producto omitido, ubicación no es Cartagena de Indias: {ubicacion}")
                continue  # Salta si no es de Cartagena de Indias
            
            link = producto.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            if link and "facebook.com/marketplace/item/" in link and link not in links_guardados and link not in links:
                link = limpiar_link(link)
                links.append(link)
        except NoSuchElementException:
            continue

    # Une los links antiguos y los nuevos, sin duplicados
    links_nuevos = [l for l in links if l not in links_guardados]
    todos_los_links = links_guardados + links_nuevos
    print( f"Se encontraron {len(links_nuevos)} nuevos links.")
    print(f"Total de links encontrados: {len(todos_los_links)}")
    # Guarda la lista actualizada en links.json
    guardar_links_json(todos_los_links)
    links = cargar_links_json()
    
    return links

def limpiar_link(link):
    match = re.search(r"(https://www\.facebook\.com/marketplace/item/\d+)", link)
    if match:
        return match.group(1)
    return link


def cargar_links_json():
    if os.path.exists("links.json"):
        with open("links.json", "r", encoding="utf-8") as f:
            links = json.load(f)
    else:
        links = []
    
    return links 

def guardar_links_json(links):
    with open("links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)

