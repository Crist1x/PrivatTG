from aiogram.fsm.state import StatesGroup, State


class GetWalletForm(StatesGroup):
    GET_WALLET = State()
