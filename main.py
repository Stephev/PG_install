#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/10/18 0018 
# @Author  : Stephev
# @Site    : 
# @File    : main.py
# @Software:

import Rpm_install.rpminstall as install
import System_mod.systemmod as sysmod
import Database_mod.databasesmod as database


def sys_sure():
    sysmod.selinux_mod()
    sysmod.firewall_mod()
    return

def pg_install():
    install.check_user()
    install.rpm_install()
    install.set_path()
    install.set_data()
    install.db_init()
    return

def databa_mod():
    database.connect_mod()
    database.log_strategy()
    basic_parameter()
    database.restart_db()
    return

def main():
    sys_sure()
    pg_install()
    databa_mod()
    return

if __name__ == '__main__':
    main()
