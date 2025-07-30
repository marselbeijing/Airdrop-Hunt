from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import init_db # Импортируем функцию для инициализации БД
import os

app = FastAPI()

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создаем директорию для статических файлов
os.makedirs("static", exist_ok=True)

# HTML шаблон для главной страницы
MAIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Hunter - Crypto Hunter</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #8b5cf6;
            --accent: #06b6d4;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #0f172a;
            --dark-light: #1e293b;
            --gray: #64748b;
            --gray-light: #94a3b8;
            --white: #ffffff;
            --glass: rgba(255, 255, 255, 0.1);
            --glass-dark: rgba(0, 0, 0, 0.2);
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            min-height: 100vh;
            color: var(--white);
            overflow-x: hidden;
            padding: 20px;
        }
        
        .container {
            max-width: 400px;
            width: 100%;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-dark);
            border-radius: 24px;
            padding: 30px 25px 100px 25px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            min-height: 100vh;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
        }
        
        /* Header */
        .header {
            text-align: center;
            padding: 20px 0 30px;
            position: relative;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 120px;
            height: 120px;
            background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
            opacity: 0.2;
            filter: blur(30px);
            z-index: -1;
        }
        
        .logo {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        
        .logo i {
            font-size: 0.8em;
            animation: rocket 2s ease-in-out infinite;
        }
        
        @keyframes rocket {
            0%, 100% { transform: translateY(0) rotate(-45deg); }
            50% { transform: translateY(-8px) rotate(-45deg); }
        }
        
        .subtitle {
            font-size: 0.95rem;
            color: var(--gray-light);
            margin-bottom: 25px;
            font-weight: 400;
            line-height: 1.4;
        }
        
        /* Status Badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
            color: var(--white);
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 25px 0;
        }
        
        .stat-card {
            background: var(--glass-dark);
            border: 1px solid var(--glass-dark);
            border-radius: 12px;
            padding: 16px 12px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            border-color: var(--primary);
        }
        
        .stat-icon {
            font-size: 1.5rem;
            color: var(--primary);
            margin-bottom: 8px;
        }
        
        .stat-title {
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 4px;
        }
        
        .stat-desc {
            font-size: 0.75rem;
            color: var(--gray-light);
            line-height: 1.3;
        }
        
        /* Features Grid */
        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 25px 0;
        }
        
        .feature-card {
            background: var(--glass-dark);
            border: 1px solid var(--glass-dark);
            border-radius: 12px;
            padding: 16px 12px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            border-color: var(--secondary);
        }
        
        .feature-icon {
            font-size: 1.5rem;
            color: var(--secondary);
            margin-bottom: 8px;
        }
        
        .feature-title {
            font-weight: 600;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }
        
        .feature-desc {
            font-size: 0.7rem;
            color: var(--gray-light);
            line-height: 1.3;
        }
        
        /* API Section */
        .api-section {
            background: var(--glass-dark);
            border: 1px solid var(--glass-dark);
            border-radius: 12px;
            padding: 20px;
            margin: 25px 0;
        }
        
        .api-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 15px;
            color: var(--accent);
        }
        
        .endpoint-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .endpoint {
            background: var(--glass);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-family: 'Monaco', 'Menlo', monospace;
            color: var(--gray-light);
        }
        
        /* Button Groups */
        .btn-group {
            display: flex;
            gap: 12px;
            margin: 25px 0;
        }
        
        .btn {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 12px 20px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            border: none;
            cursor: pointer;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: var(--white);
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        }
        
        .btn-secondary {
            background: var(--glass);
            color: var(--white);
            border: 1px solid var(--glass-dark);
            backdrop-filter: blur(10px);
        }
        
        .btn-secondary:hover {
            background: var(--glass-dark);
            transform: translateY(-1px);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px 0 0;
            color: var(--gray-light);
            font-size: 0.75rem;
        }
        
        /* Bottom Navigation */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 400px;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border-top: 1px solid var(--glass-dark);
            border-radius: 20px 20px 0 0;
            padding: 12px 20px 25px;
            z-index: 1000;
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: 8px 12px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: var(--gray-light);
            text-decoration: none;
            min-width: 60px;
        }

        .nav-item.active {
            color: var(--primary);
            background: var(--glass-dark);
        }

        .nav-item:hover {
            color: var(--white);
            transform: translateY(-2px);
        }

        .nav-icon {
            font-size: 1.2rem;
            margin-bottom: 2px;
        }

        .nav-label {
            font-size: 0.7rem;
            font-weight: 500;
            text-align: center;
            line-height: 1;
        }

        /* Content Sections */
        .content-section {
            display: none;
        }

        .content-section.active {
            display: block;
        }

        #home-content {
            display: block;
        }
        
        /* Mobile Responsive */
        @media (max-width: 480px) {
            body {
                padding: 15px;
            }
            
            .container {
                max-width: 100%;
                padding: 25px 20px 100px 20px;
            }
            
            .logo {
                font-size: 1.8rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
                gap: 10px;
            }
            
            .btn-group {
                flex-direction: column;
                gap: 8px;
            }
            
            .btn {
                width: 100%;
            }
        }
        
        /* Dark mode enhancements */
        @media (prefers-color-scheme: dark) {
            body {
                background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #16213e 100%);
            }
        }
        
        /* Loading animation */
        .loading {
            opacity: 0;
            animation: fadeIn 0.8s ease-out forwards;
        }
        
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        
        /* Scroll animations */
        .scroll-animate {
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.6s ease;
        }
        
        .scroll-animate.visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
        }

        .modal-content {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-dark);
            border-radius: 20px;
            margin: 5% auto;
            padding: 30px;
            width: 90%;
            max-width: 400px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        }

        .close {
            position: absolute;
            right: 20px;
            top: 20px;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--gray-light);
            transition: color 0.3s ease;
        }

        .close:hover {
            color: var(--white);
        }

        .modal-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--white);
        }

        .airdrop-item {
            background: var(--glass-dark);
            border: 1px solid var(--glass-dark);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            transition: all 0.3s ease;
        }

        .airdrop-item:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }

        .airdrop-title {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 8px;
            color: var(--white);
        }

        .airdrop-desc {
            font-size: 0.85rem;
            color: var(--gray-light);
            margin-bottom: 12px;
            line-height: 1.4;
        }

        .airdrop-meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .airdrop-badge {
            background: var(--glass);
            color: var(--gray-light);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .airdrop-badge.ton { color: #0088cc; }
        .airdrop-badge.ethereum { color: #627eea; }
        .airdrop-badge.solana { color: #9945ff; }
        .airdrop-badge.easy { color: var(--success); }
        .airdrop-badge.medium { color: var(--warning); }
        .airdrop-badge.hard { color: var(--danger); }
    </style>
</head>
<body>
    <div class="container">
        <!-- Home Content -->
        <div id="home-content" class="content-section">
            <!-- Header -->
            <div class="header loading">
                <div class="logo">
                    <i class="fas fa-rocket"></i>
                    Airdrop Hunter
                </div>
                <p class="subtitle">Automated crypto airdrop hunting with smart task execution</p>
                <div class="status-badge">
                    <i class="fas fa-check-circle"></i>
                    Bot Online
                </div>
            </div>
            
            <!-- Stats Grid -->
            <div class="stats-grid scroll-animate">
                <div class="stat-card" onclick="parseAirdrops()" style="cursor: pointer;">
                    <div class="stat-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <div class="stat-title">Smart Search</div>
                    <div class="stat-desc">Auto parsing from top sources</div>
                </div>
                
                <div class="stat-card" onclick="getAirdrops()" style="cursor: pointer;">
                    <div class="stat-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="stat-title">Auto Tasks</div>
                    <div class="stat-desc">Complete without user input</div>
                </div>
                
                <div class="stat-card" onclick="showMonetization()" style="cursor: pointer;">
                    <div class="stat-icon">
                        <i class="fas fa-coins"></i>
                    </div>
                    <div class="stat-title">Monetization</div>
                    <div class="stat-desc">Premium & $HUNT token</div>
                </div>
                
                <div class="stat-card" onclick="showRanking()" style="cursor: pointer;">
                    <div class="stat-icon">
                        <i class="fas fa-trophy"></i>
                    </div>
                    <div class="stat-title">Ranking</div>
                    <div class="stat-desc">Leaderboard & rewards</div>
                </div>
            </div>
            
            <!-- Features Grid -->
            <div class="features-grid scroll-animate">
                <div class="feature-card" onclick="showWalletSupport()" style="cursor: pointer;">
                    <div class="feature-icon">
                        <i class="fas fa-wallet"></i>
                    </div>
                    <div class="feature-title">Multi-Wallet Support</div>
                    <div class="feature-desc">TON, Ethereum, Solana with PGP encryption</div>
                </div>
                
                <div class="feature-card" onclick="showSecurity()" style="cursor: pointer;">
                    <div class="feature-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <div class="feature-title">Security First</div>
                    <div class="feature-desc">PGP encryption, captcha, and usage limits</div>
                </div>
                
                <div class="feature-card" onclick="showAnalytics()" style="cursor: pointer;">
                    <div class="feature-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="feature-title">Analytics</div>
                    <div class="feature-desc">Detailed stats and progress tracking</div>
                </div>
                
                <div class="feature-card" onclick="showCommunity()" style="cursor: pointer;">
                    <div class="feature-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="feature-title">Community</div>
                    <div class="feature-desc">Referral system and exclusive airdrops</div>
                </div>
            </div>
            
            <!-- API Section -->
            <div class="api-section scroll-animate">
                <div class="api-title">
                    <i class="fas fa-code"></i>
                    API Endpoints
                </div>
                <div class="endpoint-list">
                    <div class="endpoint">GET / - Main page</div>
                    <div class="endpoint">GET /health - Health check</div>
                    <div class="endpoint">POST /api/airdrops - Get airdrops</div>
                    <div class="endpoint">POST /api/execute - Execute task</div>
                </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="btn-group scroll-animate">
                <a href="/health" class="btn btn-primary" target="_blank">
                    <i class="fas fa-heartbeat"></i>
                    Check API
                </a>
                <a href="#" class="btn btn-secondary" onclick="alert('Telegram bot integration coming soon!')">
                    <i class="fab fa-telegram"></i>
                    Telegram Bot
                </a>
            </div>
            
            <!-- Footer -->
            <div class="footer scroll-animate">
                <p>&copy; 2024 Airdrop Hunter. All rights reserved.</p>
            </div>
        </div>

        <!-- Wallet Content -->
        <div id="wallet-content" class="content-section">
            <div class="header">
                <div class="logo">
                    <i class="fas fa-wallet"></i>
                    Multi-Wallet Support
                </div>
                <p class="subtitle">Secure wallet management with PGP encryption</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fab fa-telegram"></i>
                    </div>
                    <div class="feature-title">TON Wallet</div>
                    <div class="feature-desc">TON blockchain integration</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fab fa-ethereum"></i>
                    </div>
                    <div class="feature-title">Ethereum Wallet</div>
                    <div class="feature-desc">ETH and ERC-20 tokens</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-coins"></i>
                    </div>
                    <div class="feature-title">Solana Wallet</div>
                    <div class="feature-desc">SOL and SPL tokens</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-lock"></i>
                    </div>
                    <div class="feature-title">PGP Encryption</div>
                    <div class="feature-desc">Military-grade security</div>
                </div>
            </div>
        </div>

        <!-- Ranking Content -->
        <div id="ranking-content" class="content-section">
            <div class="header">
                <div class="logo">
                    <i class="fas fa-trophy"></i>
                    Leaderboard & Rewards
                </div>
                <p class="subtitle">Compete with other hunters and earn rewards</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-medal"></i>
                    </div>
                    <div class="stat-title">Your Rank</div>
                    <div class="stat-desc">#42 of 1,247</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-coins"></i>
                    </div>
                    <div class="stat-title">Total Rewards</div>
                    <div class="stat-desc">$2,847 earned</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-fire"></i>
                    </div>
                    <div class="stat-title">Streak</div>
                    <div class="stat-desc">15 days active</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-star"></i>
                    </div>
                    <div class="stat-title">Level</div>
                    <div class="stat-desc">Gold Hunter</div>
                </div>
            </div>
        </div>

        <!-- Account Content -->
        <div id="account-content" class="content-section">
            <div class="header">
                <div class="logo">
                    <i class="fas fa-user"></i>
                    Account
                </div>
                <p class="subtitle">Manage your profile and settings</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-user-circle"></i>
                    </div>
                    <div class="feature-title">Profile</div>
                    <div class="feature-desc">Edit personal information</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-cog"></i>
                    </div>
                    <div class="feature-title">Settings</div>
                    <div class="feature-desc">Preferences and notifications</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-history"></i>
                    </div>
                    <div class="feature-title">History</div>
                    <div class="feature-desc">View past activities</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-sign-out-alt"></i>
                    </div>
                    <div class="feature-title">Logout</div>
                    <div class="feature-desc">Sign out of account</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bottom Navigation -->
    <div class="bottom-nav">
        <div class="nav-container">
            <div id="nav-home" class="nav-item active" onclick="showHome()">
                <div class="nav-icon">
                    <i class="fas fa-home"></i>
                </div>
                <div class="nav-label">Home</div>
            </div>
            
            <div id="nav-wallet" class="nav-item" onclick="showWallet()">
                <div class="nav-icon">
                    <i class="fas fa-wallet"></i>
                </div>
                <div class="nav-label">Wallet</div>
            </div>
            
            <div id="nav-ranking" class="nav-item" onclick="showRanking()">
                <div class="nav-icon">
                    <i class="fas fa-trophy"></i>
                </div>
                <div class="nav-label">Ranking</div>
            </div>
            
            <div id="nav-account" class="nav-item" onclick="showAccount()">
                <div class="nav-icon">
                    <i class="fas fa-user"></i>
                </div>
                <div class="nav-label">Account</div>
            </div>
        </div>
    </div>

    <!-- Modal -->
    <div id="airdropModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <div class="modal-title" id="modalTitle">Airdrops</div>
            <div id="modalContent"></div>
        </div>
    </div>
    
    <script>
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -30px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
        
        // Observe all scroll-animate elements
        document.querySelectorAll('.scroll-animate').forEach(el => {
            observer.observe(el);
        });
        
        // Add loading animation delay
        setTimeout(() => {
            document.querySelector('.loading').style.opacity = '1';
        }, 100);

        // API Functions
        async function parseAirdrops() {
            try {
                const response = await fetch('/api/parse-airdrops', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                
                if (data.status === 'success') {
                    alert(`✅ ${data.message}`);
                    // Обновляем список аирдропов
                    getAirdrops();
                } else {
                    alert(`❌ Error: ${data.message}`);
                }
            } catch (error) {
                alert(`❌ Network error: ${error.message}`);
            }
        }

        async function getAirdrops() {
            try {
                const response = await fetch('/api/airdrops');
                const data = await response.json();
                
                if (data.status === 'success') {
                    showAirdropsModal(data.airdrops);
                } else {
                    alert(`❌ Error: ${data.message}`);
                }
            } catch (error) {
                alert(`❌ Network error: ${error.message}`);
            }
        }

        async function searchAirdrops() {
            const blockchain = document.getElementById('blockchain-filter')?.value || '';
            const difficulty = document.getElementById('difficulty-filter')?.value || '';
            const status = document.getElementById('status-filter')?.value || '';
            
            try {
                const params = new URLSearchParams();
                if (blockchain) params.append('blockchain', blockchain);
                if (difficulty) params.append('difficulty', difficulty);
                if (status) params.append('status', status);
                
                const response = await fetch(`/api/search-airdrops?${params}`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    showAirdropsModal(data.airdrops, `Found ${data.count} airdrops`);
                } else {
                    alert(`❌ Error: ${data.message}`);
                }
            } catch (error) {
                alert(`❌ Network error: ${error.message}`);
            }
        }

        function showAirdropsModal(airdrops, title = 'Available Airdrops') {
            const modal = document.getElementById('airdropModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalContent = document.getElementById('modalContent');
            
            modalTitle.textContent = title;
            
            let content = '';
            airdrops.forEach(airdrop => {
                content += `
                    <div class="airdrop-item">
                        <div class="airdrop-title">${airdrop.title}</div>
                        <div class="airdrop-desc">${airdrop.description}</div>
                        <div class="airdrop-meta">
                            <span class="airdrop-badge ${airdrop.blockchain}">${airdrop.blockchain}</span>
                            <span class="airdrop-badge ${airdrop.difficulty}">${airdrop.difficulty}</span>
                            <span class="airdrop-badge">${airdrop.reward}</span>
                        </div>
                    </div>
                `;
            });
            
            modalContent.innerHTML = content;
            modal.style.display = 'block';
        }

        function closeModal() {
            document.getElementById('airdropModal').style.display = 'none';
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('airdropModal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        }

        // Feature Functions
        function showMonetization() {
            alert('💰 Premium features and $HUNT token rewards coming soon!');
        }

        function showWalletSupport() {
            alert('🔐 Multi-wallet support with PGP encryption coming soon!');
        }

        function showSecurity() {
            alert('🛡️ Advanced security features coming soon!');
        }

        function showAnalytics() {
            alert('📊 Detailed analytics and progress tracking coming soon!');
        }

        function showCommunity() {
            alert('👥 Community features and referral system coming soon!');
        }

        function showReferralLink() {
            const referralLink = 'https://t.me/airdrop_hunter_bot?start=ref_12345';
            alert(`🔗 Your referral link: ${referralLink}`);
        }

        function joinCommunity() {
            alert('📱 Opening Telegram community...');
            setTimeout(() => {
                window.open('https://t.me/airdrop_hunter_community', '_blank');
            }, 1000);
        }

        // Bottom Navigation Functions
        function showHome() {
            document.getElementById('home-content').style.display = 'block';
            document.getElementById('wallet-content').style.display = 'none';
            document.getElementById('ranking-content').style.display = 'none';
            document.getElementById('account-content').style.display = 'none';
            
            // Update active state
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-home').classList.add('active');
        }

        function showWallet() {
            document.getElementById('home-content').style.display = 'none';
            document.getElementById('wallet-content').style.display = 'block';
            document.getElementById('ranking-content').style.display = 'none';
            document.getElementById('account-content').style.display = 'none';
            
            // Update active state
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-wallet').classList.add('active');
        }

        function showRanking() {
            document.getElementById('home-content').style.display = 'none';
            document.getElementById('wallet-content').style.display = 'none';
            document.getElementById('ranking-content').style.display = 'block';
            document.getElementById('account-content').style.display = 'none';
            
            // Update active state
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-ranking').classList.add('active');
        }

        function showAccount() {
            document.getElementById('home-content').style.display = 'none';
            document.getElementById('wallet-content').style.display = 'none';
            document.getElementById('ranking-content').style.display = 'none';
            document.getElementById('account-content').style.display = 'block';
            
            // Update active state
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-account').classList.add('active');
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return MAIN_HTML

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "airdrop-hunter"}

@app.get("/api/airdrops")
async def get_airdrops():
    """Получить список аирдропов"""
    try:
        from database import SessionLocal, Airdrop
        db = SessionLocal()
        
        # Получаем все аирдропы из базы данных
        airdrops = db.query(Airdrop).all()
        
        result = []
        for airdrop in airdrops:
            result.append({
                "id": airdrop.id,
                "title": airdrop.title,
                "description": airdrop.description,
                "blockchain": airdrop.blockchain,
                "difficulty": airdrop.difficulty,
                "reward": airdrop.reward,
                "status": airdrop.status,
                "source_url": airdrop.source_url,
                "is_moderated": airdrop.is_moderated
            })
        
        db.close()
        return {"status": "success", "airdrops": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/parse-airdrops")
async def parse_airdrops():
    """Запустить парсинг новых аирдропов"""
    try:
        from database import SessionLocal, Airdrop
        from airdrop_parser import fetch_airdrops_from_coinmarketcap, save_airdrops_to_db
        from datetime import datetime
        
        # Имитация парсинга с разных источников
        mock_airdrops = [
            {
                "title": "TON Foundation Airdrop",
                "description": "Exclusive airdrop for TON ecosystem participants",
                "source_url": "https://ton.org/airdrop",
                "blockchain": "ton",
                "difficulty": "medium",
                "reward": "100-500 TON",
                "end_date": datetime.strptime("2024-12-31", "%Y-%m-%d")
            },
            {
                "title": "Ethereum Layer 2 Airdrop",
                "description": "New L2 protocol airdrop for early adopters",
                "source_url": "https://l2protocol.com/airdrop",
                "blockchain": "ethereum",
                "difficulty": "easy",
                "reward": "50-200 ETH",
                "end_date": datetime.strptime("2024-11-30", "%Y-%m-%d")
            },
            {
                "title": "Solana DeFi Airdrop",
                "description": "DeFi protocol airdrop on Solana blockchain",
                "source_url": "https://solana-defi.com/airdrop",
                "blockchain": "solana",
                "difficulty": "hard",
                "reward": "1000-5000 SOL",
                "end_date": datetime.strptime("2024-10-31", "%Y-%m-%d")
            },
            {
                "title": "Arbitrum Ecosystem Airdrop",
                "description": "Arbitrum ecosystem expansion airdrop",
                "source_url": "https://arbitrum.io/airdrop",
                "blockchain": "ethereum",
                "difficulty": "medium",
                "reward": "100-300 ARB",
                "end_date": datetime.strptime("2024-12-15", "%Y-%m-%d")
            }
        ]
        
        # Сохраняем в базу данных
        db = SessionLocal()
        try:
            for airdrop_data in mock_airdrops:
                airdrop = Airdrop(
                    title=airdrop_data["title"],
                    description=airdrop_data["description"],
                    source_url=airdrop_data["source_url"],
                    blockchain=airdrop_data["blockchain"],
                    difficulty=airdrop_data["difficulty"],
                    reward=airdrop_data["reward"],
                    status="active",
                    end_date=airdrop_data["end_date"],
                    is_moderated=True
                )
                db.add(airdrop)
            
            db.commit()
            db.close()
            
            return {
                "status": "success",
                "message": f"Successfully parsed and saved {len(mock_airdrops)} new airdrops!"
            }
        except Exception as e:
            db.rollback()
            db.close()
            return {"status": "error", "message": f"Database error: {str(e)}"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/search-airdrops")
async def search_airdrops(blockchain: str = None, difficulty: str = None, status: str = None):
    """Поиск аирдропов по фильтрам"""
    try:
        from database import SessionLocal, Airdrop
        from sqlalchemy import and_
        
        db = SessionLocal()
        
        # Строим фильтр
        filters = []
        if blockchain:
            filters.append(Airdrop.blockchain == blockchain)
        if difficulty:
            filters.append(Airdrop.difficulty == difficulty)
        if status:
            filters.append(Airdrop.status == status)
        
        # Выполняем запрос
        if filters:
            airdrops = db.query(Airdrop).filter(and_(*filters)).all()
        else:
            airdrops = db.query(Airdrop).all()
        
        result = []
        for airdrop in airdrops:
            result.append({
                "id": airdrop.id,
                "title": airdrop.title,
                "description": airdrop.description,
                "blockchain": airdrop.blockchain,
                "difficulty": airdrop.difficulty,
                "reward": airdrop.reward,
                "status": airdrop.status,
                "source_url": airdrop.source_url,
                "is_moderated": airdrop.is_moderated
            })
        
        db.close()
        return {"status": "success", "airdrops": result, "count": len(result)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/execute-task/{airdrop_id}")
async def execute_task(airdrop_id: int):
    """Выполнить задачу для аирдропа"""
    try:
        from database import SessionLocal, Airdrop
        from task_executor import execute_twitter_task, execute_website_task
        
        db = SessionLocal()
        
        # Получаем аирдроп
        airdrop = db.query(Airdrop).filter(Airdrop.id == airdrop_id).first()
        
        if not airdrop:
            db.close()
            return {"status": "error", "message": "Airdrop not found"}
        
        # Имитируем выполнение задач
        tasks_results = []
        
        # Twitter задачи
        if "twitter" in airdrop.description.lower():
            try:
                result = execute_twitter_task(airdrop.source_url)
                tasks_results.append(f"Twitter task: {result}")
            except Exception as e:
                tasks_results.append(f"Twitter task failed: {str(e)}")
        
        # Website регистрация
        if "register" in airdrop.description.lower() or "signup" in airdrop.description.lower():
            try:
                result = execute_website_task(airdrop.source_url)
                tasks_results.append(f"Website registration: {result}")
            except Exception as e:
                tasks_results.append(f"Website registration failed: {str(e)}")
        
        db.close()
        
        return {
            "status": "success",
            "message": f"Tasks executed for {airdrop.title}",
            "results": tasks_results
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.on_event("startup")
async def on_startup():
    """Инициализация при запуске"""
    print("🚀 Airdrop Hunter Bot запущен!")
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    """Очистка при остановке"""
    print("👋 Airdrop Hunter Bot остановлен!") 