import pandas as pd

df = pd.read_csv('daily_steps.csv')

def record_date(top, df):
    return df.nlargest(top, 'steps')

def antirecord_date(top, df):
    return df.nsmallest(top, 'steps')



