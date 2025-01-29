# Importação das bibliotecas necessárias
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import json
import os
import requests

# Carrega as configurações do arquivo
config_path = os.path.join(os.path.dirname(__file__), '../cfg/config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Pegar as cotações históricas
tickers = ["BRL=X", "BTC-USD", "^BVSP", "^GSPC", "EURBRL=X", "^IXIC"]
market_data = yf.download(tickers, period="6mo")
market_data = market_data["Close"]

# Tratar dados coletados
market_data = market_data.dropna()
market_data.columns = ["DOLAR", "BTC", "EURO", "IBOVESPA", "S&P500", "NASDAQ"]

# Criar gráficos de performance
plt.style.use("cyberpunk")

# Diretório de saída para imagens
output_path = "../img"
os.makedirs(output_path, exist_ok=True)

# Função para salvar gráficos
def salvar_grafico(nome, dados):
    plt.figure()
    plt.plot(dados)
    plt.title(nome)
    plt.savefig(os.path.join(output_path, f"{nome.lower()}.png"))
    plt.close()

# Salvar gráficos
salvar_grafico("IBOVESPA", market_data["IBOVESPA"])
salvar_grafico("DOLAR", market_data["DOLAR"])
salvar_grafico("S&P500", market_data["S&P500"])
salvar_grafico("BTC", market_data["BTC"])
salvar_grafico("EURO", market_data["EURO"])
salvar_grafico("NASDAQ", market_data["NASDAQ"])

# Calcular retornos diários
daily_returns = market_data.pct_change()

dolar_return = daily_returns["DOLAR"].iloc[-1]
ibovespa_return = daily_returns["IBOVESPA"].iloc[-1]
sp500_return = daily_returns["S&P500"].iloc[-1]
btc_return = daily_returns["BTC"].iloc[-1]
euro_return = daily_returns["EURO"].iloc[-1]
nasdaq_return = daily_returns["NASDAQ"].iloc[-1]

dolar_return = str(round(dolar_return * 100, 2)) + "%" 
ibovespa_return = str(round(ibovespa_return * 100, 2)) + "%"
sp500_return = str(round(sp500_return * 100, 2)) + "%"
btc_return = str(round(btc_return * 100, 2)) + "%"
euro_return = str(round(euro_return * 100, 2)) + "%"
nasdaq_return = str(round(nasdaq_return * 100, 2)) + "%"

# Configurar e enviar o e-mail usando Gmail
def send_email_from_gmail():
    # Criar o objeto de mensagem
    msg = MIMEMultipart('related')
    msg['From'] = config['email']['sender']
    msg['To'] = ', '.join(config['email']['recipients'])
    msg['Subject'] = "Relatório Diário do Mercado"

    # Corpo do e-mail em HTML
    body = f'''
    <html>
    <body>
        <p>Olá! Segue o relatório de mercado do dia {datetime.now().strftime("%d/%m/%Y")}:</p>
        <ul>
            <li>O Ibovespa teve o retorno de {ibovespa_return}, fechando em {market_data["IBOVESPA"].iloc[-1].round(2)}.</li>
            <li>O Dólar teve o retorno de {dolar_return}, fechando em {market_data["DOLAR"].iloc[-1].round(2)}.</li>
            <li>O S&P500 teve o retorno de {sp500_return}, fechando em {market_data["S&P500"].iloc[-1].round(2)}.</li>
            <li>O BTC teve o retorno de {btc_return}, preço atual em {market_data["BTC"].iloc[-1].round(2)}.</li>
            <li>O EURO teve o retorno de {euro_return}, fechando em {market_data["EURO"].iloc[-1].round(2)}.</li>
            <li>O NASDAQ teve o retorno de {nasdaq_return}, fechando em {market_data["NASDAQ"].iloc[-1].round(2)}.</li>
        </ul>
        <p>Segue a performance dos ativos nos últimos 6 meses:</p>
        <img src="cid:ibovespa"><br>
        <img src="cid:dolar"><br>
        <img src="cid:sp500"><br>
        <img src="cid:btc"><br>
        <img src="cid:euro"><br>
        <img src="cid:nasdaq"><br>
        <p>Att,<br>{config['email']['name']}</p>
    </body>
    </html>
    '''
    msg.attach(MIMEText(body, 'html'))

    # Anexar imagens ao e-mail
    for nome in ["ibovespa", "dolar", "sp500", "btc", "euro", "nasdaq"]:
        with open(os.path.join(output_path, f"{nome}.png"), "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', f'<{nome}>')
            msg.attach(img)

    # Configurar o servidor SMTP
    server = smtplib.SMTP(config['smtp']['server'], config['smtp']['port'])
    server.starttls()
    server.login(config['email']['sender'], config['email']['password'])

    # Enviar o e-mail
    server.sendmail(
        config['email']['sender'],
        config['email']['recipients'],
        msg.as_string()
    )
    server.quit()
    print("E-mail enviado com sucesso!")

# Chamar a função para enviar o e-mail
send_email_from_gmail()

def send_pushover_notification():
    user_key = config['pushover']['user_key']  # Get user key from config
    api_token = config['pushover']['api_token']  # Get API token from config
    message = f'''Relatório de Mercado do dia {datetime.now().strftime("%d/%m/%Y")}:
    - IBOVESPA: {ibovespa_return} - Fechou em {market_data["IBOVESPA"].iloc[-1].round(2)}
    - DÓLAR: {dolar_return} - Fechou em {market_data["DOLAR"].iloc[-1].round(2)}
    - S&P500: {sp500_return} - Fechou em {market_data["S&P500"].iloc[-1].round(2)}
    - BTC: {btc_return} - Preço atual em {market_data["BTC"].iloc[-1].round(2)}
    - EURO: {euro_return} - Fechou em {market_data["EURO"].iloc[-1].round(2)}
    - NASDAQ: {nasdaq_return} - Fechou em {market_data["NASDAQ"].iloc[-1].round(2)}
    '''
    
    payload = {
        "token": api_token,
        "user": user_key,
        "message": message,
        "title": "Relatório de Mercado"
    }
    
    response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
    
    if response.status_code == 200:
        print("Notificação enviada com sucesso!")
    else:
        print(f"Erro ao enviar notificação: {response.status_code} - {response.text}")

# Chamar a função para enviar a notificação
send_pushover_notification()