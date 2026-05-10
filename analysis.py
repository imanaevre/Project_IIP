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

def an_month(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    month_of_year = df.groupby('month')['steps'].mean().astype(int)
    return max(month_of_year), min(month_of_year), month_of_year


def an_year(df):
    df['year'] = pd.to_datetime(df['date'])
    df['year'] = df['year'].dt.year
    years = df.groupby('year')['steps'].mean().astype(int)
    return max(years), min(years), years

def trend_activity(df, year):
    df['year'] = pd.to_datetime(df['date'])
    df = df[df['year'].dt.year == year]
    first_steps = df['steps'].head(30).sum()
    last_steps = df['steps'].tail(30).sum()
    if first_steps > last_steps:
        return 'К концу года ваша активность немного снизилась!'
    elif first_steps == last_steps:
        return 'Ваша активность осталась стабильной!'
    else:
        return 'К концу года ваша активность возросла!'

def target(df, tg):
    df_target = df[df['steps'] >= tg]
    percent = len(df_target) / len(df) * 100
    return f'Цель в {tg} шагов была выполнена в {percent:.2f}% дней'






