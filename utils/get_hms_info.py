import re

import requests
from bs4 import BeautifulSoup
import json


def get_hms_info(url):
    # 请求网页
    response = requests.get(url)

    # 如果请求成功，处理网页内容
    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找到特定的 div
        content_list = soup.findAll('blockquote')

        if content_list:
            # 提取所需内容
            hms_code_list = []
            for content in content_list:
                msg_title = content.find('strong')
                codes = content.find('span', class_='text-tiny')
                if msg_title and codes:
                    msg_title_text = msg_title.contents[0]
                    msg_title_zh = re.search(r': (.+)', msg_title_text)
                    if msg_title_zh:
                        msg_title_zh = msg_title_zh.group(1)

                    # 处理 codes，提取 i 节点中的内容并以','分割
                    code_items = codes.find_all('i')
                    codes_list = []
                    codes_result_list = []
                    if code_items:
                        codes_list = [code.contents[0] for code in code_items]
                        codes_str = codes_list[0]
                        codes_result_list = codes_str.split(',')
                    for code in codes_result_list:
                        code_item_list = code.split('-')
                        code_str = ''.join(code_item_list)
                        hms_code_list.append({
                            'ecode':code_str,
                            'intro':msg_title_zh,
                        })
            print('hms_code_list:', hms_code_list)
        else:
            print("未找到blockquote标签")
    else:
        print(f"请求失败，状态码：{response.status_code}")


if __name__ == '__main__':
    get_hms_info('https://wiki.bambulab.com/zh/hms/home')
