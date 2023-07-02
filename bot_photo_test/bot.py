import logging
import pprint

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot_photo_test import settings
from bot_photo_test.data import objects
from bot_photo_test.keyboards import root_keyboard, address_keyboard, work_keyboard, flat_keyboard

bot = Bot(token=settings.TELEGA_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(LoggingMiddleware())

# состояния
class PhotoCoord(StatesGroup):
    objects = State()
    address = State()
    work = State()
    flat = State()
    make_photo = State()

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 's'], state='*')
async def send_welcome(message: types.Message):
    await message.answer(f"Объекты", parse_mode='HTML', reply_markup=root_keyboard(objects))
    await PhotoCoord.objects.set()
    args = message.get_args()

    # Проверка на аргументы через ссылку https://t.me/photofix_bot?start=FOO
    if args:
        print(args)
    # for obj in objects:
    #     print(f"{obj.address} [pk={obj.pk}]")
    #     for w in obj.works:
    #         print(f"  {w.work} [pk={w.pk}], {w.address.address}")
    #         for f in w.flats:
    #             print(f"    {f.name} [pk={f.pk}] {f.work.work} {f.work.address.address}")

# Обработчик корневой. Меню - все адреса.
@dp.callback_query_handler(lambda c: c.data == "root", state='*')
async def process_callback_root(callback_query: types.CallbackQuery):
    await PhotoCoord.address.set()
    await callback_query.message.answer(
        "Объекты",
        reply_markup=root_keyboard(objects)
    )
    await bot.answer_callback_query(callback_query.id)

# Обработчик кнопки нажатия адреса. В меню - виды работ на адресе.
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('obj'), state='*')
async def process_callback_address(callback_query: types.CallbackQuery, state: FSMContext):
    idx = int(callback_query.data.split('-')[1])
    address = objects[idx]
    async with state.proxy() as data:
        data['address'] = address
    await PhotoCoord.work.set()
    await callback_query.message.answer(
        f"Адрес: {address.address}",
        reply_markup=address_keyboard(address)
    )
    await bot.answer_callback_query(callback_query.id)

# Обработчик кнопки нажатия вида работ. В меню - все квартиры в виде работ.
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('work'), state='*')
async def process_callback_address_work(callback_query: types.CallbackQuery, state: FSMContext):
    addr_idx = int(callback_query.data.split('-')[2])
    address = objects[addr_idx]
    work_idx = int(callback_query.data.split('-')[1])
    work = address.works[work_idx]
    async with state.proxy() as data:
        data['address'] = address
        data['work'] = work
    await PhotoCoord.flat.set()
    await callback_query.message.answer(
        f"Адрес: {address.address}. Работа {work.work}",
        reply_markup=work_keyboard(work)
    )
    await bot.answer_callback_query(callback_query.id)

#Обработчик нажатия кнопки квартиры. В меню - только кнопка возврата из квартиры.
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('flat'), state='*')
async def process_callback_flat(callback_query: types.CallbackQuery, state: FSMContext):
    address_idx = int(callback_query.data.split('-')[3])
    address = objects[address_idx]
    work_idx = int(callback_query.data.split('-')[2])
    work = address.works[work_idx]
    flat_idx = int(callback_query.data.split('-')[1])
    flat = work.flats[flat_idx]
    async with state.proxy() as data:
        data['address'] = address
        data['work'] = work
        data['flat'] = flat
    await PhotoCoord.make_photo.set()

    await callback_query.message.answer(
        f"Адрес: {address.address}. Работа {work.work}. Квартира {flat.name}\nДелайте ФОТО",
        reply_markup=flat_keyboard(flat)
    )
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(state=PhotoCoord.make_photo)
async def text_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        address = data['address']
        work = data['work']
        flat = data['flat']
    await message.answer(f"address={address.address}, work={work.work}, flat={flat.name}, text={message.text}")


if __name__ == '__main__':
    print('bot started...')
    executor.start_polling(dp, skip_updates=True)