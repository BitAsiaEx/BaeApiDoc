#coding=utf-8
from requests import Session
from bs4 import BeautifulSoup
import configparser
import easygui
import time
import sys
import ctypes
import requests
from decimal import *

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

#read trade.ini
config = configparser.ConfigParser()
config.read('trade.ini')
publicKey = config.get('Section_Header', 'PUBLICKEY')
apiKey = config.get('Section_Header', 'APIKEY')
baseUrl = config.get('Section_Header', 'BASEURL')

secretKey = config.get('Section_Header', 'SECRETKEY')
pairName = config.get('Section_Header', 'PAIRNAME')
count = config.get('Section_Header', 'COUNT') 
freq = float(config.get('Section_Header', 'FREQUENCY')) 


#pair price interval 
miniGap = {
    "BTCCNY": 0.02,
    "XRPCNY": 0.001
}

getMarketCusUrl = baseUrl + 'app/v1/getMarketCus'
getDifficultyUrl = baseUrl + 'app/v1/getDifficulty'
entrustSubmitCusUrl = baseUrl + 'app/v1/entrustSubmitCus'
getFullDepthCusUrl = baseUrl + 'app/v1/getFullDepthCus'

#rsa string
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
                'accept-language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'accept-encoding':'gzip, deflate',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Content-Type':"application/json",
                'method':'get'
        },
        params = data
    )
    return response.json()

def postApi(url, data):
    response = requests.post(
        url=url,
        headers={
            'accept': '*/*',
            'accept-language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-encoding':'gzip, deflate',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type':"application/json",
            'method':'POST' 
        },
        data=data
    )

    return response.json()

#auto trade in n seconds
def autoTrade(n):
    while True:        
        data = {'pairname':str(pairName)}
        realTimeData = getApi(getFullDepthCusUrl, data)

        if len(realTimeData["data"]["asks"])==0:
            continue;
        if len(realTimeData["data"]["bids"])==0:
            continue;

        print(realTimeData["data"]["asks"][0][0])
        print(realTimeData["data"]["bids"][0][0])

        ask = float(realTimeData["data"]["asks"][0][0])
        bid = float(realTimeData["data"]["bids"][0][0])
        p = float(bid + miniGap[str(pairName)])

        if p > bid and p < ask:
            print("价格正常")
        else:
            print("行情價格異常")
            time.sleep(n)
            continue
        
        #加密訊息
        messageBuy = "{\"secretKey\":\""+ str(secretKey) +"\",\"type\":\""+ "0" + "\",\"pairname\":\""+ str(pairName) + "\",\"price\":"+ str(p) +",\"count\":" + str(count) +"}"
        messageSell = "{\"secretKey\":\""+ str(secretKey) +"\",\"type\":\""+ "1" + "\",\"pairname\":\""+ str(pairName) + "\",\"price\":"+ str(p) +",\"count\":" + str(count) +"}"
        
        #使用rsa加密
        cipher_Buy = rsaTransform(s, messageBuy)
        cipher_Sell = rsaTransform(s, messageSell)

        postDataBuy="{\"apiKey\":\""+ str(apiKey) +"\",\"data\":\"" + cipher_Buy + "\"}"
        postDataSell="{\"apiKey\":\""+ str(apiKey) +"\",\"data\":\"" + cipher_Sell + "\"}"

        #委託買單
        while True:
            buyOrder = postApi(entrustSubmitCusUrl, postDataBuy)
            print("buy:" + buyOrder["msg"])
            if(buyOrder["code"] != 200):
                print("failed")
                time.sleep(2)
            else:
                break
        #委託賣單
        while True:
            sellOrder = postApi(entrustSubmitCusUrl, postDataSell)
            print("sell:" + sellOrder["msg"])
            if(sellOrder["code"] != 200):
                print("failed")
                time.sleep(2)
                continue
            else:
                break

        time.sleep(n)
        

autoTrade(freq)
