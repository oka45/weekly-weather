from datetime import datetime

import requests
import streamlit as st

PREFECTURE_CAPITALS = [
    {"name": "北海道", "capital": "札幌市", "longitude": 141.346667, "latitude": 43.064167},
    {"name": "青森県", "capital": "青森市", "longitude": 140.740000, "latitude": 40.824167},
    {"name": "岩手県", "capital": "盛岡市", "longitude": 141.152500, "latitude": 39.703333},
    {"name": "宮城県", "capital": "仙台市", "longitude": 140.871944, "latitude": 38.268889},
    {"name": "秋田県", "capital": "秋田市", "longitude": 140.102222, "latitude": 39.718611},
    {"name": "山形県", "capital": "山形市", "longitude": 140.363333, "latitude": 38.240278},
    {"name": "福島県", "capital": "福島市", "longitude": 140.467500, "latitude": 37.750000},
    {"name": "茨城県", "capital": "水戸市", "longitude": 140.446667, "latitude": 36.341667},
    {"name": "栃木県", "capital": "宇都宮市", "longitude": 139.883611, "latitude": 36.565556},
    {"name": "群馬県", "capital": "前橋市", "longitude": 139.060833, "latitude": 36.391111},
    {"name": "埼玉県", "capital": "さいたま市", "longitude": 139.648889, "latitude": 35.856944},
    {"name": "千葉県", "capital": "千葉市", "longitude": 140.123056, "latitude": 35.604444},
    {"name": "東京都", "capital": "新宿区", "longitude": 139.691667, "latitude": 35.689167},
    {"name": "神奈川県", "capital": "横浜市", "longitude": 139.642500, "latitude": 35.447778},
    {"name": "新潟県", "capital": "新潟市", "longitude": 139.023056, "latitude": 37.902222},
    {"name": "富山県", "capital": "富山市", "longitude": 137.211111, "latitude": 36.695000},
    {"name": "石川県", "capital": "金沢市", "longitude": 136.625556, "latitude": 36.594444},
    {"name": "福井県", "capital": "福井市", "longitude": 136.221667, "latitude": 36.065000},
    {"name": "山梨県", "capital": "甲府市", "longitude": 138.568333, "latitude": 35.663889},
    {"name": "長野県", "capital": "長野市", "longitude": 138.180833, "latitude": 36.651111},
    {"name": "岐阜県", "capital": "岐阜市", "longitude": 136.721944, "latitude": 35.390833},
    {"name": "静岡県", "capital": "静岡市", "longitude": 138.383056, "latitude": 34.976667},
    {"name": "愛知県", "capital": "名古屋市", "longitude": 136.906667, "latitude": 35.180278},
    {"name": "三重県", "capital": "津市", "longitude": 136.508333, "latitude": 34.730278},
    {"name": "滋賀県", "capital": "大津市", "longitude": 135.868056, "latitude": 35.004167},
    {"name": "京都府", "capital": "京都市", "longitude": 135.755556, "latitude": 35.021111},
    {"name": "大阪府", "capital": "大阪市", "longitude": 135.520000, "latitude": 34.686389},
    {"name": "兵庫県", "capital": "神戸市", "longitude": 135.183056, "latitude": 34.691111},
    {"name": "奈良県", "capital": "奈良市", "longitude": 135.832778, "latitude": 34.685278},
    {"name": "和歌山県", "capital": "和歌山市", "longitude": 135.167222, "latitude": 34.225833},
    {"name": "鳥取県", "capital": "鳥取市", "longitude": 134.238056, "latitude": 35.503333},
    {"name": "島根県", "capital": "松江市", "longitude": 133.050278, "latitude": 35.472222},
    {"name": "岡山県", "capital": "岡山市", "longitude": 133.935000, "latitude": 34.661667},
    {"name": "広島県", "capital": "広島市", "longitude": 132.459444, "latitude": 34.396389},
    {"name": "山口県", "capital": "山口市", "longitude": 131.471389, "latitude": 34.185556},
    {"name": "徳島県", "capital": "徳島市", "longitude": 134.559167, "latitude": 34.065556},
    {"name": "香川県", "capital": "高松市", "longitude": 134.043056, "latitude": 34.340000},
    {"name": "愛媛県", "capital": "松山市", "longitude": 132.765833, "latitude": 33.841667},
    {"name": "高知県", "capital": "高知市", "longitude": 133.530833, "latitude": 33.559444},
    {"name": "福岡県", "capital": "福岡市", "longitude": 130.418056, "latitude": 33.606389},
    {"name": "佐賀県", "capital": "佐賀市", "longitude": 130.298611, "latitude": 33.249167},
    {"name": "長崎県", "capital": "長崎市", "longitude": 129.867222, "latitude": 32.750000},
    {"name": "熊本県", "capital": "熊本市", "longitude": 130.741667, "latitude": 32.789444},
    {"name": "大分県", "capital": "大分市", "longitude": 131.612500, "latitude": 33.238056},
    {"name": "宮崎県", "capital": "宮崎市", "longitude": 131.423889, "latitude": 31.910833},
    {"name": "鹿児島県", "capital": "鹿児島市", "longitude": 130.558056, "latitude": 31.560278},
    {"name": "沖縄県", "capital": "那覇市", "longitude": 127.680833, "latitude": 26.212222},
]

WEATHER_ICON_BY_CODES = {
    frozenset({0}): "☀️",
    frozenset({1, 2}): "⛅️",
    frozenset({3}): "☁️",
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


def get_weather_api(longitude=139.6917, latitude=35.6895):
    """
    天気APIを使い最高気温・最低気温・天気状態を取得する関数
    Returns:
        dict or None: 正常に取得できた場合は dict、例外が発生した場合は None
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
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

            date_text, temperature_max, temperature_min, weather_code = forecast_rows[index - 1]
            dt = datetime.strptime(date_text, "%Y-%m-%d")
            st.write(dt.strftime("%m月%d日"))
            st.write(get_weather_icon(weather_code))
            st.text(f"{temperature_max}\n{temperature_min}")


option = st.selectbox(
    "都道府県を選択してください",
    PREFECTURE_CAPITALS,
    index=12,  # 初期値は東京
    format_func=lambda prefecture: prefecture["name"],
)


data = get_weather_api(option["longitude"], option["latitude"])

if data is not None:
    st.write(f"{option['name']} {option['capital']}の天気")
    display_weather_forecast(data)