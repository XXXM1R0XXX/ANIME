from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


bot = Bot(token="5189998907:AAG5A5jHt-iRLISwItg74_b9yNONJzasmoI")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class FSMInputName(StatesGroup):
    name = State()


@dp.message_handler(commands=["x"])
async def cmd_tese1(message: types.Message):
    await message.answer(mes)

@dp.message_handler(commands=["name"])
async def cmd_tese1(message: types.Message):
    await message.answer("Введите название")
    await FSMInputName.name.set()


@dp.message_handler(state=FSMInputName.name)
async def state1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    global mes
    mes=message.text
    await message.answer(message.text)
    await state.finish()
    # после этого данные в fsm пропадают, поэтому думайте когда закрывать стейт


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

