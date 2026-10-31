import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions  # Изменено на Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Формируем абсолютный путь к нашему HTML файлу
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PATH = f"file://{os.path.join(CURRENT_DIR, '../app/index.html')}"


@pytest.fixture
def driver():
    # Настройка опций для Microsoft Edge
    options = EdgeOptions()
    options.add_argument("--headless=new")  # Фоновый режим для CI
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера Edge
    browser = webdriver.Edge(options=options)
    browser.get(APP_PATH)
    yield browser
    browser.quit()


def test_add_task(driver):
    # Сценарий 1: Успешное добавление задачи
    wait = WebDriverWait(driver, 5)
    input_field = wait.until(EC.visibility_of_element_located((By.ID, "task-input")))
    input_field.send_keys("Подготовить отчет по практике")
    driver.find_element(By.ID, "add-btn").click()

    task_list = driver.find_elements(By.CLASS_NAME, "task-item")
    assert len(task_list) == 1
    assert "Подготовить отчет по практике" in task_list[0].text


def test_complete_task(driver):
    # Сценарий 2: Отметка задачи как выполненной
    driver.find_element(By.ID, "task-input").send_keys("Сдать практическую работу")
    driver.find_element(By.ID, "add-btn").click()

    task_text = driver.find_element(By.CLASS_NAME, "task-text")
    task_text.click()

    task_item = driver.find_element(By.CLASS_NAME, "task-item")
    # Проверяем, что класс изменился (добавился 'completed')
    assert "completed" in task_item.get_attribute("class")


def test_delete_task(driver):
    # Сценарий 3: Удаление задачи
    driver.find_element(By.ID, "task-input").send_keys("Временная задача")
    driver.find_element(By.ID, "add-btn").click()

    assert len(driver.find_elements(By.CLASS_NAME, "task-item")) == 1

    delete_btn = driver.find_element(By.CLASS_NAME, "delete-btn")
    delete_btn.click()

    # Убеждаемся, что список пуст
    wait = WebDriverWait(driver, 5)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "task-item")))
    assert len(driver.find_elements(By.CLASS_NAME, "task-item")) == 0