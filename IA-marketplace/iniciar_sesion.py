from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import pickle
import time

COOKIES_FILE = "facebook_cookies.pkl"
CHROMEDRIVER_PATH = r"C:\drivers\chromedriver.exe"

def iniciarSesion():
    if not os.path.exists(COOKIES_FILE):
        print("No hay cookies guardadas.")
        login_manual_y_guardar_cookies()
        return None
    else:
        driver = acceder_con_cookies()
        return driver

def guardar_cookies(driver, COOKIES_FILE):
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def login_manual_y_guardar_cookies():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.facebook.com")
    print("Por favor, inicia sesión manualmente, resuelve el captcha si hay, y accede a Facebook.")
    time.sleep(40)
    guardar_cookies(driver, COOKIES_FILE)
    print("Cookies guardadas con éxito.")
    time.sleep(2)
    driver.quit()

def cargar_cookies(driver, COOKIES_FILE):
    with open(COOKIES_FILE, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if "sameSite" in cookie:
                cookie.pop("sameSite")
            driver.add_cookie(cookie)

def acceder_con_cookies():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.facebook.com/")
    time.sleep(3)
    cargar_cookies(driver, COOKIES_FILE)
    return driver
