#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from MysqlTools.source_tool import config


def drop_database(db_name):
    cmd1 = 'mysql -u root -e "show database like \'%s\';"' % db_name
    output = os.popen(cmd1)
    if output.read():
        cmd2 = 'mysql -u root -e "drop database %s";' % db_name
        err_code = os.system(cmd2)
        if err_code == 0:
            with open('source.log', 'a+') as f:
                localtime = time.asctime(time.localtime(time.time()))
                f.write('%s--------Database %s dropped.\n' % (localtime, db_name))
                f.close()
        else:
            with open('source.log', 'a+') as f:
                localtime = time.asctime(time.localtime(time.time()))
                f.write('%s--------Database %s dropped failed.Error code:%s\n' % (localtime, db_name, err_code))
                f.close()
    else:
        pass


def create_database(db_name):
    cmd1 = 'mysql -u root -e "show databases like \'%s\';"' % db_name
    output = os.popen(cmd1)
    if output.read():
        pass
    else:
        cmd = 'mysql -u root -e "create database %s;"' % db_name
        err_code = os.system(cmd)
        if err_code == 0:
            with open('source.log', 'a+') as f:
                localtime = time.asctime(time.localtime(time.time()))
                f.write('%s--------Database %s created.\n' % (localtime, db_name))
                f.close()
        else:
            with open('source.log', 'a+') as f:
                localtime = time.asctime(time.localtime(time.time()))
                f.write('%s--------Database %s created failed.Error code:%s\n' % (localtime, db_name, err_code))
                f.close()


def source_database(db_name, path):
    cmd = 'mysql -u root %s < %s/%s.sql' % (db_name, path, db_name)
    err_code = os.system(cmd)
    if err_code == 0:
        with open('source.log', 'a+') as f:
            localtime = time.asctime(time.localtime(time.time()))
            f.write('%s--------Database %s sourced.\n' % (localtime, db_name))
            f.close()
    else:
        with open('source.log', 'a+') as f:
            localtime = time.asctime(time.localtime(time.time()))
            f.write('%s--------Database %s sourced failed.Error code:%s\n' % (localtime, db_name, err_code))
            f.close()


def main():
    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------[MISSION START].\n' % localtime)
        f.write('%s--------[DROP DATABASE].\n' % localtime)
        f.close()
    for db_name in config.database_list:
        drop_database(db_name)
    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------[CREATE DATABASE].\n' % localtime)
        f.close()
    for db_name in config.database_list:
        create_database(db_name)
    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------[SOURCE DATABASE].\n' % localtime)
        f.close()
    for db_name in config.database_list:
        source_database(db_name, config.path)
    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------[MISSION DONE].\n' % localtime)
        f.close()


if __name__ == '__main__':
    main()
