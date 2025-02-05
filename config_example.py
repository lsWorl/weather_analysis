# MQTT配置
MQTT_CONFIG = {
    "broker_address": "连接地址",
    "broker_port": 8883,  #端口
    "broker_topic": "esp32/#", #订阅主题
    "username": "name",     #访问控制里面的客户端认证用户名（自己设置的）
    "password": "pwd",      #访问控制里面的客户端认证密码
    "client_id": "python_client", #客户端id，可以自定义
    "ca_certs": "./emqxsl-ca.crt",  # CA证书路径  将EMQX中整数下载放在根目录下
    "tls_version": 2  # TLS版本
}

# 腾讯位置服务API配置
TENCENT_CONFIG = {
    "key": "腾讯位置key",
    "ip_location_url": "https://apis.map.qq.com/ws/location/v1/ip"
}


# 和风天气API配置
QWEATHER_CONFIG = {
    "key": "和风天气key",
    "weather_api": "https://devapi.qweather.com/v7/weather/now",
    "city_lookup_api": "https://geoapi.qweather.com/v2/city/lookup"
}

# TiDB配置
TIDB_CONFIG = {
    "host": "gateway01.us-east-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "36yVzSYVQLRJdFE.root",
    "password": "tqVQCMLiyAOC7z72",
    "database": "test"
}


# 省会城市经纬度信息
CAPITAL_CITIES_INFO = [
    {"name": "Beijing", "longitude": 116.41, "latitude": 39.90},
    {"name": "Shanghai", "longitude": 121.47, "latitude": 31.23},
    {"name": "Guangzhou", "longitude": 113.28, "latitude": 23.13},
    {"name": "Chongqing", "longitude": 106.55, "latitude": 29.57},
    {"name": "Chengdu", "longitude": 104.07, "latitude": 30.67},
    {"name": "Wuhan", "longitude": 114.31, "latitude": 30.59},
    {"name": "Hangzhou", "longitude": 120.21, "latitude": 30.25},
    {"name": "Nanjing", "longitude": 118.78, "latitude": 32.07},
    {"name": "沈阳", "longitude": 123.43, "latitude": 41.80},
    {"name": "长春", "longitude": 125.32, "latitude": 43.82},
    {"name": "哈尔滨", "longitude": 126.63, "latitude": 45.75},
    {"name": "西安", "longitude": 108.95, "latitude": 34.27},
    {"name": "济南", "longitude": 117.12, "latitude": 36.65},
    {"name": "郑州", "longitude": 113.65, "latitude": 34.76},
    {"name": "长沙", "longitude": 112.98, "latitude": 28.22},
    {"name": "福州", "longitude": 119.30, "latitude": 26.08},
    {"name": "贵阳", "longitude": 106.63, "latitude": 26.65},
    {"name": "昆明", "longitude": 102.73, "latitude": 25.04},
    {"name": "南宁", "longitude": 108.37, "latitude": 22.82},
    {"name": "海口", "longitude": 110.35, "latitude": 20.02},
    {"name": "兰州", "longitude": 103.82, "latitude": 36.07},
    {"name": "西宁", "longitude": 101.78, "latitude": 36.62},
    {"name": "银川", "longitude": 106.27, "latitude": 38.47},
    {"name": "呼和浩特", "longitude": 111.75, "latitude": 40.84},
    {"name": "乌鲁木齐", "longitude": 87.62, "latitude": 43.82},
    {"name": "拉萨", "longitude": 91.13, "latitude": 29.65},
    {"name": "太原", "longitude": 112.55, "latitude": 37.87},
    {"name": "合肥", "longitude": 117.27, "latitude": 31.86},
    {"name": "南昌", "longitude": 115.89, "latitude": 28.68}
] 