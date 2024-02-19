import pandas as pd


def load_articles_from_xls():
    df = pd.read_excel(r'C:\Users\OstryiEA\PycharmProjects\wb_feedbacks\articles_list.xlsx')
    articles_list = df.iloc[:, 1].tolist()
    return articles_list
