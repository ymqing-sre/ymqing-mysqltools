#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:Ymq

# 基础配置参数
# 检查间隔(秒)
interval = 5
# 服务虚地址
vip = '192.168.20.77'
# 故障联系人
contacts = 'YeMaoQing'
# 微信通知的日志地址
log_path = '/data/keepalived/check.log'
# 微信token存储地址
token_path = '/data/keepalived/scripts/tokencache'
# mysql执行文件位置
mysql_base_dir = '/export/home/mysql'

# 检查项开关
# 是否检查mysql存活状态(0:不检查,1:检查)
is_mysql_status = 1

# 是否检查mysql连接响应状态(0:不检查,1:检查)
is_mysql_response = 1

# 是否检查网络状态(0:不检查,1:检查)
is_network_status = 1
# 网关地址
gateway_ip = '192.168.20.254'
# 允许的延迟(ms)
latency = 800
# 允许的掉包率
loss_percentage = 0.5

# 是否检查文件系统状态(0:不检查,1:检查)
is_filesystem_status = 1
# 文件系统清单
filesystem = []
