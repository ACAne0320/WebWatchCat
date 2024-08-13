import os
import requests

API_KEY = os.getenv("SENIVERSE_API_KEY")
LOCATION = "changsha"
BASE_URL = "https://api.seniverse.com/v3"

def fetch_data(endpoint, params):
    url = f"{BASE_URL}/{endpoint}.json"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None

def get_current_weather():
    params = {
        "key": API_KEY,
        "location": LOCATION,
    }
    data = fetch_data("weather/now", params)
    if data:
        result = data['results'][0]
        location = result['location']
        weather = result['now']

        summary = (
            f"位置: {location['name']}, {location['country']}, "
            f"时区: {location['timezone']}, 上次更新时间: {result['last_update']}\n"
            f"当前天气: {weather['text']}, 温度: {weather['temperature']}°C, "
        )
        print(summary)
        return summary
    return "获取当前天气信息失败。"

def get_weather_suggestion():
    params = {
        "key": API_KEY,
        "location": LOCATION,
        "days": 1,
    }
    data = fetch_data("life/suggestion", params)
    if data:
        result = data['results'][0]
        location = result['location']
        suggestion = result['suggestion']

        summary = (
            f"位置: {location['name']}, {location['country']}, "
            f"时区: {location['timezone']}, 上次更新时间: {result['last_update']}\n"
            f"日期: {suggestion[0]['date']}\n"
            f"空调建议: {suggestion[0]['ac']['brief']}, 详情: {suggestion[0]['ac']['details']}\n"
            f"空气污染: {suggestion[0]['air_pollution']['brief']}, 详情: {suggestion[0]['air_pollution']['details']}\n"
            f"晾晒建议: {suggestion[0]['airing']['brief']}, 详情: {suggestion[0]['airing']['details']}\n"
            f"舒适度: {suggestion[0]['comfort']['brief']}, 详情: {suggestion[0]['comfort']['details']}\n"
            f"心情: {suggestion[0]['mood']['brief']}, 详情: {suggestion[0]['mood']['details']}\n"
            f"是否带伞: {suggestion[0]['umbrella']['brief']}, 详情: {suggestion[0]['umbrella']['details']}\n"
            f"紫外线: {suggestion[0]['uv']['brief']}, 详情: {suggestion[0]['uv']['details']}\n"
        )
        print(summary)
        return summary
    return "获取天气建议失败。"
