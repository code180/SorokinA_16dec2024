import requests
import pytest
import allure

BASE_URL = "https://altaivita.ru/engine/cart"
COOKIES = {
    "CID": "9eb130fc0a3c4f5732a17c6d501d1d",
    "PHPSESSID": "b4kg7a5h74t1jim67olt9hfqn2",
    "_userGUID": "0m4mvmby:RK5ZRPuKfVNJAjBE970j1FG5uvig8",
    "site_countryID": "247"
}

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "; ".join([f"{key}={value}" for key, value in COOKIES.items()])
}


@allure.feature("Корзина")
@allure.story("Добавление товара в корзину")
@pytest.mark.parametrize("product_id, quantity", [(6554, 1)])
def test_add_product_to_cart(product_id, quantity):
    """
    Проверка успешного добавления товара в корзину.
    """
    with allure.step("Формирование данных запроса"):
        payload = {
            "product_id": product_id,
            "LANG_key": "ru",
            "S_wh": "1",
            "S_CID": COOKIES["CID"],
            "S_cur_code": "rub",
            "S_koef": "1",
            "quantity": quantity,
            "S_hint_code": "",
            "S_customerID": ""
        }

    with allure.step("Отправка POST-запроса на добавление товара в корзину"):
        response = requests.post(f"{BASE_URL}/add_products_to_cart_from_preview.php", headers=HEADERS, data=payload)

    with allure.step("Проверка ответа"):
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        assert "error" not in response.text, "Response contains error"


@allure.feature("Корзина")
@allure.story("Изменение количества товара в корзине")
@pytest.mark.parametrize("product_id, quantity", [(6554, 5)])
def test_update_product_quantity_in_cart(product_id, quantity):
    """
    Проверка успешного изменения количества товара в корзине.
    """
    with allure.step("Формирование данных запроса"):
        payload = {
            "product_id": product_id,
            "LANG_key": "ru",
            "S_wh": "1",
            "S_CID": COOKIES["CID"],
            "S_cur_code": "rub",
            "S_koef": "1",
            "quantity": quantity,
            "S_hint_code": "",
            "S_customerID": ""
        }

    with allure.step("Отправка POST-запроса на изменение количества товара"):
        response = requests.post(f"{BASE_URL}/add_products_to_cart_from_preview.php", headers=HEADERS, data=payload)

    with allure.step("Проверка ответа"):
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        assert "error" not in response.text, "Response contains error"
