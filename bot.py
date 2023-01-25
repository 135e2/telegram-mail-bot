import logging
import os
import sys
from telegram import Update, Bot
from telegram.constants import MessageLimit, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from utils.client import EmailClient


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s:%(lineno)d - %(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

bot_token = os.environ["TELEGRAM_TOKEN"]

owner_chat_id = int(os.environ["OWNER_CHAT_ID"])


def is_owner(update: Update) -> bool:
    return update.message.chat_id == owner_chat_id


def handle_large_text(text):
    while text:
        if len(text) < MessageLimit.MAX_TEXT_LENGTH:
            yield text
            text = None
        else:
            out = text[: MessageLimit.MAX_TEXT_LENGTH]
            yield out
            text = text.lstrip(out)


def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def start_callback(update: Update, context: CallbackContext) -> None:
    if not is_owner(update):
        return
    msg = "Use /help to get help"
    # print(update)
    await update.message.reply_text(msg)


async def _help(update: Update, context: CallbackContext) -> None:
    if not is_owner(update):
        return
    """Send a message when the command /help is issued."""
    help_str = """邮箱设置:
/setting john.doe@example.com password
/inbox
/get mail_index
/help get help"""
    # help_str = "*Mailbox Setting*:\n" \
    #            "/setting john.doe@example.com password\n" \
    #            "/inbox\n" \
    #            "/get mail_index"
    await context.bot.send_message(
        update.message.chat_id,
        # parse_mode=ParseMode.MARKDOWN,
        text=help_str,
    )


async def setting_email(update: Update, context: CallbackContext) -> None:
    if not is_owner(update):
        return
    global email_addr, email_passwd, inbox_num
    email_addr = context.args[0]
    email_passwd = context.args[1]
    logger.info("received setting_email command.")
    await update.message.reply_text("Configure email success!")
    with EmailClient(email_addr, email_passwd) as client:
        inbox_num = client.get_mails_count()
    context.job_queue.run_repeating(
        periodic_task, interval=60, chat_id=update.message.chat_id
    )
    # chat_data['job'] = job
    logger.info("periodic task scheduled.")


async def periodic_task(context: CallbackContext) -> None:
    global inbox_num
    logger.info("entering periodic task.")
    with EmailClient(email_addr, email_passwd) as client:
        new_inbox_num = client.get_mails_count()
        if new_inbox_num > inbox_num:
            for i in range(inbox_num, new_inbox_num + 1):
                mail = client.get_mail_by_index(i)
                content = mail.__repr__()
                for text in handle_large_text(content):
                    await context.bot.send_message(context.job.chat_id, text=text)
            inbox_num = new_inbox_num


async def inbox(update: Update, context: CallbackContext) -> None:
    if not is_owner(update):
        return
    logger.info("received inbox command.")
    try:
        with EmailClient(email_addr, email_passwd) as client:
            global inbox_num
            new_num = client.get_mails_count()
            reply_text = (
                "The index of newest mail is *%d*,"
                " received *%d* new mails since last"
                " time you checked." % (new_num, new_num - inbox_num)
            )
            inbox_num = new_num
            await context.bot.send_message(
                update.message.chat_id, parse_mode=ParseMode.MARKDOWN, text=reply_text
            )
    except NameError as e:
        await context.bot.send_message(
            update.message.chat_id,
            parse_mode=ParseMode.MARKDOWN,
            text="Email unset, please set valid email by the '/setting' command.",
        )
        logger.warning(e)


async def get_email(update: Update, context: CallbackContext) -> None:
    if not is_owner(update):
        return
    index = context.args[0]
    if not index:
        await context.bot.send_message(
            update.message.chat_id, text="$index should be a positive number!"
        )
    logger.info("received get command.")
    try:
        with EmailClient(email_addr, email_passwd) as client:
            mail = client.get_mail_by_index(index)
            content = mail.__repr__()
            for text in handle_large_text(content):
                await context.bot.send_message(update.message.chat_id, text=text)
    except NameError as e:
        await context.bot.send_message(
            update.message.chat_id,
            parse_mode=ParseMode.MARKDOWN,
            text="Email unset, please set valid email by the '/setting' command.",
        )
        logger.warning(e)


def main():
    # Create the EventHandler and pass it your bot's token.
    bot = Bot(token=bot_token)
    print(bot_token)

    application = ApplicationBuilder().bot(bot).build()

    # simple start function
    application.add_handler(CommandHandler("start", start_callback))

    application.add_handler(CommandHandler("help", _help))
    #
    #  Add command handler to set email address and account.
    application.add_handler(CommandHandler("setting", setting_email))

    application.add_handler(CommandHandler("inbox", inbox))

    application.add_handler(CommandHandler("get", get_email))

    application.add_error_handler(error)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    application.run_polling()


if __name__ == "__main__":
    main()
