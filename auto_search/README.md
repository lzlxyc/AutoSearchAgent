# 核心代码目录
- auto_search_agent.py: 最终封装的给外部直接调用的agent模块
- config.py：配置项脚本，读取根目录下的.env里面的相关配置
- function_calls.py: 提供给agent调用的外部功能函数
- llms_api.py: 大模型服务相关调用
- tools.py: 跟项目功能相关的函数库
- utils.py: 与项目功能无关的基础工具库
- main.py: 程序运行的主入口