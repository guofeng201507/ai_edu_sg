import pandas as pd


def load_excel():
    headers = ['Q_NO', 'TOPIC', 'DIFFICULTY', 'QUESTION', 'CHOICE', 'ANSWER', 'REMARK']
    df = pd.read_excel('./question_base/math_db.xls', skiprows=0)
    df.columns = headers
    return df
