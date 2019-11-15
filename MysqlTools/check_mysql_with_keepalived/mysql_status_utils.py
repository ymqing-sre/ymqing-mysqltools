#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3
# @Author:Ymq

import time
import socket
from subprocess import call, DEVNULL, getoutput, getstatusoutput
from MysqlTools.check_mysql_with_keepalived import message_sender
from MysqlTools.check_mysql_with_keepalived import mysql_check_config as mcc


def check_mysql_status():
    """
    MySQL存活校验
    使用mysqladmin工具判断mysql是否存活
    :return:
    存活 1
    错误 0
    """
    cmd = 'mysqladmin -u root ping'
    res = getoutput(cmd)
    if res == 'mysqld is alive':
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write('%s------[CheckScripts][Info]: Mysqld is alived.\n' % localtime)
            f.close()
        return 1
    else:
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write('%s------[CheckScripts][Warning]: Mysqld is not alived.Response:%s.\n' % (localtime, res))
            f.close()
        return 0


def check_mysql_response():
    """
    MySQL新建连接校验
    判断mysql是否可以创建连接并进行查询
    :return:
    """
    cmd = 'mysql -u root -e "show status;"'
    res = call(cmd, shell=True, stdout=DEVNULL)
    if res == 0:
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write('%s------[CheckScripts][Info]: Mysqld response is well.\n' % localtime)
            f.close()
        return 1
    else:
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write('%s------[CheckScripts][Warning]: Cannot make a new connection.Response:%s.\n' % (localtime, res))
            f.close()
        return 0


def check_network_status(gateway):
    """
    网络状况校验
    搜集10个ping包计算延迟和掉包率，网络正常
    :param gateway: Type Str.网关IP地址
    :return:
    正常返回 1
    不正常返回 0
    """
    cmd = 'ping -f -c 10 %s | sed -n 4p' % gateway
    output = getoutput(cmd)
    if output.lower().find('packets transmitted'):
        res = output.lower().split(',')
        packet_loss_percentage = (10 - float(res[1].lstrip().split(' ')[0])) / 10
        network_latency = float(res[-1].lstrip().split(' ')[1].replace('ms', '')) / 10
        if network_latency > mcc.latency:
            localtime = time.asctime(time.localtime(time.time()))
            with open('/data/keepalived/check.log', 'a+') as f:
                f.write('%s------[CheckScripts][Warning]: Netowork Latency is %sms.\n' % (localtime, network_latency))
                f.close()
            return 0
        elif packet_loss_percentage > mcc.loss_percentage:
            localtime = time.asctime(time.localtime(time.time()))
            with open('/data/keepalived/check.log', 'a+') as f:
                f.write(
                    '%s------[CheckScripts][Warning]: Netowork packet loss percentage is over 50%%.Now is %s%%.\n' % (
                        localtime, packet_loss_percentage * 100))
                f.close()
            return 0
        else:
            localtime = time.asctime(time.localtime(time.time()))
            with open('/data/keepalived/check.log', 'a+') as f:
                f.write('%s------[CheckScripts][Info]: Network is well.\n' % localtime)
                f.close()
            return 1
    else:
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write('%s------[CheckScripts][Error]: Cannot get network info.\n' % localtime)
            f.close()
        content = '【天虎云商】Mysql网络检查脚本执行失败，请尽快查看。检查时间：%s.\n' % localtime
        m = message_sender.WorkChatSenders(content)
        m.work_chat_message()
        return 1


def check_fs_status(filesystem):
    """
    文件系统校验
    :param filesystem: 文件系统名称
    :return:
    正常返回 1
    不正常返回 0
    """
    cmd = 'mount | grep %s' % filesystem
    output = getoutput(cmd)
    res = output.split('xfs')[1].lstrip().replace('(', '').replace(')', '').split(',')
    if 'ro' in res:
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write('%s------[CheckScripts][Warning]: Filesystem %s is read only.\n' % (localtime, filesystem))
            f.close()
        return 0
    else:
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write('%s------[CheckScripts][Info]: Filesystem:%s is well.\n' % (localtime, filesystem))
            f.close()
        return 1


def switch_to_backup():
    """
    当检查不通过时，干掉keepalived进程，以切换主从状态。
    :return:
    成功 1
    失败 0
    """
    localtime = time.asctime(time.localtime(time.time()))
    hostname = socket.getfqdn(socket.gethostname())
    ip_addr = socket.gethostbyname(hostname)
    # 记录主备切换操作
    with open('/data/keepalived/check.log', 'a+') as f:
        f.write(
            '%s------[CheckScripts][Info]Server status is failed.Try to set the server backup status.\n' % localtime)
        f.close()
    # 停止keepalived进程
    cmd1 = 'service keepalived stop'
    res1 = getstatusoutput(cmd1)
    # 假如执行状态码为0
    if res1[0] == 0:
        # 检查vip是否正常释放
        res2 = getoutput('ip addr show dev bond0').find(mcc.vip)
        # 如果没有释放则重启网卡
        if res2 >= 0:
            localtime = time.asctime(time.localtime(time.time()))
            with open('/data/keepalived/check.log', 'a+') as f:
                f.write(
                    '%s------[CheckScripts][Warning]VIP release failed.Now restart network automatically.\n' % localtime)
                f.close()
            res3 = call('service network restart', shell=True, stdout=DEVNULL)
            # 判断重启命令是否执行成功
            if res3 == 0:
                localtime = time.asctime(time.localtime(time.time()))
                with open('/data/keepalived/check.log', 'a+') as f:
                    f.write('%s------[CheckScripts][Info]Network restart succeed.\n' % localtime)
                    f.close()
                return 1
            else:
                localtime = time.asctime(time.localtime(time.time()))
                with open('/data/keepalived/check.log', 'a+') as f:
                    f.write(
                        '%s------[CheckScripts][Error]Network restart failed.Please contact the administrator.\n' % localtime)
                    f.close()
                content = '【天虎云商】%s:Keepalived进程关闭失败，请尽快查看。检查时间：%s' % (ip_addr, localtime)
                m = message_sender.WorkChatSenders(content)
                m.work_chat_message()
                return 0
        else:
            with open('/data/keepalived/check.log', 'a+') as f:
                f.write(
                    '%s------[CheckScripts][Info]Switch succeed.\n' % localtime)
                f.close()
            content = '【天虎云商】%s:Keepalived进程关闭，请尽快查看。检查时间：%s' % (ip_addr, localtime)
            m = message_sender.WorkChatSenders(content)
            m.work_chat_message()
            return 1
    else:
        localtime = time.asctime(time.localtime(time.time()))
        with open('/data/keepalived/check.log', 'a+') as f:
            f.write(
                '%s------[CheckScripts][Error]Keepalived killed failed.Reason:%s.\n' % (localtime, res1[1]))
            f.close()
        content = '【天虎云商】%s:Keepalived进程关闭失败，请尽快查看。检查时间：%s' % (ip_addr, localtime)
        m = message_sender.WorkChatSenders(content)
        m.work_chat_message()
        return 0
