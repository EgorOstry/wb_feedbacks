import os
import sys
import time
from datetime import datetime

from dotenv import load_dotenv
from app.loader import FeedbackLoader
from app.articles import load_articles_from_xls

load_dotenv(override=True)

api_token = os.getenv("api_token")
api_url = os.getenv("api_url")
take = 5000
skip = 0
articles = load_articles_from_xls()

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


# def main(api_url, headers, params):
#     global last_call_time
#     for article in articles:
#
#         current_time = time.time()
#         if current_time - last_call_time < min_interval:
#             time.sleep(
#                 min_interval - (current_time - last_call_time)
#             )
#         last_call_time = time.time()
#         loader = FeedbackLoader(api_url, headers, params, article)
#         qty = loader.load_reviews()
#         print("Insert ", qty, " feedbacks for unit ", article, " completed at ",
#               datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S'))
#
#     return print('completed')
#
#
# if __name__ == '__main__':
#     print('выгрузка запущена')
#     main(api_url, headers, params)

if __name__ == '__main__':
    print('feedbacks load started')

    for article in articles:

        current_time = time.time()
        if current_time - last_call_time < min_interval:
            time.sleep(
                min_interval - (current_time - last_call_time)
            )
        last_call_time = time.time()
        loader = FeedbackLoader(api_url, headers, params, article)
        qty = loader.load_reviews()
        print("Insert ", qty, " feedbacks for unit ", article, " completed at ",
              datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S'))
    print('completed ')
    sys.stdout.flush() #Принудительно "сбрасывает" буферизированный вывод в консоль