from sqlalchemy.orm import Session
from app.models import ProductsMapping, Feedback

class ReviewDataAccess:
    def __init__(self, session: Session):
        self.session = session

    def add_review(self, review_data: dict):
        # Предполагаем, что данные уже прошли валидацию и готовы к вставке
        review = Feedback(**review_data)
        self.session.add(review)
        self.session.commit()

    def add_bulk_reviews(self, reviews_data: list):
        # Предполагаем, что данные уже прошли валидацию и готовы к вставке
        self.session.bulk_insert_mappings(Feedback, reviews_data)
        self.session.commit()

    def get_last_review_date(self, external_code: int):
        # Получаем дату последнего отзыва по артикулу
        last_review = (self.session.query(Feedback.created_date)
                       .join(ProductsMapping, ProductsMapping.external_code == Feedback.nm_id)
                       .filter(ProductsMapping.external_code == external_code)
                       .order_by(Feedback.created_date.desc())
                       .first())
        return last_review[0] if last_review else None

# Пример использования DAO
# db_session - это объект сессии SQLAlchemy, который вы создаете, когда запускаете ваше приложение
review_dao = ReviewDataAccess(db_session)
# Добавление нового отзыва
review_dao.add_review({
    'text': 'Отличный товар',
    # ...остальные данные отзыва
})
# Добавление группы отзывов
review_dao.add_bulk_reviews([
    {'text': 'Отличный товар', 'nm_id': 123456, 'created_date': '2022-01-01'},
    # ...остальные отзывы
])
# Получение даты последнего отзыва по артикулу
last_date = review_dao.get_last_review_date(external_code=123456)
