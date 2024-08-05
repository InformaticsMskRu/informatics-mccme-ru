FROM ubuntu:focal
EXPOSE 8082
VOLUME /usr/src/app/public
WORKDIR /

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt update && \
 apt install -y vim && \
 apt-get install -y python3-pip uwsgi-core uwsgi-plugin-python3 && \
 apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY prod-container.ini uwsgi.ini
COPY pynformatics/ pynformatics/

COPY setup.py setup.py
COPY README.txt README.txt
COPY CHANGES.txt CHANGES.txt

RUN pip3 install -e .

RUN useradd -ms /bin/bash uwsgi

CMD [ "uwsgi", "--uid", "uwsgi", \
               "--protocol", "uwsgi", \
               "--ini-paste-logged", "uwsgi.ini" ]
