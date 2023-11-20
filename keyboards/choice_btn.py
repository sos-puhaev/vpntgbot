from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback_btn import buy_callback

#----------------------------------
# Главня
choice = InlineKeyboardMarkup(row_width=1)
keyboard = [
    InlineKeyboardButton(text = "🔑 Мои ключи 📜", callback_data="my_keys"),
    InlineKeyboardButton(text = "📃 Тарифы 📄", callback_data="tariff"),
    InlineKeyboardButton(text = "💰 Мой баланс 💳", callback_data="balance"),
    InlineKeyboardButton(text = "📲 Помощь в установке 💻", callback_data="install_key"),
    InlineKeyboardButton(text = "🙋 Тех поддержка 🧑‍💻", url = "tg://user?id=514988328"),
]

choice.insert(keyboard[0])
choice.insert(keyboard[1])
choice.insert(keyboard[2])
choice.insert(keyboard[3])
choice.insert(keyboard[4])
#----------------------------------

# Выбор протокола
protocol = InlineKeyboardMarkup(row_width=1)
protocol_keyboard = [
    InlineKeyboardButton(text = "🟢 V2Ray", callback_data="v2ray"),
    InlineKeyboardButton(text = "🟡 Outline", callback_data="outline"),
    InlineKeyboardButton(text = "🔴 WireGuard", callback_data="wireguard_service"),
    InlineKeyboardButton(text = "⬅️ Назад", callback_data="back_menu"),
]

protocol.insert(protocol_keyboard[0])
protocol.insert(protocol_keyboard[1])
protocol.insert(protocol_keyboard[2])
protocol.insert(protocol_keyboard[3])

#----------------------------------

# Cтраны
countri = InlineKeyboardMarkup(row_width=1)
countri_keyboard = [
    # InlineKeyboardButton(text = "🇷🇺 Россия", callback_data="russia"),
    InlineKeyboardButton(text = "🇱🇻 Латвия", callback_data="latvia"),
    InlineKeyboardButton(text = "🇹🇷 Турция", callback_data="turcia"),
    InlineKeyboardButton(text = "🇬🇪 Грузия", callback_data="georgia"),
    InlineKeyboardButton(text = "⬅️ Назад", callback_data="back_protocol"),
]

countri.insert(countri_keyboard[0])
countri.insert(countri_keyboard[1])
countri.insert(countri_keyboard[2])
countri.insert(countri_keyboard[3])
# countri.insert(countri_keyboard[4])
#----------------------------------

# Цена 
price = InlineKeyboardMarkup(row_width=1)
price_keyboard = [
    InlineKeyboardButton(text = "1 месяц    💰 210 P", callback_data="1_mounth"),
    InlineKeyboardButton(text = "3 месяца   💰 600 P", callback_data="3_mounth"),
    InlineKeyboardButton(text = "6 месяцев  💰 1200 P", callback_data="6_mounth"),
    InlineKeyboardButton(text = "12 месяцев 💰 2300 P", callback_data="12_mounth"),
    InlineKeyboardButton(text = "⬅️ Назад", callback_data="back_country"),
]

price.insert(price_keyboard[0])
price.insert(price_keyboard[1])
price.insert(price_keyboard[2])
price.insert(price_keyboard[3])
price.insert(price_keyboard[4])
#----------------------------------

# Мои ключи Outline
keys = InlineKeyboardMarkup(row_width=1)
keys_keyboard = [
    InlineKeyboardButton(text="Взять +1 ключ", callback_data="tariff"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="my_keys")
]
keys.insert(keys_keyboard[0])
keys.insert(keys_keyboard[1])
#---------------------------------

# Отсутствие ключей
not_keys = InlineKeyboardMarkup(row_width=1)
not_keys_keyboard = [
    InlineKeyboardButton(text="Приобрести ключ", callback_data="tariff"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="my_keys")
]
not_keys.insert(not_keys_keyboard[0])
not_keys.insert(not_keys_keyboard[1])
#---------------------------------

# Страница оплаты
pay = InlineKeyboardMarkup(row_width=1)
pay_keyboard = [
    InlineKeyboardButton(text="Оплатить банковской картой 💳", callback_data="pay"),
    InlineKeyboardButton(text="Оплатить со счета на балансе 💰", callback_data="pay_balance"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="back_price")
]
pay.insert(pay_keyboard[0])
pay.insert(pay_keyboard[1])
pay.insert(pay_keyboard[2])
#---------------------------------

# Кнопка назад, из за отсутствия ключей
null_line = InlineKeyboardMarkup(row_width=1)
null_line_keyboard = [
    InlineKeyboardButton(text="⬅️ Назад к выбору страны", callback_data="back_country")
]
null_line.insert(null_line_keyboard[0])

#----------------------------------

# WireGuard развилка на один сервер или сервер в связке
wg_btn = InlineKeyboardMarkup(row_width=1)
wg_keyboard_service = [
    InlineKeyboardButton(text="Одна страна WireGuard", callback_data="wireguard"),
    InlineKeyboardButton(text="Связка из двух стран WireGuard", callback_data="bundle"),
    InlineKeyboardButton(text="⬅️ Назад к выбору протокола", callback_data="back_protocol")
]
wg_btn.insert(wg_keyboard_service[0])
wg_btn.insert(wg_keyboard_service[1])
wg_btn.insert(wg_keyboard_service[2])
#---------------------------------- 

# WireGuard в связке
wg_bundle = InlineKeyboardMarkup(row_width=1)
wg_bundle_keyboard = [
    InlineKeyboardButton(text="🇷🇺 Россия -> 🇱🇻 Латвия", callback_data="rf_latvia"),
    InlineKeyboardButton(text="🇷🇺 Россия -> 🇬🇪 Грузия", callback_data="rf_georgia"),
    InlineKeyboardButton(text="🇷🇺 Россия -> 🇹🇷 Турция", callback_data="rf_turcia"),
    InlineKeyboardButton(text="⬅️ Назад к выбору WireGuard", callback_data="wireguard_service")
]
wg_bundle.insert(wg_bundle_keyboard[0])
wg_bundle.insert(wg_bundle_keyboard[1])
wg_bundle.insert(wg_bundle_keyboard[2])
wg_bundle.insert(wg_bundle_keyboard[3])
#------------------------------------

# WireGuard в связке, тарифы(Цены)
wg_price = InlineKeyboardMarkup(row_width=1)
wg_price_keyboard = [
    InlineKeyboardButton(text = "1 месяц    💰 650 P", callback_data="1_mounth_wg"),
    InlineKeyboardButton(text = "3 месяца   💰 1800 P", callback_data="3_mounth_wg"),
    InlineKeyboardButton(text = "6 месяцев  💰 3600 P", callback_data="6_mounth_wg"),
    InlineKeyboardButton(text = "12 месяцев 💰 7100 P", callback_data="12_mounth_wg"),
    InlineKeyboardButton(text = "⬅️ Назад", callback_data="back_country_bundle"),
]

wg_price.insert(wg_price_keyboard[0])
wg_price.insert(wg_price_keyboard[1])
wg_price.insert(wg_price_keyboard[2])
wg_price.insert(wg_price_keyboard[3])
wg_price.insert(wg_price_keyboard[4])
#------------------------------------

# Кнопка назад, из за отсутствия ключей wireguard в связке
null_file_wg_bundle = InlineKeyboardMarkup(row_width=1)
null_file_wg_bundle_keyboard = [
    InlineKeyboardButton(text="⬅️ Назад к выбору страны", callback_data="null_file_back_country")
]
null_file_wg_bundle.insert(null_file_wg_bundle_keyboard[0])

#----------------------------------

# Страница оплаты для wireguard в связке
pay_wg = InlineKeyboardMarkup(row_width=1)
pay_wg_keyboard = [
    InlineKeyboardButton(text="Оплатить банковской картой 💳", callback_data="pay"),
    InlineKeyboardButton(text="Оплатить со счета на балансе 💰", callback_data="pay_balance"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="back_price_wg")
]
pay_wg.insert(pay_wg_keyboard[0])
pay_wg.insert(pay_wg_keyboard[1])
pay_wg.insert(pay_wg_keyboard[2])
#---------------------------------

# Мои ключи
my_keys = InlineKeyboardMarkup(row_width=1)
my_keys_keyboard = [
    InlineKeyboardButton(text="📦 Мои «V2Ray(vless)» ключи", callback_data="my_v2ray_keys"),
    InlineKeyboardButton(text="📦 Мои «Outline» ключи", callback_data="my_outline_keys"),
    InlineKeyboardButton(text="📦 Мои «WireGuard» ключи", callback_data="my_wireguard_keys"),
    InlineKeyboardButton(text="📦 Мои «WireGuard в связке» ключи", callback_data="my_bundle_wireguard_keys"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="back_menu")
]
my_keys.insert(my_keys_keyboard[0])
my_keys.insert(my_keys_keyboard[1])
my_keys.insert(my_keys_keyboard[2])
my_keys.insert(my_keys_keyboard[3])
my_keys.insert(my_keys_keyboard[4])
#--------------------------------

# Мой баланс
my_balance = InlineKeyboardMarkup(row_width=1)
my_balance_keyboard = [
    InlineKeyboardButton(text="Пополнить баланс", callback_data="set_balance"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="back_menu")
]
my_balance.insert(my_balance_keyboard[0])
my_balance.insert(my_balance_keyboard[1])
#--------------------------------

# На какую сумму пополнить баланс
set_summ = InlineKeyboardMarkup(row_width=4)
set_summ_keyboard = [
    InlineKeyboardButton(text="210 P", callback_data="210_b"),
    InlineKeyboardButton(text="600 P", callback_data="600_b"),
    InlineKeyboardButton(text="1 200 P", callback_data="1200_b"),
    InlineKeyboardButton(text="2 300 P", callback_data="2300_b"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="balance")
]
set_summ.insert(set_summ_keyboard[0])
set_summ.insert(set_summ_keyboard[1])
set_summ.insert(set_summ_keyboard[2])
set_summ.insert(set_summ_keyboard[3])
set_summ.insert(set_summ_keyboard[4])
#--------------------------------

# В случае отсутсвия средств на балансе
back_balance = InlineKeyboardMarkup(row_width=1)
back_balance_keyboard = [
    InlineKeyboardButton(text="Пополнить баланс", callback_data="set_balance"),
    InlineKeyboardButton(text="⬅️ Назад к выбору оплат", callback_data="back_predcheck")
]
back_balance.insert(back_balance_keyboard[0])
back_balance.insert(back_balance_keyboard[1])

# После оплаты WireGuard
after_pay = InlineKeyboardMarkup(row_width=1)
after_pay_keyboard = [
    InlineKeyboardButton(text="Помощь с установкой ключа 🧑‍💻", callback_data="install_key"),
    InlineKeyboardButton(text="Главное меню", callback_data="back_menu")
]
after_pay.insert(after_pay_keyboard[0])
after_pay.insert(after_pay_keyboard[1])

# Вернутся в главное меню, после пополнения баланса
back_second_menu = InlineKeyboardMarkup(row_width=1)
back_second_menu_keyboard = [
    InlineKeyboardButton(text="🏛 Вернутся в главное меню 🏛", callback_data="back_menu"),
]
back_second_menu.insert(back_second_menu_keyboard[0])

# Список протоколов для инструкции
list_protocol = InlineKeyboardMarkup(row_width=1)
list_protocol_keyboard = [
    InlineKeyboardButton(text="V2Ray", callback_data="install_v2ray"),
    InlineKeyboardButton(text="WireGuard и WireGuard в связке", callback_data="install_wireguard"),
    InlineKeyboardButton(text="Outline", callback_data="install_outline"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="back_menu")
]
list_protocol.insert(list_protocol_keyboard[0])
list_protocol.insert(list_protocol_keyboard[1])
list_protocol.insert(list_protocol_keyboard[2])
list_protocol.insert(list_protocol_keyboard[3])

# Выбор устройства WireGuard
device_install = InlineKeyboardMarkup(row_width=1)
device_install_keyboard = [
    InlineKeyboardButton(text="📱 Android", callback_data="android"),
    InlineKeyboardButton(text="📱 Iphone/Ipad", callback_data="iphone"),
    InlineKeyboardButton(text="💻 Mac", callback_data="mac"),
    InlineKeyboardButton(text="🖥 Windows", callback_data="windows"),
    InlineKeyboardButton(text="🐧 Linux/Ubuntu", callback_data="linux"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="install_key")
]
device_install.insert(device_install_keyboard[0])
device_install.insert(device_install_keyboard[1])
device_install.insert(device_install_keyboard[2])
device_install.insert(device_install_keyboard[3])
device_install.insert(device_install_keyboard[4])
device_install.insert(device_install_keyboard[5])

# Выбор устройства Outline
device_install_outline = InlineKeyboardMarkup(row_width=1)
device_install_outline_keyboard = [
    InlineKeyboardButton(text="📱 Android", callback_data="android_outline"),
    InlineKeyboardButton(text="📱 Iphone/Ipad", callback_data="iphone_outline"),
    InlineKeyboardButton(text="💻 Mac", callback_data="mac_outline"),
    InlineKeyboardButton(text="🖥 Windows", callback_data="windows_outline"),
    InlineKeyboardButton(text="🐧 Linux/Ubuntu", callback_data="linux_outline"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="install_key")
]
device_install_outline.insert(device_install_outline_keyboard[0])
device_install_outline.insert(device_install_outline_keyboard[1])
device_install_outline.insert(device_install_outline_keyboard[2])
device_install_outline.insert(device_install_outline_keyboard[3])
device_install_outline.insert(device_install_outline_keyboard[4])
device_install_outline.insert(device_install_outline_keyboard[5])

# Выбор устройства V2Ray
device_install_v2ray = InlineKeyboardMarkup(row_width=1)
device_install_v2ray_keyboard = [
    InlineKeyboardButton(text="📱 Android", callback_data="android_v2ray"),
    InlineKeyboardButton(text="📱 Iphone/Ipad", callback_data="iphone_v2ray"),
    InlineKeyboardButton(text="💻 Mac", callback_data="mac_v2ray"),
    InlineKeyboardButton(text="🖥 Windows", callback_data="windows_v2ray"),
    InlineKeyboardButton(text="🐧 Linux/Ubuntu", callback_data="linux_v2ray"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="install_key")
]
device_install_v2ray.insert(device_install_v2ray_keyboard[0])
device_install_v2ray.insert(device_install_v2ray_keyboard[1])
device_install_v2ray.insert(device_install_v2ray_keyboard[2])
device_install_v2ray.insert(device_install_v2ray_keyboard[3])
device_install_v2ray.insert(device_install_v2ray_keyboard[4])
device_install_v2ray.insert(device_install_v2ray_keyboard[5])

# Написать в тех поддержку 
message_help = InlineKeyboardMarkup(row_width=1)
message_help_keyboard = [
    InlineKeyboardButton(text="Обратиться за помощью c установкой 🧑‍💻", url = "tg://user?id=514988328"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="install_key")
]
message_help.insert(message_help_keyboard[0])
message_help.insert(message_help_keyboard[1])
