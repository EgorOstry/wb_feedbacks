import os
from dotenv import load_dotenv
from app.loader import FeedbackLoader
from app.articles import load_articles_from_xls

load_dotenv(override=True)

api_token = os.getenv("api_token")
api_url = os.getenv("api_url")
# external_code = os.getenv("ARTICLE_NUMBER")
take = 5000
skip = 0
articles = load_articles_from_xls()

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


def main(api_url, headers, params):
    for article in articles:
        loader = FeedbackLoader(api_url, headers, params, article)
        loader.load_reviews()

    return 'completed'


if __name__ == '__main__':
    main(api_url, headers, params)
