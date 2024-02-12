from contextlib import contextmanager
from app.database import engine, Session
from app.models import Feedback, ProductsMapping

@contextmanager
def session_scope():
    """Предоставляет область действия для сессии."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ReviewDAO:

    def add_reviews_to_database(self, reviews):
        with session_scope() as session:
            for review_data in reviews:
                review = Feedback(**review_data)
                session.add(review)

    @staticmethod
    def get_max_review_date_by_article(external_code):
        with session_scope() as session:
            max_date = session.query(Feedback.created_date)\
                .join(ProductsMapping, ProductsMapping.external_code == Feedback.nm_id)\
                .filter(ProductsMapping.external_code == external_code)\
                .order_by(Feedback.created_date.desc())\
                .first()
            return max_date[0] if max_date else None

