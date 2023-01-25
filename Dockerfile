FROM python:3.11-alpine

WORKDIR /opt/workdir/telegram-mail-bot

COPY utils /opt/workdir/telegram-mail-bot/utils
COPY bot.py /opt/workdir/telegram-mail-bot/
COPY requirements.txt /opt/workdir/telegram-mail-bot/

RUN pip install --no-cache-dir -r requirements.txt

ENV OWNER_CHAT_ID=
ENV TELEGRAM_TOKEN=

CMD ["/bin/sh", "-c", "/usr/local/bin/python bot.py" ]
