# Como Usar os Scripts

**Nota: NENHUM DOS PROMPTS É AUTOMATIZADO. ATUALIZAÇÕES MANUAIS E PESQUISA APROFUNDADA SÃO NECESSÁRIAS.**

---

## gemini_trading_script.py

Este script é o motor do portefólio. Ele processa as posições, executa ordens e gera relatórios diários para o Gemini. A ordem de execução das funções é muito importante e está listada no final.

Existem 4 funções principais:

### 1. Resultados Diários (`resultados_diarios`)

Obtém os dados de negociação do dia para cada ação no portefólio e para os benchmarks (Ibovespa e Índice Small Cap). Se for um dia sem pregão, ele usará os dados do dia anterior.

Ele irá imprimir o portefólio atualizado e o saldo em caixa. **Se alguma ordem manual foi executada, certifique-se de copiar ambos e atualizar o código para o próximo dia.**

### 2. Processar Portefólio (`processar_portfolio`)

Esta função é mais simples. Lida automaticamente com os stop-losses (acionando vendas se o preço cair para o nível definido) e atualiza o ficheiro `gemini_portfolio_update.csv` com os dados do dia.

### 3. Compra e Venda Manual (`logar_compra_manual` / `logar_venda_manual`)

Ambas as funções requerem parâmetros e devem ser adicionadas manualmente ao script quando o Gemini decidir fazer uma transação.

#### Compra Manual (`logar_compra_manual`):

A função tem a seguinte assinatura:
`logar_compra_manual(preco_compra, acoes, ticker, caixa, stoploss, portfolio)`

Suponha que eu queira comprar 100 ações de "ITSA4" (Itaúsa) a R$ 10,00 por ação, com um stop-loss de R$ 9,00.

A chamada da função seria assim:
```python
caixa, gemini_portfolio = logar_compra_manual(10.00, 100, "ITSA4", caixa, 9.00, gemini_portfolio)
