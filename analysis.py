import pandas as pd

df = pd.read_csv('daily_steps.csv')

def record_date(top, df):
    return df.nlargest(top, 'steps')

def antirecord_date(top, df):
    return df.nsmallest(top, 'steps')

def mean_steps(df):
    return df['steps'].mean().astype(int)


def an_days_of_week(df):
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = df['date'].dt.dayofweek
    d_of_week = df.groupby('days')['steps'].mean().astype(int)
    return max(d_of_week), min(d_of_week), d_of_week

print(mean_steps(df))

