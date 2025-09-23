import os
import json

from config import SAVE_DATA_DIR
from tools import get_search_text, google_search


def get_answer(query:str):
    """
    当你无法回答某个问题时，调用该函数，能够获得答案
    :param query: 必选参数，询问的问题，字符串类型对象
    :return：某问题的答案，以字符串形式呈现
    """
    print(f'【1】正在接入谷歌搜索:{query}，查找和问题相关的答案...')
    # 默认搜索返回10个答案
    results = google_search(query=query, num_results=3, site_url='https://zhihu.com/')

    # 创建对应问题的子文件夹
    save_dir = os.path.join(SAVE_DATA_DIR, query)
    os.makedirs(save_dir, exist_ok=True)

    num_tokens = 0
    content = ""
    # 单独提取links放在一个list中
    print('【2】正在读取搜索的到的相关答案...')
    for item in results:
        url = item['link']
        title = get_search_text(query, url)
        print(title)

        with open(os.path.join(save_dir, f'{title}.json'), 'r') as f:
            jd = json.load(f)
        num_tokens += jd[0]['tokens']
        if num_tokens <= 12000:
            content += jd[0]['content']
        else:
            break

    print('【3】正在进行最后的整理...')
    return json.dumps({"Question": query, "Answer": content}, ensure_ascii=False)


SupportFunctionCallList = [
    {'function': {'description': '当无法回答某个问题时，调用该函数获得答案',
                  'name': 'get_answer',
                  'parameters': {'properties': {'query': {'description': '询问的问题',
                                                          'type': 'string'}},
                                 'required': ['query'],
                                 'type': 'object'}},
     'type': 'function'}
]