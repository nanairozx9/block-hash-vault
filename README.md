# CryptoPulse

**CryptoPulse** — Python-утилита для анализа аномалий и всплесков в активности Bitcoin-адреса.

## Что делает

- Получает последние 30 транзакций кошелька
- Вычисляет интервалы между транзакциями
- Определяет резкие изменения или всплески активности
- Предупреждает о нестабильных транзакционных паттернах

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python cryptopulse.py <bitcoin_address>
```

Пример:

```bash
python cryptopulse.py 1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY
```

## Под капотом

- Используется Blockchair API
- Статистический анализ (среднее и стандартное отклонение интервалов)

## Лицензия

MIT License
