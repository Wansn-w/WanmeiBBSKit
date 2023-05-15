import base64
import collections
from typing import Optional

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.primitives.serialization import load_der_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


class Sha1Utils:
    @staticmethod
    def getSign(data: str, private_key_pem: RSAPrivateKey) -> str:  # com.wanmei.basic.s.a
        """
        签名数据
        :param data: 待签名数据
        :param private_key_pem: 私钥
        :return: 签名结果
        """
        signature = private_key_pem.sign(
            data.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        return base64.b64encode(signature).decode()

    @staticmethod
    def signParams(params: dict, b64_private_key: str) -> str:  # com.wanmei.basic.s.c
        """
        签名参数
        :param params: 待签名参数
        :param b64_private_key: base64格式私钥
        :return: 签名结果
        """
        sorted_params = collections.OrderedDict(sorted(params.items()))
        param_str = '&'.join([f'{k}={v}' for k, v in sorted_params.items()])
        signature = Sha1Utils.getSign(
            param_str, Sha1Utils.loadPrivateKey(b64_private_key)
        )
        return signature

    @staticmethod
    def signParamsString(params: str, b64_private_key: str) -> str:  # com.wanmei.basic.s.b
        return Sha1Utils.getSign(
            '&'.join(sorted(params.split('&'))),
            Sha1Utils.loadPrivateKey(b64_private_key)
        )

    @staticmethod
    def loadPrivateKey(b64_private_key: str, password: Optional[str] = None) -> RSAPrivateKey:  # com.wanmei.basic.s.d
        """
        将base64编码的PKCS8格式的字符串转换为PrivateKey对象
        :param b64_private_key: base64编码的PKCS8格式的私钥字符串
        :param password: 私钥密码
        :return: RSAPrivateKey对象
        """
        private_key_ = load_der_private_key(base64.b64decode(b64_private_key), password=password)
        return private_key_

    @staticmethod
    def loadPublicKey(b64_public_key: str) -> RSAPublicKey:  # com.wanmei.basic.s.e
        """
        将base64编码的PKCS8格式的字符串转换为PrivateKey对象
        :param b64_public_key: base64编码的PKCS8格式的公钥字符串
        :return: RSAPublicKey对象
        """
        private_key_ = load_der_public_key(base64.b64decode(b64_public_key))
        return private_key_

    @staticmethod
    def verifySignString(after_sign: str, before_sign: str, public_key: RSAPublicKey) -> bool:  # com.wanmei.basic.s.f
        """
        验证签名数据
        :param after_sign: 待验证的签名后的base64字符串
        :param before_sign: 签名前的原始数据字符串
        :param public_key: RSAPublicKey对象
        :return: 验证结果
        """
        try:
            public_key.verify(
                base64.b64decode(after_sign),
                before_sign.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA1()
            )
            return True
        except InvalidKey:
            return False

    @staticmethod
    def verifySign(after_sign: str, params_before: dict, b64_public_key: str) -> bool:
        """
        验证签名参数
        :param after_sign: 待验证的签名后的base64字符串
        :param params_before: 签名前的原始数据字典
        :param b64_public_key: base64编码的PKCS8格式的公钥字符串
        :return: 验证结果
        """
        sorted_params = collections.OrderedDict(sorted(params_before.items()))
        param_str = '&'.join([f'{k}={v}' for k, v in sorted_params.items()])
        return Sha1Utils.verifySignString(
            after_sign=after_sign,
            before_sign=param_str,
            public_key=Sha1Utils.loadPublicKey(b64_public_key)
        )
