import pandas as pd
import numpy as np

def check_empty(func):
    def wrapper(df, *args, **kwargs):
        if df.empty:
            print('DataFrame пуст')
            return
        return func(df, *args, **kwargs)
    return wrapper

def show_analysis_name(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('\n' + '=' * 40)
            print(f'АНАЛИЗ: {name}')
            print('=' * 40)
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

df = pd.read_csv('daily_steps.csv')

@check_empty
@show_analysis_name('Анализ рекордных дат')
def record_date(df, top=5):
    return df.nlargest(top, 'steps')

@check_empty
@show_analysis_name('Анализ анти-рекордных дат')
def antirecord_date(df, top=5):
    return df.nsmallest(top, 'steps')

@check_empty
@show_analysis_name('Анализ среднего значения')
def mean_steps(df):
    return df['steps'].mean().astype(int)

@check_empty
@show_analysis_name('Анализ дней недели')
def an_days_of_week(df):
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = df['date'].dt.dayofweek
    d_of_week = df.groupby('days')['steps'].mean().astype(int)
    return max(d_of_week), min(d_of_week), d_of_week

@check_empty
@show_analysis_name('Анализ месяцев')
def an_month(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    month_of_year = df.groupby('month')['steps'].mean().astype(int)
    return max(month_of_year), min(month_of_year), month_of_year

@check_empty
@show_analysis_name('Анализ годов')
def an_year(df):
    df['year'] = pd.to_datetime(df['date'])
    df['year'] = df['year'].dt.year
    years = df.groupby('year')['steps'].mean().astype(int)
    return max(years), min(years), years

@check_empty
@show_analysis_name('Анализ тренда активности')
def trend_activity(df, year=2025):
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

@check_empty
@show_analysis_name('Анализ выполнения цели')
def target(df, tg):
    df_target = df[df['steps'] >= tg]
    percent = len(df_target) / len(df) * 100
    return f'Цель в {tg} шагов была выполнена в {percent:.2f}% дней'

@check_empty
@show_analysis_name('Анализ выполнения цели')
def target_done_generator(df, tg=10000):
    for _, row in df.iterrows():
        if row['steps'] >= tg:
            yield row

@check_empty
@show_analysis_name('Анализ серии дней')
def streak_generator(df, goal=10000):
    streak = 0
    for _, row in df.iterrows():
        if row['steps'] >= goal:
            streak += 1
        else:
            if streak > 0:
                yield streak
            streak = 0
    if streak > 0:
        yield streak










