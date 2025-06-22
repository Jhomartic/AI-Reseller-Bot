from iniciar_sesion import iniciarSesion_facebook
from extraer_datos import get_products
from obtener_links import obtener_todos_links
import random, time


def scrapear_marketplace(max_productos=None):
    ## Iniciar sesión en Facebook y obtener el driver
    driver = iniciarSesion_facebook()
    while True:
        # 1. Obtener todos los links actuales
        links = obtener_todos_links(driver)
        if not links:
            print("No se encontraron links de productos.")
            break

        # 2. Extraer productos en tandas hasta que no queden nuevos
        def tarea_get_products():
            print("Ejecutando extracción de productos...")
            nuevos = get_products(driver, max_productos)
            print("Extracción completada.")
            return nuevos

        while True:
            nuevos = tarea_get_products()
            if not nuevos:
                print("¡Todos los productos han sido guardados!")
                break
            espera = random.randint(9, 15) * 60
            print(f"Esperando {espera//60} minutos para la próxima tanda...")
            time.sleep(espera)
            
        driver.get("https://www.facebook.com/marketplace/category/cell-phones")    


if __name__ == "__main__":
    scrapear_marketplace(max_productos=random.randint(90, 100))  # Puedes ajustar el rango según tus necesidades
    

   



