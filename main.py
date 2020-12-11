import re
import csv

genre_input = input('Какой жанр игр Вас интересует?\n')
genre_in = list([genre.lstrip().capitalize() for genre in genre_input.split(',')])
category_input = input('В игры какой категории вы хотите поиграть?\n')
category_in = list([category.lstrip().title() for category in category_input.split(',')])
developer_input = input('Игры какого разработчика Вас интересуют?\n')
developer_in = list([developer.lstrip().title() for developer in developer_input.split(',')])
platform_input = input('Для какой платформы ищете игру?\n')
platform_in = list([platform.lstrip().lower() for platform in platform_input.split(',')])
year = input('Какой год выхода Вас интересует? (Можно ввести промежуток)\n')
cost = input('Выберите допустимую цену игры в долларах (используйте < или >)\n')
ratings = input('Положительных отзывов должно быть больше, чем отрицательных? (Введите \'да\' или \'нет\')\n').lower()


def genre_check(game_list):
    return any(genre in game_list for genre in genre_in) or (genre_in == [''])


def category_check(game_list):
    return any(category in game_list for category in category_in) or (category_in == [''])


def developer_check(game_list):
    return any(developer in game_list for developer in developer_in) or (developer_in == [''])


def platform_check(game_list):
    return any(platform in game_list for platform in platform_in) or (platform_in == [''])


def year_check(game_list, year_in=year):
    if '-' in year_in:
        year_in = year_in.split('-')
        return year_in[0] <= game_list <= year_in[1]
    else:
        return (game_list == year_in) or (year_in == '')


def cost_check(game_list, cost_in=cost):
    if cost_in == '':
        return 0.0 <= game_list <= 422.0
    elif cost_in[0] == '<':
        k = float(re.findall(r'[\d.]+', cost_in)[0])
        return 0.0 <= game_list <= k
    else:
        return cost_in == game_list


def ratings_check(game_list):
    return ((ratings == 'да') and (game_list[0] > game_list[1])) or (ratings == '')


with open('steam.csv', encoding='utf-8') as f, \
        open('result.txt', 'w', encoding='utf-8') as f1:
    reader = csv.reader(f)
    for string in reader:
        if string[0] == 'appid':
            continue

        game_genre_in = string[9].split(';') and string[10].split(';')
        game_category_in = string[8].split(';')
        game_developer_in = string[4].split(';')
        game_platform_in = string[6].split(';')
        game_year_in = string[2].split('-')[0]
        game_cost_in = float(string[17])
        game_ratings_in = [int(string[12]), int(string[13])]

        if (genre_check(game_genre_in) and
                category_check(game_category_in) and
                developer_check(game_developer_in) and
                platform_check(game_platform_in) and
                year_check(game_year_in) and
                cost_check(game_cost_in) and
                ratings_check(game_ratings_in)):
            f1.write(string[1] + '\n')
