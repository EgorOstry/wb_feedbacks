import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Параметры для запроса
ARTICLE_NUMBER = os.getenv("ARTICLE_NUMBER")  # Пример артикула
MAX_REVIEWS_PER_REQUEST = 5000  # Максимум отзывов за один запрос
isAnswered = 'true'  # Пример значения параметра isAnswered
API_TOKEN = os.getenv("api_token")  # Замените на ваш фактический токен API



def get_reviews(article_number, is_answered, max_per_request, API_TOKEN):
    base_url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'
    headers = {
        'Authorization': f'{API_TOKEN}'
    }
    params = {
        'nmId': article_number,
        'take': max_per_request,
        'skip': 0,
        'isAnswered': is_answered
    }
    reviews = []

    while True:
        # Отправка запроса
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            break

        # Обработка данных
        data = response.json()['data']['feedbacks']
        reviews.extend(data)

        # Если количество отзывов меньше, чем max_per_request, то это последний запрос
        if len(data) < max_per_request:
            break

        # Увеличение параметра skip для следующего запроса
        params['skip'] += max_per_request

    return reviews


# Получаем данные
reviews_data = get_reviews(ARTICLE_NUMBER, isAnswered, MAX_REVIEWS_PER_REQUEST, API_TOKEN)

# Добавляем текущую дату к каждой записи
current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for review in reviews_data:
    review['load_date'] = current_date



# Преобразуем данные в DataFrame
df_reviews = pd.DataFrame(reviews_data)

# Обрабатываем столбец `productDetails`, преобразуя строку словаря в фактический словарь
# и затем расширяем его в отдельные столбцы
product_details = df_reviews['productDetails'].apply(pd.Series)

# Объединяем исходный DataFrame с новыми столбцами из productDetails
df_reviews = pd.concat([df_reviews.drop(['productDetails'], axis=1), product_details], axis=1)

# Сохраняем данные в CSV-файл
df_reviews.to_csv('./storage/reviews.csv', index=False, encoding='utf-8-sig')

print("Отзывы сохранены в файл 'reviews.csv'.")

