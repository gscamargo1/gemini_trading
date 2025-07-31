import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# === Carrega e prepara o portefólio do Gemini ===
# Garanta que o caminho para o ficheiro está correto
ficheiro_portfolio = 'Data/gemini_portfolio_update.csv' 

try:
    gemini_df = pd.read_csv(ficheiro_portfolio)
except FileNotFoundError:
    print(f"Erro: O ficheiro '{ficheiro_portfolio}' não foi encontrado.")
    print("Por favor, execute o 'gemini_trading_script.py' pelo menos uma vez para gerar o ficheiro.")
    exit()

gemini_totais = gemini_df[gemini_df['Ticker'] == 'TOTAL'].copy()
gemini_totais['Data'] = pd.to_datetime(gemini_totais['Data'])

# Adiciona a linha de base para o investimento inicial
# Use a data do primeiro registo como data de início
data_inicio = gemini_totais['Data'].min()
# Assumimos um investimento inicial de R$1000, ajuste se necessário
investimento_inicial = 1000.00 

linha_base = pd.DataFrame({
    "Data": [data_inicio - pd.Timedelta(days=1)], # Um dia antes do primeiro registo
    "Patrimônio Total": [investimento_inicial]   
})
gemini_totais = pd.concat([linha_base, gemini_totais], ignore_index=True).sort_values("Data")


# === Descarrega e prepara os dados do Ibovespa (^BVSP) ===
data_fim = gemini_totais['Data'].max()
ibov = yf.download("^BVSP", start=data_inicio, end=data_fim + pd.Timedelta(days=1), progress=False)
ibov = ibov.reset_index()

# Normaliza o Ibovespa para um investimento inicial de R$1000
preco_inicial_ibov = ibov["Close"].iloc[0]
fator_escala_ibov = investimento_inicial / preco_inicial_ibov
ibov["Valor Normalizado"] = ibov["Close"] * fator_escala_ibov


# === Plota o Gráfico ===
plt.figure(figsize=(12, 7))
plt.style.use("seaborn-v0_8-whitegrid")

# Linha do Portefólio do Gemini
plt.plot(gemini_totais['Data'], gemini_totais["Patrimônio Total"], label=f"Portefólio Gemini (R${investimento_inicial:.2f} Investidos)", marker="o", color="blue", linewidth=2)

# Linha do Ibovespa
plt.plot(ibov['Date'], ibov["Valor Normalizado"], label=f"Ibovespa (R${investimento_inicial:.2f} Investidos)", marker="o", color="orange", linestyle='--', linewidth=2)

# Adiciona anotações de desempenho final
data_final_grafico = gemini_totais['Data'].iloc[-1]
valor_final_gemini = gemini_totais["Patrimônio Total"].iloc[-1]
valor_final_ibov = ibov["Valor Normalizado"].iloc[-1]

retorno_gemini = ((valor_final_gemini / investimento_inicial) - 1) * 100
retorno_ibov = ((valor_final_ibov / investimento_inicial) - 1) * 100

plt.text(data_final_grafico, valor_final_gemini, f" {retorno_gemini:+.2f}%", color="blue", fontsize=10, va='bottom')
plt.text(data_final_grafico, valor_final_ibov, f" {retorno_ibov:+.2f}%", color="orange", fontsize=10, va='bottom')


# === Configurações do Gráfico ===
plt.title("Desempenho: Portefólio Gemini vs. Ibovespa", fontsize=16)
plt.xlabel("Data", fontsize=12)
plt.ylabel(f"Valor do Investimento de R${investimento_inicial:.2f}", fontsize=12)
plt.xticks(rotation=15, ha='right')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Salva o gráfico como imagem
plt.savefig("desempenho_gemini_vs_ibovespa.png")

# Mostra o gráfico
plt.show()
