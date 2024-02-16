import requests
from models import Feedback, ProductDetails
from app.database import Session


class FeedbackLoader:
    def __init__(self, api_url, headers, params):
        self.api_url = api_url
        self.headers = headers
        self.params = params

    def fetch_feedbacks(self):
        response = requests.get(self.api_url, headers=self.headers, params=self.params)
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
