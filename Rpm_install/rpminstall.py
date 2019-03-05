#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/10/18 0018 
# @Author  : Stephev
# @Site    : 
# @File    : rpminstall.py
# @Software:

import os
import commands
import string
import ConfigParser


ins = ConfigParser.ConfigParser()
ins.read('install.conf')
install_path = ins.get("INSTALL","INSTALL_PATH")
pgdata_path = ins.get("INSTALL","PGDATA_PATH")
rpm_name = ins.get("INSTALL","RPM_NAME")


def check_user():           #判断mysql用户是否存在,存在直接用，不存在创建
    print "[INFO] 正在检查系统的用户..."
    cc=os.popen('cat /etc/passwd').readlines()
    ccc=''
    for i in cc:
        user_name = i.split(':')
        ccc = cmp(user_name[0],'postgres')
    if ccc == 0:
        if os.path.exists('/home/postgres'):
            print ("[INFO] 用户postgres存在且拥有家目录，直接使用它")
        else:
            exit("[FATAL]:已存在用户postgres，但该用户没有家目录。请手动删除此用户或者为其创建家目录")
    else:
        if os.path.exists('/home/postgres'):
            exit("[FATAL]:没有postgres用户但是存在postgres家目录，请删除它或改名")
        else:
            os.system("useradd -U postgres")
            print("[INFO] 成功创建postgres用户...ok")
    return



def rpm_install():   # 解压RPM包安装
    print "[INFO] 正在解压RPM包..."
    cmd_tar = "tar -xzf"+rpm_name+" -C "+install_path+" >/dev/null"
    int_tar = os.system(cmd_tar)
    if int_tar == 0:
        print "[INFO] 解压成功...ok"
    else:
        print "[Error]:解压失败"
        exit('[FATAL]:退出安装程序...')
    print "[INFO] 正在创建软连接..."
    cmd_ln = "ln -s "+install_path+"/pgsql /usr/postgresql"
    int_ln = os.system(cmd_ln)
    if int_ln == 0:
        print "[INFO] 创建成功...ok"
    else:
        print "[Error]:创建失败"
        exit('[FATAL]:退出安装程序...')
    print "[INFO] 正在给安装包赋权..."
    cmd_chown_ln = "chown -R postgres:postgres /usr/postgresql"
    cmd_chown_pg = "chown -R postgres:postgres "+install_path+"/pgsql"
    os.system(cmd_chown_ln)
    os.system(cmd_chown_pg)
    print "[INFO] 授权成功...ok"
    return


def set_path():     # 配置好环境变量
    print "[INFO] 正在配置环境变量..."
    path_profile = open("/home/postgres/.bash_profile","a")
    path_profile.write("export PATH=/usr/postgresql/bin:$PATH\nexport LD_LIBRARY_PATH=/usr/postgresql/lib:$LD_LIBRARY_PATH"
            "\nexport PGDATA="+pgdata_path+"\nexport PGHOST=/tmp\n")
    path_profile.close()
    cmd_source = "su - postgres -c 'source .bash_profile'"
    int_source = os.system(cmd_source)
    if int_source == 0:
        print "[INFO] 环境变量配置成功...ok"
    else:
        exit('[FATAL]:环境变量生效失败，退出安装程序...')
    return


def set_data():  #检查提供的数据目录
    print "[INFO] 正在检查处理数据目录..."
    if os.path.exists(pgdata_path):
        cmd_lsdir = 'ls '+pgdata_path+'| wc -l'
        data_string = commands.getoutput(cmd_lsdir)
        data_int = string.atoi(data_string)
        if data_int>0:
            print "Error:指定为数据目录的文件夹不为空，请清空后重试"
            exit('[FATAL]:退出安装程序...')
        else:
            cmd_chown_data = 'chown -R postgres:postgres '+pgdata_path
            os.system(cmd_chown_data)
            cmd_chmod_data = 'chmod 700 '+pgdata_path
            os.system(cmd_chmod_data)
        print "[INFO] 数据目录检查完成...ok"
    else:
        print "[Error]:必须先准备好数据目录.(最好是插盘挂载，保证空间充足)"
        exit('[FATAL]:退出安装程序...')
    return


def db_init():     #初始化数据库
    print "[INFO] 正在开始初始化数据库..."
    cmd_init = "su - postgres -c 'initdb -D $PGDATA' >/dev/null"
    int_init = os.system(cmd_init)
    if int_init == 0:
        print "[INFO] 初始化数据库成功，试着启动数据库..."
    else:
        print "[Error]:初始化数据库失败，请重试"
        exit('[FATAL]:退出安装程序...')
    cmd_start = "su - postgres -c 'pg_ctl -l logfile start' >/dev/null"
    int_start = os.system(cmd_start)
    if int_start == 0:
        print "[INFO] 成功启动数据库"
        print "[INFO] PostgreSQL数据库安装成功"
    else:
        print "[Error]:启动数据库失败，请查找原因"
        exit('[FATAL]:退出安装程序...')
    return


def main():
    check_user()
    rpm_install()
    set_path()
    set_data()
    db_init()
    return


if __name__ == '__main__':
    main()
