from contextlib import contextmanager
from app.database import Session
from app.models import Feedback
from app.logger import logger


@contextmanager
def session_scope():
    """Предоставляет область действия для сессии."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        session.rollback()
        raise
    finally:
        session.close()


class ReviewsDAO:

    def __init__(self, product_detail, feedback):
        self.product_detail = product_detail
        self.feedback = feedback


    @staticmethod
    def filter_existing_feedbacks(feedbacks):
        with session_scope() as session:
            if session.query(Feedback.id).first() is None:
                return feedbacks
            # Получаем список ID отзывов
            feedback_ids = [feedback['id'] for feedback in feedbacks]

            existing_ids = set()
            batch_size = 1000
            for i in range(0, len(feedback_ids), batch_size):
                batch = feedback_ids[i:i + batch_size]
                batch_ids = session.query(Feedback.id).filter(Feedback.id.in_(batch)).all()
                existing_ids.update(id_[0] for id_ in batch_ids)

            # Исключаем уже существующие ID
            new_feedbacks = [feedback for feedback in feedbacks if feedback['id'] not in existing_ids]
            return new_feedbacks

    @staticmethod
    def get_max_review_date_by_article(nmId):
        with session_scope() as session:
            max_date = session.query(Feedback.createdDate). \
                filter(Feedback.productId == nmId). \
                order_by(Feedback.createdDate.desc()). \
                first()
            return max_date[0] if max_date else None

    @staticmethod
    def add_review(feedbacks_data, batch_size=10000):
        total_inserted = 0
        with session_scope() as session:
            feedbacks_data = ReviewsDAO.filter_existing_feedbacks(feedbacks_data)

            # Разбиение списка отзывов на пакеты по batch_size
            for i in range(0, len(feedbacks_data), batch_size):
                batch = feedbacks_data[i:i + batch_size]
                session.bulk_insert_mappings(Feedback, batch)
                # print(f'{len(batch)} строк добавлено')
                logger.info(f'{len(batch)} строк добавлено')
                # commit вызывается автоматически при выходе из контекстного менеджера
                total_inserted += len(batch)

        return total_inserted

    ## разовая загрузка, не пачками
    # @staticmethod
    # def add_review(feedbacks_data):
    #     with session_scope() as session:
    #         feedbacks_data = ReviewsDAO.filter_existing_feedbacks(feedbacks_data)
    #         session.bulk_insert_mappings(Feedback, feedbacks_data)
    #         return len(feedbacks_data)