import requests
from config import TENCENT_CONFIG
import json
import logging

class LocationAnalyzer:
    def __init__(self):
        self.api_key = TENCENT_CONFIG["key"]
        self.logger = logging.getLogger('LocationAnalyzer')
        
    def get_location_by_ip(self, ip=None):
        """
        使用腾讯位置服务API通过IP获取位置信息
        :param ip: 可选，指定IP地址。如果不指定，API将使用请求的源IP
        """
        try:
            self.logger.debug(f"开始IP定位查询，IP: {ip if ip else '当前IP'}")
            
            params = {
                'key': self.api_key,
                'output': 'json',
            }
            
            if ip:
                params['ip'] = ip
                
            response = requests.get(
                TENCENT_CONFIG["ip_location_url"],
                params=params,
                proxies={"http": None, "https": None}
            )
            
            self.logger.debug(f"API响应状态码: {response.status_code}")
            self.logger.debug(f"API响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 0:  # 0表示成功
                    location = result.get('result', {}).get('location', {})
                    address = result.get('result', {}).get('ad_info', {})
                    return {
                        'longitude': location.get('lng'),
                        'latitude': location.get('lat'),
                        'nation': address.get('nation'),
                        'province': address.get('province'),
                        'city': address.get('city'),
                        'district': address.get('district'),
                        'address': f"{address.get('nation')}{address.get('province')}{address.get('city')}{address.get('district')}",
                        'ip': result.get('result', {}).get('ip'),
                        'adcode': address.get('adcode')
                    }
                else:
                    self.logger.error(f"API返回错误: {result.get('message')}")
                    return None
            
            return None
            
        except Exception as e:
            self.logger.error(f"IP定位请求失败: {e}", exc_info=True)
            return None
            
    def process_location_data(self, ip=None):
        """
        处理位置数据
        """
        try:
            location_info = self.get_location_by_ip(ip)
            if location_info:
                self.logger.info(f"获取到位置信息: {location_info}")
                return location_info
            else:
                self.logger.warning("未能获取位置信息")
                return None
                
        except Exception as e:
            self.logger.error(f"处理位置数据错误: {e}", exc_info=True)
            return None 