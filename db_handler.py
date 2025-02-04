import mysql.connector
from config import TIDB_CONFIG
import logging
from datetime import datetime

class DBHandler:
    def __init__(self):
        self.logger = logging.getLogger('DBHandler')
        self.conn = None
        self.connect()
        
    def connect(self):
        """连接到TiDB"""
        try:
            self.conn = mysql.connector.connect(
                host=TIDB_CONFIG["host"],
                port=TIDB_CONFIG["port"],
                user=TIDB_CONFIG["user"],
                password=TIDB_CONFIG["password"],
                database=TIDB_CONFIG["database"]
            )
            self.create_tables()
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            
    def create_tables(self):
        """创建必要的数据表"""
        try:
            print("创建表...")
            cursor = self.conn.cursor()
            
            # 创建天气数据表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    city_name VARCHAR(50),
                    temperature FLOAT,
                    humidity INT,
                    weather VARCHAR(50),
                    wind_direction VARCHAR(50),
                    wind_speed FLOAT,
                    timestamp DATETIME,
                    location_type VARCHAR(20)
                )
            """)
            
            self.conn.commit()
            cursor.close()
        except Exception as e:
            self.logger.error(f"创建表失败: {e}")
            
    def save_weather_data(self, city_name, weather_data, location_type="capital"):
        """保存天气数据到数据库"""
        try:
            print("保存天气数据...")
            cursor = self.conn.cursor()
            
            query = """
                INSERT INTO weather_data 
                (city_name, temperature, humidity, weather, 
                wind_direction, wind_speed, timestamp, location_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                city_name,
                float(weather_data['temp']),
                int(weather_data['humidity']),
                weather_data['text'],
                weather_data['windDir'],
                float(weather_data['windSpeed']),
                datetime.now(),
                location_type
            )
            
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()
            
        except Exception as e:
            self.logger.error(f"保存天气数据失败: {e}")
            
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close() 