# Roteiro da apresentação técnica de 45 minutos

Apresentação prevista em regras.docx para 17/10, com duração mínima de 40 e máxima de 50 minutos. Este roteiro soma 45 minutos, incluindo quatro minutos para arguição ou comentários. A organização geral da turma prevê cinco grupos, dois com quatro integrantes e três com três. Os nomes deste grupo não constam dos materiais. Distribuir os blocos entre os integrantes sem alterar o tempo total.

Cada bloco combina explicação e demonstração. Antes de uma consulta, mostrar a previsão, pedir que a turma a avalie e só então executar. Usar o dossiê para detalhes, sem lê-lo integralmente durante a apresentação.

| Bloco e slides | Tempo | Conteúdo e ação |
| --- | --- | --- |
| 1. Contexto, slides 1 a 3 | 4 min | Apresentar Atlas, objetivo de triagem e limites. Explicar ambiente físico e retrato discreto do programa. |
| 2. Conhecimento, slides 4 a 6 | 6 min | Explicar fonte, R01 a R04, redundância, ambiguidade, compressor e isolamento por ocorrência. |
| 3. Lógica, slides 7 e 8 | 5 min | Traduzir R01 e R04. Mostrar por que há 32 linhas e explicar as 29 implicações verdadeiras sem confundir com hipótese provada. |
| 4. Conflito e fluxo, slides 9 a 11 | 6 min | Prever C04, preservar duas hipóteses, justificar prioridade. Percorrer diagrama e diferenciar hipótese de estado. |
| 5. Prolog e inferência, slides 12 a 15 | 10 min | Executar C01 e C05, enumerar C04 com ; e ler trace. Explicar unificação e desfazer vínculos. |
| 6. Validação e evolução, slides 16 a 18 | 6 min | Mostrar matriz, Parte A, R05 e C07. Comparar previsão e execução nas bases separadas. |
| 7. Limitações e conclusão, slides 19 e 20 | 4 min | Explicar raciocínio causal versus dedução, mundo fechado, limitação pedagógica e resultado dos testes. |
| 8. Arguição e comentários | 4 min | Responder mudança de condição proposta pelo professor, prevendo antes de executar. |
| Total | 45 min | Caso não haja arguição, usar os quatro minutos para a dinâmica de alteração de um fato. |

## Preparação local

Abrir Apresentacao.pptx, Dossie.pdf e um terminal na pasta entrega. Confirmar `swipl --version`. Manter evidencias/trace_sucesso_c04.txt e trace_falha_c05.txt disponíveis para comparação. Se o projetor ou terminal falhar, mostrar as evidências reais previamente geradas, deixando claro que são registros da execução e não uma demonstração ao vivo.

## Demonstração da base original

No terminal:

```text
swipl -q -s prolog/base_original.pl
```

1. Antes de executar C01, dizer: “Esperamos sucesso porque T e C estão na mesma ocorrência e satisfazem R01”. Consultar `hipotese(c01,sobrecarga,r01).` e conferir true.
2. Antes de executar C05, dizer: “Esperamos falha porque a entrada informa corrente não elevada”. Consultar `hipotese(c05,sobrecarga,r01).` e explicar que false não é prova de ausência de sobrecarga.
3. Prever duas hipóteses para C04. Consultar `hipotese(c04,H,R).`. Após mecanica/r02, pedir próxima solução com `;` e obter condicao_critica/r04. Explicar por que a ordem no arquivo não decide prioridade.
4. Consultar `trilha(c04,condicao_critica,r04,E).` e ler os três sintomas. Relacionar a justificativa à frase da fonte e à inspeção prioritária.
5. Consultar C07, solicitando duas vezes a próxima solução com `;`. Prever três respostas antes de executar.

## Demonstração do trace

```prolog
leash(-all).
trace.
hipotese(c04,H,R).
```

Solicitar a segunda resposta com `;`. Mostrar o Fail da corrente em R01, o Exit de R02, o Redo para buscar alternativa, o Fail do tipo bomba em R03 e o Exit de R04. Para não perder tempo com todo o log, comparar os pontos com o registro integral. Encerrar o modo trace com `notrace.`.

Repetir `trace.` e consultar `hipotese(c05,sobrecarga,r01).`. Mostrar o sucesso da temperatura e a falha da corrente. Explicar que não há Redo visível nessa consulta específica, enquanto o C04 o demonstra. Finalizar com `notrace.` e `halt.`.

## Demonstração da evolução

Abrir uma sessão nova para cada versão. Não carregar duas bases alternativas na mesma sessão.

Parte A: antes de executar, prever que C06 passa a ter hipótese hidráulica quando ruido_anormal(c06) é acrescentado. Abrir `swipl -q -s prolog/base_fato_alterado.pl` e consultar `hipotese(c06,hidraulica,r03).`. Conferir true e explicar a mudança de estado.

Parte B: abrir `swipl -q -s prolog/base_regra_nova.pl`. Prever que C06 ainda não sustenta obstrução por faltar corrente e consultar `hipotese(c06,obstrucao,r05).`. Em sessão independente com base_regra_nova_teste.pl, prever true porque a entrada experimental fornece corrente elevada. Mostrar que nenhuma regra original foi alterada.

## Demonstração do fluxo completo

Se Python estiver disponível, executar `python ferramentas/triagem.py c04`. Ler as frases com R04 e R02 e percorrer Aguardando ocorrência, Em triagem, Hipóteses concorrentes, Encaminhado para inspeção prioritária. Explicar que o sistema não declara uma inspeção finalizada automaticamente.

Sem Python, carregar somente prolog/maquina_estados.pl e consultar as transições com os eventos correspondentes. A quantidade de regras provadas foi determinada antes pelas consultas de Prolog.

## Perguntas para a arguição

- Se retirar a temperatura de C04, R04 deixa de ser provada e R02 permanece. A classificação passa a Hipótese identificada, com hipótese mecânica e sem prioridade crítica pela base.
- Se acrescentar ruído a C06, R03 passa a ser provada na Parte A. Não é necessário alterar a regra.
- Se acrescentar apenas corrente a C06 na base original, R03 continua sem prova. Na base com R05, passa a haver suspeita de obstrução.
- Por que uma tabela pode ter a implicação verdadeira sem concluir K? Porque antecedente falso não ativa a regra, e a verdade vacuosa não fornece os requisitos de uma prova.
- Por que não usar sintomas diretamente em motor_m1? Porque isso reuniria fatos de ocorrências diferentes e alteraria indevidamente C05.
- O que acontece com compressor e falta de óleo? A fonte deixa o assunto fora do procedimento, então nada é derivável.
- É preciso escolher uma única hipótese em C04? A fonte não impõe exclusão. Preservamos ambas e damos a prioridade operacional que R04 exige.
- Por que efeito para causa não é dedução garantida? A causa é uma explicação possível dos sinais; a prova do programa vale para a classificação definida pela base.

## Tempo e encerramento

Verificar o relógio ao final dos blocos 2, 4 e 5. Não encurtar a demonstração prática para ler tabelas inteiras. Se houver atraso, usar os registros integrais para concentrar a explicação do trace. Respeitar o mínimo de 40 minutos mesmo sem perguntas. A conclusão deve conectar o trecho da fonte, a fórmula, a prova e a transição, com a ressalva de triagem inicial.
