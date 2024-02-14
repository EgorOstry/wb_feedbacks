from contextlib import contextmanager
from .database import Session
from .models import Feedback, ProductDetails

@contextmanager
def session_scope():
    """Предоставляет область действия для сессии."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
        raise
    finally:
        session.close()

class ReviewsDAO:
    def add_review(self, review_data):
        with session_scope() as session:
            review = Feedback(**review_data)
            session.add(review)

    def add_product_details(self, product_details_data):
        with session_scope() as session:
            details = ProductDetails(**product

