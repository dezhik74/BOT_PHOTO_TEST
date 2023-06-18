from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_photo_test.data import Address, AddressWork, Flat


def root_keyboard(objects: List[Address]) -> InlineKeyboardMarkup:
    res = InlineKeyboardMarkup(row_width=3)
    res.add(*[InlineKeyboardButton(obj.address, callback_data=f"obj-{obj.pk}") for obj in objects])
    return res

def address_keyboard(address: Address) -> InlineKeyboardMarkup:
    res = InlineKeyboardMarkup(row_width=3)
    res.add(InlineKeyboardButton(f"Вернуться к списку объектов", callback_data=f"root"))
    res.add(*[InlineKeyboardButton(w.work, callback_data=f"work-{w.pk}-{address.pk}") for w in address.works])
    return res

def work_keyboard(work: AddressWork) -> InlineKeyboardMarkup:
    res = InlineKeyboardMarkup(row_width=3)
    res.add(InlineKeyboardButton(f"Вернуться к {work.address.address}", callback_data=f"obj-{work.address.pk}"))
    res.add(*[InlineKeyboardButton(f.name, callback_data=f"flat-{f.pk}-{work.pk}-{work.address.pk}") for f in work.flats])
    return res

def flat_keyboard(flat: Flat) -> InlineKeyboardMarkup:
    res = InlineKeyboardMarkup()
    res.add(InlineKeyboardButton(f"Вернуться к {flat.work.work}", callback_data=f"work-{flat.work.pk}-{flat.work.address.pk}"))
    return res


