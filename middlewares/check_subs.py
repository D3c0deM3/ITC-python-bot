import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import GROUPS
from keyboards.inline.obuna import subscribe
from utils.misc import subscription
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return
        logging.info(user)
        result = "Botdan Foydalanish uchun quyidagi guruhga obuna bo'ling:\n"
        final_status = True
        for group in GROUPS:
            status = await subscription.check(user_id=user,
                                              group=group)
            final_status *= status
            group = await bot.get_chat(group)
            if not status:
                invite_link = await group.export_invite_link()
                result += (f"👉 <a href='{invite_link}'>{group.title}</a>\n")
        if not final_status:
            await update.message.answer(result, reply_markup=subscribe, disable_web_page_preview=True)
            raise CancelHandler()


import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import GROUPS
from keyboards.inline.obuna import subscribe
from utils.misc import subscription
from loader import bot



class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            if update.message.chat.type == types.ChatType.PRIVATE:
                if update.message:
                    user = update.message.from_user.id
                elif update.callback_query:
                    user = update.callback_query.from_user.id
                else:
                    return
                result = "рџ¤– Botdan foydalanish uchun bizning <b>rasmiy</b> kanalimizga a'zo bo'ling, iltimos!\n\n"
                final_status = True
                for channel in GROUPS:
                    status = await subscription.check(user_id=user, channel=channel)
                    final_status *= status
                    channel = await bot.get_chat(channel)
                    if not status:
                        invite_link = await channel.export_invite_link()
                        result += (f"👉 <a href='{invite_link}'>{channel.title}</a>\n\n")
                        result += f"➕—A'zo bo'lgandan keyin qaytadan /start ustiga bosing..."
                if not final_status:
                    await update.message.answer(result, reply_markup=subscribe, disable_web_page_preview=True)
                    raise CancelHandler()
        elif update.callback_query.message:
            if update.callback_query.message.chat.type == types.ChatType.PRIVATE:
                user = update.callback_query.from_user.id
                result = "Botdan foydalanishdan oldin bizning rasmiy kanalimizga ulaning iltimos!\n"
                final_status = True
                for channel in GROUPS:
                    status = await subscription.check(user_id=user, channel=channel)
                    final_status *= status
                    channel = await bot.get_chat(channel)
                    if not status:
                        invite_link = await channel.export_invite_link()
                        result += (f"рџ‘‰ <a href='{invite_link}'>{channel.title}</a>\n")
                if not final_status:
                    await update.callback_query.message.answer(result, reply_markup=subscribe, disable_web_page_preview=True)
                    raise CancelHandler()

