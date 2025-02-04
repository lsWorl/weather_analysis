from location_analyzer import LocationAnalyzer
import logging

logger = logging.getLogger('TestIPLocation')

def test_ip_location():
    analyzer = LocationAnalyzer()
    
    # 测试当前IP定位
    logger.info("测试当前IP定位")
    result = analyzer.process_location_data()
    logger.info(f"当前IP定位结果: {result}")
    
    # 测试指定IP定位
    test_ip = "119.29.29.29"  # 测试用IP
    logger.info(f"测试指定IP定位: {test_ip}")
    result = analyzer.process_location_data(test_ip)
    logger.info(f"指定IP定位结果: {result}")

if __name__ == "__main__":
    test_ip_location() 