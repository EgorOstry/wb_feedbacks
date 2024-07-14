import os
import time
from dotenv import load_dotenv
from app.DAO import ReviewsDAO
from app.loader import FeedbackLoader
from app.database import Base, engine
from app.articles import load_articles_from_xls
from app.logger import logger

load_dotenv(override=True)

api_token = os.getenv("api_token")
api_url = os.getenv("api_url")
take = 5000
skip = 0
articles = load_articles_from_xls()
# articles = [86102106,23648862,23652151] #для тестов, вместо предыдущей строки

last_call_time = 0
min_interval = 1

headers = {'Authorization': f'{api_token}'}

params = {
    'isAnswered': None,
    'nmId': None,
    'take': f"{take}",
    'skip': f"{skip}",
    'order': 'dateAsc',
    'dateFrom': None,
    'dateTo': None
}

if __name__ == '__main__':

    full_data_to_insert = []
    Base.metadata.create_all(engine)
    logger.info('Начало загрузки отзывов')

    for article in articles:
        current_time = time.time()
        if current_time - last_call_time < min_interval:
            time.sleep(min_interval - (current_time - last_call_time))
        last_call_time = time.time()
        loader = FeedbackLoader(api_url, headers, params, article)
        feedbacks_data = loader.load_reviews()
        logger.info(f"загружено {len(feedbacks_data): 5} отзывов по артикулу {article: 10}")
        full_data_to_insert.extend(feedbacks_data)

    logger.info('загрузка завершена\nдобавление записей в бд...')
    qty = ReviewsDAO.add_review(full_data_to_insert)
    logger.info(f"добавлено {qty} отзывов")
