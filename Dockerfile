FROM python:3.11-alpine

WORKDIR /opt/workdir/telegram-mail-bot

COPY utils /opt/workdir/telegram-mail-bot/utils
COPY bot.py /opt/workdir/telegram-mail-bot/
COPY Pipfile Pipfile.lock /opt/workdir/telegram-mail-bot/

RUN pip install pipenv
RUN pipenv install --system --deploy

ENV OWNER_CHAT_ID=
ENV TELEGRAM_TOKEN=

CMD ["/bin/sh", "-c", "/usr/local/bin/python bot.py" ]
