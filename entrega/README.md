# Projeto Manutenção Inteligente

Entrega da Situação de Aprendizagem 02. Comece por documentacao/Dossie.pdf, leia o checklist e use a apresentação com o roteiro de 45 minutos. As fontes originais permanecem na pasta superior.

## Estrutura

```text
entrega/
  README.md
  documentacao/
    Dossie.pdf
    Dossie.md
    Checklist_final.md
    maquina_estados.mmd
    maquina_estados.svg
  prolog/
    base_original.pl
    base_fato_alterado.pl
    base_regra_nova.pl
    base_regra_nova_teste.pl
    maquina_estados.pl
  apresentacao/
    Apresentacao.pptx
    Roteiro_45_minutos.md
  evidencias/
    consultas_c01_c07.txt
    trace_sucesso_c04.txt
    trace_falha_c05.txt
    resultados.json
    testes.txt
  ferramentas/
    triagem.py
    testar.py
```

## Executar diretamente no SWI-Prolog

Requisito principal: SWI-Prolog instalado. No terminal, a partir da pasta entrega:

```text
swipl -q -s prolog/base_original.pl
```

No prompt `?-`, digite as consultas, sem copiar o próprio prompt:

```prolog
hipotese(c01, sobrecarga, r01).
hipotese(c04, H, R).
```

No C04, pressione `;` depois da primeira resposta para obter a segunda. A primeira é mecanica/r02 e a segunda condicao_critica/r04. Quando o interpretador encerra a consulta com ponto final, não digite outro `;`. Consulte C07 da mesma forma e solicite duas vezes a próxima solução para obter três hipóteses.

```prolog
hipotese(c05, sobrecarga, r01).
hipotese(c06, hidraulica, r03).
trilha(c03, hidraulica, r03, Evidencias).
halt.
```

C05 e C06 retornam false: não foi possível provar. C03 retorna evidencias(bomba,fluxo_reduzido,ruido_anormal).

## Observar o motor

Em uma sessão com base_original.pl:

```prolog
leash(-all).
trace.
hipotese(c04, H, R).
```

Solicite a segunda resposta com `;`. Depois execute `notrace.`. Para a falha, repita `trace.` e consulte `hipotese(c05,sobrecarga,r01).`. `leash(-all)` mostra as portas sem interromper a cada passo. Os registros integrais já estão em evidencias.

## Evoluções independentes

Encerre a sessão anterior com `halt.` e abra uma sessão nova para cada arquivo:

```text
swipl -q -s prolog/base_fato_alterado.pl
swipl -q -s prolog/base_regra_nova.pl
swipl -q -s prolog/base_regra_nova_teste.pl
```

Parte A: consulte `hipotese(c06,hidraulica,r03).`, que sucede com o ruído acrescentado. Parte B, só regra nova: `hipotese(c06,obstrucao,r05).` falha porque falta corrente. Parte B, entrada positiva: a mesma consulta sucede em base_regra_nova_teste.pl. Nunca carregue as bases alternativas juntas.

## Consultar o fluxo

```text
swipl -q -s prolog/maquina_estados.pl
```

```prolog
transicao(em_triagem, varias_regras_satisfeitas, Proximo).
transicao(hipoteses_concorrentes, criterio_aplicado_prioritario, Proximo).
transicao(encaminhado_para_inspecao, inspecao_finalizada, Proximo).
```

As respostas são hipoteses_concorrentes, encaminhado_para_inspecao e encerrado. O último evento deve ser informado somente quando a inspeção terminar.

## Interface opcional e testes

Python 3.9 ou posterior, somente biblioteca padrão, com SWI-Prolog no PATH ou no caminho padrão do Windows. Na pasta entrega:

```text
python ferramentas/triagem.py c04
python ferramentas/triagem.py c06 --versao fato
python ferramentas/triagem.py c06 --versao regra_teste
python ferramentas/testar.py
```

A interface mostra cada hipótese com sintomas e regra, preserva todas as provas, prioriza a condição crítica e mostra a sequência de estados. A classificação e a trilha são consultadas no Prolog; Python somente apresenta e controla os eventos. Sem Python, todas as operações obrigatórias podem ser demonstradas pelas consultas acima.

O teste dura aproximadamente um minuto, conforme o computador, e atualiza somente evidencias. Uma falha interrompe a execução com descrição. O projeto não exige servidor, banco de dados, pacote Python ou acesso à internet.

## Apresentação e informações ausentes

regras.docx prevê desenvolvimento em 26/09 e 03/10 e apresentação em 17/10, entre 40 e 50 minutos. O roteiro soma 45 minutos, com demonstrações práticas, predição antes da execução e discussão do raciocínio. Os documentos não exigem um formato de dossiê específico: foram produzidos PDF e Markdown editável. Não há nomes dos integrantes, número do grupo ou divisão individual de falas nos materiais; esses dados não foram inventados. A apresentação oral e as arguições serão realizadas pelo grupo.

As regras e cenários são simplificações pedagógicas. Todas as saídas são triagem inicial, não laudos ou procedimentos de manutenção industrial.
