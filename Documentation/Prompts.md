# Prompts: Gemini Trading

Este ficheiro documenta os prompts utilizados para interagir com o Gemini na gestão do portefólio de micro-capitalização brasileiro.

---

### Prompt 1 (Pesquisa Inicial):
“Você é um estratega de portefólio de nível profissional. Tenho exatamente R$ 1.000 e quero que construa o portefólio de ações mais forte possível, utilizando apenas posições com ações inteiras de micro-capitalização listadas na B3 (Brasil). O seu objetivo é gerar o máximo retorno de hoje (data de início) até daqui a 6 meses (data final). Este é o seu prazo; você não pode tomar decisões após a data final. Dentro destas restrições, a escolha entre catalisadores de curto prazo ou posições de longo prazo é sua. Eu irei atualizá-lo diariamente sobre a cotação de cada ação e perguntarei se deseja alterar algo. Você tem controlo total sobre o dimensionamento da posição, gestão de risco, colocação de stop-loss e tipos de ordem. As suas decisões devem ser baseadas numa pesquisa profunda e verificável que você acredite que será positiva para a conta. Agora, use a sua capacidade de pesquisa e crie o seu portefólio.”

---

### Prompt para Reavaliação Semanal (Deep Research):
“Você é um analista de portefólio de nível profissional. Use a sua capacidade de pesquisa aprofundada para reavaliar o seu portefólio. Você pode verificar as posições atuais e/ou encontrar novas ações. Lembre-se, você tem controlo total, desde que sejam micro-capitalizações brasileiras (comprar, vender, etc.). Você pode comprar qualquer ativo desde que tenha o capital disponível (neste momento, tem X em caixa). A sua tese para o portefólio atual era a seguinte: (inserir aqui o resumo da tese da semana anterior). Lembre-se que o seu único objetivo é gerar alfa. No final, por favor, escreva um breve resumo para que eu possa ter uma revisão da tese para a próxima semana.”

---

### Prompt para Atualizações Diárias (Sem Pesquisa Aprofundada):
“Você é um analista de portefólio de nível profissional. Estamos na semana X, dia Y. Este é o seu portefólio atual: (dicionário ou lista do portefólio), com (valor em caixa) em caixa. Atualmente, este é o seu retorno em relação ao mercado: (inserir retorno vs. Ibovespa). A sua tese da semana passada para as posições atuais foi esta: (inserir resumo da última tese). Com base nos dados de hoje, você gostaria de fazer alguma alteração?”

---
**Nota:** Estes prompts foram desenhados para serem consistentes e fornecer ao Gemini todo o contexto necessário para tomar decisões informadas, mantendo o foco no objetivo principal do experimento. Sinta-se à vontade para os adaptar conforme necessário.
