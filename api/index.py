# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Airdrop Hunter</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                text-align: center;
                max-width: 400px;
            }
            .logo {
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #6366f1, #8b5cf6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .status {
                background: #10b981;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                display: inline-block;
                margin: 20px 0;
            }
            .btn {
                background: #6366f1;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                display: inline-block;
                margin: 10px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🚀 Airdrop Hunter</div>
            <div class="status">✅ Bot Online</div>
            <p>Automated crypto airdrop hunting with smart task execution</p>
            <a href="/health" class="btn">Check API</a>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "airdrop-hunter"} 