#!/bin/sh

if [ $(ps aux | grep node | grep -v grep | wc -l | tr -s "\n") -eq 0 ]
then
    export PATH=/usr/local/bin:$PATH
    export NODE_ENV=production
    NODE_ENV=production forever start --sourceDir /var/www/ghost/ index.js >> /var/log/ghost-log 2>&1
fi
