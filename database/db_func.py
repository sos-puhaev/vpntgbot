from database.db import supabase

# Проверка, существует ли пользователь
def is_select_user(user_id):
    result = supabase.table("tg_users").select("*").execute().data
    for item in result:
        if item['user_id'] == user_id:
            return 1
    return 0

# Запись нового пользователя
def add_new_user(user_id, first_name):
    supabase.table("tg_users").insert([{"user_id": user_id, "name": first_name, "keys": "", "balance": "200.0"}]).execute()

# Запрос на просмотр ключей Outline
def show_my_keys(user_id):
    result = supabase.table("tg_users").select("keys").eq("user_id", user_id).execute().data
    str = ""
    for item in result:
        str = item['keys']
        if not str or str is None:
            return 1
    return 0

# Запрос на просмотр ключей V2Ray ключей
def show_my_keys_v2ray(user_id):
    result = supabase.table("tg_users").select("vless").eq("user_id", user_id).execute().data
    str = ""
    for item in result:
        str = item['vless']
        if not str or str is None:
            return 1
    return 0

# Запрос на просмотр ключей WireGuard
def show_my_keys_wg(user_id):
    result = supabase.table("tg_users").select("wg_keys").eq("user_id", user_id).execute().data
    str = ""
    for item in result:
        str = item['wg_keys']
        if not str or str is None:
            return 1
    return 0

# Запрос на просмотр ключей WireGuard в связке
def show_my_keys_wg_bundle(user_id):
    result = supabase.table("tg_users").select("wg_bundle_keys").eq("user_id", user_id).execute().data
    str = ""
    for item in result:
        str = item['wg_bundle_keys']
        if not str or str is None:
            return 1
    return 0

# Запись нового ключа для Outline
def update_keys_outline(id, keys, country, end_data):
    result = supabase.table("tg_users").select("keys").eq("user_id", id).execute().data
    str = ""
    for item in result:
        str = item['keys']
        if not str or str is None:
            str = f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"keys": str}).eq("user_id",id).execute()
        else:
            str = f"{item['keys']}" + f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"keys": str}).eq("user_id",id).execute()

# Запись нового ключа для V2Ray
def update_keys_v2ray(id, keys, country, end_data):
    result = supabase.table("tg_users").select("vless").eq("user_id", id).execute().data
    str = ""
    for item in result:
        str = item['vless']
        if not str or str is None:
            str = f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"vless": str}).eq("user_id",id).execute()
        else:
            str = f"{item['vless']}" + f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"vless": str}).eq("user_id",id).execute()

# Запись нового ключа для WireGuard
def update_keys_wireguard(id, keys, country, end_data):
    result = supabase.table("tg_users").select("wg_keys").eq("user_id", id).execute().data
    str = ""
    for item in result:
        str = item['wg_keys']
        if not str or str is None:
            str = f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"wg_keys": str}).eq("user_id",id).execute()
        else:
            str = f"{item['wg_keys']}" + f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"wg_keys": str}).eq("user_id",id).execute()

# Запись нового ключа для WireGuard в связке
def update_keys_wireguard_bundle(id, keys, country, end_data):
    result = supabase.table("tg_users").select("wg_bundle_keys").eq("user_id", id).execute().data
    str = ""
    for item in result:
        str = item['wg_bundle_keys']
        if not str or str is None:
            str = f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"wg_bundle_keys": str}).eq("user_id",id).execute()
        else:
            str = f"{item['wg_bundle_keys']}" + f"{keys}|" + f"{country}|" + f"{end_data},"
            supabase.table("tg_users").update({"wg_bundle_keys": str}).eq("user_id",id).execute()

# Пополнение баланса
def update_balance(id, total_amount):
    result = supabase.table("tg_users").select("balance").eq("user_id", id).execute().data
    amount = ""
    for item in result:
        amount = item['balance']
        res_total = float(amount) + float(total_amount)
        supabase.table("tg_users").update({"balance": res_total}).eq("user_id",id).execute()

# Получить баланс
def show_balance(id):
    result = supabase.table("tg_users").select("balance").eq("user_id", id).execute().data
    amount = ""
    for item in result:
        amount = item['balance']
    return amount

# Изменения баланса в связи покупкой
def pay_update_balance(id, total_amount):
    supabase.table("tg_users").update({"balance": total_amount}).eq("user_id",id).execute()
    
    