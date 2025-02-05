import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class AlgorithmAnalyze:
    def __init__(self):
        pass

    def temp_hum_chart(self, smoothed_data):
        print(smoothed_data)
        plt.figure(figsize=(10, 5))
        plt.plot(
            smoothed_data["timestamp"],
            smoothed_data["temperature"],
            label="Temperature (°C)",
        )
        plt.plot(
            smoothed_data["timestamp"], smoothed_data["humidity"], label="Humidity (%)"
        )
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Filtered Temperature and Humidity Data')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    # 生成测试数据
    num_points = 50  # 生成 50 个数据点
    time_series = pd.date_range(start="2023-01-01", periods=num_points, freq="H")
    # 模拟温度和湿度数据
    np.random.seed(42)  # 固定随机种子，确保可复现
    temperature = np.random.normal(
        loc=20, scale=5, size=num_points
    )  # 以 20°C 为均值的正态分布
    humidity = np.random.normal(
        loc=50, scale=10, size=num_points
    )  # 以 50% 为均值的正态分布
    # 生成 DataFrame
    smoothed_data = pd.DataFrame(
        {"timestamp": time_series, "temperature": temperature, "humidity": humidity}
    )
    algorithm_analyze = AlgorithmAnalyze()
    algorithm_analyze.temp_hum_chart(smoothed_data)
