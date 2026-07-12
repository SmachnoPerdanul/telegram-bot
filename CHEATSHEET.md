# Справочник: команды и деплой

Часть 1 — команды по темам. Часть 2 — пошаговый деплой на сервер.

---

# ЧАСТЬ 1. Справочник команд

## Git — база

```bash
git status                      # ЧТО СЕЙЧАС ПРОИСХОДИТ. Первая команда, когда не понимаешь
git add имя_файла               # подготовить один файл к коммиту
git add -A                      # подготовить все изменения (включая удаления)
git commit -m "сообщение"       # зафиксировать в истории
git push                        # отправить на GitHub
git pull                        # забрать изменения с GitHub (нужно на сервере!)
git clone https://github.com/ЛОГИН/РЕПО.git   # склонировать репозиторий
```

Первичная настройка:
```bash
git config --global user.name "Имя"
git config --global user.email "почта@example.com"
git config --global core.autocrlf true     # чтобы не ругался на LF/CRLF (Windows)
```

Создание репозитория с нуля из локальной папки:
```bash
git init
git add -A
git commit -m "Первый коммит"
git branch -M main                                    # переименовать master -> main
git remote add origin https://github.com/ЛОГИН/РЕПО.git
git push -u origin main                               # первый пуш
```

## Git — история и откаты

```bash
git log                         # вся история (выход — клавиша q)
git log --oneline               # компактно: хеш + сообщение
```

**Отменить несохранённые изменения** (файл изменён, но не закоммичен):
```bash
git restore имя_файла           # откатить файл к последнему коммиту
git restore .                   # откатить все файлы
git restore --staged имя_файла  # убрать из подготовки (после git add)
```

**Отменить ЗАКОММИЧЕННОЕ** (с сохранением истории):
```bash
git revert <хэш>                            # отменить один коммит новым коммитом
git revert --no-commit <хэш>..HEAD          # отменить всё после указанного коммита
git commit -m "Откат к версии X"            # завершить откат одним коммитом
```

**Посмотреть старую версию** (не меняя ничего):
```bash
git checkout <хэш>              # переместиться в прошлое (detached HEAD — не пугаться)
git switch -                    # вернуться обратно
git checkout <хэш> -- bot.py    # достать один файл из старого коммита
git checkout <хэш> -- .         # достать ВСЕ файлы старой версии в текущую ветку
```

`restore` — для незакоммиченного (теряется навсегда). `revert` / `checkout` — для закоммиченного (ничего не теряется).
`reset --hard` — стирает историю.

## Python-окружение

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
deactivate
```

**Linux (сервер):**
```bash
python3 -m venv venv
source venv/bin/activate
deactivate
```

**Общее:**
```bash
pip install имя_пакета
pip install -r requirements.txt     # поставить всё из файла
pip freeze > requirements.txt       # записать зависимости в файл
pip show имя_пакета                 # версия и путь установки
```

ВАЖНО: всегда запускать с активным `(venv)` в начале строки. Иначе пакеты берутся из глобального Python и получаются ошибки.

## Качество кода

```bash
pip install black ruff
ruff check .            # найти проблемы (мусорные импорты и т.д.)
ruff check . --fix      # исправить, что можно, автоматически
black . --diff          # показать, что изменится (не меняя)
black .                 # отформатировать код
```
ВАЖНО: Форматирование коммитить отдельно от смысловых правок — иначе история нечитаемая.

## SSH и ключи

Сгенерировать ключ (на своём компьютере):
```cmd
ssh-keygen -t ed25519 -C "почта@example.com"
```

Посмотреть публичный ключ:
```cmd
type "%USERPROFILE%\.ssh\id_ed25519.pub"
```

- `id_ed25519.pub` — ПУБЛИЧНЫЙ.
- `id_ed25519` — ПРИВАТНЫЙ.

Подключение:
```bash
ssh root@IP_АДРЕС
ssh -v root@IP_АДРЕС        # подробный режим — если не пускает, смотреть сюда
exit                        # выйти с сервера
```

Добавить ключ на сервер вручную через VNC-консоль:
```bash
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys     # вставить публичный ключ, Ctrl+O, Enter, Ctrl+X
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

## Linux

```bash
ls                  # список файлов (аналог dir)
cd папка            # перейти в папку
cd ..               # на уровень выше
pwd                 # где я сейчас
cat файл            # показать содержимое файла
nano файл           # редактировать (Ctrl+O сохранить, Enter, Ctrl+X выйти)
rm файл             # удалить файл
passwd              # сменить пароль текущего пользователя
```

Пакеты системы:
```bash
apt update && apt upgrade -y                        # обновить систему
apt install -y python3 python3-venv python3-pip git # поставить нужное
```

Диагностика сети (проверить, доступен ли сайт с сервера):
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://api.telegram.org
```

## systemd

```bash
systemctl daemon-reload           # перечитать конфиги (после правки .service)
systemctl enable имя_службы       # включить автозапуск при загрузке сервера
systemctl start имя_службы        # запустить
systemctl stop имя_службы         # остановить
systemctl restart имя_службы      # перезапустить (после обновления кода!)
systemctl status имя_службы       # статус — ищем зелёное "active (running)"

journalctl -u имя_службы -f       # логи в реальном времени (Ctrl+C — выйти из просмотра)
journalctl -u имя_службы -n 50    # последние 50 строк логов
```

## Обновить бота на сервере (частая операция)

```bash
cd /root/telegram-bot
git pull
systemctl restart cryptobot
systemctl status cryptobot
```
Если менялись зависимости — между `git pull` и `restart`:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

# ЧАСТЬ 2. Деплой бота с нуля 

## Шаг 1. Подключиться

```bash
ssh root@IP_АДРЕС
```

Проверить, что Telegram доступен:
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://api.telegram.org
```

## Шаг 2. Подготовить систему

```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip git
```

## Шаг 3. Забрать код

```bash
cd /root
git clone https://github.com/SmachnoPerdanul/telegram-bot.git
cd telegram-bot
ls
```

## Шаг 4. Окружение и зависимости

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Шаг 5. Токен

`.env` 
```bash
nano .env
```
Вписать:
```
BOT_TOKEN=твой_токен
```
Сохранить: `Ctrl+O` → Enter → `Ctrl+X`. Проверить: `cat .env`

## Шаг 6. Проверить вручную

```bash
python bot.py
```
Написать боту в Telegram. Работает → `Ctrl+C` и дальше.

## Шаг 7. Сделать сервисом (systemd)

```bash
nano /etc/systemd/system/cryptobot.service
```

Содержимое:
```ini
[Unit]
Description=Telegram Crypto Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/telegram-bot
ExecStart=/root/telegram-bot/venv/bin/python /root/telegram-bot/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Ключевое:
- `WorkingDirectory` — чтобы бот нашёл `.env`
- `ExecStart` — python берётся ИЗ VENV, пути абсолютные
- `Restart=always` — сам перезапустится при падении
- `WantedBy=multi-user.target` — автостарт после перезагрузки сервера

## Шаг 8. Запустить

```bash
systemctl daemon-reload
systemctl enable cryptobot
systemctl start cryptobot
systemctl status cryptobot
```
Ищем зелёное `active (running)`.

## Шаг 9. Финальный тест

Закрыть SSH-терминал (`exit`) и написать боту в Telegram. Отвечает → **ДЕПЛОЙ ГОТОВ.**

---

# Ошибки возникшие в процессе работы

| Симптом | Причина | Лечение |
|---|---|---|
| `Missing dependencies for SOCKS support` | Включён VPN | Выключить VPN, или `pip install requests[socks]` |
| `Connection closed by ... port 22` (SSH) | Включён VPN | Выключить VPN |
| Пакет встал не туда, «мистические» ошибки | Забыл активировать venv | Проверять `(venv)` в начале строки |
| `not a git repository` | Ты не в папке репозитория | `cd` в папку проекта |
| `curl` к api.telegram.org зависает | Российский сервер | Нужен зарубежный VPS |
| В git попал мусор (`.idea`, `venv`) | Нет в `.gitignore` | Добавить, затем `git restore --staged` |
| Пароль в Linux «не вводится» | Символы не отображаются | Печатать вслепую, это нормально |
| `TypeError: list indices...` в клавиатуре | Забыта запятая между рядами кнопок | Проверить запятые |

# Что НИКОГДА не коммитить

- `.env` (токены, пароли, ключи)
- `venv/`
- `.idea/`, `.vscode/`
- `__pycache__/`, `*.pyc`
- архивы, бинарники, большие файлы

Базовый `.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
.idea/
```
