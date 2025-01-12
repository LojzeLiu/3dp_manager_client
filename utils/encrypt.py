import json

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import utils

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlEoD+RXnRnGboia+bUDm
D0wAJ8+GVUpW9r5vPnAsnbsTew6Vr0xGQR+v8tERO1VRcToKSF+pH1ui5kehgL4A
bwQwLWamjXbYQOVCr3yS3Vz/pcIWPz5Gw1AIRoKh3NLa86vvZFHNgG/3VwfyW9ZJ
rr4zbFuiN5zQMNfWqoTZyB02UDMqc1UTLGeQ4j08j5ZI3bpFugX4O1XSaPcg9uiQ
vUk1mw51cRCuQwJbPaGlCVAiAZxWaScrSa1HrIopRDBJyhl1s0LKhjxueGAEH9MQ
4709NX2vvUSy/dLGNizD5K/wluw9g+FyGIngG6wjaOwattA0xEshn/Oev7vxOOxi
swIDAQAB
-----END PUBLIC KEY-----"""

class Encrypt:
    def __init__(self):
        # 加载公钥
        self.public_key = RSA.import_key(public_key)

    def encrypt_dict(self, data):
        """加密字典类型数据"""
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_data = cipher_rsa.encrypt(json.dumps(data).encode())
        return encrypted_data

    def encrypt_str(self, buf: str):
        """
        加密字符串
        :param buf: 要加密的字符串
        :return:
        """
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_data = cipher_rsa.encrypt(buf.encode())
        return encrypted_data


encrypt = Encrypt()
