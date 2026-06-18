from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_login_exitoso():
    driver = webdriver.Edge()
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)

    campo_usuario = driver.find_element(By.ID, "user-name")
    campo_usuario.send_keys("standard_user")

    campo_password = driver.find_element(By.ID, "password")
    campo_password.send_keys("secret_sauce")

    boton_login = driver.find_element(By.ID, "login-button")
    boton_login.click()

    time.sleep(2)

    assert "inventory" in driver.current_url

    driver.quit()