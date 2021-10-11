import html
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html

from tg_bot import dispatcher, LOGGER, MUTE_STICKER, UNMUTE_STICKER
from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_admin, is_user_admin, can_restrict
from tg_bot.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from tg_bot.modules.helper_funcs.string_handling import extract_time
from tg_bot.modules.log_channel import loggable


@run_async
@bot_admin
@user_admin
@loggable
def mute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("به من یک یوزرنیم بده یا ریپلای کن روی آن.")
        return ""

    if user_id == bot.id:
        message.reply_text("من خودمو نمیتونم خفه کنم!")
        return ""

    member = chat.get_member(int(user_id))

    if member:
        if is_user_admin(chat, user_id, member=member):
            message.reply_text("نمیتونم دهان ادمینی را ببندم!")

        elif member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chat.id, user_id, can_send_messages=False)
            bot.send_sticker(chat.id, MUTE_STICKER)
            message.reply_text("خفه باش فعلا!")
            return "<b>{}:</b>" \
                   "\n#MUTE" \
                   "\n<b>Admin:</b> {}" \
                   "\n<b>User:</b> {}".format(html.escape(chat.title),
                                              mention_html(user.id, user.first_name),
                                              mention_html(member.user.id, member.user.first_name))

        else:
            message.reply_text("این کاربر خفه میباشد!")
    else:
        message.reply_text("این کاربر در گروه نمیباشد!")

    return ""


@run_async
@bot_admin
@user_admin
@loggable
def unmute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("به من یک یوزرنیم بده یا ریپلای کن روی آن.")
        return ""

    member = chat.get_member(int(user_id))

    if member:
        if is_user_admin(chat, user_id, member=member):
            message.reply_text("این یک ادمینه احمق!")
            return ""

        elif member.status != 'kicked' and member.status != 'left':
            if member.can_send_messages and member.can_send_media_messages \
                    and member.can_send_other_messages and member.can_add_web_page_previews:
                message.reply_text("این کاربر درحال حاضر میتونه حرف بزنه!")
                return ""
            else:
                bot.restrict_chat_member(chat.id, int(user_id),
                                         can_send_messages=True,
                                         can_send_media_messages=True,
                                         can_send_other_messages=True,
                                         can_add_web_page_previews=True)
                bot.send_sticker(chat.id, UNMUTE_STICKER)
                message.reply_text("از خفگی درآمد!")
                return "<b>{}:</b>" \
                       "\n#UNMUTE" \
                       "\n<b>Admin:</b> {}" \
                       "\n<b>User:</b> {}".format(html.escape(chat.title),
                                                  mention_html(user.id, user.first_name),
                                                  mention_html(member.user.id, member.user.first_name))
    else:
        message.reply_text("این کاربر در گروه نمیباشد!")

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_mute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("به شخصی اشاره نکرده ای.")
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("نمیتونم این کاربر پیدا کنم!")
            return ""
        else:
            raise

    if is_user_admin(chat, user_id, member):
        message.reply_text("خیلی دوست داشتم ادمینا رو خفه میکردم...")
        return ""

    if user_id == bot.id:
        message.reply_text("من خودمو نمیتونم ساکت کنم احمق جان!")
        return ""

    if not reason:
        message.reply_text("زمانی برای سکوت انتخاب نکردی!")
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = "<b>{}:</b>" \
          "\n#TEMP MUTED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {}" \
          "\n<b>Time:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name),
                                     mention_html(member.user.id, member.user.first_name), time_val)
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        if member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chat.id, user_id, until_date=mutetime, can_send_messages=False)
            bot.send_sticker(chat.id, MUTE_STICKER)
            message.reply_text("خفه شد به مدت {}!".format(time_val))
            return log
        else:
            message.reply_text("این کاربر درحال حاضر خفه میباشد!")

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            bot.send_sticker(chat.id, MUTE_STICKER)
            message.reply_text("خفه شد به مدت {}!".format(time_val), quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR muting user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text("اوه؛ نمیتونم این شخص ساکت کنم.")

    return ""


__help__ = """
*فقط ادمین ها:*
 - /mute <userhandle>: سکوت یک کاربر با ریپلای روی آن یا یوزرنیم یا آیدی
 - /tmute <userhandle> x(m/h/d): سکوت یک کاربر به مدت مشخص شده. m = minutes, h = hours, d = days.
 - /unmute <userhandle>: خروج از سکوت با ریپلای روی آن یا یوزرنیم یا آیدی
"""

__mod_name__ = "سکوت"

MUTE_HANDLER = CommandHandler("mute", mute, pass_args=True, filters=Filters.group)
UNMUTE_HANDLER = CommandHandler("unmute", unmute, pass_args=True, filters=Filters.group)
TEMPMUTE_HANDLER = CommandHandler(["tmute", "tempmute"], temp_mute,
                                  pass_args=True, filters=Filters.group)

dispatcher.add_handler(MUTE_HANDLER)
dispatcher.add_handler(UNMUTE_HANDLER)
dispatcher.add_handler(TEMPMUTE_HANDLER)
