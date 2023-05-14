import time
from main import filter_geo, unique_id, find_max_volume_channel
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.parametrize('country, expected_count', [
    ('Россия', 6)
])
def test_filter_geo_logs_by_country(country, expected_count):
    filtered_logs = filter_geo()
    actual_count = len(filtered_logs)
    assert actual_count == expected_count


@pytest.mark.parametrize("expected_result", [
    [213, 15, 54, 119, 98, 35].sort(),
])
def test_unique_id(expected_result):
    assert unique_id() == expected_result


@pytest.mark.parametrize("stats, expected_channel", [
    ({'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}, 'yandex'),
    ({'facebook': 10, 'yandex': 20, 'vk': 30, 'google': 40, 'email': 50, 'ok': 60}, 'ok'),
    ({'facebook': 70, 'yandex': 50, 'vk': 80, 'google': 90, 'email': 30, 'ok': 40}, 'google')
])
def test_find_max_volume_channel(stats, expected_channel):
    assert find_max_volume_channel(stats) == expected_channel


@pytest.fixture
def token():
    return 'your_yandex_disk_token_here'


@pytest.mark.parametrize('folder_name, path, expected_status_code', [
    ('', '', 400),  # Создание папки в корне диска без имени
    ('test_folder', '', 201),  # Создание папки в корне диска с заданным именем
    ('', '/my_dir', 400),  # Создание папки в заданной директории без имени
    ('test_folder', '/my_dir', 201),  # Создание папки в заданной директории с заданным именем
    ('test_folder', '', 409),  # Попытка создания папки с уже существующим именем в корне диска
    ('test_folder', '/my_dir', 409),  # Попытка создания папки с уже существующим именем в заданной директории
])
def test_create_folder_yandex_disk(token, folder_name, path, expected_status_code):
    headers = {
        'Authorization': f'OAuth {token}'
    }
    params = {
        'path': f'{path}/{folder_name}'
    }
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                            headers=headers,
                            params=params)
    assert response.status_code == expected_status_code


@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.mark.parametrize('username, password', [
    ('ЛОГИН', 'ПАРОЛЬ'),
    ('', ''),
    ('userfahwjfawf', ''),
    ('фацлафца', 'fawlfawf')
])
def test_yandex_auth(browser, username, password):
    browser.get('https://passport.yandex.ru/auth/')

    input_login = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, 'passp-field-login')))
    input_login.send_keys(username)
    input_login.send_keys(Keys.RETURN)
    time.sleep(2)
    input_password = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
    input_password.send_keys(password)
    input_password.send_keys(Keys.RETURN)

    try:
        element = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.ID, 'passp-field-phoneCode'))
        )
    except:
        element = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'auth-challenge-form-hint'))
        )

    assert element is not None
