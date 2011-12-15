#! /usr/bin/env sh
# File: ctlapp.sh
# Date: 2009-11-23
# Author: jyf

# 后端控制脚本

case $1 in
    start)
        zdaemon -C daemon.conf start
        ;;
    stop)
        zdaemon -C daemon.conf stop
        ;;
    restart)
        zdaemon -C daemon.conf restart
        ;;
    log)
        tail -f logdaemon.log
        ;;
    *)
        echo "Usage: ./ctlapp.sh start | stop | restart | log"
        ;;
esac
