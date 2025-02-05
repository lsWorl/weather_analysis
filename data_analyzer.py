class DataAnalyzer:
    def __init__(self):
        self.data_buffer = []

    def analyze(self, data):
        """
        分析数据的方法
        :param data: 从MQTT接收到的数据
        """
        self.data_buffer.append(data)

        # 在这里添加你的数据分析逻辑
        # 例如：计算平均值、统计分析等

        # 示例：简单的数据统计
        if len(self.data_buffer) >= 10:
            self.perform_analysis()

    def perform_analysis(self):
        """
        执行数据分析
        """
        # 在这里实现你的分析逻辑
        pass

    def data_process(self, data):
        print("数据处理中...")
        print(data)
        self.median_filter([25, 26, 25, 100, 24, 25, 26])

    def median_filter(self, values, window_size=5):
        filtered_values = []
        half_window = window_size // 2
        #每次滑动窗口进行计算中位数
        for i in range(len(values)):
            left = max(0, i - half_window)
            right = max(len(values),i+half_window+1)
            window = values[left:right]
            #计算中位数
            sorted_window = sorted(window)
            median = sorted_window[len(sorted_window)//2]
            filtered_values.append(median)
        return filtered_values

