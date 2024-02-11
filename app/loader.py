from app.database import engine, Session
from app.models import Feedback, ProductsMapping
from contextlib import contextmanager



class Loader:
    def __init__(self):
        self.session_factory = Session

    @contextmanager
    def session_scope(self):
        """Предоставляет транзакционную область действия для сессии."""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_max_review_date_by_article(self, external_code):
        with self.session_factory() as session:
            try:
                max_date = session.query(Feedback.created_date). \
                    join(ProductsMapping, ProductsMapping.external_code == Feedback.nm_id). \
                    filter(ProductsMapping.external_code == external_code). \
                    order_by(Feedback.created_date.desc()). \
                    first()

                if max_date:
                    return max_date[0]
                else:
                    return None

    def load_reviews(self, external_code):
        max_review_date = self.get_max_review_date_by_article(external_code)

        if max_review_date is not None:
            # Преобразуем дату в Unix timestamp
            date_from = int(max_review_date.timestamp())
            # Теперь устанавливаем параметры запроса к API с date_from
            api_params = {
                'date_from': date_from,
                # Остальные параметры...
            }
        else:
            # Параметры запроса к API без date_from, чтобы получить все отзывы
            api_params = {
                # Остальные параметры...
            }

        # Остальная логика загрузки отзывов...

