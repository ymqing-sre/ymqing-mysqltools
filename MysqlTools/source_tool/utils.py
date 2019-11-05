#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3
import os
import time
import threading
import queue
from MysqlTools.source_tool import config

threads = []
que = queue.Queue(config.queue_num)
queueLock = threading.Lock()


class TheadsSource(threading.Thread):
    def __init__(self, q, path):
        threading.Thread.__init__(self)
        self.q = q
        self.path = path

    def run(self):
        source(self.q, self.path)


def source(q, path):
    queueLock.acquire()
    if not que.empty():
        database = q.get()
        queueLock.release()
        mysql_cmd = 'mysql -u root %s < %s/%s.sql' % (database, path, database)
        localtime = time.asctime(time.localtime(time.time()))
        with open('source.log', 'a+') as f:
            f.write('%s--------Database %s is sourcing.\n' % (localtime, database))
            f.close()
        err_code = os.system(mysql_cmd)
        if err_code == 0:
            localtime = time.asctime(time.localtime(time.time()))
            msg = '%s--------Database %s is sourced.\n' % (localtime, database)
            with open('source.log', 'a+') as f:
                f.write(msg)
                f.close()
        else:
            localtime = time.asctime(time.localtime(time.time()))
            msg = '%s--------Database %s sourced failed.Error code:%s.Please check the OS code table for reason.\n' % (
                localtime, database, err_code)
            with open('source.log', 'a+') as f:
                f.write(msg)
                f.close()
    else:
        queueLock.release()


def threads_source(database_list, path):
    for db_name in database_list:
        que.put(db_name)
        t = TheadsSource(que, path)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------Part database sourced.\n' % localtime)
        f.close()


def drop_database(db_name):
    cmd1 = 'mysql -u root -e "show databases like \'%s\';"' % db_name
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
