import os
from dotenv import load_dotenv
from app.DAO import ReviewDAO
from app.loader import ReviewsLoader

load_dotenv(override=True)

# external_code = os.getenv("ARTICLE_NUMBER")


def main(external_code, max_per_request):
    loader = ReviewsLoader()
    dao = ReviewDAO()
    all_reviews = loader.aggregate_reviews(external_code)
    dao.add_reviews_to_database(all_reviews)


if __name__ == '__main__':
    external_code = os.getenv("ARTICLE_NUMBER")
    main(external_code, 3)
