import os
import pandas as pd

CSV_FILE = "daily_steps.csv"


def prepare_data():
    if not os.path.exists(CSV_FILE):
        print("Файл daily_steps.csv не найден. Запускаю обработку data.xml...")
        import data_loader
        print("Файл daily_steps.csv создан.")


def print_result(title, result):
    print(f"\n{title}")
    print("-" * 40)
    print(result)


def main():
    prepare_data()

    import analysis

    df = pd.read_csv(CSV_FILE)

    print_result("Рекордные даты:", analysis.record_date(df))
    print_result("Антирекордные даты:", analysis.antirecord_date(df))
    print_result("Среднее количество шагов:", analysis.mean_steps(df))
    print_result("Анализ дней недели:", analysis.an_days_of_week(df))
    print_result("Анализ месяцев:", analysis.an_month(df))
    print_result("Анализ годов:", analysis.an_year(df))
    print_result("Тренд активности:", analysis.trend_activity(df, year=2025))
    print_result("Выполнение цели:", analysis.target(df, 10000))

    print("\nДни, когда цель была выполнена:")
    print("-" * 40)
    for day in analysis.target_done_generator(df, tg=10000):
        print(day["date"], "-", day["steps"], "шагов")

    print("\nСерии активных дней:")
    print("-" * 40)
    for streak in analysis.streak_generator(df, goal=10000):
        print(streak, "дней подряд")

    median, std, percentile = analysis.numpy_analysis(df)
    print("\nNumPy анализ:")
    print("-" * 40)
    print("Ваше типичное количество шагов за день, основываясь на NumPy анализе:", median)
    if std < 2000:
        conclusion = 'Физическая активность достаточно стабильна.'
    elif std < 5000:
        conclusion = 'Физическая активность умеренно изменяется.'
    else:
        conclusion = 'Физическая активность нестабильна.'
    print(f'Стандартное отклонение: {std}')
    print(conclusion)
    print(f"В 90% дней пользователь ходил меньше {percentile} шагов",)


if __name__ == "__main__":
    main()
