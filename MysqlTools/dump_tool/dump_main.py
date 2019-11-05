#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MysqlTools.dump_tool import utils, config
import time
import os


def main():
    with open('dump.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------Dump start.\n' % localtime)
        f.close()

    utils.threads_dump(database_list, path)

    with open('dump.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------Dump done.\n' % localtime)
        f.close()

    with open('dump.log', 'a+') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write('%s--------Tar start.\n' % localtime)
        f.close()
    # utils.tar_file(backup_path, package_name, local_path)
    e = utils.pigz(local_path, process_num, backup_path, package_name)
    if e == 0:
        with open('dump.log', 'a+') as f:
            localtime = time.asctime(time.localtime(time.time()))
            f.write('%s--------Tar done.\n' % localtime)
            f.write('%s--------[ALL MISSION DONE]\n' % localtime)
            f.close()
    else:
        with open('dump.log', 'a+') as f:
            f.write('%s--------Tar Failed.Error Code:%s\n' % (localtime,e))
            f.close()


if __name__ == '__main__':
    date_fmt = time.strftime('%Y%m%d', time.localtime())
    package_name = '%s%s.tgz' % (config.package_name, date_fmt)
    backup_path = config.backup_path
    local_path = config.local_path
    path = config.path
    database_list = config.database_list
    process_num = config.process_num
    os.system('rm -rf %s' % path)
    os.system('mkdir -p %s' % path)
    main()
