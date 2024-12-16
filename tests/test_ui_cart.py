import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Корзина")
@allure.story("Добавление товара в корзину через UI")
def test_add_specific_product_to_cart_ui():
    """
    Проверка добавления конкретного товара с data-product-id=6554 в корзину через интерфейс.
    """
    # Инициализация драйвера
    browser = webdriver.Chrome(service=ChromeService())

    try:
        with allure.step("Открытие браузера, максимизация окна и переход на страницу категории"):
            browser.maximize_window()  # Установка полноэкранного режима
            browser.get("https://altaivita.ru/category/chajnye-sbory/")
            assert "Купить травяной чай (Фиточай)" in browser.title, "Страница категории не загрузилась"

            cookie = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "fa-times-circle"))
            )
            cookie.click()

        with allure.step("Прокрутка страницы вниз для отображения товара"):
            # Скроллинг страницы
            browser.execute_script("window.scrollBy(0, 400);")


            product_card = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product__item_ajax_zero_element"))
            )
            assert product_card.get_attribute("data-product-id") == "1280"

        with allure.step("Добавление товара в корзину"):
            add_to_cart_button = product_card.find_element(By.CLASS_NAME, "js-product__add_2_0_cat_preview_1280")
            add_to_cart_button.click()

            with allure.step("Проверка появления всплывающего окна"):
                popup = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "action-notification_add_to_cart"))
                )
                assert popup.text == "Товар добавлен в корзину"
    finally:
        browser.quit()

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Корзина")
@allure.story("Удаление товара из корзины через UI")
def test_remove_product_from_cart_ui():
    """
    Проверка удаления конкретного товара с data-product-id=1280 из корзины через интерфейс.
    """
    # Инициализация драйвера
    browser = webdriver.Chrome(service=ChromeService())

    try:
        with allure.step("Открытие браузера, максимизация окна и переход на страницу категории"):
            browser.maximize_window()
            browser.get("https://altaivita.ru/category/chajnye-sbory/")
            assert "Купить травяной чай (Фиточай)" in browser.title, "Страница категории не загрузилась"

            # Закрытие окна с cookie
            cookie = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "fa-times-circle"))
            )
            cookie.click()

        with allure.step("Прокрутка страницы вниз и добавление товара в корзину"):
            # Скроллинг страницы
            browser.execute_script("window.scrollBy(0, 400);")

            product_card = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product__item_ajax_zero_element"))
            )
            assert product_card.get_attribute("data-product-id") == "1280"

            # Добавление товара в корзину
            add_to_cart_button = product_card.find_element(By.CLASS_NAME, "js-product__add_2_0_cat_preview_1280")
            add_to_cart_button.click()

            # Проверка появления уведомления
            popup = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "action-notification_add_to_cart"))
            )
            assert popup.text == "Товар добавлен в корзину"

        with allure.step("Переход в корзину и удаление товара"):
            # Переход в корзину
            browser.get("https://altaivita.ru/cart/")

            # Поиск товара в корзине
            cart_item = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "js-cart-item"))
            )

            # Удаление товара
            remove_button = cart_item.find_element(By.CLASS_NAME, "js-item-delete")
            remove_button.click()

            # Ожидание исчезновения товара из корзины
            WebDriverWait(browser, 10).until(
                EC.invisibility_of_element((By.CLASS_NAME, "cart__item"))
            )

        with allure.step("Проверка, что корзина пуста"):
            empty_cart = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "js-total"))
            )
            assert "0" in empty_cart.text

    finally:
        browser.quit()
