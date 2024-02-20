from contextlib import contextmanager
from app.database import Session
from app.models import Feedback, ProductDetails


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

    def __init__(self, product_detail, feedback):
        self.product_detail = product_detail
        self.feedback = feedback

    @staticmethod
    def get_max_review_date_by_article(nmId):
        with session_scope() as session:
            max_date = session.query(Feedback.createdDate). \
                join(ProductDetails, ProductDetails.id == Feedback.productDetailId). \
                filter(ProductDetails.nmId == nmId). \
                order_by(Feedback.createdDate.desc()). \
                first()
            return max_date[0] if max_date else None

    @staticmethod
    def check_product_detail(product_details_data):
        with session_scope() as session:
            product_detail = session.query(ProductDetails).filter_by(nmId=product_details_data['nmId']).first()
            if not product_detail:
                product_detail = ProductDetails(**product_details_data)
                session.add(product_detail)
                session.flush()
            return product_detail.id

    @staticmethod
    def add_review(feedbacks_data):
        with session_scope() as session:
            session.bulk_insert_mappings(Feedback, feedbacks_data)
            return len(feedbacks_data)