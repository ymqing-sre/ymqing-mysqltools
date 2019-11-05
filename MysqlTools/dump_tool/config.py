#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 备份文件的名称
package_name = 'mysqldata'
# 备份目录
backup_path = '/home/backupdata'
# 备份源目录
local_path = '/home/backupdata/mysqldata'
# 数据导出目录
path = '/home/backupdata/mysqldata'
# 开启的并发备份线程数
queue_num = 5
# 压缩需要的线程数
process_num = 4
# 需要备份的库名
database_list = ['activemq',
                 'activities',
                 'b2c',
                 'b2cios',
                 'b2clog',
                 'dataoutput',
                 'hmmitem',
                 'hmmper',
                 'hmmsystem',
                 'hmmtrade',
                 'hmmuser',
                 'huodong',
                 'imf',
                 'paycenter',
                 'ry',
                 'test',
                 'tyfo_activity_sys',
                 'tyfo_member_admin',
                 'tyfoaccount',
                 'tyfoactivity',
                 'tyfobargain',
                 'tyfobp',
                 'tyfocollege',
                 'tyfoeco',
                 'tyfofinancial',
                 'tyfogroupbuying',
                 'tyfogrouppurchas',
                 'tyfohistory',
                 'tyfoitem',
                 'tyfojd',
                 'tyfomarketingpromotion',
                 'tyfomember',
                 'tyfooffline',
                 'tyfoopen',
                 'tyfoother',
                 'tyfopartner',
                 'tyfoper',
                 'tyfoperfp',
                 'tyfoscm',
                 'tyfoservice',
                 'tyfosso',
                 'tyfosystem',
                 'tyfotemplateplatform',
                 'tyfotobedel',
                 'tyfototal',
                 'tyfotrade',
                 'tyfouser',
                 'tyfovideo',
                 'tyfowangka',
                 'ynuser']
