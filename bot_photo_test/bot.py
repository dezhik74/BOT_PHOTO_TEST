import logging
import pprint

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from bot_photo_test import settings
from bot_photo_test.data import objects
from bot_photo_test.keyboards import root_keyboard, address_keyboard, work_keyboard

bot = Bot(token=settings.TELEGA_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 's'])
async def send_welcome(message: types.Message):
    await message.reply(f"Объекты", parse_mode='HTML', reply_markup=root_keyboard(objects))
    # for obj in objects:
    #     print(f"{obj.address} [pk={obj.pk}]")
    #     for w in obj.works:
    #         print(f"  {w.work} [pk={w.pk}], {w.address.address}")
    #         for f in w.flats:
    #             print(f"    {f.name} [pk={f.pk}] {f.work.work} {f.work.address.address}")


@dp.callback_query_handler(lambda c: c.data == "root")
async def process_callback_root(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        f"Объекты",
        parse_mode='HTML',
        reply_markup=root_keyboard(objects)
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('obj'))
async def process_callback_address(callback_query: types.CallbackQuery):
    idx = int(callback_query.data.split('-')[1])
    address = objects[idx]
    await bot.send_message(
        callback_query.from_user.id,
        f"Адрес: {address.address}",
        reply_markup=address_keyboard(address)
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('work'))
async def process_callback_address_work(callback_query: types.CallbackQuery):
    addr_idx = int(callback_query.data.split('-')[2])
    address = objects[addr_idx]
    work_idx = int(callback_query.data.split('-')[1])
    work = address.works[work_idx]
    await bot.send_message(
        callback_query.from_user.id,
        f"Адрес: {address.address}. Работа {work.work}",
        reply_markup=work_keyboard(work)
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('flat'))
async def process_callback_work(callback_query: types.CallbackQuery):
    address_idx = int(callback_query.data.split('-')[3])
    address = objects[address_idx]
    work_idx = int(callback_query.data.split('-')[2])
    work = address.works[work_idx]
    flat_idx = int(callback_query.data.split('-')[1])
    flat = work.flats[flat_idx]
    await bot.send_message(
        callback_query.from_user.id,
        f"Адрес: {address.address}. Работа {work.work}. Квартира {flat.name}"
    )
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler()
async def text_handler(message: types.Message):
    await message.reply(message.text)


if __name__ == '__main__':
    print('bot started...')
    executor.start_polling(dp, skip_updates=True)