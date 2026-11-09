import math

movies = [
    {"title": "The Dune Chronicles", "year": 2021, "genres": {"sci-fi", "drama"},
     "rating": 8.6, "duration_min": 155, "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]}, # noqa: E501
    {"title": "Kitchen Stories", "year": 2019, "genres": {"comedy", "drama"},
     "rating": 7.1, "duration_min": 98, "actors": ["A. Novak", "M. Ferguson"]},
    {"title": "silent hours", "year": 2016, "genres": {"thriller", "drama"},
     "rating": 6.4, "duration_min": 112, "actors": ["J. Bloom", "K. Lee"]},
    {"title": "Comet Racers", "year": 2023, "genres": {"sci-fi", "action"},
     "rating": 5.9, "duration_min": 101, "actors": ["O. Isaac", "P. Diaz"]},
    {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
     "rating": 7.8, "duration_min": 89, "actors": ["A. Novak", "T. Chalamet"]},
    {"title": "midnight in oslo", "year": 2020, "genres": {"thriller", "mystery"},
     "rating": 8.9, "duration_min": 124, "actors": ["K. Lee", "R. Ferguson"]},
    {"title": "Garden of Static", "year": 2022, "genres": {"drama"},
     "rating": 4.8, "duration_min": 137, "actors": ["P. Diaz", "J. Bloom"]},
    {"title": "The Quiet Algorithm", "year": 2024, "genres": {"sci-fi", "drama"},
     "rating": 9.2, "duration_min": 118, "actors": ["M. Ferguson", "O. Isaac"]},
    {"title": "Two Left Shoes", "year": 2011, "genres": {"comedy"},
     "rating": 6.0, "duration_min": 95, "actors": ["A. Novak", "K. Lee"]},
    {"title": "Red Harbor", "year": 2018, "genres": {"action", "thriller"},
     "rating": 7.3, "duration_min": 129, "actors": ["P. Diaz", "T. Chalamet"]},
]


# Этап 1

def average_rating(movies):
    """Средняя оценка по каталогу, округлённая до одного знака"""
    return round(sum(m["rating"] for m in movies) / len(movies), 1)


def catalog_age_stats(movies, current_year=2026):
    """
    возвращает кортеж 
    (самый старый фильм в годах, самый новый фильм в годах, среднее)
    """
    ages = [current_year - m["year"] for m in movies]
    return (max(ages), min(ages), math.ceil(sum(ages) / len(ages)))


def duration_in_hours(minutes):
    """Переводит минуты в формат 'Xч Yм'."""
    return f"{minutes // 60}ч {minutes % 60}м"


# Этап 2

def rating_tier(rating):
    """Категория оценки. Содержит тернарный оператор в return."""
    if rating >= 9:
        tier = "шедевр"
    elif rating >= 7:
        tier = "хорошо"
    elif rating >= 5:
        tier = "средне"
    else:
        tier = "слабо"
    return tier if rating <= 10 else "некорректный рейтинг"


def decade_label(year):
    """Метка десятилетия через match с case _ if."""
    match year:
        case _ if year > 2020:
            return "новые"
        case _ if year >= 2015:
            return "недавние"
        case _:
            return "старые"


# Этап 3

def count_long_movies(movies, threshold=120):
    """Считает фильмы длиннее threshold минут через накопитель."""
    count = 0
    for movie in movies:
        if movie["duration_min"] > threshold:
            count += 1
    return count


# Этап 4

def normalize_title(title):
    """Title Case вручную, без str.title() """
    words = title.split()
    return " ".join(word[0].upper() + word[1:] for word in words)


def make_slug(title):
    """Слаг вида 'silent-hours' через .lower() и .replace()"""
    return title.lower().replace(" ", "-")


def format_report_line(movie):
    """Единая строка описания фильма через f-строку """
    genres = ", ".join(sorted(movie["genres"]))
    return (
        f'"{normalize_title(movie["title"])}" ({movie["year"]}) — '
        f'{movie["rating"]}/10, {duration_in_hours(movie["duration_min"])}, '
        f"жанры: {genres}"
    )


# Этап 5

def titles_sorted_by_rating(movies):
    """Названия фильмов по убыванию рейтинга (без изменения исходника) """
    sorted_movies = sorted(movies, key=lambda m: m["rating"], reverse=True)
    return [m["title"] for m in sorted_movies]


def top_n_by_rating(movies, n=3):
    """Топ-n как список кортежей (title, rating) """
    sorted_movies = sorted(movies, key=lambda m: m["rating"], reverse=True)
    return [(m["title"], m["rating"]) for m in sorted_movies[:n]]


# Этап 6

def count_by_genre(movies):
    """{жанр: количество} через dict.get(), без Counter """
    counts = {}
    for movie in movies:
        for genre in movie["genres"]:
            counts[genre] = counts.get(genre, 0) + 1
    return counts


def actor_filmography(movies):
    """{актер: [названия фильмов]} """
    filmography = {}
    for movie in movies:
        for actor in movie["actors"]:
            filmography.setdefault(actor, []).append(movie["title"])
    return filmography


def movies_above_average(movies):
    """{title: rating} для rating > среднего сделать dict comprehension """
    avg = average_rating(movies)
    return {m["title"]: m["rating"] for m in movies if m["rating"] > avg}


# Этап 7

def all_genres(movies):
    """Множество всех уникальных жанров (через |=) """
    genres = set()
    for movie in movies:
        genres |= movie["genres"]
    return genres


def common_actors(movie1, movie2):
    """Актёры, снимавшиеся в обоих фильмах (пересечение &) """
    return set(movie1["actors"]) & set(movie2["actors"])


def genres_only_in_one(movies_a, movies_b):
    """Жанры из movies_a, которых нет в movies_b (разность -) """
    return all_genres(movies_a) - all_genres(movies_b)


# Этап 8

def iter_high_rated(movies, min_rating=8.0):
    """Лениво отдаёт фильмы с рейтингом >= min_rating через yield """
    for movie in movies:
        if movie["rating"] >= min_rating:
            yield movie


# Этап 9

def build_report(movies):
    """Единая точка входа - печатает полный отчёт по каталогу """
    avg_rating = average_rating(movies)
    _, _, avg_age = catalog_age_stats(movies)

    print("ОТЧЁТ ПО КАТАЛОГУ")
    print(f"Средний рейтинг: {avg_rating}")
    print(f"Средний возраст фильмов: {avg_age} лет")
    print()

    print("Топ-3 фильма:")
    for movie in sorted(movies, key=lambda m: m["rating"], reverse=True)[:3]:
        print(f"  {format_report_line(movie)}")
    print()

    print("Фильмов по жанрам:")
    counts = count_by_genre(movies)
    for genre, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {genre} — {count}")
    print()

    genres_list = sorted(all_genres(movies))
    print(f"Все жанры каталога: {', '.join(genres_list)}")


if __name__ == "__main__":
    # Этап 3: фильмы НЕ жанра comedy
    print("Фильмы которые НЕ относятся к жанру комедии: ")
    for movie in movies:
        if "comedy" in movie["genres"]:
            continue
        print("-", movie["title"])
        

    # Этап 8: демонстрация генератора
    for movie in iter_high_rated(movies):
        print(format_report_line(movie))
    total = sum(m["duration_min"] for m in movies if m["rating"] > 7)
    print(f"Суммарная длительность (rating > 7): {total} мин")
    print()

    # Этап 9: итоговый отчёт
    build_report(movies)