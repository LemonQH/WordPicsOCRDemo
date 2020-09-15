# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import json
import hashlib
import time
from imp import reload

from imp import reload

reload(sys)

APP_KEY = ''
APP_SECRET = ''

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(api_url,data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response=requests.post(api_url, data=data, headers=headers)
    result=j = json.loads(str(response.content, encoding="utf-8"))
    if result['errorCode']=='0':
        return result['Result']
    else:
        return "errorCode:"+result['errorCode']


def get_sign_and_salt(data,img_code):
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(img_code) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign
    #print(data)
    return data

def ocr_common(img_code):
    YOUDAO_URL='https://openapi.youdao.com/ocrapi'
    data = {}
    data['detectType'] = '10012'
    data['imageType'] = '1'
    data['langType'] = 'auto'
    data['img'] =img_code
    data['docType'] = 'json'
    data=get_sign_and_salt(data,img_code)
    response=do_request(YOUDAO_URL,data)['regions']
    result=[]
    for r in response:
        for line in r['lines']:
            result.append(line['text'])
    return result


def ocr_card(img_code,img_type):
    YOUDAO_URL='https://openapi.youdao.com/ocr_structure'
    data={}
    if img_type==2:
        data['structureType'] = 'idcard'
    elif img_type==3:
        data['structureType'] = 'namecard'
    data['q'] = img_code
    data['docType'] = 'json'
    data=get_sign_and_salt(data,img_code)
    return do_request(YOUDAO_URL,data)

def ocr_table(img_code):
    YOUDAO_URL='https://openapi.youdao.com/ocr_table'
    data = {}
    data['type'] = '1'
    data['q'] = img_code
    data['docType'] = 'json'
    data=get_sign_and_salt(data,img_code)
    return do_request(YOUDAO_URL,data)

def ocr_problem(img_code):
    YOUDAO_URL='https://openapi.youdao.com/ocr_formula'
    data = {}
    data['detectType'] = '10011'
    data['imageType'] = '1'
    data['img'] = img_code
    data['docType'] = 'json'
    data=get_sign_and_salt(data,img_code)
    response=do_request(YOUDAO_URL,data)['regions']
    result = []
    for r in response:
        for line in r['lines']:
            for l in line:
                result.append(l['text'])
    return result

# 0-hand write
# 1-print
# 2-ID card
# 3-name card
# 4-table
# 5-problem
def get_ocr_result(img_code,img_type):
    if img_type==0 or img_type==1:
        return ocr_common(img_code)
    elif img_type==2 or img_type==3 :
        return ocr_card(img_code,img_type)
    elif img_type==4:
        return ocr_table(img_code)
    elif img_type==5:
        return ocr_problem(img_code)
    else:
        return "error:undefined type!"


