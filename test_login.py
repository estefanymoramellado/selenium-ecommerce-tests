from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_abrir_saucedemo():
    driver = webdriver.Edge()

    driver.get("https://www.saucedemo.com/")

    time.sleep(2)

    assert driver.title == "Swag Labs"

    driver.quit()