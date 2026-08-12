import requests
import json
import sys

# Публичный API TON Center (для учебных и OSINT исследований)
TON_API_URL = "https://toncenter.com/api/v2/"

def get_wallet_info(address: str):
    """
    Получает базовую информацию о TON-кошельке (баланс, статус).
    """
    url = f"{TON_API_URL}getAddressInformation"
    params = {"address": address}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("ok"):
            result = data["result"]
            # Переводим нано-TON в обычные TON (1 TON = 1,000,000,000 nanoTON)
            balance_nano = int(result.get("balance", 0))
            balance_ton = balance_nano / 1e9
            
            print(f"[+] Адрес: {address}")
            print(f"[+] Баланс: {balance_ton:.4f} TON")
            print(f"[+] Статус аккаунта: {result.get('state', 'Unknown')}")
        else:
            print(f"[-] Ошибка API: {data.get('error', 'Неизвестная ошибка')}")
            
    except Exception as e:
        print(f"[-] Ошибка подключения: {e}")

def get_recent_transactions(address: str, limit: int = 5):
    """
    Получает список последних транзакций кошелька.
    """
    url = f"{TON_API_URL}getTransactions"
    params = {"address": address, "limit": limit}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("ok"):
            transactions = data["result"]
            print(f"\n[+] Последние {len(transactions)} транзакций:")
            
            for tx in transactions:
                tx_hash = tx.get("transaction_id", {}).get("hash", "N/A")
                in_msg = tx.get("in_msg", {})
                value_nano = int(in_msg.get("value", 0))
                value_ton = value_nano / 1e9
                sender = in_msg.get("source", "System/Contract")
                
                print(f"  ----------------------------------------")
                print(f"  * Tx Hash: {tx_hash[:16]}...")
                print(f"  * Отправитель: {sender}")
                print(f"  * Сумма: {value_ton:.4f} TON")
        else:
            print(f"[-] Не удалось получить транзакции")
            
    except Exception as e:
        print(f"[-] Ошибка при запросе транзакций: {e}")

if __name__ == "__main__":
    print("=== TON Blockchain OSINT Passive Inspector ===\n")
    
    # Можно передать адрес аргументом или ввести с клавиатуры
    if len(sys.argv) > 1:
        target_address = sys.argv[1]
    else:
        target_address = input("Введите TON-адрес кошелька для проверки: ").strip()
        
    if target_address:
        get_wallet_info(target_address)
        get_recent_transactions(target_address)
    else:
        print("[-] Адрес не введен. Завершение работы.")
