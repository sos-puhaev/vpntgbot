import logging
import os
import shutil
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from state.UsersState import UsersState
from state.MessageState import MessageState
from state.BalMessageState import BalMessageState
from state.KeyBundleState import KeyBundleState
from state.KeyWireState import KeyWireState
from aiogram.dispatcher import FSMContext
from database.db import supabase
from dotenv import load_dotenv
from datetime import datetime
from database.db_func import is_select_user, add_new_user, show_my_keys, update_keys_outline, update_keys_wireguard, update_keys_wireguard_bundle, show_my_keys_wg, show_my_keys_wg_bundle, update_balance, show_balance, pay_update_balance, show_my_keys_v2ray, update_keys_v2ray

from loader import dp, bot
from keyboards.choice_btn import choice, protocol, countri, price, keys, pay, null_line, wg_btn, wg_bundle, wg_price, null_file_wg_bundle, pay_wg, my_keys, not_keys, my_balance, set_summ, back_balance, after_pay, back_second_menu, list_protocol, message_help, device_install, device_install_outline, device_install_v2ray
from text.text import predCheck, parseInt, search_file_line, search_wg_file, search_bundle_wg_file, getCountry, getWgCountry, getWgTariff, getWgPrice, predCheckWgBundle, convert_bundle_country, end_data, convert_price_balance, v2ray_search_file_line
from text.sucess import search_country
from pathlib import Path


# Главная
@dp.message_handler(Command("start"))
async def show_items(message:Message):

    first_name = message.from_user.first_name
    id = message.from_user.id

    dir = Path("images", "fon.png")
    with open(dir, "rb") as photo:
        await bot.send_photo(chat_id=id, photo=photo)

    if is_select_user(id) == 1:
        await message.answer(f"С возвращением  <b>{first_name}</b> 🤟\nВаш Id: <b><code>{id}</code></b>\nОбязательно сообщи, если что-то не так 🧑‍💻", parse_mode="HTML", reply_markup=choice)
    else:
        add_new_user(id, first_name)
        await message.answer(f"Добро пожаловать {first_name} 🤟\nУ нас ты найдешь небольшой выбор VPN протоколов и стран 🧑‍💻, но мы уже тестируем новые протоколы 🥳, не переживай..., в случае блокировок либо сбоев определенных протоколов, мы обязательно переведем тебя на новый работающий VPN 🧑‍💻, и конечно бесплатно 😊 , надеюсь... ты останешся с нами 😊", parse_mode="HTML", reply_markup=choice)

# Баланс
@dp.callback_query_handler(text=["balance"])
async def show_my_balance(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id
    str = ""
    result = supabase.table("tg_users").select("balance").eq("user_id", id).execute().data
    for item in result:
        str = item['balance']

    await call.message.edit_text(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВаш баланс: <b>{str}</b> рублей. 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=my_balance)

# Пополнение баланса
@dp.callback_query_handler(text=["set_balance"], state="*")
async def set_my_balance(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.finish() # Закрываем состояние на случай перехода клиента с вкладки оплаты балансом

    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберете сумму из предложенного ниже, на которую хотите пополнить ваш баланс: 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=set_summ)

# Предчек оплаты для пополнения баланса
@dp.callback_query_handler(text=["210_b", "600_b", "1200_b", "2300_b"])
async def pred_balance(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    price = convert_price_balance(callback_data)
    await bot.send_invoice(chat_id=call.from_user.id, title="Пополнение баланса", description="Пополнение баланса", payload="invoice_balance",
                            provider_token=os.getenv('PAY_TOKEN'), currency='RUB', prices=[{'label':'Руб', 'amount': price * 100}])
    if call.message:
        await call.message.delete()

# Показать мои ключи 
@dp.callback_query_handler(text=["my_keys"])
async def show_my_keys_protocol(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберете протокол VPN, <b>чтобы посмотреть свои ключи:</b> 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=my_keys)

# Показать ключи Outline
@dp.callback_query_handler(text=["my_outline_keys"])
async def show_keys(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id

    async def edit_message(): # функция показывающая ключи
        result = supabase.table("tg_users").select("keys").eq("user_id", id).execute()
        data = result.data
        formatted_messages = []

        for item in data:
            keys = item.get('keys', '')
            if keys:
                key_list = keys.split(",")
                for key in key_list:
                    parts = key.split("|")
                    if len(parts) == 3:
                        text_message = (
                            f"Страна: <b>{getCountry(parts[1])}</b>\nДата окончания:🕒 <b>{parts[2]}</b>\n"
                            f"Ваш <b>Outline</b> ключ: ⬇️\n\n<b><code>{parts[0]}</code></b>"
                        )
                        formatted_messages.append(text_message)        

        if formatted_messages:
            formatted_text = "\n".join(formatted_messages)
            await call.message.edit_text(formatted_text, parse_mode="HTML")
        else:
            await call.message.edit_text("У вас нет данных для отображения.", parse_mode="HTML")
  
    if show_my_keys(id) == 1:
        await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nК сожелению у вас пока <b>нет активных ключей Outline</b> 🧑‍💻", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=not_keys)
    else:
        await edit_message()
        await call.message.edit_reply_markup(reply_markup=keys)
    
# Показать V2Ray ключи
@dp.callback_query_handler(text=["my_v2ray_keys"])
async def show_keys_v2ray(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id

    async def edit_message(): # функция показывающая ключи
        result = supabase.table("tg_users").select("vless").eq("user_id", id).execute()
        data = result.data
        formatted_messages = []

        for item in data:
            keys = item.get('vless', '')
            if keys:
                key_list = keys.split(",")
                for key in key_list:
                    parts = key.split("|")
                    if len(parts) == 3:
                        text_message = (
                            f"Страна: <b>{getCountry(parts[1])}</b>\nДата окончания:🕒 <b>{parts[2]}</b>\n"
                            f"Ваш <b>V2Ray(vless)</b> ключ: ⬇️\n\n<b><code>{parts[0]}</code></b>"
                        )
                        formatted_messages.append(text_message)        

        if formatted_messages:
            formatted_text = "\n".join(formatted_messages)
            await call.message.edit_text(formatted_text, parse_mode="HTML")
        else:
            await call.message.edit_text("У вас нет данных для отображения.", parse_mode="HTML")
  
    if show_my_keys_v2ray(id) == 1:
        await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nК сожелению у вас пока <b>нет активных ключей V2Ray(vless)</b> 🧑‍💻", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=not_keys)
    else:
        await edit_message()
        await call.message.edit_reply_markup(reply_markup=keys)

# Показать ключи WireGuard
@dp.callback_query_handler(text=["my_wireguard_keys"])
async def show_keys_wireguard(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id

    result = supabase.table("tg_users").select("wg_keys").eq("user_id", id).execute()
    data = result.data
    dest_path = f"vpn_keys/wireguard/total"

    btn = [
        InlineKeyboardButton(text="Взять +1 ключ", callback_data="tariff"),
        InlineKeyboardButton(text="⬅️ Назад к просмотру своих протоколов", callback_data="my_keys")
    ]
    key_btn = types.InlineKeyboardMarkup(row_width=1)
    key_btn.add(*btn)
  
    if show_my_keys_wg(id) == 1:
        await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nК сожелению у вас пока <b>нет активных ключей WireGuard</b> 🧑‍💻", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=not_keys)
    else:
        await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВаши <b>WireGuard</b> ключи 🧑‍💻", parse_mode="HTML")
        for item in data:
            keys = item.get('wg_keys', '')
            if keys:
                key_list = keys.split(",")
                for key in key_list:
                    parts = key.split("|")
                    if len(parts) == 3:
                        text_message = (
                            f"Страна: <b>{getCountry(parts[1])}</b>\nДата окончания:🕒 <b>{parts[2]}</b>\n"
                            f"Ваш <b>WireGuard</b> ключ: ⬇️"
                        )
                        await call.message.answer(f"{text_message}", parse_mode="HTML")
                        file_path = f"{dest_path}/{parts[0]}"
                        with open(file_path, 'rb') as wg_file:
                            await call.bot.send_document(id, document=wg_file)

        await call.message.answer("___________________", reply_markup=key_btn)
        if call.message:
            await call.message.delete()

# Показать ключи WireGuard в связке
@dp.callback_query_handler(text=["my_bundle_wireguard_keys"])
async def show_keys_wireguard(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id

    result = supabase.table("tg_users").select("wg_bundle_keys").eq("user_id", id).execute()
    data = result.data
    dest_path = f"vpn_keys/wireguard-bundle/total"

    btn = [
        InlineKeyboardButton(text="Взять +1 ключ", callback_data="tariff"),
        InlineKeyboardButton(text="⬅️ Назад к просмотру своих протоколов", callback_data="my_keys")
    ]
    key_btn = types.InlineKeyboardMarkup(row_width=1)
    key_btn.add(*btn)
  
    if show_my_keys_wg_bundle(id) == 1:
        await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nК сожелению у вас пока <b>нет активных ключей WireGuard в связке</b> 🧑‍💻", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=not_keys)
    else:
        await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВаши <b>WireGuard в связке</b> ключи 🧑‍💻", parse_mode="HTML")
        for item in data:
            keys = item.get('wg_bundle_keys', '')
            if keys:
                key_list = keys.split(",")
                for key in key_list:
                    parts = key.split("|")
                    if len(parts) == 3:
                        text_message = (
                            f"Страна: <b>{getWgCountry(parts[1])}</b>\nДата окончания:🕒 <b>{parts[2]}</b>\n"
                            f"Ваш <b>WireGuard в связке</b> ключ: ⬇️"
                        )
                        await call.message.answer(f"{text_message}", parse_mode="HTML")
                        file_path = f"{dest_path}/{parts[0]}"
                        with open(file_path, 'rb') as wg_file:
                            await call.bot.send_document(id, document=wg_file)

        await call.message.answer("_______________", reply_markup=key_btn)
        if call.message:
            await call.message.delete()

# Показать протоколы
@dp.callback_query_handler(text=["tariff"])
async def show_protocol(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\n🟢 <b>V2Ray</b> - Китайский протокол, является стабильным решением, обходит современные блокировки РКН.\n\n🟡 <b>Outline(Shadowsocks)</> - принцип работы схож с V2Ray, скорость быстрее, но более заметен РКН.\n\n🔴 <b>WireGuard</b> - простой для обноружения РКН, но быстрее чем V2Ray и Outline.\n\n 📌 <b>Замена протоколов, осуществляется бесплатно.</b> 📌\n\nВыберете <b>VPN протокол:</b> 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=protocol)
    await UsersState.protocol.set() # Запускаем состояние

# Назад в главное меню
@dp.callback_query_handler(text=["back_menu"], state="*")
async def back_first_menu(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id

    await state.finish()
    await call.message.edit_text(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВы находитесь в главном меню\nВаш ID: {id} 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=choice)

# Показать сервисы wireguard
@dp.callback_query_handler(text=["wireguard_service"], state="*")
async def show_protocol(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await UsersState.protocol.set()
    await call.message.edit_text("Выберете тип <b>WireGuard</b> протокола: 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=wg_btn)


# Показать страны
@dp.callback_query_handler(text=["v2ray", "outline", "wireguard"], state=UsersState.protocol)
async def show_country(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберете страну, через которую хотите пускать ваш трафик: 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=countri)
    await state.update_data(protocol = callback_data) # Обрабатываем предыдущее действие(выб. протокола)
    await UsersState.country.set()

# Назад к выбору протокола
@dp.callback_query_handler(text=["back_protocol"], state="*")
async def back_first_menu(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\n🟢 <b>V2Ray</b> - Китайский протокол, является стабильным решением, обходит современные блокировки РКН.\n\n🟡 <b>Outline(Shadowsocks)</> - принцип работы схож с V2Ray, скорость быстрее, но более заметен РКН.\n\n🔴 <b>WireGuard</b> - простой для обноружения РКН, но быстрее чем V2Ray и Outline.\n\n 📌 <b>Замена протоколов, осуществляется бесплатно.</b> 📌\n\nВыберете <b>VPN протокол:</b> 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=protocol)
    await UsersState.protocol.set() # Запускаем состояние


# Показать цены
@dp.callback_query_handler(text=["russia", "latvia", "turcia", "georgia"], state=UsersState.country)
async def show_price(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    data = await state.get_data() # Обращамся к стеку
    data_name_country = getCountry(callback_data) # Конвертируем имя страны в вид для текста
    data_protocol = data['protocol'] # Достаем имя протокол
    w_exam = search_wg_file(callback_data) # Проверка наличия файла wg 0=истина, 1=ложь
    o_exam = search_country(callback_data) # Поиск имени файла по выбору страны outline |
    v2ray = search_country(callback_data) # Проверка наличия ключа v2ray +

    result_o_exam = search_file_line(o_exam) # Результат наличие строк в найденом файле Outline 0=истина, 1=ложь |
    result_v2ray = v2ray_search_file_line(v2ray) # Результат наличие строк в найденом файле V2Ray 0=истина, 1=ложь +

    if data_protocol == "outline":
        if result_o_exam == 1: # ключ отсутствует
            await call.message.edit_text(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nКлючи <b>Outline</b> страны <b>{data_name_country}</b> закончились, но мы уже их загружем 🧑‍💻\nВыберете другую страну, либо обратитесь в тех поддержку 🧑‍💻", parse_mode="HTML")
            await call.message.edit_reply_markup(reply_markup=null_line)
        else:
            await state.update_data(country = callback_data) # Обрабатываем предыдущее действие(выб. страну)
            await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберите подходящий для вас <b>тариф</b>: 🧑‍💻", parse_mode="HTML")
            await call.message.edit_reply_markup(reply_markup=price)
            await UsersState.price.set()

    if data_protocol == "v2ray":
        if result_v2ray == 1: # ключ отсутствует
            await call.message.edit_text(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nКлючи <b>V2Ray(vless)</b> страны <b>{data_name_country}</b> закончились, но мы уже их загружем 🧑‍💻\nВыберете другую страну, либо обратитесь в тех поддержку 🧑‍💻", parse_mode="HTML")
            await call.message.edit_reply_markup(reply_markup=null_line)
        else:
            await state.update_data(country = callback_data) # Обрабатываем предыдущее действие(выб. страну)
            await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберите подходящий для вас <b>тариф</b>: 🧑‍💻", parse_mode="HTML")
            await call.message.edit_reply_markup(reply_markup=price)
            await UsersState.price.set()

    if data_protocol == "wireguard":
        if w_exam == 1: # ключ отсутствует
            await call.message.edit_text(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nКлючи <b>WireGuard</b> страны <b>{data_name_country}</b> закончились 🧑‍💻, но мы уже их загружем\nВыберете другую страну, либо обратитесь в тех поддержку 🧑‍💻", parse_mode="HTML")
            await call.message.edit_reply_markup(reply_markup=null_line)
        else:
            await state.update_data(country = callback_data) # Обрабатываем предыдущее действие(выб. страну)
            await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберите подходящий для вас <b>тариф</b>: 🧑‍💻", parse_mode="HTML")
            await call.message.edit_reply_markup(reply_markup=price)
            await UsersState.price.set()

# Проверка на существование ключей
@dp.callback_query_handler(text=["null_line"], state="*")
async def null_line_window(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    
# Назад к выбору стран
@dp.callback_query_handler(text=["back_country"], state="*")
async def back_country(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.set_state(UsersState.country)
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберете страну, через которую хотите пускать ваш <b>трафик:</b> 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=countri)

# Оплата тарифа
@dp.callback_query_handler(text=["1_mounth", "3_mounth", "6_mounth", "12_mounth"], state=UsersState.price)
async def show_pay(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.update_data(tariff = callback_data) # Обрабатываем предыдущее действие(выб. тариф)
    data = await state.get_data()
    print(data)
    #print(data['country'])
    str = predCheck(data)
    await call.message.edit_text(f"{str}", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=pay)

# Хандлер кнопки вернуться назад, из-за отрицательного баланса
@dp.callback_query_handler(text=["back_predcheck"], state="*")
async def back_predcheck(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    data = await state.get_data()
    if data['protocol'] == "bundle": # если протокол Wireguard в связке
        str = predCheckWgBundle(data)
        await call.message.edit_text(f"{str}", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=pay_wg)
    else: # Остальные протоколы
        str = predCheck(data)
        await call.message.edit_text(f"{str}", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=pay)
    

# Назад к выбору цены тарифа
@dp.callback_query_handler(text=["back_price"], state="*")
async def back_country(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.set_state(UsersState.price)
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберите подходящий для вас <b>тариф</b>: 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=price)

# Процесс оплаты
@dp.callback_query_handler(text="pay", state="*")
async def process_pay(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    data = await state.get_data()
    price_int = parseInt(data["tariff"], data['protocol']) # Конвертируем тариф в int цену
    await bot.send_invoice(chat_id=call.from_user.id, title="Покупка ключа", description="Покупка ключа доступа", payload="invoice",
                            provider_token=os.getenv('PAY_TOKEN'), currency='RUB', prices=[{'label':'Руб', 'amount': price_int * 100}])
    

@dp.pre_checkout_query_handler(lambda query:True, state="*")
async def process_pre_checkout_query_handler(pre_checkout_query: types.PreCheckoutQuery, state:FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    


# В случае успеха оплаты
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state="*")
async def success_pay(message: types.Message, state:FSMContext):

    id = message.from_user.id # id пользователя

    # Invoice пополнения баланса
    invoice = message.successful_payment.invoice_payload
    if invoice == "invoice_balance":
        total_amount = message.successful_payment.total_amount / 100.0
        update_balance(id, total_amount)
        await message.answer(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВаш баланс успешно пополнен на сумму {total_amount} рублей 🧑‍💻", reply_markup=back_second_menu)
        if message:
            await message.delete()
        
    #---------------------------
    # Покупка ключа
    else:
        data = await state.get_data()
        data_protocol = data['protocol'] # Извлекаем протокол из стека

        country = search_country(data['country']) # Поиск файла страны
        dir = Path("vpn_keys", country) # Путь к файлу Outline
        in_key = ""  # Для ключа Outline
        w_exam = 1 # Переменная, которая хранит наличие файла wg и wg в связке
        current_date = end_data(data['tariff']) # Тариф 

        if data_protocol == "wireguard":
            w_exam = search_wg_file(data['country']) # Проверка наличия файла wg 0=истина, 1=ложь
        if data_protocol == "bundle":
            w_exam = search_bundle_wg_file(data['country']) # Проверка наличия файла wg в связке 0=истина, 1=ложь

        if data_protocol == "outline":
            if search_file_line(country) == 1:
                await message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!!",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                await bot.send_photo(chat_id=id, photo=photo)

                await message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nCкопируйте ключ, который находится ниже и вставтье его в приложение <b>Outline</b>🧑‍💻  ⬇️", parse_mode="HTML")
                with open(dir, "r") as f: # Открытие файла
                    text = f.readlines()
                    in_key = text[0] # Берем первую строку
                # Удаление первой строки {
                f=open(dir).readlines()
                for i in [0]:
                    f.pop(i)
                with open(dir,'w') as F:
                    F.writelines(f)
                # }
                # Запись базу данных ключа outline
                update_keys_outline(id, in_key, data['country'],current_date)
                #---------------------------------
                await message.answer(text=f"<b><code>{in_key}</code></b>", parse_mode="HTML")
                await message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if message:
                await message.delete()

        if data_protocol == "v2ray":
            dir_v2ray = Path("vpn_keys/v2ray", country) # Путь к файлу V2Ray
            in_key_v2 = ""  # Для ключа V2Ray

            if v2ray_search_file_line(country) == 1:
                await message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!!",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                await bot.send_photo(chat_id=id, photo=photo)

                await message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nCкопируйте ключ, который находится ниже и вставтье его в приложение <b>V2Ray</b>🧑‍💻  ⬇️", parse_mode="HTML")
                with open(dir_v2ray, "r") as f: # Открытие файла
                    text_v2 = f.readlines()
                    in_key_v2 = text_v2[0] # Берем первую строку
                # Удаление первой строки {
                f=open(dir_v2ray).readlines()
                for j in [0]:
                    f.pop(j)
                with open(dir_v2ray,'w') as D:
                    D.writelines(f)
                # }
                # Запись базу данных ключа v2ray
                update_keys_v2ray(id, in_key_v2, data['country'], current_date)
                #---------------------------------
                await message.answer(text=f"<b><code>{in_key_v2}</code></b>", parse_mode="HTML")
                await message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if message:
                await message.delete()

        if data_protocol == "wireguard":
            if w_exam == 1:
                await message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!!",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                await bot.send_photo(chat_id=id, photo=photo)

                await message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИмпортируйте файл в приложение <b>WireGuard</b>🧑‍💻  ⬇️", parse_mode="HTML")

                wg_dir = Path(f"vpn_keys/wireguard/{data['country']}") # Путь к директории страны
                file_name = os.listdir(wg_dir) # Получить имя файла в директории
                source_path = f"{wg_dir}/{file_name[0]}" # Получаем полный путь к файлу для перемещения
                dest_path = Path(f"vpn_keys/wireguard/total/{file_name[0]}") # Папка куда будем перемещать файл

                with open(f"{wg_dir}/{file_name[0]}", 'rb') as wg_file:
                    await bot.send_document(id, document=wg_file) # Отправляем файл пользователю
                shutil.move(source_path, dest_path) # Перемещаем файл

                # Запись базу данных ключа wireguard
                update_keys_wireguard(id, file_name[0], data['country'], current_date)
                #---------------------------------
                await message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if message:
                await message.delete()

        if data_protocol == "bundle":
            if w_exam == 1:
                await message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!!",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                await bot.send_photo(chat_id=id, photo=photo)

                wg_bundle_country = convert_bundle_country(data["country"]) # Конвертируем страну с перфиксом rf_ в без него
                await message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИмпортируйте файл в приложение <b>WireGuard</b> 🧑‍💻  ⬇️", parse_mode="HTML")
                wg_dir_bundle = Path(f"vpn_keys/wireguard-bundle/{wg_bundle_country}") # Путь к директории страны
                file_name_bundle = os.listdir(wg_dir_bundle) # Получить имя файла в директории
                source_path = f"{wg_dir_bundle}/{file_name_bundle[0]}" # Получаем полный путь к файлу для перемещения
                dest_path = Path(f"vpn_keys/wireguard-bundle/total/{file_name_bundle[0]}") # Папка куда будем перемещать файл

                with open(f"{wg_dir_bundle}/{file_name_bundle[0]}", 'rb') as wg_file_bundle:
                    await bot.send_document(id, document=wg_file_bundle) # Отправляем файл пользователю
                shutil.move(source_path, dest_path) # Перемещаем файл

                # Запись базу данных ключа wireguard в связке
                update_keys_wireguard_bundle(id, file_name_bundle[0], data['country'], current_date)
                #---------------------------------

                await message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if message:
                await message.delete()


# Оплата балансом
@dp.callback_query_handler(text=["pay_balance"], state="*")
async def pay_balance(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id # id пользователя
    data = await state.get_data()
    price_tariff = parseInt(data["tariff"], data["protocol"]) # узнать цену тариффа нужного протокола
    balance = show_balance(id) # Узнать баланс
    
    if float(price_tariff) > float(balance):
        await call.message.edit_text(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВаш баланс: <b>{balance} P</b>. К сожелению этого не достаточно для покупки ключа 😔. Вернитесь к <b>выбору оплат</b> или можете <b>пополнить ваш баланс</b>. 🧑‍💻", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=back_balance)

    else:
        result_balance = float(balance) - float(price_tariff) # Вычитаем из баланса сумму тарифа
        pay_update_balance(id, result_balance) # Записываем итоговую сумму в базу

        data_protocol = data['protocol'] # Извлекаем протокол из стека

        country = search_country(data['country']) # Поиск файла страны
        dir = Path("vpn_keys", country) # Путь к файлу
        in_key = ""  # Для ключа Outline
        w_exam = 1 # Переменная, которая хранит наличие файла wg и wg в связке
        current_date = end_data(data['tariff']) # Тариф 

        if data_protocol == "wireguard":
            w_exam = search_wg_file(data['country']) # Проверка наличия файла wg 0=истина, 1=ложь
        if data_protocol == "bundle":
            w_exam = search_bundle_wg_file(data['country']) # Проверка наличия файла wg в связке 0=истина, 1=ложь

        if data_protocol == "outline":
            if search_file_line(country) == 1:
                await call.message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!! 🧑‍💻",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                async def photo_success_send():
                    mess = await bot.send_photo(chat_id=id, photo=photo)
                    return mess.message_id
                BalMessageState.message_one = await photo_success_send()

                async def mess_info():
                    mess = await call.message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nCкопируйте ключ, который находится ниже и вставтье его в приложение <b>Outline</b> 🧑‍💻  ⬇️", parse_mode="HTML")
                    return mess.message_id
                BalMessageState.message_two = await mess_info()

                with open(dir, "r") as f: # Открытие файла
                    text = f.readlines()
                    in_key = text[0] # Берем первую строку
                # Удаление первой строки {
                f=open(dir).readlines()
                for i in [0]:
                    f.pop(i)
                with open(dir,'w') as F:
                    F.writelines(f)
                # }
                # Запись базу данных ключа outline
                update_keys_outline(id, in_key, data['country'],current_date)
                #---------------------------------
                async def show_key():
                    k = await call.message.answer(text=f"<b><code>{in_key}</code></b>", parse_mode="HTML")
                    return k.message_id
                BalMessageState.message_three = await show_key()
                
                await call.message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if call.message:
                await call.message.delete()

        # Оплата V2Ray
        if data_protocol == "v2ray":
            if v2ray_search_file_line(country) == 1:
                await call.message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!! 🧑‍💻",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                dir_v2ray = Path("vpn_keys/v2ray", country) # Путь к файлу
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                async def photo_success_send():
                    mess = await bot.send_photo(chat_id=id, photo=photo)
                    return mess.message_id
                BalMessageState.message_one = await photo_success_send()

                async def mess_info():
                    mess = await call.message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nCкопируйте ключ, который находится ниже и вставтье его в приложение <b>V2Ray</b> 🧑‍💻  ⬇️", parse_mode="HTML")
                    return mess.message_id
                BalMessageState.message_two = await mess_info()

                with open(dir_v2ray, "r") as f: # Открытие файла
                    text = f.readlines()
                    in_key = text[0] # Берем первую строку
                # Удаление первой строки {
                f=open(dir_v2ray).readlines()
                for i in [0]:
                    f.pop(i)
                with open(dir_v2ray,'w') as F:
                    F.writelines(f)
                # }
                # Запись базу данных ключа outline
                update_keys_v2ray(id, in_key, data['country'],current_date)
                #---------------------------------
                async def show_key():
                    k = await call.message.answer(text=f"<b><code>{in_key}</code></b>", parse_mode="HTML")
                    return k.message_id
                BalMessageState.message_three = await show_key()
                
                await call.message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if call.message:
                await call.message.delete()

        if data_protocol == "wireguard":
            if w_exam == 1:
                await call.message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!! 🧑‍💻",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                async def success_photo():
                    photo_success = await bot.send_photo(chat_id=id, photo=photo)
                    return photo_success.message_id
                KeyWireState.message_one = await success_photo()

                async def mess_info():
                    mess = await call.message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИмпортируйте файл в приложение <b>WireGuard</b> 🧑‍💻  ⬇️", parse_mode="HTML")
                    return mess.message_id
                KeyWireState.message_two = await mess_info()
                
                wg_dir = Path(f"vpn_keys/wireguard/{data['country']}") # Путь к директории страны
                file_name = os.listdir(wg_dir) # Получить имя файла в директории
                source_path = f"{wg_dir}/{file_name[0]}" # Получаем полный путь к файлу для перемещения
                dest_path = Path(f"vpn_keys/wireguard/total/{file_name[0]}") # Папка куда будем перемещать файл

                async def send_file():
                    with open(f"{wg_dir}/{file_name[0]}", 'rb') as wg_file:
                        f = await bot.send_document(id, document=wg_file) # Отправляем файл пользователю
                    shutil.move(source_path, dest_path) # Перемещаем файл
                    return f.message_id
                KeyWireState.message_three = await send_file()

                # Запись базу данных ключа wireguard
                update_keys_wireguard(id, file_name[0], data['country'], current_date)
                #---------------------------------
                await call.message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if call.message:
                await call.message.delete()

        if data_protocol == "bundle":
            if w_exam == 1:
                await call.message.answer(text="Упс!!! Пока вы покупали, ключи закончились, срочно напишите в тех поддержку чтоб они выслали вам купленный ключ с бесплатным продлением на 1 месяц!!! 🧑‍💻",reply_markup=null_line)
                await state.finish() # завершаем стейт
            else:
                img_dir = Path("images", "payment_success.png")
                photo = open(img_dir, "rb")
                async def success_photo():
                    mess = await bot.send_photo(chat_id=id, photo=photo)
                    return mess.message_id
                KeyBundleState.message_one = await success_photo()

                wg_bundle_country = convert_bundle_country(data["country"]) # Конвертируем страну с перфиксом rf_ в без него
                async def message_info():
                    mess = await call.message.answer(text="\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИмпортируйте файл в приложение <b>WireGuard</b> 🧑‍💻  ⬇️", parse_mode="HTML")
                    return mess.message_id
                KeyBundleState.message_two = await message_info()

                wg_dir_bundle = Path(f"vpn_keys/wireguard-bundle/{wg_bundle_country}") # Путь к директории страны
                file_name_bundle = os.listdir(wg_dir_bundle) # Получить имя файла в директории
                source_path = f"{wg_dir_bundle}/{file_name_bundle[0]}" # Получаем полный путь к файлу для перемещения
                dest_path = Path(f"vpn_keys/wireguard-bundle/total/{file_name_bundle[0]}") # Папка куда будем перемещать файл
                async def file_send():
                    with open(f"{wg_dir_bundle}/{file_name_bundle[0]}", 'rb') as wg_file_bundle:
                        fil = await bot.send_document(id, document=wg_file_bundle) # Отправляем файл пользователю
                    shutil.move(source_path, dest_path) # Перемещаем файл
                    return fil.message_id
                KeyBundleState.message_three = await file_send()

                # Запись базу данных ключа wireguard в связке
                update_keys_wireguard_bundle(id, file_name_bundle[0], data['country'], current_date)
                #---------------------------------

                await call.message.answer(text="Спасибо за покупку ☺️", reply_markup=after_pay)
                await state.finish()
            if call.message:
                await call.message.delete()


# Связка двух стран WireGuard, выбор страны
@dp.callback_query_handler(text=["bundle"], state=UsersState.protocol)
async def show_protocol(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.update_data(protocol = callback_data)
    # data = await state.get_data()
    # print(data)
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\n<b>WireGuard в связке двух стран</b>, означает, что <b>РФ ресурсы: ВКонтакте, Банки, ГосУслуги и т.д.</b> будут работать через <b>РФ сервер</b>, а все зарубежные ресурсы, через страну, которую вы можете <b>выбрать ниже</b>, это дает возможность не включать/выключать VPN постоянно. 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=wg_bundle)
    await UsersState.country.set()

# Хандлер для выбор тарифа WireGuard для связки
@dp.callback_query_handler(text=["rf_latvia", "rf_georgia", "rf_turcia"], state=UsersState.country)
async def show_tariff_wg_bundle(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    data_name_country = getWgCountry(callback_data) # Конвертируем имя страны в вид для текста
    data = await state.get_data() # удалить
    w_exam = search_bundle_wg_file(callback_data) # Проверка наличия файла wg для связки 0=истина, 1=ложь

    if w_exam == 1: # ключ отсутствует
        await call.message.edit_text(f"\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nКлючи <b>WireGuard в связке</b> страны <b>{data_name_country}</b> закончились, но мы уже их загружем 🧑‍💻\nВыберете другую страну, либо обратитесь в тех поддержку 🧑‍💻", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=null_file_wg_bundle)
    else:
        await state.update_data(country = callback_data) # Обрабатываем предыдущее действие(выб. страну)
        await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\n<b>(WireGuard в связке)</b> Выберете подходящий тариф: 🧑‍💻", parse_mode="HTML")
        await call.message.edit_reply_markup(reply_markup=wg_price)
        await UsersState.price.set()

# Назад из за отсутствия ключей wireguard в связке
@dp.callback_query_handler(text=["null_file_back_country"], state="*")
async def null_line_window_wg(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\n<b>WireGuard в связке двух стран</b>, означает, что <b>РФ ресурсы: ВКонтакте, Банки, ГосУслуги и т.д.</b> будут работать через <b>РФ сервер</b>, а все зарубежные ресурсы, через страну, которую вы можете <b>выбрать ниже</b>, это дает возможность не включать/выключать VPN постоянно. 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=wg_bundle)
    await UsersState.country.set()
    
# Назад к выбору стран wireguard в связке
@dp.callback_query_handler(text=["back_country_bundle"], state="*")
async def back_country_bundle(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.set_state(UsersState.country)
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\n<b>WireGuard в связке двух стран</b>, означает, что <b>РФ ресурсы: ВКонтакте, Банки, ГосУслуги и т.д.</b> будут работать через <b>РФ сервер</b>, а все зарубежные ресурсы, через страну, которую вы можете <b>выбрать ниже</b>, это дает возможность не включать/выключать VPN постоянно. 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=wg_bundle)

# Хандлер для выбора цены WireGuard для связки
@dp.callback_query_handler(text=["1_mounth_wg", "3_mounth_wg", "6_mounth_wg", "12_mounth_wg"], state=UsersState.price)
async def show_price_wg_bundle(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.update_data(tariff = callback_data) # Обрабатываем предыдущее действие(выб. тариф)
    data = await state.get_data()
    print(data)
    #print(data['country'])
    str = predCheckWgBundle(data)
    await call.message.edit_text(f"{str}", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=pay_wg)

# Назад к выбору цены тарифа wireguard в связке
@dp.callback_query_handler(text=["back_price_wg"], state="*")
async def back_country_wg(call: CallbackQuery, state:FSMContext):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await state.set_state(UsersState.price)
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\n<b>(WireGuard в связке)</b> Выберете подходящий тариф: 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=wg_price)

# Инструкция
@dp.callback_query_handler(text=["install_key"], state="*")
async def instruction(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    if MessageState.message_one:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=MessageState.message_one)
        except Exception as e:
            MessageState.message_one = "0"
    if MessageState.message_two:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=MessageState.message_two)
        except Exception as e:
            MessageState.message_two = "0"

    if BalMessageState.message_one:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=BalMessageState.message_one)
        except Exception as e:
            BalMessageState.message_one = "0"
    if BalMessageState.message_two:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=BalMessageState.message_two)
        except Exception as e:
            BalMessageState.message_two = "0"
    if BalMessageState.message_three:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=BalMessageState.message_three)
        except Exception as e:
            BalMessageState.message_three = "0"

    if KeyBundleState.message_one:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=KeyBundleState.message_one)
        except Exception as e:
            KeyBundleState.message_one = "0"
    if KeyBundleState.message_two:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=KeyBundleState.message_two)
        except Exception as e:
            KeyBundleState.message_two = "0"
    if KeyBundleState.message_three:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=KeyBundleState.message_three)
        except Exception as e:
            KeyBundleState.message_three = "0"

    if KeyWireState.message_one:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=KeyWireState.message_one)
        except Exception as e:
            KeyWireState.message_one = "0"
    if KeyWireState.message_two:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=KeyWireState.message_two)
        except Exception as e:
            KeyWireState.message_two = "0"
    if KeyWireState.message_three:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=KeyWireState.message_three)
        except Exception as e:
            KeyWireState.message_three = "0"

    await call.message.edit_text("👨‍🏫<b>Инструкция по установке</b>👨‍🏫\n\nВыберете протокол своего ключа, который вы приобрели ранее. 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=list_protocol)

# Инструкция Wireguard
#-------------------------------------------------------------------------
@dp.callback_query_handler(text=["install_wireguard"])
async def instruction(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберете устройство, на которое нужно установить <b>WireGuard VPN:</b> 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=device_install)
        
# Установка Андроид
@dp.callback_query_handler(text=["android"], state="*")
async def instruction_android(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id # id пользователя
    video_path = Path("video", "android.mp4")
    link = hlink('«Скачать приложение WireGuard»', 'https://play.google.com/store/apps/details?id=com.wireguard.android&pcampaignid=web_share')
    text = f"<b>1 Пункт.</b> {link}\n<b>2 Пункт.</b> Перейдите в боте «Главное меню» -> «Мои ключи», выберете протокол VPN купленного вами ключа, скачайте его.\n<b>3 Пункт.</b> Откройте скаченное приложение WireGuard.\n<b>4 Пункт.</b> Нажмите на плюсик вправом нижнем углу приложения. Далее, импортировать файл(Откроется окно с вашими папкам и файлами).\n<b>5 Пункт.</b> Найдите ранее скаченный в пункте 2 ваш файл (имя_файла.conf). Нажмите на него.\n<b>6 Пункт.</b> Далее у вас появится в окне приложения имя того файла, на которое вы нажали, рядом расположен ползунок, нажмите на него, и VPN должен включится.  🧑‍💻\n\n⚠️ <b>Один ключ, одно устройство, иначе будут зависания</b> ⚠️\n"

    async def video_send(chat_id, video_path, caption): # Загрузка видео
        with open(video_path, "rb") as file:
            video_message =  await bot.send_video(chat_id, video=types.InputFile(file), caption=caption, parse_mode="HTML")
            return video_message.message_id
            
    async def h1_message():
        mess = await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИнструкция по установке <b>WireGuard</b> на <b>Android</b> 🧑‍💻", parse_mode="HTML")
        return mess.message_id

    MessageState.message_one = await h1_message()
    MessageState.message_two = await video_send(id, video_path, text)

    await call.message.answer("Если у вас не получилось установить приложение и импортировать ключ, нажмите на кнопку <b>Обратиться за помощью с установкой</b> 🧑‍💻", reply_markup=message_help)

    if call.message:
        await call.message.delete()

# Установка Iphone/Ipad
@dp.callback_query_handler(text=["iphone"], state="*")
async def instruction_iphone(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id # id пользователя
    video_path = Path("video", "iphone.mp4")
    link = hlink('«Скачать приложение WireGuard»', 'https://apps.apple.com/ru/app/wireguard/id1441195209')
    text = f"<b>1 Пункт.</b> {link}\n<b>2 Пункт.</b> Перейдите в боте «Главное меню» -> «Мои ключи», выберете протокол VPN купленного вами ключа\n<b>3 Пункт.</b> Откройте файл, в появившемся окне, влевом нижнем углу, нажмите на стрелку, которая указывает вверх.\n<b>4 Пункт.</b> В списке приложений, который вы видете, найдите WireGuard и нажмите на него, если его нет, прокрутите до конца и нажмите «Еще», в открывшемся списке найдите WireGuard, оно должно быть там (посмотрите внимательно 🧑‍💻) .\n<b>5 Пункт.</b> Откроется небольшое окно, нажмите «Разрешить» .\n<b>6 Пункт.</b> Вы увидете в окне приложения имя вашего скаченного файла, справо от него будет тумблер, нажмите на него и ВПН должен включиться.  🧑‍💻\n\n⚠️ <b>Один ключ, одно устройство, иначе будут зависания</b> ⚠️\n"

    async def video_send(chat_id, video_path, caption): # Загрузка видео
        with open(video_path, "rb") as file:
            video_message =  await bot.send_video(chat_id, video=types.InputFile(file), caption=caption, parse_mode="HTML")
            return video_message.message_id
            
    async def h1_message():
        mess = await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИнструкция по установке <b>WireGuard</b> на <b>Iphone/Ipad</b> 🧑‍💻", parse_mode="HTML")
        return mess.message_id

    MessageState.message_one = await h1_message()
    MessageState.message_two = await video_send(id, video_path, text)

    await call.message.answer("Если у вас не получилось установить приложение и импортировать ключ, нажмите на кнопку <b>Обратиться за помощью с установкой</b> 🧑‍💻", reply_markup=message_help)

    if call.message:
        await call.message.delete()
#-------------------------------------------------------------------------


# Инструкция Outline
#-------------------------------------------------------------------------
@dp.callback_query_handler(text=["install_outline"])
async def instruction_out(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберете устройство, на которое нужно установить <b>Outline VPN:</b> 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=device_install_outline)
        
# Установка Андроид
@dp.callback_query_handler(text=["android_outline"], state="*")
async def instruction_android_out(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")


    id = call.from_user.id # id пользователя
    video_path = Path("video", "android_outline.mp4")
    link = hlink('«Скачать приложение Outline»', 'https://play.google.com/store/apps/details?id=org.outline.android.client&pcampaignid=web_share')
    text = f"<b>1 Пункт.</b> {link}\n<b>2 Пункт.</b> Перейдите в боте «Главное меню» -> «Мои ключи», выберете протокол VPN Outline и <b>скопируйте ключ</b>.\n<b>3 Пункт.</b> Откройте скаченное приложение <b>Outline</b>.\n<b>4 Пункт.</b> Нажмите по середине «Добавить сервер».\n<b>5 Пункт.</b> Вставьте в открывшемся окне ключ, который вы скопировали ранее (Обычно ключ уже бывает вставлен и вам просто нужно нажать «Подключиться» ).\n<b>6 Пункт.</b>Нажмите подключиться, и VPN должен включится.  🧑‍💻\n\n⚠️ <b>Один ключ, одно устройство, иначе будут зависания</b> ⚠️\n"

    async def video_send(chat_id, video_path, caption): # Загрузка видео
        with open(video_path, "rb") as file:
            video_message =  await bot.send_video(chat_id, video=types.InputFile(file), caption=caption, parse_mode="HTML")
            return video_message.message_id
            
    async def h1_message():
        mess = await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИнструкция по установке <b>Outline</b> на <b>Android</b> 🧑‍💻", parse_mode="HTML")
        return mess.message_id

    MessageState.message_one = await h1_message()
    MessageState.message_two = await video_send(id, video_path, text)

    await call.message.answer("Если у вас не получилось установить приложение и импортировать ключ, нажмите на кнопку <b>Обратиться за помощью с установкой</b> 🧑‍💻", reply_markup=message_help)

    if call.message:
        await call.message.delete()

# Установка Iphone/Ipad
@dp.callback_query_handler(text=["iphone_outline"], state="*")
async def instruction_iphone_out(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id # id пользователя
    video_path = Path("video", "iphone_outline.mp4")
    link = hlink('«Скачать приложение Outline»', 'https://apps.apple.com/ru/app/outline-app/id1356177741')
    text = f"<b>1 Пункт.</b> {link}\n<b>2 Пункт.</b> Перейдите в боте «Главное меню» -> «Мои ключи», выберете протокол VPN Outline и <b>скопируйте ключ</b>.\n<b>3 Пункт.</b> Откройте скаченное приложение <b>Outline</b>.\n<b>4 Пункт.</b> Нажмите в середине «Добавить сервер».\n<b>5 Пункт.</b> Вставьте в открывшемся окне, ключ, который вы скопировали ранее (Обычно ключ уже бывает вставлен и вам просто нужно нажать «подключиться» ).\n<b>6 Пункт.</b>Нажмите подключиться, и VPN должен включится.  🧑‍💻\n\n⚠️ <b>Один ключ, одно устройство, иначе будут зависания</b> ⚠️\n"

    async def video_send(chat_id, video_path, caption): # Загрузка видео
        with open(video_path, "rb") as file:
            video_message =  await bot.send_video(chat_id, video=types.InputFile(file), caption=caption, parse_mode="HTML")
            return video_message.message_id
            
    async def h1_message():
        mess = await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИнструкция по установке <b>Outline</b> на <b>Iphone/Ipad</b> 🧑‍💻", parse_mode="HTML")
        return mess.message_id

    MessageState.message_one = await h1_message()
    MessageState.message_two = await video_send(id, video_path, text)

    await call.message.answer("Если у вас не получилось установить приложение и импортировать ключ, нажмите на кнопку <b>Обратиться за помощью с установкой</b> 🧑‍💻", reply_markup=message_help)

    if call.message:
        await call.message.delete()

#-------------------------------------------------------------------------

# Инструкция V2Ray
#-------------------------------------------------------------------------
@dp.callback_query_handler(text=["install_v2ray"])
async def instruction_v2ray(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    
    await call.message.edit_text("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nВыберете устройство, на которое нужно установить <b>V2Ray VPN:</b> 🧑‍💻", parse_mode="HTML")
    await call.message.edit_reply_markup(reply_markup=device_install_v2ray)
        
# Установка Андроид
@dp.callback_query_handler(text=["android_v2ray"], state="*")
async def instruction_android_v2ray(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")


    id = call.from_user.id # id пользователя
    video_path = Path("video", "android_v2ray.mp4")
    link = hlink('«Скачать приложение V2RayNG»', 'https://play.google.com/store/apps/details?id=com.v2ray.ang&hl=ru&gl=US')
    text = f"<b>1 Пункт.</b> {link}\n<b>2 Пункт.</b> Перейдите в боте «Главное меню» -> «Мои ключи», выберете протокол V2Ray и <b>скопируйте ключ</b>.\n<b>3 Пункт.</b> Откройте скаченное приложение <b>V2RayNG</b>.\n<b>4 Пункт.</b> Нажмите в правом верхнем углу «Плюс» , далее в открывшемся списке выбрать «Импорт профиля из буфера обмена».\n<b>5 Пункт.</b> Вправом нижнем углу нажать на круглую кнопку (В ней расположена буква V), и VPN должен будет включиться.\n🧑‍💻\n\n⚠️ <b>Один ключ, одно устройство, иначе будут зависания</b> ⚠️\n"

    async def video_send(chat_id, video_path, caption): # Загрузка видео
        with open(video_path, "rb") as file:
            video_message =  await bot.send_video(chat_id, video=types.InputFile(file), caption=caption, parse_mode="HTML")
            return video_message.message_id
            
    async def h1_message():
        mess = await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИнструкция по установке <b>V2Ray</b> на <b>Android</b> 🧑‍💻", parse_mode="HTML")
        return mess.message_id

    MessageState.message_one = await h1_message()
    MessageState.message_two = await video_send(id, video_path, text)

    await call.message.answer("Если у вас не получилось установить приложение и импортировать ключ, нажмите на кнопку <b>Обратиться за помощью с установкой</b> 🧑‍💻", reply_markup=message_help)

    if call.message:
        await call.message.delete()

# Установка Iphone/Ipad
@dp.callback_query_handler(text=["iphone_v2ray"], state="*")
async def instruction_iphone_v2ray(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    id = call.from_user.id # id пользователя
    video_path = Path("video", "iphone_v2ray.mp4")
    link = hlink('«Скачать приложение Streisand для V2Ray»', 'https://apps.apple.com/ru/app/streisand/id6450534064')
    text = f"<b>1 Пункт.</b> {link}\n<b>2 Пункт.</b> Перейдите в боте «Главное меню» -> «Мои ключи», выберете протокол V2Ray и <b>скопируйте ключ</b>.\n<b>3 Пункт.</b> Откройте скаченное приложение <b>Streisand</b>.\n<b>4 Пункт.</b> Нажмите в правом верхнем углу «Плюсик», делее «Добавить из буфера».\n<b>5 Пункт.</b> Нажмите на большую круглую синию кнопку и VPN должен будет включиться 🧑‍💻\n\n⚠️ <b>Один ключ, одно устройство, иначе будут зависания</b> ⚠️\n"

    async def video_send(chat_id, video_path, caption): # Загрузка видео
        with open(video_path, "rb") as file:
            video_message =  await bot.send_video(chat_id, video=types.InputFile(file), caption=caption, parse_mode="HTML")
            return video_message.message_id
            
    async def h1_message():
        mess = await call.message.answer("\n🌕🌖🌗🌘<b>ART VPN</b>🌒🌓🌔🌕\n\nИнструкция по установке <b>V2Ray</b> на <b>Iphone/Ipad</b> 🧑‍💻", parse_mode="HTML")
        return mess.message_id

    MessageState.message_one = await h1_message()
    MessageState.message_two = await video_send(id, video_path, text)

    await call.message.answer("Если у вас не получилось установить приложение и импортировать ключ, нажмите на кнопку <b>Обратиться за помощью с установкой</b> 🧑‍💻", reply_markup=message_help)

    if call.message:
        await call.message.delete()

#-------------------------------------------------------------------------