import os
from dotenv import load_dotenv
# from app.DAO import ReviewDAO
from app.loader import ReviewsLoader
from app.loader2 import FeedbackLoader

load_dotenv(override=True)

api_token = os.getenv("api_token")
api_url = os.getenv("api_url")
external_code = os.getenv("ARTICLE_NUMBER")
take = 5
skip = 0

headers = {'Authorization': f'{api_token}'}

params = {
    'isAnswered': 'true',
    'nmid': f"{external_code}",
    'take': f"{take}",
    'skip': f"{skip}",
    'order': 'dateAsc',
    'dateFrom': None,
    'dateTo': None
}

def main(api_url, headers, params):
    loader = FeedbackLoader(api_url, headers, params)
    dao = ReviewDAO()
    all_reviews = loader.aggregate_reviews(external_code)
    dao.add_reviews_to_database(all_reviews)


if __name__ == '__main__':
    external_code = os.getenv("ARTICLE_NUMBER")
    main(external_code, 3)

# Пример использования:
api_url = 'http://example.com/api/v1/feedbacks'  # Замените на ваш URL
params = {
    'isAnswered': True,
    'take': 3,
    'skip': 0,
    # другие параметры запроса
}

loader = FeedbackLoader(api_url, params)
feedbacks_json = loader.fetch_feedbacks()
loader.load_into_db(feedbacks_json)