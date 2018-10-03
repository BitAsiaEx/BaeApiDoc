# coding=utf-8
import time
import requests
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

# 讀取trade.ini
publicKey = 'PUBLICKEY'
apiKey = 'APIKEY'
secretKey = 'SECRETKEY'

getMarketCusUrl = 'https://www.bitasiabit.com/app/v1/getMarketCus'

# rsa加密string
s = """-----BEGIN RSA PUBLIC KEY-----\n""" + str(publicKey) + """\n-----END RSA PUBLIC KEY-----"""


def rsaTransform(key, message):
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(message))
    return cipher_text


def getApi(url, data):
    response = requests.get(
        url=url,
        headers={
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type': "application/json",
            'method': 'get'
        },
        params=data
    )
    return response.json()


def postApi(url, data):
    response = requests.post(
        url=url,
        headers={
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type': "application/json",
            'method': 'POST'
        },
        data=data
    )

    return response.json()


req = getApi(getMarketCusUrl, {'pairname': 'BACCNY'})
print (req)
