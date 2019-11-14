#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3
# @Author:Ymq

import json
from urllib import request
import os
import base64
import time
from MysqlTools.chek_mysql_with_keepalived import mysql_check_config as msc

corpid = 'ww42e8e4f8486bda5a'
corpsecret = 'vYYWbHKiVobwArFoGf7w707JHp12aV5RdgwqwZL6yz0'


class CipherAlgorithm(object):

    def __init__(self, text):
        self.text = text
        self.secret_key = 'vpxYDXtwxhGrPmapOGiasrS6'

    def encrypt(self):
        s1 = self.text + self.secret_key
        s2 = base64.b64encode(bytes(s1, 'utf-8'))
        return s2.decode('utf-8')

    def decrypt(self):
        s1 = base64.b64decode(self.text)
        s1 = s1.decode('utf-8')
        s2 = s1[:-24]
        return s2


class GetToken(object):
    def __init__(self, cropid, secret):
        self.corp_id = cropid
        self.corp_secret = secret

    def get_token_workchat(self):
        with request.urlopen(
                'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (
                        self.corp_id, self.corp_secret)) as f:
            data = f.read()
            data = eval(data.decode('utf-8'))
            access_token = data['access_token']
            cipher = CipherAlgorithm(access_token)
            ciphertext = cipher.encrypt()
            os.system('echo "%s" > %s' % (ciphertext, msc.token_path))


class WorkChatSenders(object):
    def __init__(self, msg):
        self.contacts = msc.contacts
        self.msg = msg

    def work_chat_message(self):
        if os.path.exists(msc.token_path):
            f1 = open(msc.token_path, 'r')
            access_token = f1.read()
            f1.close()
            plain = CipherAlgorithm(access_token)
            plaintext = plain.decrypt()
            url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % plaintext
            req = request.Request(url)
            body = {
                "touser": self.contacts,
                "msgtype": "text",
                "agentid": 1000004,
                "text":
                    {"content": self.msg},
                "safe": 0}
            with request.urlopen(req, data=json.dumps(body).encode(encoding='utf-8'), timeout=3) as f2:
                data = f2.read()
                data_dic = eval(data.decode('utf-8'))
                localtime = time.asctime(time.localtime(time.time()))
                if f2.status == 200:
                    if data_dic["errcode"] == 40014:
                        s = GetToken(corpid, corpsecret)
                        s.get_token_workchat()
                        os.system("echo '%s------[wechat_sender]: Retrieve Token' >> %s" % (
                            localtime, msc.log_path))
                        return self.work_chat_message()
                    elif data_dic["errcode"] == 0:
                        os.system("echo '%s------[wechat_sender]: WorkChat Message Send Successful' >> %s" % (
                            localtime, msc.log_path))
                    else:
                        os.system(
                            "echo '%s------[wechat_sender]: WorkChat Message Send Failed. Message:%s' >> %s" % (
                                localtime, data, msc.log_path))
                else:
                    os.system(
                        "echo '%s------[wechat_sender]: Network Failed. Message:%s' >> %s" % (
                            localtime, f2.status, msc.log_path))
        else:
            localtime = time.asctime(time.localtime(time.time()))
            s = GetToken(corpid, corpsecret)
            s.get_token_workchat()
            os.system(
                "echo '%s------[wechat_sender]: Retrieve Token' >> %s" % (
                    localtime, msc.log_path))
            return self.work_chat_message()
