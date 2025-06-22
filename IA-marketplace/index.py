from iniciar_sesion import iniciarSesion
from extraer_datos import get_products
from obtener_links import obtener_todos_links
import random, time, schedule


def scrapear_marketplace(max_productos=None):
    ## Iniciar sesión en Facebook y obtener el driver
    driver = iniciarSesion()
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
            espera = random.randint(15, 20) * 60
            print(f"Esperando {espera//60} minutos para la próxima tanda...")
            time.sleep(espera)

        # 3. Espera antes de volver a obtener todos los links (para detectar productos nuevos)
        print("Esperando 10 minutos antes de volver a buscar nuevos productos...")
        time.sleep(600)  # Espera 10 minutos antes de volver a scrapear links


if __name__ == "__main__":
    scrapear_marketplace(max_productos=random.randint(80, 100))  # Puedes ajustar el rango según tus necesidades
    

   



