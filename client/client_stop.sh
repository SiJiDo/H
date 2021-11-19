ps -ef |grep celery |awk '{print $2}'|xargs kill -9
ps -ef |grep phantomjs |awk '{print $2}'|xargs kill -9
ps -ef |grep xray |awk '{print $2}'|xargs kill -9