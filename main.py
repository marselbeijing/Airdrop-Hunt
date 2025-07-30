from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import init_db
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
    <script async src="https://telegram.org/js/telegram-widget.js?22"></script>
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
            padding: 0;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        
        .container {
            max-width: 375px;
            width: 100%;
            min-height: 100vh;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-dark);
            border-radius: 0;
            padding: 20px 20px 120px 20px;
            box-shadow: 0 0 0 rgba(0, 0, 0, 0);
            position: relative;
            overflow-y: auto;
            margin: 0;
            box-sizing: border-box;
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
        
        /* Bottom Navigation - Modern Design */
        .bottom-nav {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding: 6px 0 12px 0;
            border-radius: 0;
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            bottom: 0;
            width: 375px;
            z-index: 1000;
            box-shadow: 0 -2px 24px 0 rgba(0,0,0,0.12);
        }
        .nav-container {
            max-width: 375px;
            margin: 0 auto;
            display: flex;
            justify-content: space-around;
            align-items: center;
            gap: 8px;
            padding: 0 20px;
        }

        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
            padding: 6px 10px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--gray-light);
            text-decoration: none;
            min-width: 55px;
            position: relative;
            overflow: hidden;
        }

        .nav-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            opacity: 0;
            transition: opacity 0.3s ease;
            border-radius: 16px;
        }

        .nav-item.active {
            color: var(--white);
            transform: translateY(-4px);
        }

        .nav-item.active::before {
            opacity: 1;
        }

        .nav-item:hover {
            color: var(--white);
            transform: translateY(-2px);
        }

        .nav-item:hover::before {
            opacity: 0.3;
        }

        .nav-icon {
            font-size: 1.1rem;
            margin-bottom: 1px;
            position: relative;
            z-index: 1;
        }

        .nav-label {
            font-size: 0.6rem;
            font-weight: 600;
            text-align: center;
            line-height: 1;
            position: relative;
            z-index: 1;
        }

        /* Login Styles */
        .login-container {
            padding: 20px 0;
        }

        .login-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-dark);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin-bottom: 20px;
        }

        .login-header {
            margin-bottom: 25px;
        }

        .login-header i {
            font-size: 3rem;
            color: #0088cc;
            margin-bottom: 15px;
        }

        .login-header h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 10px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .login-header p {
            color: var(--gray-light);
            font-size: 0.9rem;
            margin: 0;
        }

        .login-benefits {
            margin: 25px 0;
        }

        .benefit-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 12px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
        }

        .benefit-item i {
            color: #10b981;
            font-size: 1.1rem;
        }

        .benefit-item span {
            color: var(--gray-light);
            font-size: 0.9rem;
        }

        .btn-telegram {
            background: linear-gradient(135deg, #0088cc 0%, #00a8ff 100%);
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 20px 0;
            width: 100%;
        }

        .btn-telegram:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 136, 204, 0.3);
        }

        .login-note {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--gray-light);
            font-size: 0.8rem;
            margin-top: 15px;
        }

        .login-note i {
            color: #3b82f6;
        }

        /* Profile Styles */
        .profile-container {
            padding: 20px 0;
        }

        .profile-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-dark);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
        }

        .profile-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
        }

        .profile-avatar {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .profile-avatar i {
            font-size: 2rem;
            color: white;
        }

        .profile-info h3 {
            font-size: 1.3rem;
            font-weight: 700;
            margin: 0 0 5px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .profile-info p {
            color: var(--gray-light);
            margin: 0;
            font-size: 0.9rem;
        }

        .profile-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 25px 0;
        }

        .stat-item {
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #10b981;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--gray-light);
        }

        .profile-actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        .btn-outline {
            background: transparent;
            border: 1px solid var(--gray-light);
            color: var(--gray-light);
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn-outline:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: #ef4444;
            color: #ef4444;
        }

        /* Active indicator */
        .nav-item.active::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 4px;
            height: 4px;
            background: var(--primary);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        /* Modern glass effect for nav */
        .bottom-nav::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border-radius: 24px 24px 0 0;
            pointer-events: none;
        }

        /* Hover effects */
        .nav-item:hover .nav-icon {
            transform: scale(1.1);
            transition: transform 0.2s ease;
        }

        /* Active state animations */
        .nav-item.active .nav-icon {
            animation: bounce 0.6s ease;
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-8px);
            }
            60% {
                transform: translateY(-4px);
            }
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
        
        /* Mobile Responsive */
        @media (max-width: 480px) {
            body {
                padding: 0;
            }
            
            .container {
                max-width: 100%;
                height: 100vh;
                border-radius: 0;
            }
            
            .bottom-nav {
                width: 100%;
                left: 0;
                transform: none;
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
            
            <!-- Login Section -->
            <div id="login-section" class="login-container">
                <div class="login-card">
                    <div class="login-header">
                        <i class="fab fa-telegram"></i>
                        <h3>Login with Telegram</h3>
                        <p>Connect your Telegram account to access all features</p>
                    </div>
                    
                    <div class="login-benefits">
                        <div class="benefit-item">
                            <i class="fas fa-shield-alt"></i>
                            <span>Secure authentication</span>
                        </div>
                        <div class="benefit-item">
                            <i class="fas fa-sync"></i>
                            <span>Sync across devices</span>
                        </div>
                        <div class="benefit-item">
                            <i class="fas fa-bell"></i>
                            <span>Get notifications</span>
                        </div>
                    </div>
                    
                    <button class="btn btn-telegram" onclick="loginWithTelegram()">
                        <i class="fab fa-telegram"></i>
                        Login with Telegram
                    </button>
                    
                    <div class="login-note">
                        <i class="fas fa-info-circle"></i>
                        <span>We'll never share your data with third parties</span>
                    </div>
                </div>
            </div>
            
            <!-- User Profile Section -->
            <div id="user-profile" class="profile-container" style="display: none;">
                <div class="profile-card">
                    <div class="profile-header">
                        <div class="profile-avatar">
                            <i class="fas fa-user-circle"></i>
                        </div>
                        <div class="profile-info">
                            <h3 id="user-name">User Name</h3>
                            <p id="user-username">@username</p>
                        </div>
                    </div>
                    
                    <div class="profile-stats">
                        <div class="stat-item">
                            <div class="stat-value">24</div>
                            <div class="stat-label">Airdrops Found</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">$1,247</div>
                            <div class="stat-label">Total Earned</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">15</div>
                            <div class="stat-label">Days Active</div>
                        </div>
                    </div>
                    
                    <div class="profile-actions">
                        <button class="btn btn-secondary" onclick="showProfileSettings()">
                            <i class="fas fa-cog"></i>
                            Settings
                        </button>
                        <button class="btn btn-outline" onclick="logout()">
                            <i class="fas fa-sign-out-alt"></i>
                            Logout
                        </button>
                    </div>
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
                    alert(`Found ${data.airdrops.length} airdrops!`);
                } else {
                    alert(`❌ Error: ${data.message}`);
                }
            } catch (error) {
                alert(`❌ Network error: ${error.message}`);
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

        function loginWithTelegram() {
            // Telegram Login Widget configuration
            const telegramLoginWidget = {
                dataOnauth: function(user) {
                    // Handle successful login
                    console.log('Telegram login successful:', user);
                    document.getElementById('login-section').style.display = 'none';
                    document.getElementById('user-profile').style.display = 'block';
                    document.getElementById('user-name').textContent = user.first_name + ' ' + (user.last_name || '');
                    document.getElementById('user-username').textContent = '@' + user.username;
                    
                    // Store user data
                    localStorage.setItem('telegramUser', JSON.stringify(user));
                    
                    // Show success message
                    showNotification('Successfully logged in with Telegram!', 'success');
                }
            };
            
            // Initialize Telegram Login Widget
            if (window.Telegram && window.Telegram.Login) {
                window.Telegram.Login.auth(telegramLoginWidget, {
                    bot_id: 'YOUR_BOT_ID', // Replace with your bot ID
                    request_access: true
                });
            } else {
                // Fallback for demo purposes
                showNotification('Telegram login widget loading...', 'info');
                setTimeout(() => {
                    const mockUser = {
                        id: 123456789,
                        first_name: 'John',
                        last_name: 'Doe',
                        username: 'johndoe',
                        photo_url: 'https://via.placeholder.com/100'
                    };
                    telegramLoginWidget.dataOnauth(mockUser);
                }, 1000);
            }
        }

        function logout() {
            localStorage.removeItem('telegramUser');
            document.getElementById('login-section').style.display = 'block';
            document.getElementById('user-profile').style.display = 'none';
            showNotification('Successfully logged out!', 'success');
        }

        function showProfileSettings() {
            alert('Profile settings coming soon!');
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                z-index: 10000;
                font-size: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            `;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 3000);
        }

        // Check if user is already logged in on page load
        window.addEventListener('load', function() {
            const savedUser = localStorage.getItem('telegramUser');
            if (savedUser) {
                const user = JSON.parse(savedUser);
                document.getElementById('login-section').style.display = 'none';
                document.getElementById('user-profile').style.display = 'block';
                document.getElementById('user-name').textContent = user.first_name + ' ' + (user.last_name || '');
                document.getElementById('user-username').textContent = '@' + user.username;
            }
        });
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
                "referral_link": airdrop.referral_link,
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

@app.on_event("startup")
async def on_startup():
    """Инициализация при запуске"""
    print("🚀 Airdrop Hunter Bot запущен!")
    init_db()

@app.on_event("shutdown")
async def on_shutdown():
    """Очистка при остановке"""
    print("👋 Airdrop Hunter Bot остановлен!") 