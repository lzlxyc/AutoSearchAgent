"""
Auto Search Agent
================

一个智能的自动搜索代理，集成多种搜索工具和LLM能力。

主要功能：
- 自动网络搜索
- 智能回答生成
- 多源信息整合

快速开始：
    >>> from auto_search import AutoSearchAgent
    >>> agent = AutoSearchAgent()
    >>> result = agent.chat("什么是机器学习？")
"""

from .agent import AutoSearchAgent

# 版本信息
__version__ = "0.1.0"
__author__ = "Lin ZeLun"
__email__ = "lzl_xyc@163.com"


# 导出的主要类
__all__ = [
    "AutoSearchAgent",
]
