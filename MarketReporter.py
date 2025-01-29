# Importação das bibliotecas necessárias
import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json

# Carrega as configurações do arquivo
with open('config.json', 'r') as f:
    config = json.load(f)

# Pegar as cotações históricas
tickers = ["BRL=X", "BTC-USD", "^BVSP", "^GSPC", "EURBRL=X"]
market_data = yf.download(tickers, period="6mo")
market_data = market_data["Close"]

# Tratar dados coletados
market_data = market_data.dropna()
market_data.columns = ["DOLAR", "BTC", "EURO", "IBOVESPA", "S&P500"]

# Criar gráficos de performance
plt.style.use("cyberpunk")

# Gráfico IBOVESPA
plt.figure()
plt.plot(market_data["IBOVESPA"])
plt.title("IBOVESPA")
plt.savefig("ibovespa.png")
plt.close()

# Gráfico DOLAR
plt.figure()
plt.plot(market_data["DOLAR"])
plt.title("DOLAR")
plt.savefig("dolar.png")
plt.close()

# Gráfico S&P500
plt.figure()
plt.plot(market_data["S&P500"])
plt.title("S&P500")
plt.savefig("sp500.png")
plt.close()

# Gráfico BTC
plt.figure()
plt.plot(market_data["BTC"])
plt.title("BTC")
plt.savefig("btc.png")
plt.close()

# Gráfico EURO
plt.figure()
plt.plot(market_data["EURO"])
plt.title("EURO")
plt.savefig("euro.png")
plt.close()

# Calcular retornos diários
daily_returns = market_data.pct_change()

dolar_return = daily_returns["DOLAR"].iloc[-1]
ibovespa_return = daily_returns["IBOVESPA"].iloc[-1]
sp500_return = daily_returns["S&P500"].iloc[-1]
btc_return = daily_returns["BTC"].iloc[-1]
euro_return = daily_returns["EURO"].iloc[-1]

dolar_return = str(round(dolar_return * 100, 2)) + "%"
ibovespa_return = str(round(ibovespa_return * 100, 2)) + "%"
sp500_return = str(round(sp500_return * 100, 2)) + "%"
btc_return = str(round(btc_return * 100, 2)) + "%"
euro_return = str(round(euro_return * 100, 2)) + "%"

# Configurar e enviar o e-mail usando Gmail
def send_email_from_gmail():
    # Criar o objeto de mensagem
    msg = MIMEMultipart()
    msg['From'] = config['email']['sender']
    msg['To'] = ', '.join(config['email']['recipients'])
    msg['Subject'] = "Relatório Diário do Mercado"

    # Corpo do e-mail
    body = f'''Opaa, segue o relatório de mercado do dia {datetime.now().strftime("%d/%m/%Y")}:

    * O Ibovespa teve o retorno de {ibovespa_return}.
    * O Dólar teve o retorno de {dolar_return}.
    * O S&P500 teve o retorno de {sp500_return}.
    * O BTC teve o retorno de {btc_return}.
    * O EURO teve o retorno de {euro_return}.
    Segue em anexo a peformance dos ativos nos últimos 6 meses.

    Att,
    {config['email']['name']}
    '''
    msg.attach(MIMEText(body, 'plain'))

    # Anexar arquivos
    import os

    base_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Área de Trabalho", "Programming", "MarketReporter")
    anexos = [
        os.path.join(base_path, "ibovespa.png"),
        os.path.join(base_path, "dolar.png"),
        os.path.join(base_path, "sp500.png"),
        os.path.join(base_path, "btc.png"),
        os.path.join(base_path, "euro.png")
    ]

    for anexo in anexos:
        with open(anexo, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={anexo.split("\\")[-1]}')
            msg.attach(part)

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