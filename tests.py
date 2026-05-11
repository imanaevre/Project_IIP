import os
import sys
import importlib

import pandas as pd
import pytest


@pytest.fixture(scope="session", autouse=True)
def prepare_csv_for_analysis_import():
    if not os.path.exists("daily_steps.csv"):
        df = pd.DataFrame({
            "date": [
                "2025-01-01",
                "2025-01-02",
                "2025-01-03",
                "2025-01-04",
                "2025-01-05",
                "2025-01-06",
            ],
            "steps": [5000, 12000, 3000, 15000, 10000, 8000],
        })
        df.to_csv("daily_steps.csv", index=False)


@pytest.fixture
def analysis_module():
    if "analysis" in sys.modules:
        return sys.modules["analysis"]

    return importlib.import_module("analysis")


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": [
            "2025-01-01",
            "2025-01-02",
            "2025-01-03",
            "2025-01-04",
            "2025-01-05",
            "2025-01-06",
        ],
        "steps": [5000, 12000, 3000, 15000, 10000, 8000],
    })


def test_record_date(analysis_module, sample_df):
    result = analysis_module.record_date(sample_df, top=2)

    assert len(result) == 2
    assert result.iloc[0]["steps"] == 15000
    assert result.iloc[1]["steps"] == 12000


def test_antirecord_date(analysis_module, sample_df):
    result = analysis_module.antirecord_date(sample_df, top=2)

    assert len(result) == 2
    assert result.iloc[0]["steps"] == 3000
    assert result.iloc[1]["steps"] == 5000


def test_mean_steps(analysis_module, sample_df):
    result = analysis_module.mean_steps(sample_df)

    assert result == int(sample_df["steps"].mean())


def test_an_days_of_week(analysis_module, sample_df):
    result = analysis_module.an_days_of_week(sample_df.copy())

    assert isinstance(result, str)
    assert "Больше всего пользователь ходит" in result
    assert "Меньше всего активность" in result
    assert "Saturday" in result
    assert "Friday" in result
    assert "15000" in result
    assert "3000" in result


def test_an_month(analysis_module, sample_df):
    result = analysis_module.an_month(sample_df.copy())

    assert isinstance(result, str)
    assert "Больше всего пользователь ходил" in result
    assert "Меньше всего активность была" in result
    assert "январе" in result
    assert "8833" in result


def test_an_year(analysis_module, sample_df):
    result = analysis_module.an_year(sample_df.copy())

    assert isinstance(result, str)
    assert "Самый активный год: 2025" in result
    assert "Самый неактивный год: 2025" in result
    assert "долгосрочный тренд определить нельзя" in result


def test_trend_activity_grows(analysis_module):
    df = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=60),
        "steps": [1000] * 30 + [2000] * 30,
    })

    result = analysis_module.trend_activity(df, year=2025)

    assert "возросла" in result


def test_target(analysis_module, sample_df):
    result = analysis_module.target(sample_df, 10000)

    assert "Цель в 10000 шагов" in result
    assert "50.00%" in result


def test_target_done_generator(analysis_module, sample_df):
    result = list(analysis_module.target_done_generator(sample_df, tg=10000))

    assert len(result) == 3
    assert all(row["steps"] >= 10000 for row in result)


def test_streak_generator(analysis_module, sample_df):
    result = list(analysis_module.streak_generator(sample_df, goal=10000))

    assert result == [1, 2]


def test_numpy_analysis(analysis_module, sample_df):
    median, std, percentile = analysis_module.numpy_analysis(sample_df)

    assert isinstance(median, int)
    assert isinstance(std, float)
    assert isinstance(percentile, int)

    assert median == 9000
    assert percentile == 13500


def test_empty_dataframe(analysis_module):
    empty_df = pd.DataFrame(columns=["date", "steps"])

    result = analysis_module.record_date(empty_df)

    assert result is None
