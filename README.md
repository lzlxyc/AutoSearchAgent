# AutoSearchAgent

<div align="center">

![GitHub](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**智能搜索代理 | 自动判断搜索需求 | 智能爬取与分析**

</div>

## 📖 简介

AutoSearchAgent 是一个智能搜索代理系统，能够自动判断用户问题是否需要联网搜索，并智能地进行信息检索、爬取和分析。目前主要支持通过知乎平台进行搜索和数据获取。

## 🚀 核心特性

- 🤖 **智能判断** - 自动识别问题是否需要联网搜索
- 🔍 **多渠道搜索** - 支持搜索引擎集成（当前只支持知乎）
- 📊 **数据爬取** - 自动获取和分析搜索结果
- 💾 **数据持久化** - 智能保存搜索记录和结果
- 🧠 **大模型集成** - 结合AI模型进行智能问答

## ⚡ 快速开始

### 环境配置

1. **克隆项目**
```bash
git clone https://github.com/lzlxyc/AutoSearchAgent.git
cd AutoSearchAgent
```

2. **配置环境变量**
- 在项目根目录中，将`.env.example`重命名为 `.env` 文件，配置以下参数：
```shell
cp .env.example .env
```

- 在.env文件中配置相关参数
```env
# 大模型API-KEY配置
DS_API_KEY=
DS_API_URL=https://api.deepseek.com

# 外部函数API-KEY配置
GOOGLE_SEARCH_KEY=
CSE_ID=

# Google搜索网路相关配置
COOKIE=
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36

# 项目配置：
# 1、保存的数据地址
SAVE_DATA_DIR=../search_data
```
- [cookit获取方式请点击此处](assets/cookit获取.png)
- google_search_key获取方式: https://blog.csdn.net/whatday/article/details/113750998


3. **安装依赖**
```bash
pip install -r requirements.txt
```

### 运行方式
- 本地验证
```shell
cd scripts & python ./main.py
```
- web可视化问答
```shell
cd server & python -m streamlit run app.py
```


**具体模块调用**
```python
from auto_search import AutoSearchAgent

if __name__ == '__main__':
    auto_search = AutoSearchAgent()
    auto_search.chat('请帮我介绍一下RLHF算法的相关知识')
```

## 🏗️ 系统架构
```text
用户问题输入
    ↓
关键词提炼模型
    ↓
判断模型 → 无需搜索 → 直接生成答案
    ↓
需要搜索
    ↓
调用搜索引擎
    ↓
搜索结果清洗
    ↓
目标网站爬取
    ↓
数据提取与处理
    ↓
智能答案生成
    ↓
最终输出
```

## 🔧 核心模块

### 1. 关键词提取模块
- 智能分析用户问题
- 提取核心搜索关键词

### 2. 搜索判断模块
- 基于大模型智能判断搜索需求
- 优化搜索策略选择

### 3. 数据爬取模块
- 自动化网页爬取
- 智能数据清洗和提取

### 4. 答案生成模块
- 结合上下文生成精准答案
- 支持多种输出格式

## 📈 当前功能

✅ **智能问答系统** - 基于大模型的对话能力  
✅ **自动搜索触发** - 智能识别知识边界  
✅ **数据爬取保存** - 自动化信息收集  
✅ **报告生成** - 结构化结果输出  

## 🎯 开发计划

### 短期目标
- [ ] **可视化界面开发** - 提供友好的用户交互界面
- [ ] **API服务封装** - 支持外部系统调用
- 
### 长期规划
- [ ] 多平台搜索支持（百度、谷歌等）
- [ ] 高级数据分析功能
- [ ] 实时搜索监控
- [ ] 个性化搜索配置
- [ ] 专门的论文搜索
- [ ] 加入rag检索相关的内容

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- 项目主页：https://github.com/lzlxyc/AutoSearchAgen
- 问题反馈：https://github.com/lzlxyc/AutoSearchAgen/issues
- 邮箱：lzl_xyc@163.com

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ 支持一下！**

</div>
```