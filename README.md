## 简介

该项目旨在通过 MQTT 协议实现设备间的通信，主要功能包括从传感器获取数据、分析数据相似度，并将结果发布给其他订阅设备。

## 功能

1. **数据采集**：
   - 从传感器设备获取环境数据（如温度、湿度等）。
   - 通过 MQTT 协议接收传感器数据。

2. **数据处理**：
   - 使用气候分析模块计算当前环境与其他城市的气候相似度。
   - 处理并解析接收到的 JSON 数据。

3. **数据发布**：
   - 将相似度高的城市信息通过 MQTT 发布到指定主题。
   - 确保发布的主题不包含通配符。

4. **日志记录**：
   - 记录系统运行日志，便于调试和监控。

## 使用方法

1. **配置环境**：
   - 安装所需的 Python 库：`mysql-connector-python`、`requests`、`paho-mqtt` 等。
   - 配置 `config.py` 文件中的数据库和 MQTT 连接信息。

2. **运行项目**：
   - 启动 MQTT 代理服务器。
   - 运行主程序以开始数据采集和处理。

3. **订阅主题**：
   - 其他设备可以订阅指定的 MQTT 主题以接收相似度数据。

## 注意事项

- 确保 MQTT 主题名称不包含通配符。
- 确保网络连接正常，以便与 MQTT 代理和外部 API 通信。
