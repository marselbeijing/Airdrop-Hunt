# 🚀 Airdrop Hunter

**Automated crypto airdrop hunting with smart task execution**

[![GitHub](https://img.shields.io/badge/GitHub-Airdrop%20Hunter-blue)](https://github.com/marselbeijing/Airdrop-Hunt)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-red)](https://fastapi.tiangolo.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)](https://telegram.org)

## 📋 Overview

Airdrop Hunter is a comprehensive web application for automated cryptocurrency airdrop hunting. It features a modern mobile-first interface, Telegram bot integration, and smart task execution capabilities.

## ✨ Features

### 🔍 Smart Search
- **Auto parsing** from top sources
- **Real-time monitoring** of new airdrops
- **Multi-source integration** (Twitter, Telegram, etc.)

### 🤖 Auto Tasks
- **Automated task completion** without user input
- **Smart execution** of social media tasks
- **Progress tracking** and analytics

### 💰 Monetization
- **Premium features** for advanced users
- **$HUNT token rewards** system
- **Referral program** with bonuses

### 🏆 Ranking System
- **Leaderboard** with real-time updates
- **Rewards distribution** based on performance
- **Achievement system** with badges

### 🔐 Multi-Wallet Support
- **TON blockchain** integration
- **Ethereum** and ERC-20 tokens
- **Solana** and SPL tokens
- **PGP encryption** for security

### 🛡️ Security First
- **Telegram authentication** for secure login
- **PGP encryption** for sensitive data
- **Daily limits** for free users
- **Captcha protection** for critical actions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/marselbeijing/Airdrop-Hunt.git
cd Airdrop-Hunt
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp env_example.txt .env
# Edit .env with your API keys
```

5. **Initialize database**
```bash
python -c "from database import init_db; init_db()"
```

6. **Run the application**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

7. **Open in browser**
```
http://localhost:8080
```

## 🔧 Configuration

### Required API Keys

Create a `.env` file with the following variables:

```env
# Telegram Bot
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_user_id

# Twitter API
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# PGP Encryption
PGP_RECIPIENT_EMAIL=your_email@example.com
GPG_HOME_DIR=~/.gnupg
```

### Getting API Keys

#### Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create new bot with `/newbot`
3. Copy the token to `BOT_TOKEN`

#### Twitter API
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create new app
3. Generate API keys and tokens

## 📱 Features

### Web Interface
- **Mobile-first design** with responsive layout
- **Modern UI** with glassmorphism effects
- **Bottom navigation** for easy access
- **Real-time updates** and notifications

### Telegram Integration
- **Secure authentication** via Telegram Login Widget
- **Bot commands** for quick access
- **Push notifications** for new airdrops
- **Profile synchronization** across devices

### Database
- **SQLite** for local development
- **PostgreSQL** ready for production
- **User management** with PGP encryption
- **Airdrop tracking** and analytics

## 🏗️ Architecture

```
Airdrop Hunter/
├── main.py              # FastAPI application
├── bot.py               # Telegram bot logic
├── database.py          # Database models and operations
├── config.py            # Configuration management
├── airdrop_parser.py    # Airdrop parsing logic
├── task_executor.py     # Task execution engine
├── requirements.txt     # Python dependencies
├── static/             # Static files (CSS, JS, images)
└── templates/          # HTML templates
```

## 🔄 API Endpoints

### Web Interface
- `GET /` - Main application interface
- `GET /health` - Health check endpoint

### Airdrop Management
- `GET /api/airdrops` - Get all airdrops
- `POST /api/parse-airdrops` - Parse new airdrops
- `GET /api/search-airdrops` - Search airdrops
- `POST /api/execute-task/{airdrop_id}` - Execute airdrop task

## 🎯 Usage

### Web Application
1. Open `http://localhost:8080`
2. Navigate through sections using bottom navigation
3. Login with Telegram in Account section
4. Use Smart Search to find airdrops
5. Monitor your progress in Ranking section

### Telegram Bot
1. Start bot with `/start`
2. Use `/help` for available commands
3. `/search` to find airdrops
4. `/profile` to view your stats

## 🔒 Security

- **PGP encryption** for sensitive user data
- **Telegram authentication** for secure login
- **Rate limiting** to prevent abuse
- **Input validation** for all API endpoints
- **Environment variables** for sensitive configuration

## 🚀 Deployment

### Local Development
```bash
python -m uvicorn main:app --reload
```

### Production (Docker)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
Set all required environment variables in production:
```bash
export BOT_TOKEN=your_token
export TWITTER_API_KEY=your_key
# ... other variables
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Aiogram](https://aiogram.dev/) for Telegram bot functionality
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
- [Font Awesome](https://fontawesome.com/) for icons

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/marselbeijing/Airdrop-Hunt/issues)
- **Telegram**: [@marselbeijing](https://t.me/marselbeijing)
- **Email**: support@airdrop-hunter.com

---

**Made with ❤️ by the Airdrop Hunter Team** 