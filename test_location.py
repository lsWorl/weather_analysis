from location_analyzer import LocationAnalyzer
from debug_config import TEST_AP_DATA
import time
import logging

logger = logging.getLogger('TestLocation')

def test_location_analyzer():
    analyzer = LocationAnalyzer()
    
    # 测试单个AP数据处理
    logger.info("测试处理单个AP数据")
    result = analyzer.process_ap_data(TEST_AP_DATA)
    logger.info(f"处理结果: {result}")
    
    # 测试多个AP数据
    logger.info("测试处理多个AP数据")
    for i in range(3):
        test_data = TEST_AP_DATA.copy()
        test_data['bssid'] = f"72:71:15:07:C7:F{i}"
        test_data['rssi'] = -44 - (i * 10)
        result = analyzer.process_ap_data(test_data)
        logger.info(f"第{i+1}个AP处理结果: {result}")
        time.sleep(1)  # 模拟间隔接收数据

if __name__ == "__main__":
    test_location_analyzer() 