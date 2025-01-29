# Importação das bibliotecas necessárias
from datetime import datetime
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
import os

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

# Gráfico IBOVESPA
plt.figure()
plt.plot(market_data["IBOVESPA"])
plt.title("IBOVESPA")
plt.savefig(os.path.join(output_path, "ibovespa.png"))
plt.close()

# Gráfico DOLAR
plt.figure()
plt.plot(market_data["DOLAR"])
plt.title("DOLAR")
plt.savefig(os.path.join(output_path, "dolar.png"))
plt.close()

# Gráfico S&P500
plt.figure()
plt.plot(market_data["S&P500"])
plt.title("S&P500")
plt.savefig(os.path.join(output_path, "sp500.png"))
plt.close()

# Gráfico BTC
plt.figure()
plt.plot(market_data["BTC"])
plt.title("BTC")
plt.savefig(os.path.join(output_path, "btc.png"))
plt.close()

# Gráfico EURO
plt.figure()
plt.plot(market_data["EURO"])
plt.title("EURO")
plt.savefig(os.path.join(output_path, "euro.png"))
plt.close()

# Gráfico NASDAQ
plt.figure()
plt.plot(market_data["NASDAQ"])
plt.title("NASDAQ")
plt.savefig(os.path.join(output_path, "nasdaq.png"))
plt.close()

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
    msg = MIMEMultipart()
    msg['From'] = config['email']['sender']
    msg['To'] = ', '.join(config['email']['recipients'])
    msg['Subject'] = "Relatório Diário do Mercado"

    # Corpo do e-mail
    body = f'''Opaa, segue o relatório de mercado do dia {datetime.now().strftime("%d/%m/%Y")}:

    * O Ibovespa teve o retorno de {ibovespa_return}, fechando em {market_data["IBOVESPA"].iloc[-1].round(2)}.
    * O Dólar teve o retorno de {dolar_return}, fechando em {market_data["DOLAR"].iloc[-1].round(2)}.
    * O S&P500 teve o retorno de {sp500_return}, fechando em {market_data["S&P500"].iloc[-1].round(2)}.
    * O BTC teve o retorno de {btc_return}, fechando em {market_data["BTC"].iloc[-1].round(2)}.
    * O EURO teve o retorno de {euro_return}, fechando em {market_data["EURO"].iloc[-1].round(2)}.
    * O NASDAQ teve o retorno de {nasdaq_return}, fechando em {market_data["NASDAQ"].iloc[-1].round(2)}.
    Segue em anexo a peformance dos ativos nos últimos 6 meses.

    Att,
    {config['email']['name']}
    '''
    msg.attach(MIMEText(body, 'plain'))

    # Anexar arquivos
    anexos = [
        os.path.join(output_path, "ibovespa.png"),
        os.path.join(output_path, "dolar.png"),
        os.path.join(output_path, "sp500.png"),
        os.path.join(output_path, "btc.png"),
        os.path.join(output_path, "euro.png"),
        os.path.join(output_path, "nasdaq.png")
    ]

    for anexo in anexos:
        with open(anexo, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(anexo)}')
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