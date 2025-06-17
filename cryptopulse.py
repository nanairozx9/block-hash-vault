"""
CryptoPulse: Анализ всплесков активности Bitcoin-адреса.
"""

import requests
from datetime import datetime
import argparse
import statistics

def fetch_address_transactions(address):
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Ошибка при получении данных.")
    return response.json()["data"][address]["transactions"]

def fetch_tx_time(txid):
    url = f"https://api.blockchair.com/bitcoin/raw/transaction/{txid}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    try:
        time_stamp = r.json()["data"][txid]["decoded_raw_transaction"]["time"]
        return datetime.utcfromtimestamp(time_stamp)
    except:
        return None

def analyze_pulse(address):
    print(f"🔎 Анализ всплесков активности на адресе: {address}")
    tx_ids = fetch_address_transactions(address)
    timestamps = []

    for txid in tx_ids[:30]:  # последние 30 транзакций
        t = fetch_tx_time(txid)
        if t:
            timestamps.append(t)

    if len(timestamps) < 5:
        print("Недостаточно данных для анализа активности.")
        return

    timestamps.sort()
    intervals = [(timestamps[i] - timestamps[i-1]).total_seconds() / 3600 for i in range(1, len(timestamps))]

    avg_interval = round(statistics.mean(intervals), 2)
    stdev_interval = round(statistics.stdev(intervals), 2) if len(intervals) > 1 else 0

    print(f"⏱ Средний интервал между транзакциями: {avg_interval} ч")
    print(f"📈 Cтандартное отклонение: {stdev_interval} ч")

    if stdev_interval < avg_interval * 0.5:
        print("✅ Активность стабильна.")
    else:
        print("⚠️ Обнаружен всплеск или нестабильная активность — возможна аномалия.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CryptoPulse — анализирует резкие изменения активности Bitcoin-кошелька.")
    parser.add_argument("address", help="Bitcoin-адрес для анализа")
    args = parser.parse_args()
    analyze_pulse(args.address)
