import html
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html

from tg_bot import dispatcher, LOGGER
from tg_bot.modules.helper_funcs.chat_status import user_admin, can_delete
from tg_bot.modules.log_channel import loggable


@run_async
@user_admin
@loggable
def purge(bot: Bot, update: Update, args: List[str]) -> str:
    msg = update.effective_message  # type: Optional[Message]
    if msg.reply_to_message:
        user = update.effective_user  # type: Optional[User]
        chat = update.effective_chat  # type: Optional[Chat]
        if can_delete(chat, bot.id):
            message_id = msg.reply_to_message.message_id
            delete_to = msg.message_id - 1
            if args and args[0].isdigit():
                new_del = message_id + int(args[0])
                # No point deleting messages which haven't been written yet.
                if new_del < delete_to:
                    delete_to = new_del

            for m_id in range(delete_to, message_id - 1, -1):  # Reverse iteration over message ids
                try:
                    bot.deleteMessage(chat.id, m_id)
                except BadRequest as err:
                    if err.message == "Message can't be deleted":
                        bot.send_message(
                            chat.id, "نمیتونم همه پیام هارا پاک کنم بعضی از آنها بسیار قدیمی هستند.")

                    elif err.message != "Message to delete not found":
                        LOGGER.exception("Error while purging chat messages.")

            try:
                msg.delete()
            except BadRequest as err:
                if err.message == "Message can't be deleted":
                    bot.send_message(
                        chat.id, "نمیتونم همه پیام هارا پاک کنم بعضی از آنها بسیار قدیمی هستند.")

                elif err.message != "Message to delete not found":
                    LOGGER.exception("Error while purging chat messages.")

            bot.send_message(chat.id, "حذف کامل شد.")
            return "<b>{}:</b>" \
                   "\n#PURGE" \
                   "\n<b>Admin:</b> {}" \
                   "\nPurged <code>{}</code> messages.".format(html.escape(chat.title),
                                                               mention_html(
                                                                   user.id, user.first_name),
                                                               delete_to - message_id)

    else:
        msg.reply_text("ریپلای کن به پیامی که میخوای تا اونجا پاک شه")

    return ""


@run_async
@user_admin
@loggable
def purges(bot: Bot, update: Update, args: List[str]) -> str:
    msg = update.effective_message  # type: Optional[Message]
    if msg.reply_to_message:
        user = update.effective_user  # type: Optional[User]
        chat = update.effective_chat  # type: Optional[Chat]
        if can_delete(chat, bot.id):
            message_id = msg.reply_to_message.message_id
            delete_to = msg.message_id - 1
            if args and args[0].isdigit():
                new_del = message_id - int(args[0])
                # No point deleting messages which haven't been written yet.
            for m_id in range(new_del, message_id, 1):  # Reverse iteration over message ids
                try:
                    bot.deleteMessage(chat.id, m_id)
                except BadRequest as err:
                    if err.message == "Message can't be deleted":
                        bot.send_message(
                            chat.id, "نمیتونم همه پیام هارا پاک کنم بعضی از آنها بسیار قدیمی هستند.")

                    elif err.message != "Message to delete not found":
                        LOGGER.exception("Error while purging chat messages.")

            try:
                msg.delete()
            except BadRequest as err:
                if err.message == "Message can't be deleted":
                    bot.send_message(
                        chat.id, "نمیتونم همه پیام هارا پاک کنم بعضی از آنها بسیار قدیمی هستند.")

                elif err.message != "Message to delete not found":
                    LOGGER.exception("Error while purging chat messages.")

            bot.send_message(chat.id, "حذف کامل شد.")
            return "<b>{}:</b>" \
                   "\n#PURGE" \
                   "\n<b>Admin:</b> {}" \
                   "\nPurged <code>{}</code> messages.".format(html.escape(chat.title),
                                                               mention_html(
                                                                   user.id, user.first_name),
                                                               delete_to - message_id)

    else:
        msg.reply_text("ریپلای کن به پیامی که میخوای تا اونجا پاک شه")

    return ""


@run_async
@user_admin
@loggable
def del_message(bot: Bot, update: Update) -> str:
    if update.effective_message.reply_to_message:
        user = update.effective_user  # type: Optional[User]
        chat = update.effective_chat  # type: Optional[Chat]
        if can_delete(chat, bot.id):
            update.effective_message.reply_to_message.delete()
            update.effective_message.delete()
            return "<b>{}:</b>" \
                   "\n#DEL" \
                   "\n<b>Admin:</b> {}" \
                   "\nMessage deleted.".format(html.escape(chat.title),
                                               mention_html(user.id, user.first_name))
    else:
        update.effective_message.reply_text("چه چیزی را میخوای پاک کنی?")

    return ""


__help__ = """
*فقط ادمین ها:*
 - /del: پاک کردن پیامی که ریپلای شده
 - /purge: پاک کردن همه ی پیام ها
 - /purge <integer X>: پاک کردن پیامی که ریپلای شده روی آن و X پیام بعد از آن
 - /purges <integer X> : پاک کردن پیامی که ریپلای شده روی آن و X پیام قبل از آن
"""

__mod_name__ = "پاکسازی"

DELETE_HANDLER = CommandHandler("del", del_message, filters=Filters.group)
PURGE_HANDLER = CommandHandler("purge", purge, filters=Filters.group, pass_args=True)
PURGGE_HANDLER = CommandHandler("purges", purges, filters=Filters.group, pass_args=True)

dispatcher.add_handler(DELETE_HANDLER)
dispatcher.add_handler(PURGE_HANDLER)
dispatcher.add_handler(PURGGE_HANDLER)
