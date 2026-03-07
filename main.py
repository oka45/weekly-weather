import streamlit as st
import requests

def get_weather_api():
    """
    天気APIを使い最高気温・最低気温・天気状態を取得する関数
    Returns:
        dict or None: 正常に取得できた場合は dict、例外が発生した場合は None
    """
    url = 'https://api.open-meteo.com/v1/forecast'
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

data = get_weather_api()

if data is not None:
    st.write(data)
