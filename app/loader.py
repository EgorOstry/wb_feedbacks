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

    def transform_review_data(self, review_data):
        # Функция для преобразования строки в формат datetime
        def parse_datetime(date_str):
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') if date_str else None
        # Преобразование ключей из API в ключи модели
        transformed = {
            'id': review_data['id'],
            'text': review_data['text'],
            'product_valuation': review_data['productValuation'],
            'created_date': parse_datetime(review_data['createdDate']),
            "answer": review_data["answer"],
            "state": review_data["state"],
            # Для поля "video", если оно может быть None
            "video": review_data["video"] if review_data["video"] is not None else '',
            "was_viewed": review_data["wasViewed"],
            # Для поля "photoLinks", если оно может быть None
            "photo_links": review_data["photoLinks"] if review_data["photoLinks"] is not None else '',
            "user_name": review_data["userName"],
            "matching_size": review_data["matchingSize"],
            "is_able_supplier_feedback_valuation": review_data["isAbleSupplierFeedbackValuation"],
            "supplier_feedback_valuation": review_data["supplierFeedbackValuation"],
            "is_able_supplier_product_valuation": review_data["isAbleSupplierProductValuation"],
            "supplier_product_valuation": review_data["supplierProductValuation"],
            "is_able_return_product_orders": review_data["isAbleReturnProductOrders"],
            "return_product_orders_date": review_data["returnProductOrdersDate"],
            # Также может потребовать преобразования
            "bables": review_data["bables"] if review_data["bables"] is not None else ''
        }

        # Вложенный словарь productDetails
        product_details = review_data['productDetails']
        transformed.update({
            'imt_id': product_details['imtId'],
            'nm_id': product_details['nmId'],
            'product_name': product_details['productName'],
            "supplier_article": product_details["supplierArticle"],
            "supplier_name": product_details["supplierName"],
            "brand_name": product_details["brandName"],
            "size": product_details["size"]
        })

        return transformed
