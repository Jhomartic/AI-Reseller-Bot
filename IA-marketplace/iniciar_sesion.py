from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os, pickle, random, time

COOKIES_FILE = "facebook_cookies.pkl"
CHROMEDRIVER_PATH = r"C:\drivers\chromedriver.exe"

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

def iniciarSesion_facebook():
    driver.get("https://www.facebook.com")
    time.sleep(3)
    if not os.path.exists(COOKIES_FILE):
        time.sleep(40)
        guardar_cookies(driver, COOKIES_FILE)
        time.sleep(2)
        driver.quit()
        return None
    else:
        cargar_cookies(driver, COOKIES_FILE)
        driver.get("https://www.facebook.com/marketplace/category/cell-phones")
        time.sleep(random.uniform(2, 4))   
        return driver


def cargar_cookies(driver, COOKIES_FILE):
    with open(COOKIES_FILE, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if "sameSite" in cookie:
                cookie.pop("sameSite")
            driver.add_cookie(cookie)
            
def guardar_cookies(driver, COOKIES_FILE):
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)            

