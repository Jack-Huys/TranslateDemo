# -*- coding: utf-8 -*-
import requests
import json
from utils.AuthV3Util import addAuthParams
import redis
import sys
import time

#个人应用ID
APP_KEY = ''
#个人应用密钥
APP_SECRET = ''

# 定义一个结构体来存储JSON数据
class DictionaryResult:
    def __init__(self, tSpeakUrl, requestId, query, translation, mTerminalDict, errorCode, dict, webdict, l, isWord, speakUrl):
        self.tSpeakUrl = tSpeakUrl
        self.requestId = requestId
        self.query = query
        self.translation = translation
        self.mTerminalDict = mTerminalDict
        self.errorCode = errorCode
        self.dict = dict
        self.webdict = webdict
        self.l = l
        self.isWord = isWord
        self.speakUrl = speakUrl


def createRequest(text, lang_from, lang_to, tar_path):
    vocab_id = ''
    data = {'q': text, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    print(data)
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    print(str(res.content, 'utf-8'))
    result = fromJson(str(res.content, 'utf-8'))
    for translation in result.translation:
        print(translation)
        with open(tar_path, 'a', encoding='utf-8') as f:
            # 将数据写入文件
            f.write(translation+'\n')

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

def fromJson(translateStr):
    # 将JSON字符串解析为Python字典
    data = json.loads(translateStr)

    result = DictionaryResult(
        tSpeakUrl=data['tSpeakUrl'],
        requestId=data['requestId'],
        query=data['query'],
        translation=data['translation'],
        mTerminalDict=data['mTerminalDict'],
        errorCode=data['errorCode'],
        dict=data['dict'],
        webdict=data['webdict'],
        l=data['l'],
        isWord=data['isWord'],
        speakUrl=data['speakUrl']
    )
    return result
    # 获取翻译结果
    #translation = data.get("translation", [])
    #print("Translation:", result.translation)
    # 获取数组
    #translation_array = data.get('translation', [])   
        
    #for attr, value in vars(result).items():
    #    print(f"{attr}: {value}")

# 网易有道智云翻译服务api
# https://openapi.youdao.com/api
        
        
#   'ar': arabic
#   'zh-CHS': 'chinese (simplified)',
#   'fr': 'french',
#   'ko': 'korean',
#   'ru': 'russian', 
#   'es': 'spanish',

if __name__ == '__main__':
    #python TranslateDemo.py word.txt zh-CHS ru translated_output.txt
    print("**************开始连接redis*************************")
    r = redis.Redis(host='localhost', port=6379, db=0)
    # r = redis.Redis(host='localhost', port=6379, db=0, password='yourpassword')
    if(r.ping()):
        print("redis连接成功*****")
    else:
        print("redis连接失败*****")

    print("**************开始获取参数*************************")
    arc_path = sys.argv[1]
    lang_from = sys.argv[2]
    lang_to = sys.argv[3]
    tar_path = sys.argv[4]
    print("**************参数获取成功*************************")

    print("**************开始翻译文档*************************")
    with open(arc_path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break            # 如果读取到的行为空，表示文件已经读取完毕
            print(line.strip())  # 处理每一行
            createRequest(line.strip(), lang_from, lang_to, tar_path) 
            time.sleep(1) #为防止频繁请求失败
        
    print("**************文档翻译成功*************************")
    #text = ['无人机', '返航模式', '低电量','自主模式', '起飞']
    #text = '无人机,返航模式,低电量,自主模式,起飞'
    #lang_from = 'zh-CHS' #源语言
    #lang_to = 'ru'   #目标语言
    
