#!venv/bin/python
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
conn = sqlite3.connect('Video.db')
cur = conn.cursor()

# Объект бота
bot = Bot(token="5189998907:AAG5A5jHt-iRLISwItg74_b9yNONJzasmoI")
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Хэндлер на команду /test1
@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await bot.send_video(message.chat.id, 'BAACAgIAAxkBAANEYp-ed22ete3mtjeTY5l7ZLKnqhwAAocYAAJoBAABSdX7TCY9FV05JAQ')
    await bot.copy_message(from_chat_id=919865126, chat_id=message.chat.id, message_id=234)
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    await message.answer("Введите название аниме для начала просмотра")
@dp.message_handler(content_types=['text'])
async def start_message(message: types.Message):
    global users_id
    users_id = str(message.text)
    cur.execute(
        "SELECT count(*) FROM SQL WHERE name = ? ", (users_id,))
    info = cur.fetchone()[0]
    if info==0:
        await message.answer("Такого аниме нима")
        await message.answer("Но,в ближайшее время добавим)")
        await bot.copy_message(from_chat_id=message.chat.id, chat_id=919865126, message_id=message.message_id)
    else:
        await message.answer("Введите номер сезона")
        await FSMInputName.sizon1.set()
class FSMInputName(StatesGroup):
    name = State()
    sizon=State()
    seria=State()
    sizon1=State()
    seria1=State()



@dp.message_handler(content_types=["video"])
async def video_and_text_id(message: types.Message):
    if message.chat.id == 919865126:
        await message.answer(message.video.file_id)
        await message.answer(message.message_id)
        global msg_id
        msg_id=message.message_id
        await message.answer("Введите название аниме")
        await FSMInputName.name.set()


        # cur.execute(f'SELECT * FROM SQL WHERE id = "{message.message_id}"')
        # result = cur.fetchall()

    else:
        await message.answer('Вы не админ')

@dp.message_handler(commands="test2")
async def cmd_test1(message: types.Message):
    await message.answer(message.chat.id)

@dp.message_handler(state=FSMInputName.name)
async def state1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    global mes
    mes=message.text
    await message.answer("Введите номер сезона")
    await FSMInputName.sizon.set()



@dp.message_handler(state=FSMInputName.sizon)
async def state2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sizon'] = message.text
    global siz
    siz=message.text
    await message.answer("Введите номер серии")
    await FSMInputName.seria.set()

@dp.message_handler(state=FSMInputName.seria)
async def state3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['seria'] = message.text
    global ser
    ser=message.text
    user=(mes,msg_id,siz,ser)
    cur.execute("INSERT INTO SQL VALUES(?, ?, ?, ?);", user)
    conn.commit()
    # cur.execute("SELECT * FROM SQL;")
    # all_results = cur.fetchall()[0]
    # await message.answer(all_results)
    conn.commit()
    await state.finish()

@dp.message_handler(state=FSMInputName.sizon1)
async def state4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sizon1'] = message.text
    global siz1
    siz1 = int(message.text)
    cur.execute(
        "SELECT count(*) FROM SQL WHERE siz = ? and name=?", (siz1,users_id))
    info = cur.fetchone()[0]
    if info==0:
        await message.answer("Такого сезона нима")
    else:
        await message.answer("Введите номер серии")
        await FSMInputName.seria1.set()

@dp.message_handler(state=FSMInputName.seria1)
async def state5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['seria1'] = message.text
    global ser1
    ser1 = int(message.text)
    cur.execute(
        "SELECT count(*) FROM SQL WHERE ser = ? and siz=? and name=? ", (ser1,siz1,users_id))
    info = cur.fetchone()[0]
    if info==0:
        await message.answer("Такой серии нима")
    else:
        cur.execute(f"SELECT id FROM SQL WHERE name='{users_id}' and siz={siz1} and ser={ser1}")
        res = cur.fetchone()[0]
        await bot.copy_message(from_chat_id=919865126, chat_id=message.chat.id, message_id=res)
        await state.finish()
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)