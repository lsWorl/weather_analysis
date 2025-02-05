import requests
import logging
from config import QWEATHER_CONFIG


class WeatherAnalyzer:
    def __init__(self):
        self.api_key = QWEATHER_CONFIG["key"]
        self.logger = logging.getLogger("WeatherAnalyzer")

    def get_weather_by_location(self, longitude, latitude):
        """
        使用经纬度获取天气数据
        :param longitude: 经度
        :param latitude: 纬度
        """
        try:
            # 将经纬度组合成location参数
            location = f"{longitude},{latitude}"
            params = {"key": self.api_key, "location": location}

            self.logger.debug(f"正在获取位置天气数据: {location}")
            response = requests.get(
                QWEATHER_CONFIG["weather_api"],
                params=params,
                proxies={"http": None, "https": None},
            )

            if response.status_code == 200:
                result = response.json()
                self.logger.debug(f"天气API响应: {result}")

                if result.get("code") == "200":
                    return result["now"]
                else:
                    self.logger.error(f"天气API返回错误: {result.get('code')}")
            return None

        except Exception as e:
            self.logger.error(f"获取天气数据失败: {e}")
            return None

    def get_weather_for_cities(self, cities_info):
        """
        获取多个城市的天气数据
        :param cities_info: 包含城市经纬度信息的列表
        """
        weather_data = {}
        for city in cities_info:
            try:
                weather = self.get_weather_by_location(
                    city["longitude"], city["latitude"]
                )
                if weather:
                    weather_data[city["name"]] = weather
            except Exception as e:
                self.logger.error(f"获取城市{city['name']}天气失败: {e}")

        return weather_data
