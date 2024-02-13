import time
from datetime import datetime

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

