import json
import sys

def categorize_population(value):
    """Категоризация размера города по населению (в миллионах)."""
    if value <= 0.5:
        return 1
    elif 0.5 < value <= 1:
        return 2
    else:
        return 3

def categorize_infrastructure(value):
    """Категоризация уровня инфраструктуры."""
    if value <= 4:
        return 1
    elif 5 <= value <= 7:
        return 2
    else:
        return 3

def categorize_greenery(value):
    """Категоризация уровня озеленения."""
    if value <= 4:
        return 1
    elif 5 <= value <= 7:
        return 2
    else:
        return 3

def categorize_cultural_activities(value):
    """Категоризация социальной активности."""
    if value <= 4:
        return 1
    elif 5 <= value <= 7:
        return 2
    else:
        return 3

def load_cities_from_json(json_file_path):
    """Загрузка списка городов из JSON файла."""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def parse_arguments(args):
    """Парсинг аргументов из командной строки."""
    try:
        # Разбираем параметры пользователя
        work_mode = [int(x) for x in args[0].split(';')]
        lifestyle = [int(x) for x in args[1].split(';')]
        climate = int(args[2])
        weather_stability = int(args[3])
        population = int(args[4])
        city_rhythm = int(args[5])
        infrastructure = categorize_infrastructure(int(args[6]))
        preferred_objects = [int(x) for x in args[7].split(';')]
        greenery = categorize_greenery(int(args[8]))
        green_preference = int(args[9])
        safety = int(args[10])
        cultural_activities = categorize_cultural_activities(int(args[11]))

        return {
            "climate": climate,
            "weather_stability": weather_stability,
            "population": population,
            "city_rhythm": city_rhythm,
            "infrastructure": infrastructure,
            "greenery": greenery,
            "work_mode": work_mode,
            "lifestyle": lifestyle,
            "preferred_objects": preferred_objects,
            "safety": safety,
            "cultural_activities": cultural_activities,
            "green_preference": green_preference
        }
    except (ValueError, IndexError):
        print("Ошибка ввода аргументов. Убедитесь, что переданы корректные значения.")
        sys.exit(1)

def calculate_similarity(city, user_prefs):
    """Расчет схожести города с предпочтениями пользователя."""
    weights = {
        "climate": 5,
        "weather_stability": 2,
        "population": 5,
        "city_rhythm": 2,
        "infrastructure": 1,
        "greenery": 1,
        "work_mode": 1,
        "lifestyle": 1,
        "preferred_objects": 1,
        "safety": 2,
        "cultural_activities": 1,
        "green_preference": 1,
    }
    
    score = 0
    score += weights["climate"] * abs(user_prefs["climate"] - city["climate"])
    score += weights["population"] * abs(user_prefs["population"] - city["population"])
    score += weights["weather_stability"] * abs(user_prefs["weather_stability"] - city["weather_stability"])
    score += weights["city_rhythm"] * abs(user_prefs["city_rhythm"] - city["city_rhythm"])
    score += weights["infrastructure"] * abs(user_prefs["infrastructure"] - city["infrastructure"])
    score += weights["greenery"] * abs(user_prefs["greenery"] - city["greenery"])
    score += weights["safety"] * abs(user_prefs["safety"] - city["safety"])
    score += weights["cultural_activities"] * abs(user_prefs["cultural_activities"] - city["cultural_activities"])
    score += weights["green_preference"] * abs(user_prefs["green_preference"] - city["green_preference"])

    # Work mode, lifestyle and preferred objects
    score += weights["work_mode"] * (1 - len(set(user_prefs["work_mode"]) & set(city["work_mode"])) / len(user_prefs["work_mode"]))
    score += weights["lifestyle"] * (1 - len(set(user_prefs["lifestyle"]) & set(city["lifestyle"])) / len(user_prefs["lifestyle"]))
    score += weights["preferred_objects"] * (1 - len(set(user_prefs["preferred_objects"]) & set(city["preferred_objects"])) / len(user_prefs["preferred_objects"]))

    return score

def find_best_cities(user_prefs, cities, top_n=5):
    """Найти наиболее подходящие города."""
    city_scores = [(city, calculate_similarity(city, user_prefs)) for city in cities]
    city_scores.sort(key=lambda x: x[1])
    return [city for city, _ in city_scores[:top_n]]

if __name__ == "__main__":
    if len(sys.argv) < 13:
        print("Использование: python3 script.py <work_mode> <lifestyle> <climate> <weather_stability> <population> <city_rhythm> <infrastructure> <preferred_objects> <greenery> <green_preference> <safety> <cultural_activities>")
        sys.exit(1)

    # Загрузка данных из JSON
    cities = load_cities_from_json('cities.json')
    
    # Получение предпочтений из аргументов
    user_preferences = parse_arguments(sys.argv[1:])

    # Рекомендации городов
    recommended_cities = find_best_cities(user_preferences, cities)
    print("Наиболее подходящие города:")
    for city in recommended_cities:
        print(f"- {city['name']}")
