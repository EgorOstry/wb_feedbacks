from datetime import timedelta

import pytz
import requests
import time
from app.DAO import ReviewsDAO


class FeedbackLoader:
    def __init__(self, api_url, headers, params):
        self.api_url = api_url
        self.headers = headers
        self.params = params

    def get_reviews(self):
        max_review_date = ReviewsDAO.get_max_review_date_by_article(int(self.params["nmId"]))
        if max_review_date is not None:
            # Проверяем, находится ли max_review_date в UTC
            if not max_review_date.tzinfo:
                max_review_date = pytz.utc.localize(max_review_date)

            # Добавляем 1 секунду к максимальной дате
            next_second_utc = max_review_date + timedelta(seconds=1)

            # Получаем Unix timestamp
            timestamp = int(next_second_utc.timestamp())
            self.params["dateFrom"] = timestamp

        reviews = []

        while True:
            response = requests.get(self.api_url, headers=self.headers, params=self.params)
            if response.status_code != 200:
                print(f"Ошибка запроса: {response.status_code}")
                break

            data = response.json()['data']['feedbacks']

            reviews.extend(data)
            if len(data) < int(self.params["take"]):
                break

            self.params['skip'] = str(int(self.params['skip']) + int(self.params['take']))

            time.sleep(1)

        feedbacks_data = self.transform_feedbacks(reviews)
        ReviewsDAO.add_review(feedbacks_data)

        return

    @staticmethod
    def transform_feedbacks(reviews):
        feedbacks_to_load = []
        for feedback in reviews:
            product_details_data = feedback['productDetails']
            product_id = ReviewsDAO.check_product_detail(product_details_data)
            feedbacks_data = feedback
            del feedbacks_data['productDetails']
            feedbacks_data.pop('answer', None)  # Удаляем 'answer', если он есть
            feedbacks_data.pop('photoLinks', None)  # Удаляем 'photoLinks', если он есть
            feedbacks_data.pop('video', None)  # Удаляем 'video', если он есть
            feedbacks_data['productDetailId'] = product_id
            feedbacks_to_load.append(feedbacks_data)

        return feedbacks_to_load
