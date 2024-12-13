import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict
import json
import time
from datetime import datetime

print("Добро пожаловать! Этот код предназначен для сайта dextools.io.")


if not os.path.exists("dextools"):os.mkdir("dextools")

existing_json_files = [f for f in os.listdir("dextools") if f.endswith(".json")]
if existing_json_files:
    print(f"В папке dextools найдены JSON-файлы.Учтите,при новом запуске папка очищается для новых токенов")
    proceed = input("Все равно начать работу? (да/нет): ").strip().lower()
    if proceed != "да":
        print("Работа приостоновленна. Сохраните необходимые транзакции токенов,если не хотите их ликвидации.")
        exit()
# Удаление старых файлов из папки
for filename in os.listdir("dextools"):
    if filename.endswith(".json"):os.remove(os.path.join("dextools", filename))


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

# Получаем путь к директории, где находится main.py
base_dir = os.path.dirname(os.path.abspath(__file__))
# Инициализируем Service с относительным путем
s = Service(executable_path=os.path.join(base_dir, 'chromedriver-win64', 'chromedriver.exe'))
driver = webdriver.Chrome(service=s, options=options)

with open('addresses.json', 'r', encoding='utf-8') as f:
    addresses = json.load(f)

try:
    driver.maximize_window()
    driver.get("https://www.dextools.io/app/en/hot-pairs")
    wait = WebDriverWait(driver, 15)

    # Закрываем всплывающее окно, если оно появилось
    try:
        close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))
        close.click()
    except Exception:
        pass  # Если окна нет, продолжаем
    try:
        close =driver.find_element(By.XPATH,"//button[@class = 'cky-btn cky-btn-accept'][@aria-label = 'Accept All']")
        close.click()
    except Exception:
        pass


    time.sleep(2)
    for entry in addresses:
        links_list = []  # Очищаем links_list для каждой итерации
        entry_date_str = entry.get("date")
        try:
            # Преобразуем дату из entry в объект datetime
            current_year = datetime.now().year
            entry_date = datetime.strptime(entry_date_str, "%b %d %H:%M:%S").replace(year=current_year)
        except ValueError:
            print(f"Некорректный формат даты в адресах: {entry_date_str}")
            break
        try:
            search = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'extra-container')))
            driver.execute_script("arguments[0].scrollIntoView();", search)
            time.sleep(2)
            search.click()
            time.sleep(2)
            search2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
            search2.click()
            search2.clear()
            search2.send_keys(f"{entry.get("address")}")
            time.sleep(3)

            # Получаем ссылки
            uls = driver.find_element(By.TAG_NAME, 'app-new-pairs-search-results').find_element(By.TAG_NAME, 'ul')
            link = uls.find_element(By.TAG_NAME, 'li').find_element(By.TAG_NAME, 'a')
            link.click()
            time.sleep(6)

            pause_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button'][@class='btn btn-outline-secondary pair-explorer-actions__button pair-explorer-actions__button--pause']")))
            driver.execute_script("arguments[0].scrollIntoView();", pause_button)
            time.sleep(4)
            pause_button.click()
            name = (driver.find_element(By.XPATH, "//span[@class='token-left size-l ng-star-inserted']")).text
            name = name.replace('\x00', '')
            stop_iteration = False
            while not stop_iteration:
                wallet = driver.find_element(By.CLASS_NAME, 'datatable-body')
                last_scroll_top = driver.execute_script("return arguments[0].scrollTop;", wallet)
                max_scroll_top = driver.execute_script("return arguments[0].scrollHeight - arguments[0].clientHeight;",
                                                       wallet)
                remaining_scroll = max_scroll_top - last_scroll_top
                if remaining_scroll < 525:
                    driver.execute_script(f"arguments[0].scrollTop = arguments[0].scrollTop + {remaining_scroll};",
                                          wallet)
                    time.sleep(3)
                    driver.execute_script(f"arguments[0].scrollTop = arguments[0].scrollTop - {remaining_scroll};",
                                          wallet)

                links = driver.find_elements(By.XPATH, "//datatable-body-cell[@role='cell'][@tabindex='-1'][@style='width: 150px; min-width: 150px; height: 35px;']")
                dates = driver.find_elements(By.XPATH, "//datatable-body-cell[@role='cell'][@tabindex='-1'][@style='width: 120px; min-width: 120px; height: 35px;']")

                max_links = 14
                count = 0

                for link, datee in zip(links, dates):
                    try:
                        href = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        date = (datee.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div'))
                        date_text = date.text.strip()
                        date = datetime.strptime(date_text, "%b %d %H:%M:%S").replace(year=datetime.now().year)
                        #print(date)
                        if date <= entry_date:
                            stop_iteration = True
                            break
                        links_list.append(href)
                        count += 1
                        if count >= max_links:
                            break
                    except Exception:
                        continue
                time.sleep(1)
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 525;", wallet)
                time.sleep(1)
        except Exception as e:
            print(e)

        # Сохраняем ссылки даже в случае ошибки
        href_count = defaultdict(int)
        for href in links_list:
            cleaned_href = href.replace('\x00', '')
            href_count[cleaned_href] += 1
        sorted_links = sorted(href_count.items(), key=lambda item: item[1], reverse=True)

        existing_files = [f for f in os.listdir("dextools") if f.endswith(".json")]
        file_number = len(existing_files) + 1
        json_file_path = os.path.join("dextools", f"{name}.json")
        with open(json_file_path, "w", encoding='utf-8-sig') as json_file:
            json.dump(sorted_links, json_file, ensure_ascii=False, indent=4)

finally:
    driver.quit()
    print("Работа завершена. Все данные помещены в папку 'dextools'.")
