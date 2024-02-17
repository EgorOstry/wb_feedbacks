import os
from dotenv import load_dotenv
from app.loader import FeedbackLoader

load_dotenv(override=True)

api_token = os.getenv("api_token")
api_url = os.getenv("api_url")
external_code = os.getenv("ARTICLE_NUMBER")
take = 5000
skip = 0

headers = {'Authorization': f'{api_token}'}

params = {
    'isAnswered': 'true',
    'nmId': f"{external_code}",
    'take': f"{take}",
    'skip': f"{skip}",
    'order': 'dateAsc',
    'dateFrom': None,
    'dateTo': None
}


def main(api_url, headers, params):
    loader = FeedbackLoader(api_url, headers, params)
    loader.get_reviews()

    return 'completed'


if __name__ == '__main__':
    main(api_url, headers, params)
