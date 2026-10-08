# Vita — Checkpoint 02: IA Generativa com Python

**Integrante:** Julia Correa e Souza de Altino — **RM 564870**  
**Tema:** Saúde e bem-estar (IoB), com interpretação educacional de dados de wearables.  
**Disciplina:** Disruptive Architectures: IoT, IoB & Generative AI.  
**Base:** notebook de referência disponibilizado pelo professor.

## Objetivo

Desenvolver um assistente de IA generativa voltado a passos, sono e indicadores de dispositivos vestíveis, com instruções de comportamento (guardrails), comparação de temperaturas, memória de conversação, interface Gradio e uma API REST opcional.

## Implementação e evidências

| Etapa | Implementação | Evidência real nesta entrega |
|---|---|---|
| 1 — Guardrails | Três configurações de instruções para Hugging Face e Gemini | Respostas Gemini sobre passos e recusa de tema externo; erros de cota registrados |
| 2 — Temperaturas | Testes 0.0 e 1.0 nos dois provedores | Quatro respostas Gemini registradas, curtas; HF não executado |
| 3 — Memória e troca | Histórico compartilhado e escolha do provedor | Código disponível; teste de memória/troca não executado |
| 4 — Gradio | Chat, seletor de provedor, temperatura e exemplos | Interface aberta; captura em `prints/gradio.png`; sem conversa validada |
| 5 — FastAPI (bônus) | Endpoints e sessões independentes em `app_avaliacao.py` | Código disponível; execução real não realizada |

## Limitações encontradas

O Hugging Face retornou **HTTP 402 (Payment Required)** por falta de créditos de inferência. **A implementação foi mantida**, para que o professor possa executar com credenciais e créditos próprios, mas nenhuma resposta do Hugging Face foi simulada.

O Gemini (`gemini-2.5-flash`) respondeu a parte dos testes, mas depois apresentou **HTTP 429 (RESOURCE_EXHAUSTED)** ao atingir a cota. As respostas iniciais da etapa de temperatura foram curtas, limitando a comparação qualitativa. O limite de saída foi ajustado posteriormente, sem que se atribuíssem novas respostas aos testes já registrados.

O notebook conserva as saídas realmente produzidas no Colab e explicita os exercícios não validados. A captura da interface comprova os controles do Gradio, **não** o funcionamento de uma conversa completa.

## Estrutura

- `avaliacao_ia_generativa.ipynb`: código, saídas de execução e observações do grupo.
- `prints/gradio.png`: evidência visual da interface Gradio.
- `app_avaliacao.py`: implementação da API REST bônus.
- `requirements.txt`: dependências.

## Como executar

1. Abra o notebook no [Google Colab](https://colab.research.google.com/).
2. Cadastre `GEMINI_API_KEY` e `HF_TOKEN` em **Secrets** e habilite acesso ao notebook. Para testar HF é necessário token com permissão e créditos disponíveis.
3. Execute as células de instalação e configuração e, em seguida, as etapas desejadas. A versão de Gemini usada na execução foi `gemini-2.5-flash`.
4. Para abrir o Gradio, execute as células da etapa 4. A API bônus exige disponibilizar `app_avaliacao.py` no ambiente de execução.
5. As respostas podem variar conforme disponibilidade, modelo e cotas. Não publique credenciais no repositório.

**Aviso:** o assistente tem finalidade educacional; não realiza diagnóstico nem prescrição médica.
