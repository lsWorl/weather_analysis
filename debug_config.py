import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# 测试数据
TEST_SENSOR_DATA = {
    "data": "Temperature: 25.6C, Humidity: 65.0%",
    "device": "esp32"
}

TEST_AP_DATA = {
    "ssid": "starbucks",
    "bssid": "72:71:15:07:C7:F4",
    "rssi": -44,
    "channel": 1
} 