from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Airdrop Hunter", version="1.0.0")

# Упрощенный HTML без сложных функций
SIMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Hunter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            max-width: 375px;
            min-height: 100vh;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 30px 25px 120px 25px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow-y: auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .feature-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .feature-desc {
            font-size: 0.8rem;
            opacity: 0.9;
        }
        
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 375px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px 20px 0 0;
            padding: 6px 0 12px 0;
            box-shadow: 0 -2px 24px 0 rgba(0,0,0,0.12);
            z-index: 1000;
        }
        
        .nav-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 6px 10px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 55px;
            gap: 3px;
        }
        
        .nav-item.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .nav-icon {
            font-size: 1.1rem;
            margin-bottom: 1px;
        }
        
        .nav-label {
            font-size: 0.6rem;
            font-weight: 500;
        }
        
        @media (max-width: 480px) {
            .container {
                max-width: 100%;
                border-radius: 0;
                padding: 20px 20px 120px 20px;
            }
            
            .bottom-nav {
                width: 100%;
                left: 0;
                transform: none;
                border-radius: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀</div>
            <h1>Airdrop Hunter</h1>
            <p class="subtitle">Find the best crypto airdrops</p>
        </div>
        
        <div class="features-grid">
            <div class="feature-card" onclick="alert('Smart Search coming soon!')">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Smart Search</div>
                <div class="feature-desc">Auto parsing from top sources</div>
            </div>
            
            <div class="feature-card" onclick="alert('Telegram Bot coming soon!')">
                <div class="feature-icon">📱</div>
                <div class="feature-title">Telegram Bot</div>
                <div class="feature-desc">Get notifications instantly</div>
            </div>
            
            <div class="feature-card" onclick="alert('Multi-Wallet Support coming soon!')">
                <div class="feature-icon">💼</div>
                <div class="feature-title">Multi-Wallet</div>
                <div class="feature-desc">TON, Ethereum, Solana</div>
            </div>
            
            <div class="feature-card" onclick="alert('Ranking System coming soon!')">
                <div class="feature-icon">🏆</div>
                <div class="feature-title">Ranking</div>
                <div class="feature-desc">Leaderboard & rewards</div>
            </div>
        </div>
    </div>
    
    <div class="bottom-nav">
        <div class="nav-container">
            <div class="nav-item active">
                <div class="nav-icon">🏠</div>
                <div class="nav-label">Home</div>
            </div>
            <div class="nav-item">
                <div class="nav-icon">💼</div>
                <div class="nav-label">Wallet</div>
            </div>
            <div class="nav-item">
                <div class="nav-icon">🏆</div>
                <div class="nav-label">Ranking</div>
            </div>
            <div class="nav-item">
                <div class="nav-icon">👤</div>
                <div class="nav-label">Account</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return SIMPLE_HTML

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Airdrop Hunter is running!"} 