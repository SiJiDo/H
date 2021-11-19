FROM ubuntu:18.04

ENV FLASK_APP run.py

ADD ./docker_config/sources.list /etc/apt/
ADD ./docker_config/localtime /etc/localtime
ADD ./docker_config/init.sh /tmp/
ADD ./docker_config/H.sql /tmp/

ADD run.py /app/
ADD requirements.txt /app/
ADD config.py /app/
ADD config.ini /app/
COPY app /app/app/

RUN apt-get clean && apt-get update
RUN apt-get install -y openjdk-8-jre openjdk-8-jdk vim python3 python3-pip nmap erlang-nox mariadb-server language-pack-zh-hans fontconfig chromium-browser --fix-missing\
    && pip3 install -i https://pypi.douban.com/simple/ -r /app/requirements.txt \
    && chmod +x /tmp/init.sh

EXPOSE 5005
CMD ["/tmp/init.sh"]