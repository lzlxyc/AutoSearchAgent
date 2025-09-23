import json
import requests
from lxml import etree

from config import SAVE_DATA_DIR
from llms_api import LlmBox
from utils import generate_random_key, windows_compatible_name
from config import google_search_key, cse_id, headers

def convert_keyword(query:str, llm_box: LlmBox) -> str:
    '''将用户输入的问题转化为适合在google上进行搜索的关键词
    :param query: 输入的需要搜索的问题
    :param llm_box: 大模型api
    :return: 返回搜索关键词
    '''
    messages = [
        {"role": "system",
         "content": "你专门负责将用户的问题转化为知乎网站搜索关键词，只返回一个你认为最合适的搜索关键词即可"},
        {"role": "user", "content": "请问，GPT-3.5微调总共分为几步？"},
        {"role": "assistant", "content": "GPT-3.5微调流程"},
        {"role": "user", "content": query}
    ]
    msg_response = llm_box.chat(messages=messages)

    return msg_response.content


def identify_model(query:str, llm_box: LlmBox) -> str | None:
    '''判断模型：判断大模型是否具备用户提问的问题相关的知识, 如果不具备，就进行联网
    :param query: 输入的需要搜索的问题
    :param llm_box: LlmBox实例化类，即大模型api
    :return: 如果超出模型能回答的知识范围，就返回None，否则返回模型的输出结果
    '''
    # 创建密钥
    sk = generate_random_key()

    # 调用模型进行判别
    messages = [
        {"role": "system", "content": "你是一个识别器，专门用于判别用户问题是否超出了你的当前知识库范围。\
        若超出知识库范围，请回答“%s”，若未超出知识库范围，请正常回答" % sk},
        {"role": "user", "content": "请问，GPT-5.5微调总共分为几步？"},
        {"role": "assistant", "content": "%s" % sk},
        {"role": "user", "content": query}
    ]
    msg_response = llm_box.chat(messages=messages)
    result = msg_response.content

    if any(key in result for key in [sk, '对不起', '抱歉', '超出知识库']):
        return None
    else:
        return result


def google_search(query:str, num_results:int=3, site_url=None) -> list[dict]:
    '''调用谷歌搜索
    :param query：搜索的关键词
    :param num_results：搜索的数量
    :param site_url：需要限定访问的url
    :return: 返回搜索的结果：
        [{'title': xxx,
          'link': xxx,
          'snippet': xxx},
        ]
    '''
    # Step 1.构建请求
    url = "https://www.googleapis.com/customsearch/v1"
    # Step 2.设置查询参数
    params = {
        'q': query,           # 搜索关键词
        'key': google_search_key,   # 谷歌搜索API Key
        'num': num_results,
        'cx': cse_id                # CSE ID
    }
    if site_url:
        params["siteSearch"] = site_url
    # Step 3.发送GET请求
    response = requests.get(url, params=params)
    response.raise_for_status()

    # Step 4.解析响应
    items = response.json()['items']

    results = [{
        'title': item['title'],
        'link': item['link'],
        'snippet': item['snippet']}
        for item in items
    ]
    return results


def get_search_text(query:str, url:str) -> str | None:
    '''从具体的某一页知乎网站中进行数据的爬取, 并进行保存
    :param query: 搜索的问题
    :param url：具体网页的url
    :return: 返回这一页的title
    具体爬取的类型网址：
        url = 'https://zhuanlan.zhihu.com/p/599016986'
        url = 'https://www.zhihu.com/question/589955237/answer/2943963130'
        url = 'https://www.zhihu.com/question/589955237'
    '''

    headers['authority'] = 'zhaunlan.zhihu.com' if 'zhuanlan' in url else 'www.zhihu.com'
    res = requests.get(url, headers=headers).text
    res_xpath = etree.HTML(res)
    # 普通问答地址
    # 专栏地址
    if 'zhuanlan' in url:
        content_pattern = '//*[@id="root"]/div/main/div/div[3]/div[1]/div/article/div[1]/div/div//*[@id="content"]/div/p/text()'
    # 特定回答的问答网址
    elif 'answer' in url:
        content_pattern = '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]/span[1]/div/div//span[@id="content"]/span[1]/p/text()'
    elif 'zhihu.com/question' in url:
        content_pattern = '//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[2]//span[@id="content"]/span[1]/p/text()'
    else:
        return None

    print(f'    - {query} {url}')
    # print(res)
    # print(">> title:", res_xpath.xpath('//title/text()'))
    title_pattern = '//title/text()'
    title = res_xpath.xpath(title_pattern)
    title = windows_compatible_name(title[0]) if title else "no_title" + query

    text_d = res_xpath.xpath(content_pattern)
    # 创建问题答案正文
    text = ' '.join(str(t).replace('\n', ' ') for t in text_d)

    json_data = [
        {
            "link": url,
            "title": title,
            "content": text,
            "tokens": len(text)
        }
    ]

    save_path = f"{SAVE_DATA_DIR}/{query}/{title+'.json'}"
    with open(save_path, 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"数据已成功保存到：{save_path}！！！")

    return title