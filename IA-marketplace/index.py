from iniciar_sesion import iniciarSesion
from extraer_datos import get_products
from obtener_links import obtener_todos_links
import random, time, schedule


def scrapear_marketplace(max_productos=None):
    ## Iniciar sesión en Facebook y obtener el driver
    driver = iniciarSesion()
    
    ## obtener los links de los productos
    ##links = obtener_todos_links(driver)
    
    ## Extraer los datos de los productos usando los links obtenidos
    ##if not links: print("No se encontraron links de productos.")
        
    
    
     # Función interna para ejecutar get_products periódicamente
    def tarea_get_products():
        print("Ejecutando extracción de productos...")
        nuevos = get_products(driver, max_productos)
        print("Extracción completada.")
        return nuevos
    # Ejecuta la primera vez inmediatamente
    while True:
        nuevos = tarea_get_products()
        if not nuevos:
            print("¡Todos los productos han sido guardados!")
            break
        # Espera antes de la siguiente tanda para evitar bloqueos
        espera = random.randint(15, 20) * 60
        print(f"Esperando {espera//60} minutos para la próxima tanda...")
        time.sleep(espera)

if __name__ == "__main__":
    scrapear_marketplace(max_productos=random.randint(80, 100))  # Puedes ajustar el rango según tus necesidades
    

   



