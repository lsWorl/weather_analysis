import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from config import FILE_TEMPERATURE_PATH, FILE_HUMIDITY_PATH


class AlgorithmAnalyze:
    def __init__(self):
        self.file_temp = pd.ExcelFile(FILE_TEMPERATURE_PATH)
        self.file_hum = pd.ExcelFile(FILE_HUMIDITY_PATH)
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
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.title("Filtered Temperature and Humidity Data")
        plt.legend()
        plt.show()

    def Z_score_standarize(self, df):
        return (df.iloc[:, 1:] - df.iloc[:, 1:].mean()) / df.iloc[:, 1:].std()


if __name__ == "__main__":
    algorithm_analyze = AlgorithmAnalyze()
    data = {
        "city": ["用户所在地", "城市A", "城市B", "城市C"],
        "temperature": [22.5, 23.1, 21.8, 22.3],  # 温度
        "humidity": [55.0, 56.2, 54.8, 55.5],  # 湿度
        "rainfall": [1.2, 1.0, 1.5, 1.3],  # 降水量
    }
    df =pd.DataFrame(data)
    user_data = df.iloc[0,1:].values
    df_zscore=df.copy()
    df_zscore2 = algorithm_analyze.Z_score_standarize(df_zscore)
    print(df_zscore2)
    # df = pd.read_excel(FILE_TEMPERATURE_PATH,sheet_name='Sheet1')
    # data_dict = df.to_dict(orient='records')
    # temp_avg = []
    # for row in data_dict:
    #     temp_avg.append((row['最低温度(°C)'] +row['最高温度(°C)'])/2)
