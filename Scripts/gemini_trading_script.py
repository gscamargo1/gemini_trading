import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import numpy as np

# === Atualiza os logs do portefólio ===
def processar_portfolio(portfolio, caixa_inicial):
    resultados = []
    valor_total_acoes = 0
    pnl_total = 0
    caixa = caixa_inicial
    
    # Adiciona o sufixo '.SA' aos tickers para o yfinance
    tickers_sa = [f"{ticker}.SA" for ticker in portfolio["ticker"]]
    dados_yf = yf.download(tickers_sa, period="1d", progress=False)

    for _, acao in portfolio.iterrows():
        ticker = acao["ticker"]
        ticker_sa = f"{ticker}.SA"
        
        # Garante que as colunas sejam acessíveis
        if isinstance(dados_yf.columns, pd.MultiIndex):
            dados_dia = dados_yf.xs(ticker_sa, axis=1, level=1)
        else:
            dados_dia = dados_yf

        acoes = int(acao["acoes"])
        custo = acao["preco_compra"]
        stop = acao["stop_loss"]

        if dados_dia.empty or dados_dia["Close"].iloc[-1] is None:
            print(f"Sem dados para {ticker}")
            linha = {
                "Data": hoje, "Ticker": ticker, "Ações": acoes, "Custo Base": custo,
                "Stop Loss": stop, "Preço Atual": "", "Valor Total": "", "PnL": "",
                "Ação": "SEM DADOS", "Saldo Caixa": "", "Patrimônio Total": ""
            }
        else:
            preco = round(dados_dia["Close"].iloc[-1], 2)
            valor = round(preco * acoes, 2)
            pnl = round((preco - custo) * acoes, 2)

            if preco <= stop:
                acao_tomada = "VENDER - Stop Loss Acionado"
                caixa += valor
                logar_venda(ticker, acoes, preco, custo, pnl)
            else:
                acao_tomada = "MANTER"
                valor_total_acoes += valor
                pnl_total += pnl

            linha = {
                "Data": hoje, "Ticker": ticker, "Ações": acoes, "Custo Base": custo,
                "Stop Loss": stop, "Preço Atual": preco, "Valor Total": valor, "PnL": pnl,
                "Ação": acao_tomada, "Saldo Caixa": "", "Patrimônio Total": ""
            }

        resultados.append(linha)

    # === Adiciona a linha de TOTAL ===
    linha_total = {
        "Data": hoje, "Ticker": "TOTAL", "Ações": "", "Custo Base": "", "Stop Loss": "",
        "Preço Atual": "", "Valor Total": round(valor_total_acoes, 2), "PnL": round(pnl_total, 2),
        "Ação": "", "Saldo Caixa": round(caixa, 2), "Patrimônio Total": round(valor_total_acoes + caixa, 2)
    }
    resultados.append(linha_total)

    # === Salva em CSV ===
    ficheiro = "gemini_portfolio_update.csv"
    df = pd.DataFrame(resultados)

    if os.path.exists(ficheiro):
        existente = pd.read_csv(ficheiro)
        existente = existente[existente["Data"] != hoje]
        df = pd.concat([existente, df], ignore_index=True)

    df.to_csv(ficheiro, index=False)
    # Retorna o DataFrame do portfólio para o caso de vendas automáticas
    portfolio_atualizado = portfolio[~portfolio['ticker'].isin([r['Ticker'] for r in resultados if "VENDER" in r['Ação']])]
    return portfolio_atualizado

# === Logger de Vendas (para stop-loss) ===
def logar_venda(ticker, acoes, preco, custo, pnl):
    log = {
        "Data": hoje, "Ticker": ticker, "Ações Vendidas": acoes, "Preço Venda": preco,
        "Custo Base": custo, "PnL": pnl, "Motivo": "VENDA AUTOMÁTICA - STOPLOSS ACIONADO"
    }

    ficheiro = "gemini_trade_log.csv"
    if os.path.exists(ficheiro):
        df = pd.read_csv(ficheiro)
        df = pd.concat([df, pd.DataFrame([log])], ignore_index=True)
    else:
        df = pd.DataFrame([log])
    df.to_csv(ficheiro, index=False)

# === Logger de Compra Manual ===
def logar_compra_manual(preco_compra, acoes, ticker, caixa, stoploss, portfolio):
    # Lógica de verificação e download de dados...
    if preco_compra * acoes > caixa:
        raise SystemExit(f"Erro: você tem R${caixa:.2f} mas está a tentar gastar R${preco_compra * acoes:.2f}.")

    log = {
        "Data": hoje, "Ticker": ticker, "Ações Compradas": acoes, "Preço Compra": preco_compra,
        "Custo Total": preco_compra * acoes, "PnL": 0.0, "Motivo": "COMPRA MANUAL - Nova posição"
    }

    ficheiro = "gemini_trade_log.csv"
    if os.path.exists(ficheiro):
        df = pd.read_csv(ficheiro)
        df = pd.concat([df, pd.DataFrame([log])], ignore_index=True)
    else:
        df = pd.DataFrame([log])
    df.to_csv(ficheiro, index=False)

    novo_trade = {"ticker": ticker, "acoes": acoes, "stop_loss": stoploss, "preco_compra": preco_compra}
    portfolio = pd.concat([portfolio, pd.DataFrame([novo_trade])], ignore_index=True)
    caixa -= acoes * preco_compra
    return caixa, portfolio

# === Logger de Venda Manual ===
def logar_venda_manual(preco_venda, acoes_vendidas, ticker, caixa, portfolio):
    # Lógica de verificação...
    linha_ticker = portfolio[portfolio['ticker'] == ticker]
    total_acoes = int(linha_ticker['acoes'].item())
    if acoes_vendidas > total_acoes:
        raise ValueError(f"Você está a tentar vender {acoes_vendidas} mas possui apenas {total_acoes}.")
    
    motivo = input("Por que está a vender esta posição? ")
    preco_compra = float(linha_ticker['preco_compra'].item())
    custo_base = preco_compra * acoes_vendidas
    pnl = (preco_venda * acoes_vendidas) - custo_base
    
    log = {
        "Data": hoje, "Ticker": ticker, "Ações Vendidas": acoes_vendidas, "Preço Venda": preco_venda,
        "Custo Base": custo_base, "PnL": pnl, "Motivo": f"VENDA MANUAL - {motivo}"
    }

    ficheiro = "gemini_trade_log.csv"
    # Lógica para salvar log...
    df_log = pd.DataFrame([log])
    if os.path.exists(ficheiro):
        df_existente = pd.read_csv(ficheiro)
        df_final = pd.concat([df_existente, df_log], ignore_index=True)
    else:
        df_final = df_log
    df_final.to_csv(ficheiro, index=False)
    
    if total_acoes == acoes_vendidas:
        portfolio = portfolio[portfolio["ticker"] != ticker]
    else:
        portfolio.loc[portfolio['ticker'] == ticker, 'acoes'] = total_acoes - acoes_vendidas
        
    caixa += acoes_vendidas * preco_venda
    return caixa, portfolio

# === Relatório diário para o Gemini ===
def resultados_diarios(portfolio, caixa):
    print(f"\n--- Relatório para o Gemini - {hoje} ---")
    
    # Adiciona benchmarks brasileiros
    tickers_interesse = list(portfolio["ticker"]) + ["^BVSP", "SMLL.SA"]
    tickers_interesse_sa = [f"{t}.SA" if not t.startswith('^') else t for t in tickers_interesse]
    dados_yf = yf.download(tickers_interesse_sa, period="2d", progress=False)

    for ticker in tickers_interesse:
        ticker_yf = f"{ticker}.SA" if not ticker.startswith('^') else ticker
        try:
            preco = float(dados_yf['Close'][ticker_yf].iloc[-1])
            preco_anterior = float(dados_yf['Close'][ticker_yf].iloc[-2])
            variacao = ((preco - preco_anterior) / preco_anterior) * 100
            volume = float(dados_yf['Volume'][ticker_yf].iloc[-1])
            print(f"{ticker} - Preço de Fecho: R${preco:.2f} ({variacao:+.2f}%) | Volume: {volume:,.0f}")
        except Exception as e:
            print(f"Não foi possível obter dados para {ticker}. Erro: {e}")

    df_portfolio = pd.read_csv("gemini_portfolio_update.csv")
    total_final = df_portfolio[df_portfolio['Ticker'] == 'TOTAL'].iloc[-1]
    patrimonio_final = float(total_final['Patrimônio Total'])
    
    print(f"\nPatrimônio Final do Gemini: R${patrimonio_final:.2f}")
    
    # Comparação com o Ibovespa
    ibov = yf.download("^BVSP", start="2025-07-31", end=pd.to_datetime(hoje) + pd.Timedelta(days=1), progress=False)
    retorno_ibov = (ibov["Close"].iloc[-1] / ibov["Close"].iloc[0] - 1) * 100
    
    print(f"\nRetorno do Ibovespa no período: {retorno_ibov:+.2f}%")
    
    print("\n--- Portefólio Atual ---")
    print(portfolio.to_string(index=False))
    print(f"Saldo em Caixa: R${caixa:.2f}")
    
    print("\nGemini, aqui está a sua atualização. Pode fazer as alterações que julgar necessárias.")

# --- ORDEM DE EXECUÇÃO DIÁRIA ---

# 1. Adicionar aqui quaisquer ordens manuais decididas pelo Gemini
# Exemplo: caixa, gemini_portfolio = logar_venda_manual(13.00, 25, "MGLU3", caixa, gemini_portfolio)
# Exemplo: caixa, gemini_portfolio = logar_compra_manual(18.00, 10, "ITUB4", caixa, 16.50, gemini_portfolio)

# 2. Processar o portefólio (atualiza preços e executa stop-loss)
gemini_portfolio = processar_portfolio(gemini_portfolio, caixa)

# 3. Gerar o relatório diário para a análise do Gemini
resultados_diarios(gemini_portfolio, caixa)
