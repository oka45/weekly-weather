from datetime import datetime

import requests
import streamlit as st

WEATHER_ICON_BY_CODES = {
    frozenset({0}): "☀️",
    frozenset({1, 2, 3}): "⛅️",
    frozenset({45, 48}): "🌫️",
    frozenset({51, 53, 55, 56, 57}): "🌦️",
    frozenset({61, 63, 65, 66, 67, 80, 81, 82}): "☔️",
    frozenset({71, 73, 75, 77, 85, 86}): "❄️",
    frozenset({95, 96, 99}): "⛈️",
}


def get_weather_icon(weather_code):
    """
    Open-Meteo の weather_code を天気アイコンに変換する関数

    Args:
        weather_code (int): Open-Meteo が返す天気コード

    Returns:
        str: 表示用の天気アイコン
    """
    for weather_codes, icon in WEATHER_ICON_BY_CODES.items():
        if weather_code in weather_codes:
            return icon
    return "❓"


def get_weather_api():
    """
    天気APIを使い最高気温・最低気温・天気状態を取得する関数
    Returns:
        dict or None: 正常に取得できた場合は dict、例外が発生した場合は None
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 35.6895,
        "longitude": 139.6917,
        "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code"],
        "timezone": "Asia/Tokyo",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 4xx/5xxなら例外
    except requests.exceptions.RequestException:
        st.error("天気情報の取得に失敗")
        return None
    return response.json()


def display_weather_forecast(data):
    """
    API から取得した週間天気を画面に表示する関数

    Args:
        data (dict): Open-Meteo API のレスポンス
    """
    daily_data = data["daily"]
    times_list = daily_data["time"]
    temperature_max_list = daily_data["temperature_2m_max"]
    temperature_min_list = daily_data["temperature_2m_min"]
    weather_code_list = daily_data["weather_code"]

    forecast_rows = list(
        zip(
            times_list,
            temperature_max_list,
            temperature_min_list,
            weather_code_list,
            strict=True,
        )
    )
    cols = st.columns(len(times_list) + 1)

    for index, col in enumerate(cols):
        with col:
            if index == 0:
                st.write("日付")
                st.write("天気")
                st.write("気温(最高/最低)")
                continue

            date_text, temperature_max, temperature_min, weather_code = forecast_rows[
                index - 1
            ]
            dt = datetime.strptime(date_text, "%Y-%m-%d")
            st.write(dt.strftime("%m月%d日"))
            st.write(get_weather_icon(weather_code))
            st.text(f"{temperature_max}\n{temperature_min}")


data = get_weather_api()

if data is not None:
    display_weather_forecast(data)
