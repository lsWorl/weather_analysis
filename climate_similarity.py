import numpy as np
from collections import defaultdict

class ClimateSimilarityAnalyzer:
    def __init__(self):
        # 天气状况的相似度权重表（示例）
        self.weather_similarity_weights = {
            "晴": {
                "晴": 1.0,
                "多云": 0.8,
                "阴": 0.6,
                "小雨": 0.3,
                "中雨": 0.2,
                "大雨": 0.1
            },
            "多云": {
                "晴": 0.8,
                "多云": 1.0,
                "阴": 0.8,
                "小雨": 0.4,
                "中雨": 0.3,
                "大雨": 0.2
            },
            # 可以继续添加其他天气状况的相似度权重
        }
        
        # 各个指标的权重
        self.weights = {
            'temperature': 0.5,  # 温度权重
            'humidity': 0.3,     # 湿度权重
            'weather': 0.2       # 天气状况权重
        }
    
    def calculate_temperature_similarity(self, temp1, temp2):
        """
        计算温度相似度
        使用高斯函数计算温度差异，温差越小相似度越高
        :param temp1: 第一个温度值
        :param temp2: 第二个温度值
        :return: 相似度 (0-1)
        """
        temp_diff = abs(float(temp1) - float(temp2))
        # 使用高斯函数，温差5度时相似度降至0.5
        similarity = np.exp(-(temp_diff ** 2) / (2 * 5 ** 2))
        return similarity
    
    def calculate_humidity_similarity(self, hum1, hum2):
        """
        计算湿度相似度
        使用线性差异计算湿度相似度
        :param hum1: 第一个湿度值
        :param hum2: 第二个湿度值
        :return: 相似度 (0-1)
        """
        hum_diff = abs(float(hum1) - float(hum2))
        # 湿度差异超过50%时相似度为0
        similarity = max(0, 1 - hum_diff / 50)
        return similarity
    
    def calculate_weather_similarity(self, weather1, weather2):
        """
        计算天气状况相似度
        使用预定义的相似度权重表
        :param weather1: 第一个天气状况
        :param weather2: 第二个天气状况
        :return: 相似度 (0-1)
        """
        # 如果天气状况不在权重表中，返回默认相似度
        if weather1 not in self.weather_similarity_weights or \
           weather2 not in self.weather_similarity_weights.get(weather1, {}):
            return 0.5
        
        return self.weather_similarity_weights[weather1][weather2]
    
    def calculate_overall_similarity(self, weather_data1, weather_data2):
        """
        计算总体气候相似度
        :param weather_data1: 第一个地点的天气数据
        :param weather_data2: 第二个地点的天气数据
        :return: 总体相似度 (0-1)
        """
        # 计算各个维度的相似度
        temp_similarity = self.calculate_temperature_similarity(
            weather_data1['temp'], 
            weather_data2['temp']
        )
        
        humidity_similarity = self.calculate_humidity_similarity(
            weather_data1['humidity'], 
            weather_data2['humidity']
        )
        
        weather_similarity = self.calculate_weather_similarity(
            weather_data1['text'], 
            weather_data2['text']
        )
        
        # 计算加权平均
        overall_similarity = (
            self.weights['temperature'] * temp_similarity +
            self.weights['humidity'] * humidity_similarity +
            self.weights['weather'] * weather_similarity
        )
        
        return overall_similarity
    
    def find_similar_cities(self, user_weather, cities_weather, top_n=5):
        """
        找出与用户所在地气候最相似的城市
        :param user_weather: 用户所在地的天气数据
        :param cities_weather: 其他城市的天气数据字典
        :param top_n: 返回相似城市的数量
        :return: 排序后的相似城市列表，包含相似度分数
        """
        similarities = []
        
        for city_name, city_weather in cities_weather.items():
            similarity = self.calculate_overall_similarity(user_weather, city_weather)
            similarities.append({
                'city': city_name,
                'similarity': similarity,
                'weather_data': city_weather
            })
        
        # 按相似度降序排序
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similarities[:top_n] 