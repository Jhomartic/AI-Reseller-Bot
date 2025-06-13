from utils import acceder_con_cookies, login_manual_y_guardar_cookies
import os

COOKIES_FILE = "facebook_cookies.pkl"

def iniciarSesion():
    if not os.path.exists(COOKIES_FILE):
        print("No hay cookies guardadas.")
        login_manual_y_guardar_cookies()
        return None
    else:
        driver = acceder_con_cookies()
        return driver
    