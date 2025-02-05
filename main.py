import paho.mqtt.client as mqtt
import json
from config import MQTT_CONFIG, CAPITAL_CITIES_INFO
from datetime import datetime
import ssl  # 添加ssl模块导入
from location_analyzer import LocationAnalyzer
from weather_analyzer import WeatherAnalyzer
from db_handler import DBHandler
from climate_similarity import ClimateSimilarityAnalyzer
import logging
from data_analyzer import DataAnalyzer

class MQTTHandler:
    def __init__(self):
        self.client = mqtt.Client(client_id=MQTT_CONFIG["client_id"])
        self.setup_client()
        logging.basicConfig(level=logging.DEBUG)
        self.location_analyzer = LocationAnalyzer()
        self.weather_analyzer = WeatherAnalyzer()
        self.db_handler = DBHandler()
        self.analyzer = DataAnalyzer()
        self.climate_analyzer = ClimateSimilarityAnalyzer()
        self.temp_hum = {
            "timestamp":'',
            "temperature":0.0,
            "humidity":0.0
        }
    def setup_client(self):
        # 设置回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # 设置认证信息
        self.client.username_pw_set(MQTT_CONFIG["username"], MQTT_CONFIG["password"])

        # 配置TLS/SSL
        self.client.tls_set(
            ca_certs=MQTT_CONFIG["ca_certs"], tls_version=ssl.PROTOCOL_TLSv1_2
        )
        # 禁用证书验证（如果使用自签名证书）
        self.client.tls_insecure_set(True)

    def connect(self):
        try:
            self.client.connect(
                MQTT_CONFIG["broker_address"], MQTT_CONFIG["broker_port"], 60
            )
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("成功连接到MQTT服务器")
            # 连接成功后订阅主题
            client.subscribe(MQTT_CONFIG["broker_topic"])
        else:
            print(f"连接失败，返回码: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            # 解码消息
            payload = msg.payload.decode("utf-8", errors="replace")
            payload = payload.replace("\n", "").strip()
            # 解析JSON数据
            data = json.loads(payload)
            if "timestamp" not in data:
                # 添加时间戳
                data["timestamp"] = datetime.now().isoformat()
            # 判断数据类型并处理
            if "data" in data:  # 温湿度数据
                self.process_sensor_data(data)
            print(f"收到传感器数据 - 温度: {self.temp_hum['temperature']}°C, 湿度: {self.temp_hum['humidity']}%")
            self.process_ap_data(data)
        except json.JSONDecodeError:
            print(f"无法解析JSON数据: {payload}")
        except Exception as e:
            print(f"处理消息时出错: {e}")

    # 将相似度高的城市传到esp32
    def publish_message(self, topic, message):
        try:
            self.client.publish(topic, json.dumps(message))
            print(f"消息已发布到主题 {topic}: {message}")
        except Exception as e:
            print(f"发布消息时出错: {e}")

    def process_sensor_data(self, data):
        """处理温湿度传感器数据"""
        try:
            print("正在处理传感器数据...")
            print(f"原始数据: {data}")
            temp_hum = data["data"]
            temp = float(temp_hum.split("Temperature:")[1].split("C")[0].strip())
            hum = float(temp_hum.split("Humidity:")[1].split("%")[0].strip())
            self.temp_hum['temperature'] = temp
            self.temp_hum['humidity'] = hum
            
        except Exception as e:
            print(f"处理传感器数据错误: {e}")

    def process_ap_data(self, data):
        """处理位置数据和天气数据"""
        try:
            print("正在获取位置信息...")
            location_info = self.location_analyzer.process_location_data()
            if location_info:
                # 经纬度保留两位小数
                location_info["longitude"] = round(location_info["longitude"], 2)
                location_info["latitude"] = round(location_info["latitude"], 2)
                print("-" * 50)
                print("位置信息获取成功:")
                print(f"地址: {location_info['address']}")
                print(f"经度: {location_info['longitude']}")
                print(f"纬度: {location_info['latitude']}")

                # 获取当前位置天气
                print("\n获取当前位置天气...")
                current_weather = self.weather_analyzer.get_weather_by_location(
                    location_info["longitude"], location_info["latitude"]
                )

                if current_weather:
                    print(f"当前天气: {current_weather['text']}")
                    print(f"温度: {current_weather['temp']}°C")
                    print(f"湿度: {current_weather['humidity']}%")
                    print(f"风向: {current_weather['windDir']}")
                    print(f"风速: {current_weather['windSpeed']}km/h")
                    
                    print(f"将api的温度{current_weather['temp']}替换为传感器测到的温度{self.temp_hum['temperature']}")
                    current_weather['temp'] = self.temp_hum['temperature']
                    current_weather['humidity'] = self.temp_hum['humidity']
                    #将数据进行滤波
                    self.analyzer.data_process(current_weather)
                    return
                    # 保存当前位置天气数据
                    self.db_handler.save_weather_data(
                        location_info["city"], current_weather, "current"
                    )

                # 获取省会城市天气
                print("\n获取省会城市天气...")
                cities_weather = self.weather_analyzer.get_weather_for_cities(
                    CAPITAL_CITIES_INFO
                )

                for city_name, weather in cities_weather.items():
                    print(f"\n{city_name}天气:")
                    print(f"天气: {weather['text']}")
                    print(f"温度: {weather['temp']}°C")
                    print(f"湿度: {weather['humidity']}%")

                    # 保存省会城市天气数据
                    self.db_handler.save_weather_data(city_name, weather, "capital")

                print("-" * 50)

                # 将天气信息添加到原始数据中
                data["weather_info"] = current_weather

                if current_weather and cities_weather:
                    print("\n分析气候相似度...")
                    similar_cities = self.climate_analyzer.find_similar_cities(
                        current_weather, cities_weather, top_n=5
                    )

                    print("\n与当前位置气候最相似的城市:")
                    for city in similar_cities:
                        similarity_percentage = round(city["similarity"] * 100, 2)
                        print(f"\n{city['city']}:")
                        print(f"相似度: {similarity_percentage}%")
                        print(f"温度: {city['weather_data']['temp']}°C")
                        print(f"湿度: {city['weather_data']['humidity']}%")
                        print(f"天气: {city['weather_data']['text']}")

                    # 将相似度数据添加到原始数据中
                    data["climate_similarity"] = [
                        {"city": city["city"], "similarity": city["similarity"]}
                        for city in similar_cities
                    ]
                    for city in data["climate_similarity"]:
                        print("将相似度高的城市发布出去...")
                        print(city)
                        self.publish_message("data/similar_cities",city)
                    
            else:
                print("未能获取位置信息")

        except Exception as e:
            print(f"处理天气数据错误: {e}")
            import traceback

            print(traceback.format_exc())


def main():
    mqtt_handler = MQTTHandler()

    if mqtt_handler.connect():
        mqtt_handler.start()

        try:
            # 保持程序运行
            while True:
                pass
        except KeyboardInterrupt:
            print("正在关闭连接...")
            mqtt_handler.stop()


if __name__ == "__main__":
    main()
