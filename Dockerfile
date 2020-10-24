FROM python:3.9-buster

ENV TZ="America/Sao_Paulo"
ENV RCLONE_CONF="/root/.config/rclone/rclone.conf"
ENV SRC_FILE="/app/sourcelist.json"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends curl \
      unzip \
      cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/.ssh/
ADD ssh/ /root/.ssh/
RUN chmod 600 /root/.ssh/*

ADD rclone.conf /root/.config/rclone/
RUN curl https://rclone.org/install.sh | bash

ADD app/ /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

RUN echo '* */8 * * * root . /app/set-env && /bin/bash /app/run-bkpy.sh > /proc/1/fd/1 2>/proc/1/fd/2' > /etc/cron.d/bkpy-cron
RUN crontab /etc/cron.d/bkpy-cron

ADD entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
ENTRYPOINT [ "/opt/entrypoint.sh" ]