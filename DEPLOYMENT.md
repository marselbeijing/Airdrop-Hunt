# 🚀 Руководство по развертыванию Airdrop Hunter

## 📱 Варианты развертывания для Telegram

### **1. Только Telegram Bot (Рекомендуется)**

Самый простой способ - запустить только бота без веб-интерфейса:

```bash
# Запуск только бота
python bot_standalone.py
```

**Преимущества:**
- ✅ Простая настройка
- ✅ Работает на любом сервере
- ✅ Низкое потребление ресурсов
- ✅ Быстрый доступ через Telegram

### **2. Полное приложение на VPS**

Для полного функционала с веб-интерфейсом:

```bash
# Установка на Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Клонирование и настройка
git clone https://github.com/marselbeijing/Airdrop-Hunt.git
cd Airdrop-Hunt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка переменных окружения
cp env_example.txt .env
# Отредактируйте .env

# Запуск
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### **3. Docker развертывание**

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Сборка и запуск
docker build -t airdrop-hunter .
docker run -p 8000:8000 airdrop-hunter
```

### **4. Vercel (для веб-интерфейса)**

Если нужен только веб-интерфейс:

1. **Создайте `vercel.json`:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. **Установите Vercel CLI:**
```bash
npm i -g vercel
```

3. **Разверните:**
```bash
vercel
```

## 🔧 Настройка для Telegram

### **1. Создание бота**

1. Напишите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot`
3. Укажите имя и username бота
4. Скопируйте токен

### **2. Настройка переменных**

Создайте файл `.env`:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_user_id
```

### **3. Запуск бота**

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Запустите бота
python bot_standalone.py
```

## 🌐 Развертывание на сервере

### **1. VPS (DigitalOcean, AWS, etc.)**

```bash
# Подключение к серверу
ssh user@your-server-ip

# Установка зависимостей
sudo apt update
sudo apt install python3 python3-pip git nginx

# Клонирование проекта
git clone https://github.com/marselbeijing/Airdrop-Hunt.git
cd Airdrop-Hunt

# Настройка Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка переменных окружения
cp env_example.txt .env
nano .env  # Отредактируйте файл

# Запуск бота
python bot_standalone.py
```

### **2. Systemd сервис (для автозапуска)**

Создайте файл `/etc/systemd/system/airdrop-hunter.service`:

```ini
[Unit]
Description=Airdrop Hunter Telegram Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/Airdrop-Hunt
Environment=PATH=/path/to/Airdrop-Hunt/venv/bin
ExecStart=/path/to/Airdrop-Hunt/venv/bin/python bot_standalone.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:
```bash
sudo systemctl enable airdrop-hunter
sudo systemctl start airdrop-hunter
sudo systemctl status airdrop-hunter
```

### **3. Nginx (для веб-интерфейса)**

Создайте конфигурацию `/etc/nginx/sites-available/airdrop-hunter`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активируйте:
```bash
sudo ln -s /etc/nginx/sites-available/airdrop-hunter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 SSL сертификат (Let's Encrypt)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавьте: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Мониторинг

### **1. Логи**

```bash
# Просмотр логов systemd
sudo journalctl -u airdrop-hunter -f

# Просмотр логов nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **2. Мониторинг ресурсов**

```bash
# Установка htop
sudo apt install htop

# Мониторинг
htop
```

## 🚀 Рекомендуемая архитектура

### **Для начала (MVP):**
```
Telegram Bot (bot_standalone.py)
├── SQLite база данных
├── Базовые команды
└── Простая статистика
```

### **Для продакшена:**
```
Load Balancer (Nginx)
├── Telegram Bot (bot_standalone.py)
├── Web Interface (main.py)
├── PostgreSQL база данных
├── Redis кэш
└── Мониторинг (Prometheus + Grafana)
```

## 💰 Стоимость развертывания

### **Минимальная конфигурация:**
- **VPS**: $5-10/месяц (DigitalOcean, Vultr)
- **Домен**: $10-15/год
- **SSL**: Бесплатно (Let's Encrypt)

### **Рекомендуемая конфигурация:**
- **VPS**: $20-40/месяц (2-4 GB RAM)
- **База данных**: $15-30/месяц (PostgreSQL)
- **CDN**: $10-20/месяц (Cloudflare)

## 🔧 Troubleshooting

### **Проблемы с ботом:**
```bash
# Проверка токена
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe

# Проверка логинов
tail -f /var/log/airdrop-hunter.log
```

### **Проблемы с веб-интерфейсом:**
```bash
# Проверка портов
netstat -tlnp | grep :8000

# Проверка nginx
sudo nginx -t
sudo systemctl status nginx
```

## 📞 Поддержка

- **GitHub Issues**: [Сообщить об ошибках](https://github.com/marselbeijing/Airdrop-Hunt/issues)
- **Telegram**: [@marselbeijing](https://t.me/marselbeijing)
- **Email**: support@airdrop-hunter.com

---

**Выберите подходящий вариант развертывания в зависимости от ваших потребностей!** 🚀 