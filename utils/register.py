import base64
import datetime
import hashlib
import json
import os

from pyDes import *
import wmi

import utils

base_path = '.data/'
code_path = f'{base_path}auth_key.txt'
m_code_path = f'{base_path}auth_list.json'


def get_mac_address():
    """获取计算机Mac 地址"""
    try:
        m_wmi = wmi.WMI()
        for network in m_wmi.Win32_NetworkAdapterConfiguration():
            mac_address = network.MacAddress
            if mac_address is not None:
                return mac_address
    except Exception as e:
        utils.logger.debug(f'获取计算机Mac 地址失败：f{e}')
        return ""


def get_cpu_serial():
    """获取CPU序列号"""
    try:
        m_wmi = wmi.WMI()
        cpu_info = m_wmi.Win32_Processor()
        serial_number = None
        if len(cpu_info) > 0:
            serial_number = cpu_info[0].ProcessorId
        return serial_number
    except Exception as e:
        utils.logger.debug(f'获取计算机Mac 地址失败：f{e}')
        return ""


def get_disk_serial():
    """获取硬盘序列号"""
    try:
        m_wmi = wmi.WMI()
        disk_info = m_wmi.Win32_PhysicalMedia()
        serial_number = None
        if len(disk_info) > 0:
            serial_number = disk_info[0].SerialNumber.strip()
        return serial_number
    except Exception as e:
        utils.logger.debug(f'获取计算机Mac 地址失败：f{e}')
        return ""


def get_board_serial():
    """获取主板序列号"""
    try:
        m_wmi = wmi.WMI()
        board_info = m_wmi.Win32_BaseBoard()
        board_id = ''
        if len(board_info) > 0:
            board_id = board_info[0].SerialNumber.strip().strip('.')
        return board_id
    except Exception as e:
        utils.logger.debug(f'获取计算机Mac 地址失败：f{e}')
        return ""


def make_machine_code(more_data: str = ''):
    """
    生成机器码
    :param more_data: 更多参与计算的数据, 默认为空
    :return 机器码
    """
    try:
        # 获取机器的 Mac地址、CPU序列号、硬盘序列号、主板序列号
        mac_address = get_mac_address()
        cpu_serial = get_cpu_serial()
        disk_serial = get_disk_serial()
        board_serial = get_board_serial()

        # 将机器的硬件数据字符串拼接
        combine_str = mac_address + cpu_serial + disk_serial + board_serial + more_data
        if combine_str:
            combine_byte = combine_str.encode("utf-8")

            # 进行 MD5 编码
            machine_code = hashlib.md5(combine_byte).hexdigest()
            return machine_code.upper()
    except Exception as e:
        utils.logger.error(f'生成机器码失败：{e}')
    return ''


def encrypted(code: str) -> str:
    """生成授权码"""
    # 使用 DES-CBC加密算法加密机器码
    des_key = "J9Vqu6jC"  # 自定义 Key，需八位
    des_iv = "\x11\2\x2a\3\1\x27\2\0"  # 自定IV向量
    k = des(des_key, CBC, des_iv, pad=None, padmode=PAD_PKCS5)
    encrypt_str = k.encrypt(code)
    # 加密结果转 base64 编码
    base64_code = base64.b32encode(encrypt_str)
    # 编码结果使用 MD5 加密
    md5_code = hashlib.md5(base64_code).hexdigest().upper()
    return md5_code


def check_new_authorization(auth_code: str):
    """ 验证新的授权码 """
    machine_code = make_machine_code()
    encrypted_code = encrypted(machine_code)
    if encrypted_code == auth_code:
        token_info = {
            'code': auth_code,
        }
        # 将字典写入文件
        with open(code_path, 'w') as file:
            json.dump(token_info, file)
        return True
    return False


def need_auth():
    try:
        if not os.path.exists(base_path):
            os.mkdir(base_path)
            return True  # 需要激活

        if os.path.exists(code_path):
            with open(code_path, 'r') as file:
                code_info = json.load(file)
            curr_code = code_info.get('code', None)
            if curr_code:
                machine_code = make_machine_code()
                encrypted_code = encrypted(machine_code)
                if encrypted_code != curr_code:
                    return True
            return False  # 不需要激活
    except json.decoder.JSONDecodeError:
        utils.logger.error(f'加载签名密钥文件失败')
    except Exception as e:
        utils.logger.error(f'加载签名密钥文件失败: {str(e)}')
    return True


def make_auth_code(m_code: str, note: str = ''):
    """根据机器码生成激活码"""
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    if os.path.exists(m_code_path):
        with open(m_code_path, 'r', encoding='utf-8') as file:
            m_code_list = json.load(file)
        for old_info in m_code_list:
            old_code = old_info.get('code')
            auth_at = old_info.get('auth_at')
            old_note = old_info.get('note')
            if old_code == m_code:
                print(f'该机器码已激活, 激活时间：{auth_at}；备注：{old_note}')
                return
    else:
        m_code_list = []
    new_auth_code = encrypted(m_code)
    m_code_list.append({
        'code': m_code,
        'note': note,
        'auth_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(m_code_path, 'w', encoding='utf-8') as file:
        json.dump(m_code_list, file)
    return new_auth_code


def list_auth_info():
    if os.path.exists(m_code_path):
        with open(m_code_path, 'r', encoding='utf-8') as file:
            m_code_list = json.load(file)
        for info in m_code_list:
            old_code = info.get('code')
            auth_at = info.get('auth_at')
            old_note = info.get('note')
            print(f'机器码：{old_code}, 激活时间：{auth_at}；备注：{old_note};')
