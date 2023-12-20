import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncpg import UniqueViolationError
from docx import Document

from loader import dp


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def get_file(message: types.Message):
    await message.document.download(message.document.file_name)
    doc = Document(message.document.file_name)
    all_paras = doc.paragraphs

    for para in all_paras:
        new_string = para.text.replace('–', '-')
        if len(new_string.split('-')) == 2:
            # print(para.text.split('-'))
            print(f"{new_string.split('-')[1].rstrip()}")
            # print(f"{new_string.split('-')[1].rstrip()} - {new_string.split('-')[0].lstrip()}")
            #             unique error thrown here pass another
            try:
                word_id = await db.add_word(
                    name=new_string.split('-')[1].rstrip(),
                    language_id=1,
                )

                translation_id = await db.add_word(
                    name=new_string.split('-')[0].lstrip(),
                    language_id=2,
                )

                if word_id and translation_id:
                    await db.add_dictionary(
                        word_id=word_id,
                        translation_id=translation_id,
                    )
            except UniqueViolationError:
                print('unique error')
                pass
    os.remove(message.document.file_name)


@dp.message_handler(text='Test')
async def get_file(message: types.Message):
    rand_test = await db.get_random_test()
    test = ''
    for i in rand_test:
        test += f"{i['arabic_name']} - {i['uzbek_name']}\n"

    await message.answer(test)


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Эхо без состояния."
                         f"Сообщение:\n"
                         f"{message.text}")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
