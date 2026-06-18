import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Edge()
    driver.get("https://www.saucedemo.com/")
    yield driver        
    driver.quit()         


def hacer_login(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory"))


def test_login_exitoso(driver):
    hacer_login(driver)
    assert "inventory" in driver.current_url


def test_inventario_muestra_productos(driver):
    hacer_login(driver)
    wait = WebDriverWait(driver, 10)
    productos = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    assert len(productos) > 0