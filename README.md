# Detecção de tentativas repetidas de autenticação SSH

Identifica sequências de falhas de autenticação e sinaliza sucessos após o limiar, a partir de um CSV sintético.

**Arquivos principais**

- [detectar.py](<detectar.py>)
- [eventos.csv](<eventos.csv>)
- [esperado.txt](<esperado.txt>)

Este exercício defensivo processa um CSV com horários ISO 8601 em UTC, conta, origem e resultado. O cenário usa contas fictícias e endereços reservados para documentação.

Execute com Python 3.10 ou posterior.

```sh
python3 detectar.py eventos.csv
```

O detector agrupa por conta e origem. Ao receber cinco falhas em cinco minutos, gera um alerta. Se a mesma combinação autenticar com sucesso enquanto as cinco falhas ainda estiverem na janela, gera um segundo alerta para priorizar a análise da sessão. Um sucesso encerra a sequência.

O exemplo confirma dois resultados. As duas falhas da conta de Ana seguidas de sucesso ficam abaixo do limiar. A conta de Bruno gera um alerta na quinta falha e outro no sucesso seguinte. A saída esperada está em `esperado.txt`.

Para investigar, confirme se origem, horário e identidade coincidem com atividade autorizada. Preserve os registros e encaminhe a revisão da sessão se houver sinais de acesso indevido. Um alerta é evidência para triagem. Campanhas distribuídas entre origens ou contas podem exigir regras adicionais.

Esta implementação opera sobre registros de exemplo e corresponde à parte defensiva do tema.
