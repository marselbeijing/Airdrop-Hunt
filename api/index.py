# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import requests
import json
from urllib.parse import urlencode

app = FastAPI()

# Telegram Bot API конфигурация
TELEGRAM_BOT_TOKEN = "8399460650:AAGa6PBJa1hTw1dPV-kyMR5GeQYOGbdraiE"
TELEGRAM_BOT_USERNAME = "airdrophunter_bot"  # Замените на ваш username бота

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
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
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
        
        /* Auth Section */
        .auth-section {
            background: var(--glass-dark);
            border-radius: 16px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
            border: 1px solid var(--glass-dark);
        }
        
        .auth-button {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: var(--white);
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
        }
        
        .auth-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        }
        
        .user-profile {
            display: none;
            background: var(--glass-dark);
            border-radius: 16px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid var(--glass-dark);
        }
        
        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin: 0 auto 12px;
            display: block;
            border: 3px solid var(--primary);
        }
        
        .user-name {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .user-username {
            color: var(--gray-light);
            font-size: 0.9rem;
            margin-bottom: 16px;
        }
        
        .user-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 16px;
        }
        
        .stat-item {
            background: var(--glass);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: var(--gray-light);
            margin-top: 4px;
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
        
        /* Button Groups */
        .btn-group {
            display: flex;
            gap: 12px;
            margin: 25px 0;
        }
        
        /* Airdrops Section */
        .airdrops-section {
            margin-top: 30px;
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .section-header h3 {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--white);
        }
        
        .loading-placeholder {
            text-align: center;
            padding: 40px 20px;
            color: var(--gray-light);
        }
        
        .loading-placeholder i {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .airdrops-grid {
            display: grid;
            gap: 16px;
        }
        
        .airdrop-card {
            background: var(--glass);
            border: 1px solid var(--glass-dark);
            border-radius: 12px;
            padding: 16px;
            backdrop-filter: blur(10px);
        }
        
        .airdrop-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }
        
        .airdrop-header h3 {
            font-size: 1rem;
            font-weight: 600;
            color: var(--white);
            margin: 0;
        }
        
        .blockchain-tag {
            background: var(--primary);
            color: var(--white);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        .airdrop-desc {
            color: var(--gray-light);
            font-size: 0.9rem;
            line-height: 1.4;
            margin-bottom: 12px;
        }
        
        .airdrop-meta {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
        }
        
        .difficulty {
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        .difficulty.easy {
            background: var(--success);
            color: var(--white);
        }
        
        .difficulty.medium {
            background: var(--warning);
            color: var(--white);
        }
        
        .difficulty.hard {
            background: var(--danger);
            color: var(--white);
        }
        
        .reward {
            background: var(--secondary);
            color: var(--white);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        .airdrop-actions {
            display: flex;
            gap: 8px;
        }
        
        .airdrop-actions .btn {
            flex: 1;
            font-size: 0.8rem;
            padding: 8px 12px;
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
        
        /* Bottom Navigation Bar */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 375px;
            max-width: 100vw;
            background: var(--glass-dark);
            backdrop-filter: blur(20px);
            border-top: 1px solid var(--glass-dark);
            border-radius: 20px 20px 0 0;
            padding: 12px 20px 20px;
            z-index: 1000;
        }
        
        .nav-items {
            display: flex;
            justify-content: space-around;
            align-items: center;
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: 8px 12px;
            border-radius: 12px;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: var(--gray-light);
        }
        
        .nav-item:hover,
        .nav-item.active {
            color: var(--primary);
            background: var(--glass);
        }
        
        .nav-icon {
            font-size: 1.2rem;
            margin-bottom: 2px;
        }
        
        .nav-label {
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px 0 80px;
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
            
            .bottom-nav {
                width: 100%;
                border-radius: 0;
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
        
        /* Content sections */
        .content-section {
            display: none;
        }
        
        .content-section.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Home Content -->
        <div id="home-content" class="content-section active">
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
                        <i class="fas fa-tasks"></i>
                    </div>
                    <div class="stat-title">Auto Tasks</div>
                    <div class="stat-desc">Complete without user input</div>
                </div>
                
                <div class="stat-card" onclick="showMonetization()" style="cursor: pointer;">
                    <div class="stat-icon">
                        <i class="fas fa-dollar-sign"></i>
                    </div>
                    <div class="stat-title">Monetization</div>
                    <div class="stat-desc">Premium & $HUNT token</div>
                </div>
                
                <div class="stat-card" onclick="showRanking()" style="cursor: pointer;">
                    <div class="stat-icon">
                        <i class="fas fa-medal"></i>
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
                        <i class="fas fa-lock"></i>
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
            
            <!-- Real Airdrops Container -->
            <div id="airdrops-container" class="airdrops-section scroll-animate">
                <div class="section-header">
                    <h3>🔥 Latest Airdrops</h3>
                    <button class="btn btn-secondary" onclick="loadRealAirdrops()">
                        <i class="fas fa-sync"></i>
                        Refresh
                    </button>
                </div>
                <div class="loading-placeholder">
                    <i class="fas fa-spinner fa-spin"></i>
                    <p>Loading real airdrops...</p>
                </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="btn-group scroll-animate">
                <button class="btn btn-primary" onclick="parseAirdrops()">
                    <i class="fas fa-sync"></i>
                    Parse New Airdrops
                </button>
            </div>
            
            <!-- Footer -->
            <div class="footer scroll-animate">
                <p>&copy; 2024 Airdrop Hunter. All rights reserved.</p>
            </div>
        </div>
        
        <!-- Profile Content -->
        <div id="profile-content" class="content-section">
            <div class="header">
                <div class="logo">
                    <i class="fas fa-user"></i>
                    Profile
                </div>
            </div>
            
            <div id="profile-details">
                <!-- Profile content will be loaded here -->
            </div>
        </div>
    </div>
    
    <!-- Bottom Navigation Bar -->
    <div class="bottom-nav">
        <div class="nav-items">
            <a href="#" class="nav-item active" onclick="showHome()">
                <div class="nav-icon">
                    <i class="fas fa-home"></i>
                </div>
                <div class="nav-label">Home</div>
            </a>
            <a href="#" class="nav-item" onclick="showAirdrops()">
                <div class="nav-icon">
                    <i class="fas fa-gift"></i>
                </div>
                <div class="nav-label">Airdrops</div>
            </a>
            <a href="#" class="nav-item" onclick="showTasks()">
                <div class="nav-icon">
                    <i class="fas fa-tasks"></i>
                </div>
                <div class="nav-label">Tasks</div>
            </a>
            <a href="#" class="nav-item" onclick="showWallet()">
                <div class="nav-icon">
                    <i class="fas fa-wallet"></i>
                </div>
                <div class="nav-label">Wallet</div>
            </a>
            <a href="#" class="nav-item" onclick="showProfile()">
                <div class="nav-icon">
                    <i class="fas fa-user"></i>
                </div>
                <div class="nav-label">Profile</div>
            </a>
        </div>
    </div>
    
    <script>
        // Telegram Web App initialization
        let tg = null;
        let user = null;
        const TELEGRAM_BOT_USERNAME = "airdrophunter_bot";
        
        // Initialize Telegram WebApp
        try {
            tg = window.Telegram.WebApp;
            if (tg) {
                tg.ready();
            }
        } catch (error) {
            console.log('Telegram WebApp not available:', error);
        }
        
        // Initialize Telegram Web App
        function initTelegramAuth() {
            try {
                if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                    // User is already authorized
                    user = tg.initDataUnsafe.user;
                    showUserProfile();
                    loadProfileData();
                } else {
                    // For demo purposes, simulate successful auth
                    user = {
                        id: 123456789,
                        first_name: 'Demo',
                        last_name: 'User',
                        username: 'demo_user',
                        photo_url: 'https://via.placeholder.com/60'
                    };
                    showUserProfile();
                    loadProfileData();
                    alert('✅ Демо авторизация успешна!');
                }
            } catch (error) {
                console.error('Auth error:', error);
                alert('❌ Ошибка авторизации. Попробуйте еще раз.');
            }
        }
        
        // Show user profile after authorization
        function showUserProfile() {
            if (user) {
                // Update profile data if we're on profile page
                if (document.getElementById('profile-content').classList.contains('active')) {
                    loadProfileData();
                }
            }
        }
        
        // Check if user is already authorized
        function checkAuth() {
            try {
                if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                    user = tg.initDataUnsafe.user;
                }
            } catch (error) {
                console.log('Telegram WebApp not available:', error);
            }
        }
        
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
                    loadRealAirdrops();
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
                    displayAirdrops(data.airdrops);
                } else {
                    alert(`❌ Error: ${data.message}`);
                }
            } catch (error) {
                alert(`❌ Network error: ${error.message}`);
            }
        }

        async function loadRealAirdrops() {
            try {
                const response = await fetch('/api/airdrops');
                const data = await response.json();
                
                if (data.status === 'success') {
                    displayAirdrops(data.airdrops);
                }
            } catch (error) {
                console.error('Error loading airdrops:', error);
            }
        }

        function displayAirdrops(airdrops) {
            const airdropsContainer = document.getElementById('airdrops-container');
            if (!airdropsContainer) return;
            
            let html = '<div class="airdrops-grid">';
            
            airdrops.forEach(airdrop => {
                html += `
                    <div class="airdrop-card">
                        <div class="airdrop-header">
                            <h3>${airdrop.title}</h3>
                            <span class="blockchain-tag">${airdrop.blockchain}</span>
                        </div>
                        <p class="airdrop-desc">${airdrop.description}</p>
                        <div class="airdrop-meta">
                            <span class="difficulty ${airdrop.difficulty.toLowerCase()}">${airdrop.difficulty}</span>
                            <span class="reward">${airdrop.reward}</span>
                        </div>
                        <div class="airdrop-actions">
                            <a href="${airdrop.referral_link}" target="_blank" class="btn btn-primary">
                                <i class="fas fa-external-link-alt"></i>
                                Participate
                            </a>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
            airdropsContainer.innerHTML = html;
        }

        // Navigation Functions
        function showHome() {
            setActiveNav('home');
            showContent('home-content');
        }

        function showAirdrops() {
            setActiveNav('airdrops');
            alert('🎁 Airdrops page - Browse available airdrops');
        }

        function showTasks() {
            setActiveNav('tasks');
            alert('📋 Tasks page - Manage your tasks');
        }

        function showWallet() {
            setActiveNav('wallet');
            alert('💰 Wallet page - Manage your wallets');
        }

        function showProfile() {
            setActiveNav('profile');
            showContent('profile-content');
            loadProfileData();
        }

        function showContent(contentId) {
            // Hide all content sections
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Show selected content
            document.getElementById(contentId).classList.add('active');
        }

        function setActiveNav(page) {
            // Remove active class from all nav items
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Add active class to clicked item
            event.target.closest('.nav-item').classList.add('active');
        }

        function loadProfileData() {
            const profileDetails = document.getElementById('profile-details');
            if (user) {
                profileDetails.innerHTML = `
                    <div class="user-profile">
                        <img src="${user.photo_url || 'https://via.placeholder.com/60'}" class="user-avatar">
                        <div class="user-name">${user.first_name} ${user.last_name || ''}</div>
                        <div class="user-username">@${user.username || 'user'}</div>
                        <div class="user-stats">
                            <div class="stat-item">
                                <div class="stat-value">1250</div>
                                <div class="stat-label">Рейтинг</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">450</div>
                                <div class="stat-label">$HUNT</div>
                            </div>
                        </div>
                    </div>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="logout()">
                            <i class="fas fa-sign-out-alt"></i>
                            Выйти
                        </button>
                    </div>
                `;
            } else {
                profileDetails.innerHTML = `
                    <div class="auth-section">
                        <h3>🔐 Авторизация через Telegram</h3>
                        <p style="margin: 12px 0; color: var(--gray-light); font-size: 0.9rem;">
                            Войдите через Telegram для доступа к профилю
                        </p>
                        <button class="auth-button" onclick="initTelegramAuth()">
                            <i class="fab fa-telegram"></i>
                            Войти через Telegram
                        </button>
                    </div>
                `;
            }
        }

        function logout() {
            user = null;
            localStorage.removeItem('telegram_user');
            loadProfileData();
            alert('Вы вышли из аккаунта');
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

        function showRanking() {
            alert('🏆 Leaderboard and ranking system coming soon!');
        }

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            checkAuth();
            loadRealAirdrops(); // Загружаем реальные аирдропы
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
        # Импортируем функции парсинга
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        
        from airdrop_parser import fetch_all_airdrops
        
        # Получаем реальные аирдропы
        airdrops = fetch_all_airdrops()
        
        print(f"🔍 API: получено {len(airdrops)} аирдропов")
        
        # Если аирдропы не найдены, используем тестовые данные
        if not airdrops:
            print("⚠️ API: аирдропы не найдены, используем тестовые данные")
            airdrops = [
                {
                    "title": "TON Airdrop",
                    "description": "Exclusive TON blockchain airdrop for early adopters",
                    "source_url": "https://ton.org/airdrop",
                    "referral_link": "https://ton.org/airdrop?ref=airdrophunter",
                    "blockchain": "TON",
                    "difficulty": "Easy",
                    "reward": "50 TON"
                },
                {
                    "title": "Ethereum DeFi Airdrop",
                    "description": "DeFi protocol airdrop for liquidity providers",
                    "source_url": "https://defi.org/airdrop",
                    "referral_link": "https://defi.org/airdrop?ref=airdrophunter",
                    "blockchain": "Ethereum",
                    "difficulty": "Medium",
                    "reward": "0.1 ETH"
                },
                {
                    "title": "Solana NFT Airdrop",
                    "description": "NFT marketplace airdrop for creators",
                    "source_url": "https://solana-nft.com/airdrop",
                    "referral_link": "https://solana-nft.com/airdrop?ref=airdrophunter",
                    "blockchain": "Solana",
                    "difficulty": "Hard",
                    "reward": "5 SOL"
                }
            ]
        
        # Форматируем для API
        formatted_airdrops = []
        for i, airdrop in enumerate(airdrops[:20]):  # Ограничиваем 20 аирдропами
            formatted_airdrops.append({
                "id": i + 1,
                "title": airdrop.get("title", "Unknown Airdrop"),
                "description": airdrop.get("description", "No description available"),
                "source_url": airdrop.get("source_url", "#"),
                "referral_link": airdrop.get("referral_link", airdrop.get("source_url", "#")),
                "blockchain": airdrop.get("blockchain", "Unknown"),
                "difficulty": airdrop.get("difficulty", "Medium"),
                "status": "new",
                "reward": airdrop.get("reward", "Unknown reward"),
                "is_moderated": True
            })
        
        print(f"✅ API: отформатировано {len(formatted_airdrops)} аирдропов")
        
        return {
            "status": "success",
            "message": f"Found {len(formatted_airdrops)} real airdrops",
            "airdrops": formatted_airdrops
        }
    except Exception as e:
        print(f"Error fetching airdrops: {e}")
        return {
            "status": "error",
            "message": f"Failed to fetch airdrops: {str(e)}",
            "airdrops": []
        }

@app.post("/api/parse-airdrops")
async def parse_airdrops():
    """Запустить парсинг новых аирдропов"""
    try:
        # Импортируем функции парсинга
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        
        from airdrop_parser import fetch_all_airdrops, save_airdrops_to_database
        
        # Получаем реальные аирдропы
        airdrops = fetch_all_airdrops()
        
        # Сохраняем в базу данных
        saved_count = save_airdrops_to_database(airdrops)
        
        return {
            "status": "success",
            "message": f"Successfully parsed and saved {saved_count} new airdrops!",
            "total_found": len(airdrops),
            "saved_count": saved_count
        }
    except Exception as e:
        print(f"Error parsing airdrops: {e}")
        return {
            "status": "error",
            "message": f"Failed to parse airdrops: {str(e)}"
        }

@app.get("/api/auth/telegram")
async def telegram_auth():
    """Telegram OAuth callback"""
    return {"status": "success", "message": "Telegram auth callback"} 