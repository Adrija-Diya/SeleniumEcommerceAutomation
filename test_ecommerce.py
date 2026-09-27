import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


BASE_URL = "https://tutorialsninja.com/demo/"


def load_test_data():
    with open("test_data/test_data.json", "r") as file:
        return json.load(file)


def take_screenshot(driver, name):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")


def handle_alert(driver):
    try:
        alert = driver.switch_to.alert
        print("Alert detected:", alert.text)
        alert.accept()
    except NoAlertPresentException:
        print("No browser alert present.")


def test_ecommerce_purchase_flow():

    # -----------------------------------------
    # 1. Load test data
    # -----------------------------------------
    data = load_test_data()

    first_name = data["first_name"]
    last_name = data["last_name"]
    telephone = data["telephone"]
    password = data["password"]
    email_prefix = data["email_prefix"]
    product_name = data["product"]
    quantity = data["quantity"]

    # Generate unique email
    timestamp = int(time.time())
    email = f"{email_prefix}.{timestamp}@example.com"

    # -----------------------------------------
    # 2. Launch browser
    # -----------------------------------------
    driver = webdriver.Chrome()
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    try:

        # -----------------------------------------
        # 3. Open application
        # -----------------------------------------
        driver.get(BASE_URL)

        assert driver.title == "Your Store"

        take_screenshot(driver, "01_homepage")

        # -----------------------------------------
        # 4. Register new account
        # -----------------------------------------
        driver.get(BASE_URL + "index.php?route=account/register")

        wait.until(
            EC.visibility_of_element_located((By.NAME, "firstname"))
        ).send_keys(first_name)

        driver.find_element(By.NAME, "lastname").send_keys(last_name)

        driver.find_element(By.NAME, "email").send_keys(email)

        driver.find_element(By.NAME, "telephone").send_keys(telephone)

        driver.find_element(By.NAME, "password").send_keys(password)

        driver.find_element(By.NAME, "confirm").send_keys(password)

        driver.find_element(By.NAME, "agree").click()

        driver.find_element(
            By.XPATH, "//input[@value='Continue']"
        ).click()

        wait.until(
            EC.url_contains("route=account/success")
        )

        print("Account registration successful.")

        take_screenshot(driver, "02_registration_success")

        # -----------------------------------------
        # 5. Logout
        # -----------------------------------------
        driver.get(BASE_URL + "index.php?route=account/logout")

        # -----------------------------------------
        # 6. Login
        # -----------------------------------------
        driver.get(BASE_URL + "index.php?route=account/login")

        wait.until(
            EC.visibility_of_element_located((By.NAME, "email"))
        ).send_keys(email)

        driver.find_element(By.NAME, "password").send_keys(password)

        driver.find_element(
            By.XPATH, "//input[@value='Login']"
        ).click()

        wait.until(
            EC.url_contains("route=account/account")
        )

        print("Login successful.")

        take_screenshot(driver, "03_login_success")

        # -----------------------------------------
        # 7. Search product
        # -----------------------------------------
        search_box = wait.until(
            EC.visibility_of_element_located((By.NAME, "search"))
        )

        search_box.clear()
        search_box.send_keys(product_name)

        driver.find_element(
            By.CSS_SELECTOR, "button.btn.btn-default.btn-lg"
        ).click()

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//a[contains(text(), '{product_name}')]")
            )
        )

        print(f"Product '{product_name}' found.")

        take_screenshot(driver, "04_product_search")

        # -----------------------------------------
        # 8. Open product
        # -----------------------------------------
        driver.find_element(
            By.XPATH, f"//a[contains(text(), '{product_name}')]"
        ).click()

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@id, 'button-cart')]")
            )
        )

        take_screenshot(driver, "05_product_page")

        # -----------------------------------------
        # 9. Add product to cart
        # -----------------------------------------
        driver.find_element(
            By.ID, "button-cart"
        ).click()

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".alert-success")
            )
        )

        print("Product added to cart.")

        take_screenshot(driver, "06_product_added")

        # -----------------------------------------
        # 10. Open cart using success message
        # -----------------------------------------
        cart_link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'alert-success')]//a[contains(@href,'checkout/cart')]")
            )
        )

        cart_link.click()

        wait.until(
            EC.url_contains("route=checkout/cart")
        )

        print("Shopping cart opened successfully.")

        take_screenshot(driver, "07_cart_page")

        # -----------------------------------------
        # 11. Verify product in cart
        # -----------------------------------------
        cart_product = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[@id='content']//table//a[contains(normalize-space(.), '{product_name}')]"
                )
            )
        )

        assert cart_product.is_displayed()

        print("Product verified in cart.")

        # -----------------------------------------
        # 12. Update quantity
        # -----------------------------------------
        quantity_box = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[@id='content']//table//tr[.//a[contains(normalize-space(.), '{product_name}')]]//input[contains(@name, 'quantity')]"
                )
            )
        )

        quantity_box.clear()
        quantity_box.send_keys(quantity)

        update_button = driver.find_element(
            By.XPATH,
            f"//div[@id='content']//table//tr[.//a[contains(normalize-space(.), '{product_name}')]]//button[@data-original-title='Update']"
        )

        update_button.click()

        wait.until(
            lambda d: d.find_element(
                By.XPATH,
                f"//div[@id='content']//table//tr[.//a[contains(normalize-space(.), '{product_name}')]]//input[contains(@name, 'quantity')]"
            ).get_attribute("value") == quantity
        )

        updated_quantity = driver.find_element(
            By.XPATH,
            f"//div[@id='content']//table//tr[.//a[contains(normalize-space(.), '{product_name}')]]//input[contains(@name, 'quantity')]"
        ).get_attribute("value")

        # -----------------------------------------
        # 13. Verify quantity
        # -----------------------------------------
        assert updated_quantity == quantity

        print(f"Quantity successfully updated to {quantity}.")

        take_screenshot(driver, "08_cart_verified")

        # -----------------------------------------
        # 14. Final cart verification
        # -----------------------------------------
        assert product_name in driver.page_source

        print("===================================")
        print("TEST COMPLETED SUCCESSFULLY")
        print("Product:", product_name)
        print("Quantity:", quantity)
        print("Email:", email)
        print("===================================")

    finally:

        # -----------------------------------------
        # 15. Close browser
        # -----------------------------------------
        driver.quit()