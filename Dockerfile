FROM python:3.9

RUN pip install --no-cache-dir pytz python-telegram-bot==13.1 pyzmail36 imapclient

COPY utils /opt/workdir/telegram-mail-bot/utils
COPY bot.py /opt/workdir/telegram-mail-bot/

WORKDIR /opt/workdir/telegram-mail-bot

ENV OWNER_CHAT_ID=
ENV TELEGRAM_TOKEN=

CMD ["/bin/sh", "-c", "/usr/local/bin/python bot.py" ]
