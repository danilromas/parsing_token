import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Определяем данные
tasks = [
    "Собрать данные о целевой аудитории", "Выявить основные проблемы при сборке ПК",
    "Определить ключевые платформы и ОС", "Собрать данные о популярных решениях конкурентов",
    "Написать парсер для сбора данных с сайтов", "Сформировать базу данных комплектующих",
    "Добавить поиск и фильтры по параметрам", "Добавить возможность сортировки результатов",
    "Реализовать проверку совместимости комплектующих", "Разработать макет главного экрана",
    "Разработать экран выбора комплектующих", "Разработать экран рекомендаций",
    "Разработать экран результатов поиска", "Разработать экран деталей комплектующего",
    "Создать структуру проекта (пакеты, классы)", "Написать основной экран приложения",
    "Подключить систему рекомендаций", "Добавить возможность фильтрации по цене и бренду",
    "Обработать и сохранить пользовательские данные", "Тестирование на различных устройствах",
    "Исправление ошибок в логике", "Проверка точности рекомендаций", 
    "Проверка отображения интерфейса на разных экранах", "Подготовить описание комплектующих",
    "Написать статьи о принципах сборки ПК", "Написать пошаговую инструкцию для новых пользователей",
    "Создать страницу приложения", "Подготовить скриншоты и описание", 
    "Оптимизировать загрузку данных комплектующих", "Создать сценарии взаимодействия пользователей с приложением"
]

durations_hours = [
    12, 8, 4, 4, 2, 8, 8, 4, 4, 8, 8, 8, 8, 8, 12, 12, 8, 4, 4, 12, 12, 8, 8, 4, 4, 8, 4, 4, 8, 4
]

# Расчёт дат начала и конца задач
start_date = datetime(2024, 7, 1)
end_date = datetime(2024, 12, 5)
hours_per_day = 1.9

start_dates = []
end_dates = []

current_date = start_date
for hours in durations_hours:
    start_dates.append(current_date)
    days = hours // hours_per_day + (1 if hours % hours_per_day != 0 else 0)
    current_date += timedelta(days=days)
    end_dates.append(current_date)

fig, ax = plt.subplots(figsize=(16, 10))
y_positions = range(len(tasks))

for i, (task, start, end) in enumerate(zip(tasks, start_dates, end_dates)):
    ax.barh(i, (end - start).days, left=start, height=0.8, align='center', color="skyblue")

ax.set_yticks(y_positions)
ax.set_yticklabels(tasks, fontsize=10)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45, ha='right', fontsize=10)

plt.xlabel("Время", fontsize=12)
plt.ylabel("Задачи", fontsize=12)
plt.title("Диаграмма Ганта: 1 августа 2024 - 5 декабря 2024", fontsize=14)
plt.tight_layout()

gantt_chart_path = "gantt_chart_august_to_december_2024.png"
plt.savefig(gantt_chart_path)
plt.show()

print(f"Диаграмма Ганта сохранена в файл: {gantt_chart_path}")
