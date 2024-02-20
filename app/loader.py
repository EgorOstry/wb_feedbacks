from datetime import timedelta
import pytz
import requests
import time
from app.DAO import ReviewsDAO
from copy import deepcopy


class FeedbackLoader:
    def __init__(self, api_url, headers, params, article):
        self.api_url = api_url
        self.headers = headers
        self.params = params
        self.article = article

    @staticmethod
    def get_max_date(article):
        max_review_date = ReviewsDAO.get_max_review_date_by_article(int(article))
        if max_review_date is not None:
            # Проверяем, находится ли max_review_date в UTC
            if not max_review_date.tzinfo:
                max_review_date = pytz.utc.localize(max_review_date)

            # Добавляем 1 секунду к максимальной дате
            next_second_utc = max_review_date + timedelta(seconds=1)

            # Получаем Unix timestamp
            timestamp = int(next_second_utc.timestamp())

            return timestamp

    def load_reviews(self):
        dateFrom = self.get_max_date(self.article)
        feedbacks = []
        for isAnswered in [True, False]:
            feedbacks.extend(self.get_reviews(isAnswered, dateFrom))
        qty = ReviewsDAO.add_review(feedbacks)
        return qty

    def get_reviews(self, isAnswered, dateFrom):

        params_copy = deepcopy(self.params)
        params_copy["isAnswered"] = isAnswered
        params_copy["dateFrom"] = dateFrom
        params_copy["nmId"] = self.article
        reviews = []

        while True:
            response = requests.get(self.api_url, headers=self.headers, params=params_copy)
            if response.status_code == 429:
                time.sleep(60)
            elif response.status_code != 200:
                print(f"Ошибка запроса: {response.status_code}")
                break

            data = response.json()['data']['feedbacks']

            reviews.extend(data)
            if len(data) < int(params_copy["take"]):
                break

            params_copy['skip'] = str(int(params_copy['skip']) + int(params_copy['take']))

            time.sleep(0.5)

        feedbacks_data = self.transform_feedbacks(reviews)


        return feedbacks_data

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
