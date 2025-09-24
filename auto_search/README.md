# 核心代码目录

```text
AutoSearchAgent
│   agent.py       : 最终封装的给外部直接调用的agent模块
│   config.py      ：配置项脚本，读取根目录下的.env里面的相关配置
│   __init__.py
│   
├───api
│   │   llms.py    : 大模型服务相关调用
│   └───search.py  : 提供给agent调用的外部功能函数 
│        
└───utils
    │   helpers.py : 与项目功能无关的基础工具库
    └───tools.py   : 跟项目功能相关的函数库
```
