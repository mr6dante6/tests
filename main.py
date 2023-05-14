import requests


def filter_geo():
    geo_logs = [
        {'visit1': ['Москва', 'Россия']},
        {'visit2': ['Дели', 'Индия']},
        {'visit3': ['Владимир', 'Россия']},
        {'visit4': ['Лиссабон', 'Португалия']},
        {'visit5': ['Париж', 'Франция']},
        {'visit6': ['Лиссабон', 'Португалия']},
        {'visit7': ['Тула', 'Россия']},
        {'visit8': ['Тула', 'Россия']},
        {'visit9': ['Курск', 'Россия']},
        {'visit10': ['Архангельск', 'Россия']}
    ]

    filtered_geo_logs = []

    for visit in geo_logs:
        for country in visit.values():
            if 'Россия' in country:
                filtered_geo_logs.append(visit)
    return filtered_geo_logs


def unique_id():
    ids = {'user1': [213, 213, 213, 15, 213],
           'user2': [54, 54, 119, 119, 119],
           'user3': [213, 98, 98, 35]}

    unique_ids = set()

    for user, user_ids in ids.items():
        for user_id in user_ids:
            unique_ids.add(user_id)
    return list(unique_ids).sort()


def find_max_volume_channel(stats):
    max_volume = 0
    max_channel = ''

    for channel, volume in stats.items():
        if volume > max_volume:
            max_volume = volume
            max_channel = channel
    return max_channel


def create_folder_yandex_disk(token: str, folder_name: str, path: str = ''):
    headers = {
        'Authorization': f'OAuth {token}'
    }
    params = {
        'path': f'{path}/{folder_name}'
    }
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                            headers=headers,
                            params=params)
    response.raise_for_status()

    response = requests.get(f'https://cloud-api.yandex.net/v1/disk/resources',
                            headers=headers,
                            params=params)
    print(response.json())
