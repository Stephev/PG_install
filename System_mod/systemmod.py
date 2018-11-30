#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/10/18 0018 
# @Author  : Stephev
# @Site    : 
# @File    : systemmod.py
# @Software:

import commands
import os
import string


def selinux_mod():   #关闭selinux
    print "[INFO] 正在检查selinux设置"
    sel_status = commands.getoutput('getenforce')
    if cmp(sel_status, 'Enforcing'):
        print "[INFO] 系统selinux已经关闭"
    else:
        print "[INFO] 系统selinux没有关闭,正在关闭..."
        os.system('setenforce 0')
        print "[INFO] 临时关闭成功...ok"
    return


def firewall_mod():  #关闭防火墙
    print "[INFO] 正在关闭系统的防火墙..."
    version_awk = "cat /etc/redhat-release |awk '{gsub(/[[:blank:]]*/,\"\",$0);print $0;}'|\n" \
                  "awk '{match($0,\"release\");print substr($0,RSTART+RLENGTH)}'|cut -d '.' -f1"
    system_ver = commands.getoutput(version_awk)
    system_ver_int = string.atoi(system_ver)
    #print system_ver_int
    if system_ver_int < 7:
        os.system('service  iptables stop')
    else:
        os.system('systemctl stop firewalld')
    print "[INFO] 临时关闭成功...ok"
    return


def main():
    selinux_mod()
    firewall_mod()
    return

if __name__ == '__main__':
    main()
