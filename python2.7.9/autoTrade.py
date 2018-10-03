# coding=utf-8
import time
import requests
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

publicKey = 'PUBLICKEY'
apiKey = 'APIKEY'
secretKey = 'SECRETKEY'

entrustSubmitCusUrl = 'https://www.bitasiabit.com/app/v1/entrustSubmitCus'
getFullDepthCusUrl = 'https://www.bitasiabit.com/app/v1/getFullDepthCus'

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


def autoTrade():
    while True:

        data = {'pairname': 'BACCNY'}
        realTimeData = getApi(getFullDepthCusUrl, data)
        print('BACCNY')

        print(realTimeData["data"]["asks"][0][0])
        print(realTimeData["data"]["bids"][0][0])

        ask = float(realTimeData["data"]["asks"][0][0])
        bid = float(realTimeData["data"]["bids"][0][0])

        price = raw_input("please input price: ")
        count = raw_input("please input volume: ")

        # 加密訊息
        messageBuy = "{\"secretKey\":\"" + str(secretKey) + "\",\"type\":\"" + "0" + "\",\"pairname\":\"" + str(
            pairName) + "\",\"price\":" + str(price) + ",\"count\":" + str(count) + "}"
        messageSell = "{\"secretKey\":\"" + str(secretKey) + "\",\"type\":\"" + "1" + "\",\"pairname\":\"" + str(
            pairName) + "\",\"price\":" + str(price) + ",\"count\":" + str(count) + "}"

        # 使用rsa加密
        cipher_Buy = rsaTransform(s, messageBuy)
        cipher_Sell = rsaTransform(s, messageSell)

        postDataBuy = "{\"apiKey\":\"" + str(apiKey) + "\",\"data\":\"" + cipher_Buy + "\"}"
        postDataSell = "{\"apiKey\":\"" + str(apiKey) + "\",\"data\":\"" + cipher_Sell + "\"}"

        # 委託買單
        while True:
            buyOrder = postApi(entrustSubmitCusUrl, postDataBuy)
            print("委託買單")
            print(buyOrder["code"])
            print(buyOrder["msg"])
            if (buyOrder["code"] != 200):
                print("委託失敗")
                time.sleep(1)
            else:
                break
        # 委託賣單
        # while True:
        # 	sellOrder = postApi(entrustSubmitCusUrl, postDataSell)
        # 	print("委託賣單")
        # 	print(sellOrder["code"])
        # 	print(sellOrder["msg"])
        # 	print(sellOrder["time"])
        # 	if (sellOrder["code"] != 200):
        # 		print("委託失敗")
        # 		time.sleep(1)
        # 		continue
        # 	else:
        # 		break


autoTrade()
