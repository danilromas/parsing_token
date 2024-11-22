from datetime import datetime
import json
import os

"""
Данный файл расчитан на существовани addresses.json
если таковой отсутсвует,создайте его в том же каталоге, что и addres.py(то есть в папке solscan_parsing)
"""
from datetime import datetime
import json
import os

def get_addresses():
    addresses = []

    if os.path.exists('addresses.json'):
        addresses = []

    print("Введите адреса токенов по одному. Чтобы завершить ввод, напишите латинскими буквами 'stop'.")

    while True:
        address = input("Введите адрес: ")
        if address.lower() == 'stop':
            break

        # Проверка и обработка ввода даты
        while True:
            date_input = input("Введите дату (формат: Nov 12 22:23:23): ")
            try:
                # Обработка формата "Nov 12 22:23:23" с установкой текущего года
                date_parsed = datetime.strptime(date_input, "%b %d %H:%M:%S").replace(year=datetime.now().year)
                break
            except ValueError:
                print(f"Некорректный формат даты: {date_input}. Пожалуйста, попробуйте снова.")

        addresses.append({"address": address, "date": date_parsed.strftime("%b %d %H:%M:%S")})

    with open('addresses.json', 'w', encoding='utf-8') as f:
        json.dump(addresses, f, ensure_ascii=False, indent=4)

    print("Адреса и даты сохранены в файл addresses.json.")



if __name__ == "__main__":
    get_addresses()

