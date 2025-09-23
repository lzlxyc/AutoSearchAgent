import random
import string


def generate_random_key(length=30):
    '''随机生成的密钥，用于判断是否大模型不具备用户提问的相关知识'''
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def windows_compatible_name(s:str, max_length=255) -> str:
    """将字符串转化为符合Windows文件/文件夹命名规范的名称。
    :param s: 输入的字符串
    :param max_length: 输出字符串的最大长度，默认为255
    :return: 一个可以安全用作Windows文件/文件夹名称的字符串
    """
    # Windows文件/文件夹名称中不允许的字符列表
    forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    # 使用下划线替换不允许的字符
    for char in forbidden_chars:
        s = s.replace(char, '_')

    # 删除尾部的空格或点
    s = s.rstrip(' .')

    # 检查是否存在以下不允许被用于文档名称的关键词，如果有的话则替换为下划线
    reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
                      "COM5", "COM6", "COM7", "COM8", "COM9","LPT1", "LPT2",
                      "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
    if s.upper() in reserved_names:
        s += '_'

    # 如果字符串过长，进行截断
    if len(s) > max_length:
        s = s[:max_length]

    return s

