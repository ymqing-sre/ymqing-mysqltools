#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MysqlTools.source_tool import utils, config
import time


def source_data(database_list, path):
    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------Part source start.\n' % localtime)
        f.close()

    utils.threads_source(database_list, path)

    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------Part source done.\n' % localtime)
        f.close()


def main():
    path = config.path
    db_list1 = config.database_list1
    for db_name in db_list1:
        utils.drop_database(db_name)
        utils.create_database(db_name)
    source_data(db_list1, path)
    db_list2 = config.database_list2
    for db_name in db_list2:
        utils.drop_database(db_name)
        utils.create_database(db_name)
        utils.source_database(db_name, path)
    db_list3 = config.database_list3
    for db_name in db_list3:
        utils.drop_database(db_name)
        utils.create_database(db_name)
    source_data(db_list3, path)
    with open('source.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------[Source Mission Done].\n' % localtime)
        f.close()


if __name__ == '__main__':
    main()
