'''
配置项
'''
import os
from dotenv import load_dotenv

load_dotenv('../.env')

google_search_key = os.getenv("GOOGLE_SEARCH_KEY")
cse_id = os.getenv("CSE_ID")
cookie = os.getenv('COOKIT')
user_agent = os.getenv('USER_AGENT')
github_token = os.getenv('GITHUB_TOKEN')


cookie = "__snaker__id=RwP2VIL5VvzCS1U5; SESSIONID=ELqoIBdaxcYcJoraNEDcJmJxvYXtJBDMcPwa38jkoSE; JOID=VVsRBE91dzQQ_PLNSHFAJY3FzchRSRxxI8ykkw5EMVJLyqKfJkDY5nj78clIoXATvpFG6KuBd-gAtnqRpeXj6xg=; osd=VlAcBUl2fDkR-vHGRXBGJobIzM5SQhFwJc-vng9CMllGy6ScLU3Z4Hvw_MhOonsev5dF46aAcesLu3uXpu7u6h4=; _xsrf=KEOYSvQpTXVZPWvjFego8HXdYLESDqcg; _zap=f878de59-fd21-48b5-8867-07dfba4646b8; d_c0=AfCRCTKN-RmPTthvcR5LrQ_IvUiCoj19fc0=|1739023850; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1757865788; HMACCOUNT=8EA820CF1C5C9FDA; z_c0=2|1:0|10:1757868627|4:z_c0|92:Mi4xMkozRUNRQUFBQUFCOEpFSk1vMzVHU1lBQUFCZ0FsVk5QalcwYVFDVG9BWExzVTM5X0ZoMUQyS3d5OUN3UFhfQS1n|ac372392ab1be737023efb800794572c2f80a2a22bd0efe93aaa376b443645b0; tst=r; __zse_ck=004_tLZZ2w64PYeFKKTEHXUJYGPFlzA1FvEP3=cTLMAApK6tUQ8cOThKq=Z3AF=tnalCF6GUePx7KN0H7rlj1nkrVK7xZth9v9kcq2O1l3b4bnlK/JjQSTy4clBrFYbr/35n-yVnwsByO9pXMyL36erNHzsxkB+thO08qGy72o7OoRMqCMr7/MOjl6a6MJL9+XXyF+zTs0DdL6WCbDYATaB4ysPQCEFQ3MDV5FVWFuPBw0zA91N4kzGOeOmbq+UhF+/c6; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1758637353; BEC=738c6d0432e7aaf738ea36855cdce904"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': cookie,  # 需要手动获取cookie
    'upgrade-insecure-requests': '1',
    'user-agent': user_agent,  # 手动编写或者选择之后给出的user-agent选项选择其一填写
}

SAVE_DATA_DIR = os.getenv('SAVE_DATA_DIR', '../search_data')
os.makedirs(SAVE_DATA_DIR, exist_ok=True)
