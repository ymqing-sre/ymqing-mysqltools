#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3
import tarfile
import os
import time
import threading
import queue
from MysqlTools.dump_tool import config

threads = []
que = queue.Queue(config.queue_num)
queueLock = threading.Lock()


class ThreadsDump(threading.Thread):
    def __init__(self, q, path):
        threading.Thread.__init__(self)
        self.q = q
        self.path = path

    def run(self):
        mysqldump(self.q, path=self.path)


def mysqldump(q, path):
    queueLock.acquire()
    if not que.empty():
        database = q.get()
        queueLock.release()
        mysql_cmd = 'mysqldump -u root --add-drop-database --add-drop-table --add-drop-trigger --triggers --routines --events --extended-insert --quick --set-charset --add-locks --single-transaction --create-options %s > %s/%s.sql' % (
            database, path, database)
        err_code = os.system(mysql_cmd)
        if err_code == 0:
            localtime = time.asctime(time.localtime(time.time()))
            msg = '%s--------Database %s is dumped.Find it under path:%s.\n' % (
                localtime, database, path)
            with open('dump.log', 'a+') as f:
                f.write(msg)
                f.close()
        else:
            localtime = time.asctime(time.localtime(time.time()))
            msg = '%s--------Database %s dumped failed.Error code:%s.Please check the OS code table for reason.\n' % (
                localtime, database, err_code)
            with open('dump.log', 'a+') as f:
                f.write(msg)
                f.close()
    else:
        queueLock.release()


def threads_dump(database_list, path):
    # queueLock.acquire()
    for db_name in database_list:
        que.put(db_name)
        t = ThreadsDump(que, path)
        t.start()
        threads.append(t)
    # queueLock.release()
    for t in threads:
        t.join()
    with open('dump.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------All database dumped.\n' % localtime)
        f.close()


def tar_file(backup_path, package_name, local_path):
    os.chdir(backup_path)
    tar = tarfile.open(package_name, 'w:gz', encoding='UTF-8')
    tar.add(local_path)
    tar.close()


def pigz(local_path, process_num, backup_path, package_name):
    pigz_cmd = 'tar -cvf - %s | pigz -p %s > %s/%s' % (local_path, process_num, backup_path, package_name)
    err_code = os.system(pigz_cmd)
    return err_code
