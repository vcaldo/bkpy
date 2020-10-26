FROM python:3.9-alpine

ENV TIMEZONE="America/Sao_Paulo"
ENV RCLONE_CONF="/root/.config/rclone/rclone.conf"
ENV SRC_FILE="/app/sourcelist.json"

# ADD /usr/share/zoneinfo/$TIMEZONE /etc/localtime
# RUN echo $TIMEZONE > /etc/timezone

RUN apk update && apk add bash \
    curl \
    unzip \
    libressl-dev \
    libffi-dev \
    gcc \
    musl-dev \
    openssh-client

ADD rclone.conf /root/.config/rclone/
RUN curl https://rclone.org/install.sh | bash
    
ADD ssh/ /root/.ssh/
RUN chmod 600 /root/.ssh/*

ADD app/ /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

RUN mkdir /etc/crontab
RUN echo '* */6 * * * . /app/set-env && /bin/bash /app/run-bkpy.sh > /proc/1/fd/1 2>/proc/1/fd/2' > /etc/crontab/root
RUN crontab /etc/crontab/root

ADD entrypoint-alpine.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
ENTRYPOINT [ "/opt/entrypoint.sh" ]
