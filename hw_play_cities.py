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

@dataclass
class City:
    """
    Класс для описания города
    """
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False

class CitiesSerializer:
    """
    Класс для сериализации и десериализации списка городов
    """
    def __init__(self, city_data: list):
        self.cities = []
        for city in city_data:
            city_1 = City(
                name=city['name'],
                population=city.get('population', 0),
                subject=city.get('subject', ''),
                district=city.get('district', ''),
                latitude=city.get('latitude', 0.0),
                longitude=city.get('longitude', 0.0),
                is_used=False
            )
            self.cities.append(city_1)
    def get_all_cities(self):
        return self.cities
    
class CityGame:
    """
    Класс для управления игрой в города
    """
    def __init__(self, cities: CitiesSerializer):
        self.cities = cities.get_all_cities()
        self.cities_set = set()
        for city in self.cities:
            self.cities_set.add(city.name.lower())
        self.computer_city = ''
        self.bad_letters = self._count_bad_letters()

    def _count_bad_letters(self):
        sym_lower_set = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        bad_letters = set()

        for letter in sym_lower_set:
            letter_found = False
            for city_name in self.cities_set:
                if letter.lower() == city_name[0].lower():
                    letter_found = True
                    break
            if not letter_found:
                    bad_letters.add(letter)
        return bad_letters


    def human_move(self, city_input: str) -> bool:
        """
        Обрабатывает ход человека
        """
        if city_input.lower() not in self.cities_set:
            return False
        
        if self.computer_city and city_input[0].lower() != self.computer_city[-1].lower():
            return False
        
        self.cities_set.remove(city_input.lower())
        return True
    
    def computer_move(self, human_city: str) -> str:
        """
        Выполняет ход компьютера
        """
        for city in self.cities_set:
            if city[0].lower() == human_city[-1].lower():
                if city[-1].lower() in self.bad_letters:
                    continue
                self.computer_city = city
                self.cities_set.remove(city)
                return city
            
class GameManager:
    """
    Класс для управления игрой
    """
    def __init__(self, json_file_path: str):
        self.json_file = JsonFile(json_file_path)
        self.cities_serializer = CitiesSerializer(self.json_file.read_data())
        self.city_game = CityGame(self.cities_serializer)

    def start_game(self):
        """
        Начинает игру, включая первый ход компьютера.
        """
        while True:
            human_city = input('Введите город России: ').lower()

            if not self.city_game.human_move(human_city):
                print('Вы проиграли.')
                break

            computer_move = self.city_game.computer_move(human_city)
            if not computer_move:
                print('Компьютер проиграл.')
                break

            print(f'Компьютер назвал город: {computer_move}')

if __name__ == "__main__":
    game_manager = GameManager('cities.json')
    game_manager.start_game()