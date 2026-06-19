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


def login(driver, usuario, password):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

  
def test_login_exitoso(driver):
    login(driver, "standard_user", "secret_sauce")
    assert "inventory" in driver.current_url


def test_login_error(driver):
    login(driver, "standard_user", "clave_mala")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.is_displayed()
    assert "inventory" not in driver.current_url


def test_login_vacio(driver):
    login(driver, "standard_user", " ")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.is_displayed()
    assert "inventory" not in driver.current_url


def test_inventario_muestra_productos(driver):
    login(driver, "standard_user", "secret_sauce")
    wait = WebDriverWait(driver, 10)
    productos = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    assert len(productos) > 0

def test_agregar_producto_al_carrito(driver):
    login(driver, "standard_user", "secret_sauce")
    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack")))
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    contador = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert contador.text == "1"
   
def test_checkout_ok(driver):
    login(driver, "standard_user", "secret_sauce")
    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack")))
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()  
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link")))
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()  
    wait.until(EC.presence_of_element_located((By.ID, "checkout")))
    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.presence_of_element_located((By.ID, "first-name")))
    driver.find_element(By.ID, "first-name").send_keys("Estefany")
    wait.until(EC.presence_of_element_located((By.ID, "last-name")))
    driver.find_element(By.ID, "last-name").send_keys("Mora")
    wait.until(EC.presence_of_element_located((By.ID, "postal-code")))
    driver.find_element(By.ID, "postal-code").send_keys("8150000")
    wait.until(EC.presence_of_element_located((By.ID, "continue")))
    driver.find_element(By.ID, "continue").click()
    wait.until(EC.presence_of_element_located((By.ID, "finish")))
    driver.find_element(By.ID, "finish").click()
    mensaje = driver.find_element(By.CLASS_NAME, "complete-header")
    assert "Thank you" in mensaje.text

