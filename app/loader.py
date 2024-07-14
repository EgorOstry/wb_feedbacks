from datetime import timedelta
import pytz
import requests
import time
from app.DAO import ReviewsDAO
from copy import deepcopy
from app.logger import logger


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
        return feedbacks

    def get_reviews(self, isAnswered, dateFrom):

        params_copy = deepcopy(self.params)
        params_copy["isAnswered"] = isAnswered
        params_copy["dateFrom"] = dateFrom
        params_copy["nmId"] = self.article
        reviews = []

        while True:
            count_429error = 0
            count_503error = 0
            count_error = 0
            response = requests.get(self.api_url, headers=self.headers, params=params_copy)
            if response.status_code == 429:
                count_429error += 1
                if count_429error > 2:
                    # print(f'Артикул {params_copy["nmId"]}: 3 неудачные попытки, выгрузка данного артикула остановлена')
                    logger.warning(f'Артикул {params_copy["nmId"]}: 3 неудачные попытки, выгрузка данного артикула остановлена')
                    break
                # print(f'Артикул {params_copy["nmId"]}: Слишком много запросов в ед.времени, следующая попытка через 60сек.')
                logger.warning(
                    f'Артикул {params_copy["nmId"]}: Слишком много запросов в ед.времени, следующая попытка через 60сек.')
                time.sleep(60)
                continue
            elif response.status_code == 503:
                count_503error += 1
                if count_429error > 5:
                    # print(f'Артикул {params_copy["nmId"]}: 5 неудачных попыток, выгрузка данного артикула остановлена')
                    logger.warning(f'Артикул {params_copy["nmId"]}: 5 неудачных попыток, выгрузка данного артикула остановлена')
                    break
                # print(f'Артикул {params_copy["nmId"]}: Сервис недоступен, следующая попытка через 60сек.')
                logger.warning(f'Артикул {params_copy["nmId"]}: Сервис недоступен, следующая попытка через 60сек.')
                time.sleep(60)
                continue
            elif response.status_code != 200:
                count_error += 1
                if count_error > 5:
                    # print(f'Артикул {params_copy["nmId"]}: 5 неудачных попыток, выгрузка данного артикула остановлена')
                    logger.warning(f'Артикул {params_copy["nmId"]}: 5 неудачных попыток, выгрузка данного артикула остановлена')
                    break
                # print(f'Артикул {params_copy["nmId"]}: Ошибка запроса: код {response.status_code}, следующая попытка через 60сек.')
                logger.warning(f'Артикул {params_copy["nmId"]}: Ошибка запроса: код {response.status_code}, следующая попытка через 60сек.')
                time.sleep(60)
                continue

            data = response.json()['data']['feedbacks']

            reviews.extend(data)
            if len(data) < int(params_copy["take"]):
                break

            params_copy['skip'] = str(int(params_copy['skip']) + int(params_copy['take']))
            time.sleep(0.5)

        if len(reviews) == 0:
            return []

        product_id = params_copy["nmId"]
        feedbacks_data = self.transform_feedbacks(reviews, product_id)

        return feedbacks_data

    @staticmethod
    def transform_feedbacks(reviews, product_id):
        feedbacks_to_load = []
        for feedback in reviews:
            feedbacks_data = feedback

            if feedbacks_data["text"] == "":
                feedbacks_data["text"] = None

            feedbacks_data.pop('answer', None)  # Удаляем 'answer', если он есть
            feedbacks_data.pop('photoLinks', None)  # Удаляем 'photoLinks', если он есть
            feedbacks_data.pop('video', None)  # Удаляем 'video', если он есть
            feedbacks_data.pop('imtId', None)  # Удаляем 'imtId', если он есть
            feedbacks_data.pop('subjectId', None)  # Удаляем 'subjectId', если он есть
            feedbacks_data.pop('userName', None)  # Удаляем 'userName', если он есть
            feedbacks_data.pop('updatedDate', None)  # Удаляем 'updatedDate', если он есть
            feedbacks_data.pop('state', None)  # Удаляем 'state', если он есть
            feedbacks_data.pop('wasViewed', None)  # Удаляем 'wasViewed', если он есть
            del feedbacks_data['productDetails']

            feedbacks_data['productId'] = product_id
            feedbacks_data['source'] = 'Wildberries API'
            feedbacks_to_load.append(feedbacks_data)

        return feedbacks_to_load
