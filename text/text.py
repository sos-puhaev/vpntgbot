from pathlib import Path
from datetime import datetime, timedelta
import os
# --------------------------------------------------------
# ------- Обозначения элементов массива для пред чека ----

# Страна
def getCountry(country):
    str = ""
    if country == "russia":
        str = "🇷🇺 Россия"
        return str
    if country == "latvia":
        str = "🇱🇻 Латвия"
        return str
    if country == "turcia":
        str = "🇹🇷 Турция"
        return str
    if country == "georgia":
        str = "🇬🇪 Грузия"
        return str
    return str

# Страна для wireguard в связке
def getWgCountry(country):
    str = ""
    if country == "rf_latvia":
        return "🇷🇺 Россия -> 🇱🇻 Латвия"
    if country == "rf_georgia":
        return "🇷🇺 Россия -> 🇬🇪 Грузия"
    if country == "rf_turcia":
        return "🇷🇺 Россия -> 🇹🇷 Турция"
    return str

# Тариф для wireguard в связке
def getWgTariff(tariff):
    str = ""
    if tariff == "1_mounth_wg":
        return "1 Месяц"
    if tariff == "3_mounth_wg":
        return "3 Месяца"
    if tariff == "6_mounth_wg":
        return "6 Месяцев"
    if tariff == "12_mounth_wg":
        return "1 Год"
    return str

# Цена тарифов для wireguard в связке
def getWgPrice(price):
    str = ""
    if price == "1_mounth_wg":
        return "650"
    if price == "3_mounth_wg":
        return "1800"
    if price == "6_mounth_wg":
        return "3600"
    if price == "12_mounth_wg":
        return "7100"
    return str

# Тариф
def getTariff(tariff):
    str = ""
    if tariff == "1_mounth":
        return "1 Месяц"
    if tariff == "3_mounth":
        return "3 Месяца"
    if tariff == "6_mounth":
        return "6 Месяцев"
    if tariff == "12_mounth":
        return "1 Год"
    return str

# Цена тарифов
def getPrice(price):
    str = ""
    if price == "1_mounth":
        return "210"
    if price == "3_mounth":
        return "600"
    if price == "6_mounth":
        return "1200"
    if price == "12_mounth":
        return "2300"
    return str

# --------------------------------
# Протокол

def getProtocol(protocol):
    str = ""
    if protocol == "bundle":
        return "WireGuard в связке"
    if protocol == "wireguard":
        return "WireGuard"
    if protocol == "outline":
        return "Outline"
    if protocol == "v2ray":
        return "V2Ray(vless)"
    return str
#---------------------------------

# Вывод пред чека для пользователя 
def predCheck(check):
    country = getCountry(check['country'])
    mounth = getTariff(check['tariff'])
    price = getPrice(check['tariff'])
    protocol = getProtocol(check['protocol'])

    str = f"Если все верно, нажмите кнопку оплатить\n\nСтрана: <b>{country}</b>\nТариф: <b>{mounth}</b>\nТрафик: <b>Неограниченный</b>\nПротокол VPN: <b>{protocol}</b>\nПропускная способность: <b>до 400 мб/с</b>\nЦена: <b>{price} P.</b>"
    return str

# Вывод стоимости при оплате типа string-> int
def parseInt(price, protocol):
    if protocol == "bundle":
        if price == "1_mounth_wg":
            return 650
        if price == "3_mounth_wg":
            return 1800
        if price == "6_mounth_wg":
            return 3600
        if price == "12_mounth_wg":
            return 7100
    else:
        if price == "1_mounth":
            return 210
        if price == "3_mounth":
            return 600
        if price == "6_mounth":
            return 1200
        if price == "12_mounth":
            return 2300

# Проверка на существования файла и строк в ней outline
def search_file_line(name_file):
    dir = Path("vpn_keys", name_file)
    if dir.stat().st_size != 0:
        return 0
    return 1 # Строка отсутствует

# Проверка на существования файла и строк в ней v2ray
def v2ray_search_file_line(name_file):
    dir = Path("vpn_keys/v2ray", name_file)
    if dir.stat().st_size != 0:
        return 0
    return 1 # Строка отсутствует

# Проверка файла wireguard
def search_wg_file(country):
    if len(os.listdir(Path(f"vpn_keys/wireguard/{country}/"))):
        return 0
    return 1 # Ключей нету

# Показ пред чека для wireguard в связке
def predCheckWgBundle(check):
    country = getWgCountry(check['country'])
    mounth = getWgTariff(check['tariff'])
    price = getWgPrice(check['tariff'])
    protocol = getProtocol(check['protocol'])

    str = f"Если все верно, нажмите кнопку оплатить\n\nСтрана: <b>{country}</b>\nТариф: <b>{mounth}</b>\nТрафик: <b>Неограниченный</b>\nПротокол VPN: <b>{protocol}</b>\nПропускная способность: <b>до 400 мб/с</b>\nЦена: <b>{price} P.</b>"
    return str

# Проверка файла wireguard для связки
def search_bundle_wg_file(country):
    if country == "rf_latvia":
        country = "latvia"
    if country == "rf_georgia":
        country = "georgia"
    if country == "rf_turcia":
        country = "turcia"
    
    if len(os.listdir(Path(f"vpn_keys/wireguard-bundle/{country}/"))):
        return 0
    return 1 # Ключей нету

# Конвертация страны с перфиксом rf файла wireguard для связки
def convert_bundle_country(country):
    if country == "rf_latvia":
        return "latvia"
    if country == "rf_georgia":
        return "georgia"
    if country == "rf_turcia":
        return "turcia"
    
# Преобразование даты оканчания тарифа
def end_data(mounth):
    date_current = f"{datetime.now().date()}"
    date_arr = date_current.split("-")
    date_init = datetime(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))

    if mounth == "1_mounth_wg" or mounth == "1_mounth":
        date_new = date_init + timedelta(days=30)
        date_result = date_new.strftime("%Y-%m-%d")
        return date_result
    
    if mounth == "3_mounth_wg" or mounth == "3_mounth":
        date_new = date_init + timedelta(days=90)
        date_result = date_new.strftime("%Y-%m-%d")
        return date_result
    
    if mounth == "6_mounth_wg" or mounth == "6_mounth":
        date_new = date_init + timedelta(days=180)
        date_result = date_new.strftime("%Y-%m-%d")
        return date_result
    
    if mounth == "12_mounth_wg" or mounth == "12_mounth":
        date_new = date_init + timedelta(days=360)
        date_result = date_new.strftime("%Y-%m-%d")
        return date_result
    
# Конверт цены для баланса
def convert_price_balance(price):
    if price == "210_b":
        return 210
    if price == "600_b":
        return 600
    if price == "1200_b":
        return 1200
    if price == "2300_b":
        return 2300
    return 0