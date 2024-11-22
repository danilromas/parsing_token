import json
from collections import defaultdict
import os

# Инициализируем словарь для хранения кошельков и количества их появлений
wallet_count = defaultdict(int)

# Чтение всех файлов и сбор данных
for i in range(1, 10):  # Если файлы пронумерованы от 1 до 17
    file_path = f'dextools/{i}_token.json'  # Заменить на реальные имена файлов
    print(f"Открываем файл: {file_path}")
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 0:  # Проверка на пустоту файла
            with open(file_path, 'r', encoding='utf-8-sig') as file:  # Открытие файла с удалением BOM
                content = file.read()  # Считываем файл как строку
                print(f"Содержимое файла {file_path}: {content[:100]}...")  # Вывод первых 100 символов
                try:
                    data = json.loads(content)  # Попытка загрузить JSON
                    wallets = {wallet[0] for wallet in data}  # Извлекаем только кошельки
                    for wallet in wallets:
                        wallet_count[wallet] += 1
                except json.JSONDecodeError as e:
                    print(f"Ошибка чтения JSON в файле {file_path}: {e}")
        else:
            print(f"Файл {file_path} пустой, пропускаем его.")
    else:
        print(f"Файл {file_path} не найден.")

# Оставляем только кошельки, которые встречаются минимум в 2 файлах
filtered_wallets = {wallet: count for wallet, count in wallet_count.items() if count >= 2}

# Сортируем кошельки по количеству встреч в порядке убывания
sorted_wallets = dict(sorted(filtered_wallets.items(), key=lambda item: item[1], reverse=True))

# Запись результата в файл
with open('result.json', 'w', encoding='utf-8') as result_file:
    json.dump(sorted_wallets, result_file, indent=4, ensure_ascii=False)

# Вывод списка кошельков и их количества
print("Кошельки, которые повторяются как минимум в двух файлах (сортированы по количеству):")
for wallet, count in sorted_wallets.items():
    print(f"{wallet}: встречается в {count} файлах")

print(f"Готово! Найдено {len(sorted_wallets)} кошельков, которые встречаются как минимум в двух файлах.")