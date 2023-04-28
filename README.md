# telegram-mail-bot

A Telegram bot that retrives the newest email periodically and sends them to you as chat messages.

## Changes from [upstream](https://github.com/hyfc/telegram-mail-bot)

- Replaced POP3 with IMAP protocol (as used more widely)
- Added Docker image hosted on ghcr.io
- Updated code to support python-telegram-bot-20.x APIs
- Added a `/list` query to list all emails received
- Updated deps in Pipfile

![Python Version](https://img.shields.io/github/pipenv/locked/python-version/135e2/telegram-mail-bot)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docker Image](https://ghcr-badge.egpl.dev/135e2/telegram-mail-bot/latest_tag)](https://github.com/135e2/telegram-mail-bot/pkgs/container/telegram-mail-bot)
