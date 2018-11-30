#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/10/19 0019 
# @Author  : Stephev
# @Site    : 
# @File    : databasesmod.py
# @Software:

import ConfigParser
import os



db = ConfigParser.ConfigParser()
db.read('install.conf')
pgdata_path = db.get("INSTALL","PGDATA_PATH")
log_on = db.get("DBINFO","logging_collector")
log_stra = db.get("DBINFO","LOG_STRATETY")
connect_all = db.get("DBINFO","CONNECT_ALL")
port_mod = db.get("DBINFO","PORT")
max_conn = db.get("DBINFO","MAX_CONNECTIONS")
wal_level = db.get("DBINFO","WAL_LEVEL")



def connect_mod():     #配置数据库的连接和日志
    print "[INFO] 正在配置数据库连接设置..."
    pg_auto_conf = pgdata_path + '/postgresql.auto.conf'
    listen_addres = open(pg_auto_conf,"a")
    listen_addres.write("listen_addresses = \'*\'"
                        "\nport = "+port_mod)
    listen_addres.close()
    if connect_all == 'yes':
        pg_hba_conf = pgdata_path + '/pg_hba.conf'
        hba_conf = open(pg_hba_conf,"a")
        hba_conf.write("host    all             all             0.0.0.0/0                 md5")
        hba_conf.close()
    print "[INFO] 连接设置配置成功...ok"
    return


def log_strategy(): #pg_log日志策略
    print "[INFO] 正在配置数据库日志策略..."
    pg_auto_conf = pgdata_path + '/postgresql.auto.conf'
    if log_on == 'off':
        return
    if log_on == 'on':
        listen_addres = open(pg_auto_conf, "a")
        if log_stra == 'PlanA':
            listen_addres.write("\nlogging_collector = \'on\'"
                                "\nlog_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'"
                                "\nlog_truncate_on_rotation = off"
                                "\nlog_rotation_age = 1d"
                                "\nlog_rotation_size = 0")
            listen_addres.close()
        if log_stra == 'PlanB':
            listen_addres.write("\nlogging_collector = \'on\'"
                                "\nlog_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'"
                                "\nlog_truncate_on_rotation = off"
                                "\nlog_rotation_age = 0"
                                "\nlog_rotation_size = 10M")
            listen_addres.close()
        if log_stra == 'PlanC':
            listen_addres.write("\nlogging_collector = \'on\'"
                                "\nlog_filename = 'postgresql-%a.log'"
                                "\nlog_truncate_on_rotation = on"
                                "\nlog_rotation_age = 1d"
                                "\nlog_rotation_size = 0")
            listen_addres.close()
        print "[INFO] 数据库日志策略配置成功...ok"
    else:
        print "[ERROR] 请确认是否开启日志，填写正确的配置文件"


def basic_parameter():
    print "[INFO] 正在配置数据库基本参数..."
    postgres_conf = pgdata_path+"/postgresql.auto.conf"
    pg_conf = open(postgres_conf,"a")
    pg_conf.write("wal_level = "+wal_level)
    pg_conf.close()
    return

def restart_db():
    cmd_restart = "su - postgres -c 'pg_ctl restart'"
    if os.system(cmd_restart):
        print "[Error]:重启数据库失败，请查找原因"
        exit('[FATAL]:退出安装程序...')
    else:
        print "[INFO] 成功重启数据库"
        print "[INFO] PostgreSQL数据库基本参数配置成功"
    return


def main():
    connect_mod()
    log_strategy()
    restart_db()
    return

if __name__ == '__main__':
    main()

