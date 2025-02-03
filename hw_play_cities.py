## Задание 👷‍♂️

### Классы и их функциональность
"""
1. **Класс `JsonFile`**
   - Отвечает за чтение  данных в формате JSON.
   - Методы:
     - `read_data()`: Читает данные из JSON-файла и возвращает их.

2. **Класс `CitiesSerializer`**
   - Использует датакласс `City` для хранения информации о городах.
   - `__init__(self, city_data)`: Инициализирует список городов, создавая экземпляры `City`.
   - Методы:
     - `get_all_cities()`: Возвращает список всех городов.

3. **Класс `City`**
   - Датакласс для представления города.
   - Поля:
     - `name`: Название города.
     - `population`: Население города.
     - `subject`: Субъект федерации.
     - `district`: Район.
     - `latitude`: Широта.
     - `longitude`: Долгота.
     - `is_used`: Флаг, указывающий, использован ли город в игре.

4. **Класс `CityGame`**
   - Управляет логикой игры.
   - Методы:
     - `__init__(self, cities)`: Принимает экземпляр `CitiesSerializer` и инициализирует состояние игры.
     - `start_game()`: Начинает игру, включая первый ход компьютера.
     - `human_turn(city_input)`: Обрабатывает ход человека.
     - `computer_turn()`: Выполняет ход компьютера.
     - `check_game_over()`: Проверяет завершение игры и определяет победителя.
     - `save_game_state()`: Сохраняет состояние игры, если необходимо.

5. **Управляющий класс `GameManager`**
   - Фасад, который инкапсулирует взаимодействие между компонентами.
   - Атрибуты:
     - `json_file`: Экземпляр класса `JsonFile`.
     - `cities_serializer`: Экземпляр класса `CitiesSerializer`.
     - `city_game`: Экземпляр класса `CityGame`.
   - Методы:
     - `__call__()`: Запускает игру, вызывая методы `start_game()`, `human_turn()`, и `computer_turn()` до завершения игры.
     - `run_game()`: Координирует выполнение игры.
     - `display_game_result()`: Отображает результат игры после её завершения (опционально).


### Таблица (возможных) классов и методов

| Класс               | Методы                          | Описание                                                                                 |
|---------------------|---------------------------------|------------------------------------------------------------------------------------------|
| `JsonFile`          | `read_data()`                   | Читает данные из JSON-файла и возвращает их.                                             |
|                     | `write_data(data)`              | Записывает данные в JSON-файл.                                                           |
| `CitiesSerializer`  | `__init__(self, city_data)`     | Инициализирует список городов, создавая экземпляры `City`.                               |
|                     | `get_all_cities()`              | Возвращает список всех городов.                                                          |
| `City`              | -                               | Датакласс для представления города с полями: `name`, `population`, `subject`, `district`, `latitude`, `longitude`, `is_used`. |
| `CityGame`          | `__init__(self, cities)`        | Принимает экземпляр `CitiesSerializer` и инициализирует состояние игры.                  |
|                     | `start_game()`                  | Начинает игру, включая первый ход компьютера.                                            |
|                     | `human_turn(city_input)`        | Обрабатывает ход человека.                                                               |
|                     | `computer_turn()`               | Выполняет ход компьютера.                                                                |
|                     | `check_game_over()`             | Проверяет завершение игры и определяет победителя.                                       |
|                     | `save_game_state()`             | Сохраняет состояние игры, если необходимо.                                               |
| `GameManager`       | `__call__()`                    | Запускает игру, вызывая методы `start_game()`, `human_turn()`, и `computer_turn()` до завершения игры. |
|                     | `run_game()`                    | Координирует выполнение игры.                                                            |
|                     | `display_game_result()` (опц.)  | Отображает результат игры после её завершения (опционально).                             |

###
"""

from dataclasses import dataclass
import json

class JsonFile:
    """
    Класс для чтения данных из JSON-файла с городами России
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
    def read_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


sym_lower_set = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

# Мы можем перепаковать города в сет
cities_set = {city['name'].lower() for city in cities_list}


# Собираем сет "плохих букв"
bad_letters = set()
iter_count = 0
# Внешний цикл для обхода последних букв
for letter in sym_lower_set:
    # Вложенный цикл для обхода первых букв
    for city_2 in cities_set:
        first_letter = city_2[0]
        iter_count += 1
        if letter.lower() == first_letter.lower():
           # Что происходит, если они равны? Это хорошая буква
           break
    else:
        # Если мы обошли весь сет и ни одно слово не начинается с нашей буквы - букву заносим как "плохую"
        bad_letters.add(letter)

# print(bad_letters)
print(iter_count)

# 3. Мы можем начать писать игру
computer_city = ''
index = -1

while True:
    # Тут 
    # Ход человека
    human_city = input('Введите город России: ').lower()
    # Проверяем, что город есть в сете
    if human_city.lower() not in {city.lower() for city in cities_set}:
        print('Такого города нет. Человек проиграл.')
        break

    # Проверяем, что город соотсветствует правилам игры.
    # Если компьютер называл город:
    if computer_city:
        # Проверяем, что город начинается на последнюю букву предыдущего
        if human_city[0].lower() != computer_city[-1].lower():
            print('Невыполнение правил игры. Человек проиграл.')
            break
    
    # Удаляем город из сета
    cities_set.remove(human_city)

    # Ход компьютера

    # Тут мы можем пересчитать "Плохие буквы"

    # Обходим сет и ищем подходящий город
    for city in cities_set:
        if city[0].lower() == human_city[-1].lower():
            # Проверка на плохие буквы
            if city[-1].lower() in bad_letters:
                continue
            # Если все хорошо, то запоминаем город
            computer_city = city
            print('Компьютер назвал город:', computer_city)
            # Удаляем город из сета
            cities_set.remove(computer_city)
            break
    else:
        print('Компьютер проиграл.')
        break


