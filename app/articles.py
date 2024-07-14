import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(override=True)

article_xlsx_path = os.getenv("article_xlsx_path")

def load_articles_from_xls():
    df = pd.read_excel(article_xlsx_path)
    articles_list = df.iloc[:, 1].tolist()
    return articles_list
