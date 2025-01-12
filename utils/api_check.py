import secrets
import string


def generate_random_string(length: int):
    """
    生成指定长度的随机字符串
    :param length: 指定长度
    :return: 随机字符串
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))
