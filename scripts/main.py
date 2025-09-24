import sys
sys.path.append('..')

from auto_search import AutoSearchAgent


if __name__ == '__main__':
    auto_search = AutoSearchAgent()
    auto_search.chat('请帮我介绍一下PPO算法的相关知识')
