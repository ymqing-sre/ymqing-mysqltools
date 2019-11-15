#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:Ymq

from MysqlTools.check_mysql_with_keepalived import mysql_status_utils as msu
from MysqlTools.check_mysql_with_keepalived import mysql_check_config as mcc
import time


def main():
    is_stop = 0
    while is_stop == 0:
        # 检查mysql服务状态
        if mcc.is_mysql_status == 1:
            m_status = msu.check_mysql_status()
            if m_status == 0:
                msu.switch_to_backup()
                break
        # 检查mysql响应状态
        if mcc.is_mysql_response == 1:
            m_response = msu.check_mysql_response()
            if m_response == 0:
                msu.switch_to_backup()
                break
        # 检查网络状态
        if mcc.is_network_status == 1:
            m_network = msu.check_network_status(mcc.gateway_ip)
            if m_network == 0:
                msu.switch_to_backup()
                break
        # 检查文件系统状态
        if mcc.is_filesystem_status == 1 and mcc.filesystem:
            for fs_name in mcc.filesystem:
                m_filesystem = msu.check_fs_status(fs_name)
                if m_filesystem == 0:
                    msu.switch_to_backup()
                    is_stop = 1
                    break
        time.sleep(mcc.interval)


if __name__ == '__main__':
    main()
