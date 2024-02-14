import time
from app.DAO import ReviewDAO
import os
from dotenv import load_dotenv
import requests

load_dotenv(override=True)

API_TOKEN = os.getenv("api_token")
max_per_request = 5000


class ReviewsLoader:

    def get_reviews(self, external_code, is_answered):
        max_review_date = ReviewDAO.get_max_review_date_by_article(external_code)

        if max_review_date is not None:
            date_from = int(max_review_date.timestamp())
        else:
            date_from = None

        base_url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'
        headers = {'Authorization': f'{API_TOKEN}'}
        params = {
            'dateFrom': date_from,
            'nmId': external_code,
            'take': max_per_request,
            'skip': 0,
            'isAnswered': is_answered,
            'order': 'dateAsc'
        }

        reviews = []

        while True:
            response = requests.get(base_url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Ошибка запроса: {response.status_code}")
                break

            data = response.json()['data']['feedbacks']
            reviews.extend(data)

            if len(data) < max_per_request:
                break

            params['skip'] += max_per_request
            time.sleep(1)
        return reviews

    def aggregate_reviews(self, external_code):
        answered_reviews = self.get_reviews(external_code, True)
        unanswered_reviews = self.get_reviews(external_code, False)
        all_reviews = answered_reviews + unanswered_reviews
        all_reviews.sort(key=lambda review: review['createdDate'])
        # Преобразование каждого отзыва
        transformed_reviews = [self.transform_review_data(review) for review in all_reviews]
        return transformed_reviews


import requests
from datetime import datetime

import requests
from models import Feedback, ProductDetails, Session

class FeedbackLoader:
    def __init__(self, api_url, params):
        self.api_url = api_url
        self.params = params

    def fetch_feedbacks(self):
        response = requests.get(self.api_url, params=self.params)
        response.raise_for_status()  # Поднимает исключение при HTTP ошибке
        return response.json()

    def parse_feedback(self, feedback_json):
        # Сюда можно добавить обработку полей, если это необходимо
        return feedback_json

    def load_into_db(self, feedbacks_data):
        session = Session()

        for feedback in feedbacks_data['data']['feedbacks']:
            # Парсим данные о продукте и создаем объект ProductDetails, если его нет в базе
            product_detail_data = feedback.pop('productDetails')
            product_detail = session.query(ProductDetails).filter_by(nmId=product_detail_data['nmId']).first()
            if not product_detail:
                product_detail = ProductDetails(**product_detail_data)
                session.add(product_detail)
                session.commit()

            # Создаем объект Feedback и связываем его с ProductDetails
            feedback_data = self.parse_feedback(feedback)
            feedback_obj = Feedback(**feedback_data, productDetail=product_detail)
            session.add(feedback_obj)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Пример использования:
api_url = 'http://example.com/api/v1/feedbacks'  # Замените на ваш URL
params = {
    'isAnswered': True,
    'take': 3,
    'skip': 0,
    # другие параметры запроса
}

loader = FeedbackLoader(api_url, params)
feedbacks_json = loader.fetch_feedbacks()
loader.load_into_db(feedbacks_json)
