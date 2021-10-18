FROM ubuntu:18.04

ENV FLASK_APP run.py

ADD ./docker_config/sources.list /etc/apt/
ADD ./docker_config/localtime /etc/localtime
ADD ./docker_config/init.sh /tmp/
ADD ./docker_config/H.sql /tmp/

COPY run.py gunicorn-cfg.py requirements.txt config.py config.ini ./
COPY app app

RUN apt-get clean && apt-get update
RUN apt-get install -y vim python3 python3-pip nmap erlang-nox mariadb-server language-pack-zh-hans fontconfig --fix-missing\
    && pip3 install -i https://pypi.douban.com/simple/ -r requirements.txt \
    && chmod +x /tmp/init.sh

EXPOSE 5005
CMD ["/tmp/init.sh"]

