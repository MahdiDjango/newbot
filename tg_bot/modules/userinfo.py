import html
from typing import Optional, List

from telegram import Message, Update, Bot, User
from telegram import ParseMode, MAX_MESSAGE_LENGTH
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown

import tg_bot.modules.sql.userinfo_sql as sql
from tg_bot import dispatcher, SUDO_USERS
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user

#from tg_bot.modules.utilities import utilities
#import asyncio


@run_async
def about_me(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message  # type: Optional[Message]
    user_id = extract_user(message, args)

    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text("{}".format(escape_markdown(info)),
                                            parse_mode=ParseMode.MARKDOWN)
    elif message.reply_to_message:
        #username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text("{}".format(escape_markdown(info)),
                                            parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("تو هنوز لقبی برای خودت نذاشتی!")


@run_async
def set_about_me(bot: Bot, update: Update):
    message = update.effective_message  # type: Optional[Message]
    user_id = message.from_user.id
    text = message.text
    # use python's maxsplit to only remove the cmd, hence keeping newlines.
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            message.reply_text("لقب تنظیم شد!")
        else:
            message.reply_text(
                "لقب باید کمتر از این تعداد کارکتر{}!اما تو این مقدار دادی {}.".format(MAX_MESSAGE_LENGTH // 4, len(info[1])))


@run_async
def about_bio(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message  # type: Optional[Message]

    user_id = extract_user(message, args)
    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text("{}".format(escape_markdown(info)),
                                            parse_mode=ParseMode.MARKDOWN)
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            "{} هنوز لقبی ندارد!".format(username))
    else:
        update.effective_message.reply_text("هنوز لقبی برای خودت نذاشتی!")


@run_async
def set_about_bio(bot: Bot, update: Update):
    message = update.effective_message  # type: Optional[Message]
    sender = update.effective_user  # type: Optional[User]
    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        if user_id == message.from_user.id:
            message.reply_text(
                "تو نمیتونی برای صاحب خودت لقب بزاری...")
            return
        elif user_id == bot.id and sender.id not in SUDO_USERS:
            message.reply_text("اوم من فقط به ادمین ها برای تنظیم بیو برای خودم اعتماد دارم.")
            return

        text = message.text
        # use python's maxsplit to only remove the cmd, hence keeping newlines.
        bio = text.split(None, 1)
        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text("لقب تنظیم شد!")
            else:
                message.reply_text(
                    "لقب باید کمتر از این تعداد کارکتر{}!اما تو این مقدار دادی {}.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1])))
    else:
        message.reply_text("ریپلای کن به مسیج دیگران برای تنظیم لقب!")


'''async def run(message, matches, chat_id, step, crons=None):
    response = []
    chat = message.chat_id
    users = await utilities.client.get_participants(chat)
    uwu = ""
    bots = ""
    inde = [1, 1]
    for user in users:
        if user.username != None and user.bot == False:
            uwu = uwu + "@" + user.username + "-"
            inde[0] = inde[0] + 1
        elif user.username == None and user.first_name != None:
            continue
        elif user.bot == True:
            bots = bots + "@" + user.username + "-"
            inde[1] = inde[1] + 1
    uwu = uwu + bots
    x = 4080
    length = len(uwu)
    some_string = uwu.split("-")
    index = 0
    me_sg = ""
    while index < len(some_string):
        if some_string[index] == "  ":
            continue
        if len(me_sg) < x:
            if me_sg != "" and (
                index + 1 == len(some_string) or (me_sg != "" and index % 500 == 0)
            ):
                response.append(utilities.client.send_message(chat, me_sg[:-2]))
                response.append(asyncio.sleep(2))
                me_sg = ""
                continue
            me_sg = me_sg + some_string[index] + " - "
        else:
            if me_sg != "":
                response.append(message.reply(me_sg[:-2]))
                response.append(asyncio.sleep(2))
                me_sg = some_string[index] + " - "
        index = index + 1
    return response'''


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    if bio and me:
        return "<b>About user:</b>\n{me}\n<b>What others say:</b>\n{bio}".format(me=me, bio=bio)
    elif bio:
        return "<b>What others say:</b>\n{bio}\n".format(me=me, bio=bio)
    elif me:
        return "<b>About user:</b>\n{me}""".format(me=me, bio=bio)
    else:
        return ""


def __gdpr__(user_id):
    sql.clear_user_info(user_id)
    sql.clear_user_bio(user_id)


__help__ = """
 - /setbio <text>: تنظین لقب برای آن کاربر
 - /bio: نمایش لقب آن کاربر با ریپلای کردن روی آن
 - /setme <text>: تنظیم لقب برای خود
 - /me: نمایش لقب خود
"""

__mod_name__ = "تنظیم لقب"

SET_BIO_HANDLER = DisableAbleCommandHandler("setbio", set_about_bio)
GET_BIO_HANDLER = DisableAbleCommandHandler("bio", about_bio, pass_args=True)

SET_ABOUT_HANDLER = DisableAbleCommandHandler("setme", set_about_me)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("me", about_me, pass_args=True)

#TAG_HANDLER = DisableAbleCommandHandler("tag", run)

dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)
# dispatcher.add_handler(TAG_HANDLER)
