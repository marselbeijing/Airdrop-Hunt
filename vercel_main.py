from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Airdrop Hunter", version="1.0.0")

# Упрощенный HTML с основным функционалом
SIMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Hunter</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            min-height: 100vh;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            max-width: 375px;
            width: 100%;
            min-height: 100vh;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 0;
            padding: 20px 20px 120px 20px;
            position: relative;
            overflow-y: auto;
        }
        
        .header {
            text-align: center;
            padding: 20px 0 30px;
        }
        
        .logo {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
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
            color: #94a3b8;
            margin-bottom: 25px;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
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
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 25px 0;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 16px 12px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            border-color: #6366f1;
        }
        
        .stat-icon {
            font-size: 1.5rem;
            color: #6366f1;
            margin-bottom: 8px;
        }
        
        .stat-title {
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 4px;
        }
        
        .stat-desc {
            font-size: 0.75rem;
            color: #94a3b8;
            line-height: 1.3;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 25px 0;
        }
        
        .feature-card {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 16px 12px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            border-color: #8b5cf6;
        }
        
        .feature-icon {
            font-size: 1.5rem;
            color: #8b5cf6;
            margin-bottom: 8px;
        }
        
        .feature-title {
            font-weight: 600;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }
        
        .feature-desc {
            font-size: 0.7rem;
            color: #94a3b8;
            line-height: 1.3;
        }
        
        .bottom-nav {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding: 6px 0 12px 0;
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            bottom: 0;
            width: 375px;
            z-index: 1000;
            box-shadow: 0 -2px 24px 0 rgba(0,0,0,0.12);
        }
        
        .nav-container {
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
            transition: all 0.3s ease;
            color: #94a3b8;
            min-width: 55px;
            position: relative;
        }

        .nav-item.active {
            color: #ffffff;
            transform: translateY(-4px);
        }

        .nav-item:hover {
            color: #ffffff;
            transform: translateY(-2px);
        }

        .nav-icon {
            font-size: 1.1rem;
            margin-bottom: 1px;
        }

        .nav-label {
            font-size: 0.6rem;
            font-weight: 600;
            text-align: center;
            line-height: 1;
        }

        .content-section {
            display: none;
        }

        .content-section.active {
            display: block;
        }

        #home-content {
            display: block;
        }
        
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
            border: none;
            cursor: pointer;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        }
        
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }
        
        .footer {
            text-align: center;
            padding: 20px 0 0;
            color: #94a3b8;
            font-size: 0.75rem;
        }
        
        @media (max-width: 480px) {
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
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Home Content -->
        <div id="home-content" class="content-section">
            <div class="header">
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
            
            <div class="stats-grid">
                <div class="stat-card" onclick="alert('Smart Search coming soon!')">
                    <div class="stat-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <div class="stat-title">Smart Search</div>
                    <div class="stat-desc">Auto parsing from top sources</div>
                </div>
                
                <div class="stat-card" onclick="alert('Auto Tasks coming soon!')">
                    <div class="stat-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="stat-title">Auto Tasks</div>
                    <div class="stat-desc">Complete without user input</div>
                </div>
                
                <div class="stat-card" onclick="alert('Monetization coming soon!')">
                    <div class="stat-icon">
                        <i class="fas fa-coins"></i>
                    </div>
                    <div class="stat-title">Monetization</div>
                    <div class="stat-desc">Premium & $HUNT token</div>
                </div>
                
                <div class="stat-card" onclick="alert('Ranking coming soon!')">
                    <div class="stat-icon">
                        <i class="fas fa-trophy"></i>
                    </div>
                    <div class="stat-title">Ranking</div>
                    <div class="stat-desc">Leaderboard & rewards</div>
                </div>
            </div>
            
            <div class="features-grid">
                <div class="feature-card" onclick="alert('Multi-Wallet Support coming soon!')">
                    <div class="feature-icon">
                        <i class="fas fa-wallet"></i>
                    </div>
                    <div class="feature-title">Multi-Wallet Support</div>
                    <div class="feature-desc">TON, Ethereum, Solana with PGP encryption</div>
                </div>
                
                <div class="feature-card" onclick="alert('Security features coming soon!')">
                    <div class="feature-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <div class="feature-title">Security First</div>
                    <div class="feature-desc">PGP encryption, captcha, and usage limits</div>
                </div>
                
                <div class="feature-card" onclick="alert('Analytics coming soon!')">
                    <div class="feature-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="feature-title">Analytics</div>
                    <div class="feature-desc">Detailed stats and progress tracking</div>
                </div>
                
                <div class="feature-card" onclick="alert('Community features coming soon!')">
                    <div class="feature-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="feature-title">Community</div>
                    <div class="feature-desc">Referral system and exclusive airdrops</div>
                </div>
            </div>
            
            <div class="btn-group">
                <a href="/health" class="btn btn-primary" target="_blank">
                    <i class="fas fa-heartbeat"></i>
                    Check API
                </a>
                <a href="#" class="btn btn-secondary" onclick="alert('Telegram bot integration coming soon!')">
                    <i class="fab fa-telegram"></i>
                    Telegram Bot
                </a>
            </div>
            
            <div class="footer">
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
                <div class="feature-card" onclick="alert('Telegram login coming soon!')">
                    <div class="feature-icon">
                        <i class="fab fa-telegram"></i>
                    </div>
                    <div class="feature-title">Login with Telegram</div>
                    <div class="feature-desc">Secure authentication</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-user-circle"></i>
                    </div>
                    <div class="feature-title">Profile</div>
                    <div class="feature-desc">Manage your account</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-cog"></i>
                    </div>
                    <div class="feature-title">Settings</div>
                    <div class="feature-desc">Customize preferences</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-sign-out-alt"></i>
                    </div>
                    <div class="feature-title">Logout</div>
                    <div class="feature-desc">Sign out safely</div>
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
        function showHome() {
            document.getElementById('home-content').style.display = 'block';
            document.getElementById('wallet-content').style.display = 'none';
            document.getElementById('ranking-content').style.display = 'none';
            document.getElementById('account-content').style.display = 'none';
            
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-home').classList.add('active');
        }

        function showWallet() {
            document.getElementById('home-content').style.display = 'none';
            document.getElementById('wallet-content').style.display = 'block';
            document.getElementById('ranking-content').style.display = 'none';
            document.getElementById('account-content').style.display = 'none';
            
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-wallet').classList.add('active');
        }

        function showRanking() {
            document.getElementById('home-content').style.display = 'none';
            document.getElementById('wallet-content').style.display = 'none';
            document.getElementById('ranking-content').style.display = 'block';
            document.getElementById('account-content').style.display = 'none';
            
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-ranking').classList.add('active');
        }

        function showAccount() {
            document.getElementById('home-content').style.display = 'none';
            document.getElementById('wallet-content').style.display = 'none';
            document.getElementById('ranking-content').style.display = 'none';
            document.getElementById('account-content').style.display = 'block';
            
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById('nav-account').classList.add('active');
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return SIMPLE_HTML

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Airdrop Hunter is running!"} 