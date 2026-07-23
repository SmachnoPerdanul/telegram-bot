# Крипто-бот

Telegram-бот для получения курсов криптовалют. Пользователь выбирает монету и валюту через inline-кнопки и получает актуальную цену. Можно вести личный список избранных монет и смотреть по нему сводку одной командой.

Данные — [CoinGecko API](https://www.coingecko.com/en/api). Бот развёрнут на VPS и работает 24/7.

## Скриншот

![Работа бота](screenshots/demo.png)

## Возможности

- Курс криптовалюты в USD или RUB, выбор через inline-кнопки
- Личный список избранных монет — у каждого пользователя свой
- Сводка по всем избранным монетам одной командой
- Обработка сетевых ошибок: при недоступности API бот сообщает об этом и продолжает работать
- Логирование ошибок запросов

## Команды

| Команда | Что делает |
|---|---|
| `/start` | Приветствие |
| `/help` | Справка по возможностям |
| `/price` | Выбор монеты и валюты, вывод курса |
| `/add <монета>` | Добавить монету в избранное, например `/add bitcoin` |
| `/remove <монета>` | Убрать монету из избранного |
| `/my` | Курсы всех избранных монет |

## Стек

- **Python 3.12**
- **aiogram 3** — Telegram Bot API, команды, inline-клавиатуры, `callback_query`
- **requests** — запросы к CoinGecko API с таймаутом и `raise_for_status`
- **SQLite** — хранение избранного, параметризованные запросы, ограничение `UNIQUE(user_id, coin)` от дублей
- **python-dotenv** — токен в `.env`, не в коде
- **black + ruff** — форматирование и линтинг

## Структура

```
bot.py         — хендлеры, клавиатуры, запрос к API
database.py    — работа с SQLite, вынесена отдельным модулем
requirements.txt
```

## Запуск локально

```bash
git clone https://github.com/agladcenko/crypto-rate-bot.git
cd crypto-rate-bot
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

Создать файл `.env` рядом с `bot.py`:

```
BOT_TOKEN=токен_от_BotFather
```

Запустить:

```bash
python bot.py
```

База данных `bot.db` создаётся автоматически при первом запуске.

## Развёртывание на сервере

Бот запущен на VPS как systemd-сервис: автозапуск при загрузке, `Restart=always` при падении, логи через `journalctl`.

Пример юнита `/etc/systemd/system/crypto-bot.service`:

```ini
[Unit]
Description=Crypto Rate Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/crypto-rate-bot
ExecStart=/home/botuser/crypto-rate-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now crypto-bot
sudo journalctl -u crypto-bot -f
```
