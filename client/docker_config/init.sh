#!/bin/bash

echo "Asia/Shanghai" > /etc/timezone

echo -e "LANG=\"zh_CN.UTF-8\"\nLANGUAGE=\"zh_CN:zh:en_US:en\"" >> /etc/environment
echo -e "en_US.UTF-8 UTF-8\nzh_CN.UTF-8 UTF-8\nzh_CN.GBK GBK\nzh_CN GB2312" >> /var/lib/locales/supported.d/local
echo -e "export LANG=\"en_US.UTF-8\"\nalias python3='PYTHONIOENCODING=utf-8 python3'\nlocale-gen" >> /root/.bashrc
source /root/.bashrc

/bin/bash
