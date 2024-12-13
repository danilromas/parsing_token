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

if not os.path.exists("dextools"):
    os.mkdir("dextools")

existing_json_files = [f for f in os.listdir("dextools") if f.endswith(".json")]
if existing_json_files:
    print(f"В папке dextools найдены JSON-файлы.Учтите,при новом запуске папка очищается для новых токенов")
    proceed = input("Все равно начать работу? (да/нет): ").strip().lower()
    if proceed != "да":
        print("Работа приостоновленна. Сохраните необходимые транзакции токенов,если не хотите их ликвидации.")
        exit()

for filename in os.listdir("dextools"):
    if filename.endswith(".json"):
        os.remove(os.path.join("dextools", filename))

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

base_dir = os.path.dirname(os.path.abspath(__file__))
s = Service(executable_path=os.path.join(base_dir, 'chromedriver-win64', 'chromedriver.exe'))
driver = webdriver.Chrome(service=s, options=options)

with open('addresses.json', 'r', encoding='utf-8') as f:
    addresses = json.load(f)

try:
    driver.maximize_window()
    driver.get("https://www.dextools.io/app/en/hot-pairs")
    wait = WebDriverWait(driver, 15)

    try:
        close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))
        close.click()
    except Exception:
        pass

    try:
        close = driver.find_element(By.XPATH, "//button[@class = 'cky-btn cky-btn-accept'][@aria-label = 'Accept All']")
        close.click()
    except Exception:
        pass

    time.sleep(2)
    for entry in addresses:
        links_list = []
        entry_date_str = entry.get("date")
        try:
            current_year = datetime.now().year
            entry_date = datetime.strptime(entry_date_str, "%b %d %H:%M:%S").replace(year=current_year)
        except ValueError:
            print(f"Некорректный формат даты в адресах: {entry_date_str}")
            continue

        try:
            search = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'extra-container')))
            driver.execute_script("arguments[0].scrollIntoView();", search)
            time.sleep(2)
            search.click()
            time.sleep(2)
            search2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
            search2.click()
            search2.clear()
            search2.send_keys(f"{entry.get('address')}")
            time.sleep(3)

            uls = driver.find_element(By.TAG_NAME, 'app-new-pairs-search-results').find_element(By.TAG_NAME, 'ul')
            link = uls.find_element(By.TAG_NAME, 'li').find_element(By.TAG_NAME, 'a')
            link.click()
            time.sleep(6)

            pause_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                "//button[@type='button'][@class='btn btn-outline-secondary pair-explorer-actions__button pair-explorer-actions__button--pause']")))
            driver.execute_script("arguments[0].scrollIntoView();", pause_button)
            time.sleep(4)
            pause_button.click()
            name = (driver.find_element(By.XPATH, "//span[@class='token-left size-l ng-star-inserted']")).text
            name = name.replace('\x00', '')

            max_attempts = 3
            attempts = 0
            last_links_count = 0
            stop_iteration = False

            while not stop_iteration and attempts < max_attempts:
                wallet = driver.find_element(By.CLASS_NAME, 'datatable-body')
                links = driver.find_elements(By.XPATH,
                    "//datatable-body-cell[@role='cell'][@tabindex='-1'][@style='width: 150px; min-width: 150px; height: 35px;']")
                dates = driver.find_elements(By.XPATH,
                    "//datatable-body-cell[@role='cell'][@tabindex='-1'][@style='width: 120px; min-width: 120px; height: 35px;']")

                current_links_count = len(links_list)
                if current_links_count == last_links_count:
                    attempts += 1
                else:
                    attempts = 0
                last_links_count = current_links_count

                max_links = 14
                count = 0

                for link, datee in zip(links, dates):
                    try:
                        href = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        date = (datee.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div'))
                        date_text = date.text.strip()
                        try:
                            date = datetime.strptime(date_text, "%b %d %H:%M:%S").replace(year=datetime.now().year)
                            if date <= entry_date:
                                stop_iteration = True
                                break
                        except ValueError:
                            pass

                        links_list.append(href)
                        count += 1
                        if count >= max_links:
                            break
                    except Exception:
                        continue

                if not stop_iteration:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 525;", wallet)
                    time.sleep(1)

        except Exception as e:
            print(f"Ошибка при обработке токена {name}: {str(e)}")

        if links_list:
            href_count = defaultdict(int)
            for href in links_list:
                cleaned_href = href.replace('\x00', '')
                href_count[cleaned_href] += 1
            sorted_links = sorted(href_count.items(), key=lambda item: item[1], reverse=True)

            json_file_path = os.path.join("dextools", f"{name}.json")
            with open(json_file_path, "w", encoding='utf-8-sig') as json_file:
                json.dump(sorted_links, json_file, ensure_ascii=False, indent=4)
            print(f"Сохранены данные для токена {name}")
        else:
            print(f"Не найдено транзакций для токена {name}")

finally:
    driver.quit()
    print("Работа завершена. Все данные помещены в папку 'dextools'.")