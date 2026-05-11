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
    df['day_of_week'] = df['date'].dt.day_name()
    grouped = df.groupby('day_of_week')['steps'].mean()
    max_day = grouped.idxmax()
    min_day = grouped.idxmin()
    max_steps = int(grouped.max())
    min_steps = int(grouped.min())
    return (
        f'Больше всего пользователь ходит в {max_day} '
        f'— в среднем {max_steps} шагов.\n'
        f'Меньше всего активность в {min_day} '
        f'— в среднем {min_steps} шагов.'
    )

@check_empty
@show_analysis_name('Анализ месяцев')
def an_month(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    grouped = df.groupby('month')['steps'].mean()
    month_names = {
        1: 'январе',
        2: 'феврале',
        3: 'марте',
        4: 'апреле',
        5: 'мае',
        6: 'июне',
        7: 'июле',
        8: 'августе',
        9: 'сентябре',
        10: 'октябре',
        11: 'ноябре',
        12: 'декабре'
    }
    max_month = grouped.idxmax()
    min_month = grouped.idxmin()
    max_steps = int(grouped.max())
    min_steps = int(grouped.min())
    difference = max_steps - min_steps
    return (
        f'Больше всего пользователь ходил в {month_names[max_month]} '
        f'— в среднем {max_steps} шагов в день.\n'
        f'Меньше всего активность была в {month_names[min_month]} '
        f'— в среднем {min_steps} шагов в день.\n'
        f'Разница между самым активным и самым неактивным месяцем составила '
        f'{difference} шагов в день.'
    )


@check_empty
@show_analysis_name('Анализ годов')
def an_year(df):
    df['date'] = pd.to_datetime(df['date'])

    df['year'] = df['date'].dt.year

    grouped = df.groupby('year')['steps'].mean()

    max_year = grouped.idxmax()
    min_year = grouped.idxmin()

    max_steps = int(grouped.max())
    min_steps = int(grouped.min())

    difference = max_steps - min_steps

    if len(grouped) > 1:
        first_year = grouped.index.min()
        last_year = grouped.index.max()
        first_value = grouped.loc[first_year]
        last_value = grouped.loc[last_year]
        if last_value > first_value:
            trend = (
                f'За период с {first_year} по {last_year} средняя активность выросла '
                f'с {int(first_value)} до {int(last_value)} шагов в день.'
            )
        elif last_value < first_value:
            trend = (
                f'За период с {first_year} по {last_year} средняя активность снизилась '
                f'с {int(first_value)} до {int(last_value)} шагов в день.'
            )
        else:
            trend = (
                f'За период с {first_year} по {last_year} средняя активность не изменилась.'
            )
    else:
        trend = 'В данных есть только один год, поэтому долгосрочный тренд определить нельзя.'
    return (
        f'Самый активный год: {max_year} — в среднем {max_steps} шагов в день.\n'
        f'Самый неактивный год: {min_year} — в среднем {min_steps} шагов в день.\n'
        f'Разница между ними составила {difference} шагов в день.\n'
        f'{trend}'
    )

@check_empty
@show_analysis_name('Анализ тренда активности')
def trend_activity(df, year=2025):
    df['year'] = pd.to_datetime(df['date'])
    df = df[df['year'].dt.year == year]
    first_steps = df['steps'].head(30).sum()
    last_steps = df['steps'].tail(30).sum()
    if first_steps > last_steps:
        return f'К концу {year} года ваша активность немного снизилась!'
    elif first_steps == last_steps:
        return f'Ваша активность осталась стабильной за {year} год!'
    else:
        return f'К концу {year} года ваша активность возросла!'

@check_empty
@show_analysis_name('Анализ выполнения цели')
def target(df, tg):
    df_target = df[df['steps'] >= tg]
    percent = len(df_target) / len(df) * 100
    return f'Цель в {tg} шагов была выполнена в {percent:.2f}% дней'

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

@check_empty
@show_analysis_name('Анализ NumPy')
def numpy_analysis(df):
    steps = df['steps'].values

    median = np.median(steps)
    std = np.std(steps)
    percentile = np.percentile(steps, 90)

    return int(median), round(float(std), 2), int(percentile)








