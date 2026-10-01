# Dossiê técnico do Projeto Manutenção Inteligente

Situação de Aprendizagem 02. Sistema especialista para triagem de ocorrências de manutenção industrial da Indústria Atlas. Integração das unidades Lógica para Inteligência Artificial e Sistemas Baseados em Conhecimento, Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe.

O protótipo representa sintomas observados, aplica conhecimento explícito em Prolog, apresenta hipóteses com sua justificativa e controla a evolução do chamado por uma máquina de estados. A validação encontrou os resultados previstos nos seis casos fornecidos e no caso C07 criado para o projeto. O C04 sustenta duas hipóteses, que são preservadas, com encaminhamento prioritário por condição crítica. Os cenários e regras são pedagógicos. Toda hipótese é triagem inicial, não um laudo nem um procedimento real de manutenção.

## Planejamento e base documental

A leitura precedeu a implementação: foram estudados todos os seis PDFs de aulas, depois as nove páginas de AtividadeAvaliativa].pdf e integralmente regras.docx. O escopo é um protótipo simples, sem dados externos e sem completar lacunas do técnico. Não foram acrescentados limiares numéricos, causas reais, sensores, procedimentos de reparo ou regras para compressores.

O plano adotado foi: caracterizar o problema; extrair R01 a R04; registrar decisões de modelagem; formalizar e construir a tabela-verdade; prever C01 a C06; definir o conflito; modelar o chamado; implementar fatos e regras; consultar e ler o trace; validar as representações; preservar a base original e criar versões A e B; criar C07; preparar a apresentação e rever os documentos obrigatórios. O checklist final está em Checklist_final.md.

| Material estudado | Conteúdos e aplicação no projeto |
| --- | --- |
| Aula_01.pdf, 43 páginas | Indução, analogia e dedução; validade das premissas; revisão de conhecimento; regras explícitas e validação. Exemplos das chaves, manutenção preditiva e controle de acesso. |
| Aula_02.pdf, 58 páginas | Proposições, sintaxe, semântica, conectivos, necessidade e suficiência, tabelas-verdade e limites da validação. Exemplos do alerta industrial e acesso ao laboratório. |
| Construindo Expressões.pdf, 45 páginas | Método de seis passos, tradução reversa, regras numeradas e KB modular. Exemplos de acesso, reembolso e auditoria de decisões. |
| Maquinas_de_Estado (1).pdf, 53 páginas | Estado, evento, guard, ação, função de transição, Moore e Mealy, diagrama e tabela. Exemplos de semáforo, pedido e validação de respostas. |
| Aula01_Fundamentos_e_Contexto_Histórico_da_IA.pdf, 13 páginas | IA simbólica; base, motor e explicação. DENDRAL, MYCIN, XCON e ELIZA. MYCIN é a referência de tarefa mais próxima. |
| PROLOG_PARTE_1.pdf, 25 páginas | Fatos, regras, consultas, variáveis compartilhadas, unificação, backtracking e mundo fechado. Exemplos de família e recomendação de livros. |

Ferramentas mencionadas nas aulas incluem Google Colab, Python, SWI-Prolog, VSCode e ferramentas de IA. A implementação principal usa SWI-Prolog. Uma interface Python opcional automatiza consultas, explicações e eventos do chamado, mantendo o conhecimento em Prolog. Os arquivos de base usam somente fatos, regras, variáveis, unificação, conjunção e termos estruturados. Não há listas, recursão, corte ou predicados de negação no código Prolog. `trace`, `leash`, `write` e `halt` aparecem apenas como comandos de observação ou execução.

## Etapa 1 Caracterização do problema

| Dimensão | Classificação | Justificativa |
| --- | --- | --- |
| Observabilidade do ambiente | Parcialmente observável | Os sintomas relatados não revelam diretamente a causa nem o estado completo do equipamento. |
| Determinismo do ambiente | Estocástico, na relação observação e causa | Um conjunto de sintomas não garante uma causa única; o enunciado não fornece um modelo probabilístico numérico. |
| Evolução do ambiente | Dinâmico | Um equipamento pode mudar de condição durante o atendimento. |
| Natureza do ambiente | Contínuo, com representação discreta | Temperatura, corrente, fluxo e vibração são grandezas contínuas, convertidas pelo cenário em categorias observáveis. |
| Tarefa cognitiva | Classificação diagnóstica inicial e explicação | O protótipo sugere categorias de ocorrência a partir de sintomas e justifica o encaminhamento. |
| Sistema clássico próximo | MYCIN | O exemplo estudado relaciona observações e regras a hipóteses e oferece explicação. A proximidade é de tarefa e arquitetura, não de domínio. |

As classificações do ambiente não devem ser confundidas com a execução do programa. Uma consulta à mesma versão da base é determinística; os fatos de cada caso formam um retrato estático; o programa usa átomos discretos. Isso não transforma o equipamento físico em um ambiente completamente observável, estático ou discreto.

A passagem de efeito observado para causa possível é, precisamente, uma inferência abdutiva: propõe uma explicação plausível. O enunciado pede uma escolha entre as três formas vistas nas aulas, mas nenhuma delas descreve exatamente essa inversão causal. A indução explica a construção ou generalização de uma associação empírica pelo especialista; a analogia transferiria conhecimento de um caso semelhante; a dedução não autoriza inverter causa e efeito. Se a classificação ficar limitada às três, a aproximação é indutiva no sentido de hipótese provável fundada em regularidades, com essa ressalva conceitual. A transcrição não informa como o técnico aprendeu as associações, portanto não permite afirmar um histórico específico de aprendizagem.

Depois de declarada uma regra como R01, o motor usa dedução: dos fatos T e C e da regra que os relaciona à hipótese S, deriva a classificação S. Essa prova demonstra uma hipótese sustentada pela base pedagógica, não a causa física real. A hipótese de sobrecarga não prova que o equipamento esteja efetivamente em sobrecarga. Tampouco se pode usar a falácia de afirmação do consequente para justificar isso.

## Etapa 2 Extração e decisões de modelagem

Os trechos abaixo pertencem à transcrição fornecida, na página 2 do enunciado. R01 a R04 mantêm a mesma identificação na documentação, no código e na validação.

| Regra | Redação estruturada | Trecho que a sustenta |
| --- | --- | --- |
| R01 | Temperatura elevada e corrente elevada sustentam suspeita de sobrecarga. | “temperatura alta junto com corrente alta” e “suspeita de sobrecarga” |
| R02 | Vibração elevada e ruído anormal sustentam suspeita mecânica. | “vibração alta e barulho estranho ao mesmo tempo, a suspeita é mecânica” |
| R03 | Em uma bomba, fluxo reduzido e ruído anormal sustentam suspeita hidráulica. | “No caso das bombas, fluxo baixo com barulho estranho aponta para problema hidráulico” |
| R04 | Temperatura elevada, vibração elevada e ruído anormal sustentam condição crítica e encaminhamento para inspeção prioritária. | “temperatura alta, vibração alta e barulho estranho ao mesmo tempo” e “condição crítica e manda para inspeção prioritária” |

| Ponto | Trecho ou situação | Decisão e justificativa |
| --- | --- | --- |
| Redundância | “vibração alta sozinha não é suspeita mecânica, precisa vir com o barulho” e “só classifico se todos os sinais da regra estiverem presentes” | Exigir a conjunção dos sinais. Não criar uma regra que prove ausência de causa mecânica quando falta ruído. A repetição reforça o antecedente de R02. |
| Ambiguidade | “vibração alta sozinha não é suspeita mecânica” | Interpretar como insuficiência para sustentar a hipótese por R02, coerente com O1 e O2. A leitura alternativa como negação física universal excederia a fonte e exigiria outro conhecimento. |
| Outra ambiguidade de alcance | “só classifico se todos os sinais da regra estiverem presentes” | Usar requisitos positivos para cada prova, preservando as regras suficientes descritas pelo técnico. Não converter a frase em bicondicional sobre a existência da causa no mundo real. |
| Lacuna | “compressor com falta de óleo” e “esse procedimento ainda não cobre compressor” | Não criar equipamento, sintoma ou regra para compressor. Nada é derivável sobre esse assunto com a fonte disponível. |
| Normalização de termos | Temperatura alta, corrente alta, barulho estranho e fluxo baixo | Usar temperatura elevada, corrente elevada, ruído anormal e fluxo reduzido, conforme a tabela oficial de sintomas. |
| Isolamento de casos | M1 aparece em C01, C02 e C05 | Sintomas recebem o identificador da ocorrência. Agregar tudo em motor_m1 contaminaria os casos e criaria hipóteses indevidas. |
| Escopo de bomba | “No caso das bombas” | R03 exige que o equipamento associado à ocorrência seja do tipo bomba. R01, R02 e R04 não recebem restrição de tipo não prevista. |

As orientações O1 a O5 tratam da interpretação dos resultados; não viraram regras do domínio. Não se declarou nenhuma hipótese diretamente como fato.

## Etapa 3 Formalização e verificação semântica

Cada proposição é avaliada para uma ocorrência específica. O fato de o equipamento ser bomba participa somente da regra que o exige.

| Símbolo | Significado |
| --- | --- |
| T | A ocorrência apresenta temperatura elevada. |
| V | A ocorrência apresenta vibração elevada. |
| N | A ocorrência apresenta ruído anormal. |
| C | A ocorrência apresenta corrente elevada. |
| F | A ocorrência apresenta fluxo reduzido. |
| B | O equipamento da ocorrência é bomba. |
| S | A triagem sustenta hipótese de sobrecarga. |
| M | A triagem sustenta hipótese mecânica. |
| H | A triagem sustenta hipótese hidráulica. |
| K | A triagem sustenta classificação de condição crítica. |
| I | O chamado recebe encaminhamento para inspeção prioritária. |

| Regra | Proposições e expressão | Conectivos e leitura |
| --- | --- | --- |
| R01 | (T ∧ C) → S | Conjunção e implicação. Se há os dois sintomas, a hipótese de sobrecarga é sustentada. |
| R02 | (V ∧ N) → M | Conjunção e implicação. Vibração com ruído sustenta hipótese mecânica. |
| R03 | (B ∧ F ∧ N) → H | Conjunções e implicação. Ser bomba, ter fluxo reduzido e ruído sustenta hipótese hidráulica. |
| R04 | (T ∧ V ∧ N) → (K ∧ I) | Conjunções e implicação. Os três sintomas sustentam condição crítica e inspeção prioritária. |

R03 e R04 empatam no maior número de proposições do antecedente: três. Escolhemos R04, que explicita os dois resultados da fala do técnico. No código Prolog, `hipotese/3` prova K; a interface e a máquina de estados realizam I. I é uma ação do chamado, não uma segunda hipótese. A validação cruzada verifica os dois resultados.

A tabela completa de R04 tem cinco proposições distintas: T, V, N, K e I. Portanto tem 2⁵ = 32 linhas. Não se pode reduzir a tabela a oito linhas calculando apenas K: a atividade solicita a implicação completa, que também avalia o consequente. V significa verdadeiro e F significa falso somente nesta tabela bivalente.

| Linha | T | V | N | K | I | T∧V∧N | K∧I | R04 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | V | V | V | V | V | V | V | V |
| 2 | V | V | V | V | F | V | F | F |
| 3 | V | V | V | F | V | V | F | F |
| 4 | V | V | V | F | F | V | F | F |
| 5 | V | V | F | V | V | F | V | V |
| 6 | V | V | F | V | F | F | F | V |
| 7 | V | V | F | F | V | F | F | V |
| 8 | V | V | F | F | F | F | F | V |
| 9 | V | F | V | V | V | F | V | V |
| 10 | V | F | V | V | F | F | F | V |
| 11 | V | F | V | F | V | F | F | V |
| 12 | V | F | V | F | F | F | F | V |
| 13 | V | F | F | V | V | F | V | V |
| 14 | V | F | F | V | F | F | F | V |
| 15 | V | F | F | F | V | F | F | V |
| 16 | V | F | F | F | F | F | F | V |
| 17 | F | V | V | V | V | F | V | V |
| 18 | F | V | V | V | F | F | F | V |
| 19 | F | V | V | F | V | F | F | V |
| 20 | F | V | V | F | F | F | F | V |
| 21 | F | V | F | V | V | F | V | V |
| 22 | F | V | F | V | F | F | F | V |
| 23 | F | V | F | F | V | F | F | V |
| 24 | F | V | F | F | F | F | F | V |
| 25 | F | F | V | V | V | F | V | V |
| 26 | F | F | V | V | F | F | F | V |
| 27 | F | F | V | F | V | F | F | V |
| 28 | F | F | V | F | F | F | F | V |
| 29 | F | F | F | V | V | F | V | V |
| 30 | F | F | F | V | F | F | F | V |
| 31 | F | F | F | F | V | F | F | V |
| 32 | F | F | F | F | F | F | F | V |

O antecedente é verdadeiro em 4 linhas, a implicação inteira é verdadeira em 29 e falsa em 3. As três violações têm T=V=N=V e pelo menos um entre K e I falso. Nas 28 linhas com antecedente falso, a regra não impõe o consequente, e a implicação é verdadeira por verdade vacuosa. Isso significa ausência de violação dessa obrigação nessa linha; não significa que K foi demonstrado, que a hipótese foi descartada ou que a causa oposta foi provada. O teste de aplicabilidade do programa verifica o antecedente; não confunde a verdade da implicação com autorização para inferir sua conclusão.

## Etapa 4 Validação lógica dos casos e conflito

Na tabela seguinte, `1` significa condição estabelecida, `0e` significa informação explicitamente negativa e `?` significa não informado. Para procurar uma prova em Prolog, tanto `0e` quanto `?` deixam o objetivo positivo sem sucesso. O valor operacional 0 dessa busca não equivale a um fato negativo sobre o mundo. B=0 é conhecido para motor e ventilador. Cada caso avalia todas as quatro regras, inclusive as que não se tornam aplicáveis.

| Caso | T,V,N,C,F,B | Antecedentes de R01,R02,R03,R04 na busca | Regras efetivamente aplicáveis | Hipóteses sustentadas |
| --- | --- | --- | --- | --- |
| C01 | 1,?, ?,1,?,0 | 1,0,0,0 | R01 | Sobrecarga |
| C02 | ?,1,1,?,?,0 | 0,1,0,0 | R02 | Mecânica |
| C03 | ?,?,1,?,1,1 | 0,0,1,0 | R03 | Hidráulica |
| C04 | 1,1,1,?,?,0 | 0,1,0,1 | R02 e R04 | Mecânica e condição crítica |
| C05 | 1,?,?,0e,?,0 | 0,0,0,0 | Nenhuma | Nenhuma demonstrável |
| C06 | ?,?,?,?,1,1 | 0,0,0,0 | Nenhuma | Nenhuma demonstrável |

C01 não sustenta as demais hipóteses porque faltam seus requisitos. C02 não sustenta condição crítica sem temperatura informada. C03 não sustenta outras hipóteses sem seus sintomas. C04 não sustenta sobrecarga sem corrente informada e não sustenta hipótese hidráulica porque é ventilador. C05 falha em corrente elevada; C06 falha em ruído anormal. Em todos esses casos, ausência de prova de uma hipótese não é prova de sua negação.

No C04, o conjunto de conflito é {R02, R04}. R02 sustenta suspeita mecânica; R04 sustenta condição crítica e prioridade de inspeção. As classificações são compatíveis: uma informa uma categoria provável de ocorrência e a outra uma condição de criticidade. A fonte não afirma exclusão mútua. Conflito aqui significa mais de uma regra aplicável, não uma contradição lógica.

O critério adotado preserva todas as hipóteses e exibe a condição crítica primeiro. A prioridade de inspeção decorrente de R04 é conhecimento explícito da fonte. Já preservar os resultados e ordenar sua apresentação é uma decisão de engenharia, implementada fora da base de regras do domínio na interface opcional. A ordem das cláusulas de Prolog apenas determina a ordem de descoberta, não a gravidade. Não usamos o primeiro resultado como decisão final nem suprimimos R02. Se várias hipóteses não críticas coexistirem, mantemos todas, sem inventar uma prioridade entre elas.

## Etapa 5 Máquina de estados do chamado

A máquina é sequencial e mantém um estado ativo por chamado. O modelo didático é M=(S,E,δ,s₀), com s₀=Aguardando ocorrência e estado final Encerrado. O conjunto S contém exatamente os sete estados mínimos. Os eventos E aparecem na tabela. δ é parcial: combinações não definidas não autorizam transição e a interface as rejeita. A hipótese não substitui o estado do chamado.

| Estado atual | Evento ou condição | Próximo estado | Ação e justificativa |
| --- | --- | --- | --- |
| Aguardando ocorrência | Ocorrência registrada | Em triagem | Ler os sintomas desse chamado. |
| Em triagem | Zero regras satisfeitas | Triagem inconclusiva | Informar que não foi possível sustentar hipótese. |
| Em triagem | Exatamente uma regra satisfeita | Hipótese identificada | Mostrar a hipótese e sua trilha. |
| Em triagem | Mais de uma regra satisfeita | Hipóteses concorrentes | Preservar todas as hipóteses e analisar o conjunto de conflito. |
| Hipótese identificada | Encaminhamento normal | Encaminhado para inspeção | Registrar hipótese e encaminhamento. |
| Hipótese identificada | Encaminhamento prioritário por R04 | Encaminhado para inspeção | Registrar a prioridade exigida pela fonte. |
| Hipóteses concorrentes | Critério aplicado, sem R04 | Encaminhado para inspeção | Conservar hipóteses compatíveis, sem prioridade adicional inventada. |
| Hipóteses concorrentes | Critério aplicado, com R04 | Encaminhado para inspeção | Conservar hipóteses e registrar inspeção prioritária. |
| Triagem inconclusiva | Coleta complementar | Em triagem | Reavaliar quando novos fatos forem fornecidos. |
| Triagem inconclusiva | Encaminhamento sem hipótese | Encaminhado para inspeção | Deixar explícita a insuficiência da triagem para avaliação humana. |
| Encaminhado para inspeção | Inspeção finalizada | Encerrado | Registrar o término informado do atendimento. |

As transições de coleta, encaminhamento inconclusivo e encerramento são escolhas mínimas de organização do chamado, não novas regras de diagnóstico. O protótipo para em Encaminhado para inspeção e não inventa que uma inspeção aconteceu. A transição final pode ser consultada manualmente quando o evento for informado.

Guards de triagem: G₀=(n=0), G₁=(n=1), G₂=(n>1), onde n é a quantidade de regras cujos antecedentes foram provados. São mutuamente exclusivas. Para prioridade, K é a proposição “condição crítica sustentada”, e a ação I deve respeitar K → I. O programa conta resultados já provados; a contagem não exige listas ou metaprogramação na base Prolog.

O diagrama está em maquina_estados.mmd e em maquina_estados.svg, com os mesmos estados e eventos. A tabela executable está em prolog/maquina_estados.pl. Diagrama e tabela representam o fluxo; R01 a R04 representam conhecimento de triagem.

## Etapa 6 Modelagem da base

| Categoria | Representação | Motivo |
| --- | --- | --- |
| Fatos declarados | equipamento/2, ocorrencia/2 e os cinco predicados de sintomas por ocorrência | Descrevem equipamentos e observações, sem concluir hipóteses. |
| Regras do domínio | hipotese/3, com a ocorrência, categoria e identificador da regra | Explicam quais conjunções sustentam cada classificação. |
| Explicação | trilha/4 retorna um termo evidencias com os sinais de uma regra efetivamente provada | Conecta a hipótese ao suporte usado, sem listas. |
| Conclusões inferidas | Categorias retornadas por hipotese/3 | Não são armazenadas como fatos; devem mudar quando os fatos ou regras mudarem. |
| Controle do processo | transicao/3 e estados inicial e final | Descrevem o fluxo do chamado e ficam em arquivo separado. |

Declarar `hipotese(c01,sobrecarga,r01).` diretamente como fato eliminaria a prova pelos sintomas e poderia manter uma conclusão indevida após uma alteração da entrada. Ao usar uma regra com variável compartilhada Caso, a temperatura e a corrente precisam pertencer à mesma ocorrência. Em R03, a variável Equipamento conecta a ocorrência ao equipamento cujo tipo é bomba.

## Etapa 7 Implementação

base_original.pl contém fatos, R01 a R04 e trilhas. base_fato_alterado.pl contém a Parte A independente. base_regra_nova.pl acrescenta R05, preservando os fatos originais. base_regra_nova_teste.pl é a entrada positiva da Parte B, com corrente elevada observada em C06. Nunca se devem carregar versões alternativas juntas na mesma sessão.

Exemplo efetivo de R01:

```prolog
hipotese(Caso, sobrecarga, r01) :-
    temperatura_elevada(Caso),
    corrente_elevada(Caso).
```

Exemplo efetivo de R03:

```prolog
hipotese(Caso, hidraulica, r03) :-
    ocorrencia(Caso, Equipamento),
    equipamento(Equipamento, bomba),
    fluxo_reduzido(Caso),
    ruido_anormal(Caso).
```

Os predicados estão agrupados em seções comentadas. Não há base dinâmica, assert/retract, listas, recursão, corte, negação ou hipóteses previamente declaradas. O interpretador SWI-Prolog fornece o motor de resolução. A interface Python é dispensável para demonstrar todas as consultas exigidas; serve para produzir automaticamente a frase ao usuário e aplicar eventos à tabela de transição.

## Etapa 8 Predições, consultas e motor de inferência

As predições abaixo foram fixadas antes da execução e codificadas como expectativas independentes no teste. As saídas reais estão em evidencias/consultas_c01_c07.txt e resultados.json. A representação `true` significa sucesso na prova; `false` significa que a prova não foi encontrada na base.

| Caso | Consulta | Previsto | Obtido | Justificativa |
| --- | --- | --- | --- | --- |
| C01 | hipotese(c01,sobrecarga,r01). | true | true | Temperatura e corrente informadas. |
| C02 | hipotese(c02,mecanica,r02). | true | true | Vibração e ruído informados. |
| C03 | hipotese(c03,hidraulica,r03). | true | true | Bomba com fluxo reduzido e ruído. |
| C04 | hipotese(c04,H,R). seguida de ; | mecanica/r02 e condicao_critica/r04 | Duas respostas | R02 e R04 satisfeitas. A última solução encerra sem necessidade de outro ponto e vírgula. |
| C05 | hipotese(c05,sobrecarga,r01). | false | false | corrente_elevada(c05) não consta, conforme a entrada explicitamente negativa. |
| C06 | hipotese(c06,hidraulica,r03). | false | false | ruido_anormal(c06) não consta; o ruído não foi informado. |

### Caso que sucede e busca de alternativas C04

Consulta: `hipotese(c04,H,R).`. A unificação estrutura com estrutura compara hipotese/3 com cada cabeça, com mesmo nome e aridade. Em R01, a constante c04 unifica com a variável Caso (variável com termo), H unifica com sobrecarga e R com r01. O corpo tenta temperatura_elevada(c04), cuja estrutura unifica com o fato e cujas constantes c04 são iguais (constante com constante). O objetivo corrente_elevada(c04) falha: o único fato original é corrente_elevada(c01), e c04 não unifica com c01.

O motor retorna à escolha de cláusula de hipotese/3, desfaz os vínculos de H e R e tenta R02. Caso recebe c04, H=mecanica, R=r02. As estruturas vibracao_elevada/1 e ruido_anormal/1 unificam com os fatos correspondentes; seus argumentos c04 são idênticos. Ocorre Exit de ambos e de hipotese/3, apresentando a primeira resposta.

Ao solicitar `;`, o motor faz Redo de hipotese/3 e procura alternativas. R03 vincula Caso=c04, H=hidraulica, R=r03. ocorrencia(c04,Equipamento) unifica estrutura com estrutura com ocorrencia(c04,ventilador_v1); Equipamento recebe ventilador_v1, pela regra variável com termo. O objetivo equipamento(ventilador_v1,bomba) falha porque o fato correspondente tem ventilador no segundo argumento: constantes bomba e ventilador são diferentes. O motor desfaz essa tentativa e retorna à seleção de cláusulas.

Em R04, Caso=c04, H=condicao_critica e R=r04. Temperatura, vibração e ruído são tentados da esquerda para a direita e sucedem. A segunda resposta é a condição crítica. A ordem lógica das cláusulas é R01, R02, R03, R04, de cima para baixo. A implementação do SWI pode indexar fatos, evitando visitas desnecessárias, mas isso não muda o significado da busca declarada nem a ordem dos objetivos do corpo.

O trace real contém as quatro portas: Call ao entrar em um objetivo; Exit ao prová-lo; Fail quando a tentativa não encontra prova; Redo ao retomar hipotese/3 para outra cláusula ou outra resposta. Há Redo após a falha em corrente, após o pedido de outra solução e após a falha no tipo bomba. Consulte trace_sucesso_c04.txt para a sequência integral, com os identificadores de variáveis gerados pelo interpretador.

### Caso que falha C05

Consulta: `hipotese(c05,sobrecarga,r01).`. A estrutura hipotese/3 unifica com a cabeça de R01. Caso recebe c05 (variável com termo), sobrecarga e r01 unificam com constantes idênticas (constante com constante). No corpo, temperatura_elevada(c05) unifica estrutura com estrutura com o fato correspondente e sucede. corrente_elevada(c05) não unifica com corrente_elevada(c01), pois c05 e c01 são constantes diferentes. Portanto o segundo objetivo falha e a chamada de hipotese/3 termina em Fail.

O motor retorna à chamada anterior buscando alternativas; para esta consulta específica não existe outra cabeça com categoria sobrecarga e regra r01 nem outro fato positivo de corrente para c05. Não ocorre Redo visível nesse trace determinístico: as alternativas foram esgotadas ou excluídas pela unificação/indexação. Não se inventou uma porta Redo ausente. O arquivo trace_falha_c05.txt registra Call, Exit e Fail reais. O trace do C04 fornece a demonstração de Redo.

O resultado false não prova que sobrecarga seja falsa no mundo. Demonstra apenas a impossibilidade de provar a hipótese com a regra e os fatos disponíveis. O dado negativo de corrente é uma informação de entrada; não constitui uma regra para concluir “não sobrecarga”. As duas respostas do C04 correspondem exatamente ao conjunto de conflito {R02,R04}.

## Etapa 9 Validação cruzada e explicação

A matriz abaixo demonstra o vínculo completo entre regra de origem, lógica, consulta, suporte, frase e estado de cada ocorrência. Os trechos de origem de cada Rxx estão na Etapa 2. O estado de classificação é distinguido do estado posterior de encaminhamento. C05 e C06 também recebem explicação, inclusive quando nenhuma hipótese é sustentada.

| Caso e fonte | Lógica e consulta | Fatos usados e resultado | Justificativa ao usuário | Estado e coerência |
| --- | --- | --- | --- | --- |
| C01, R01 | (T∧C)→S. hipotese(c01,sobrecarga,r01). | temperatura_elevada(c01), corrente_elevada(c01). true. | Hipótese de sobrecarga sugerida porque foram observadas temperatura elevada e corrente elevada, conforme R01; esta é uma triagem inicial e não um laudo. | Hipótese identificada; depois Encaminhado para inspeção normal. Uma regra satisfeita. |
| C02, R02 | (V∧N)→M. hipotese(c02,mecanica,r02). | vibracao_elevada(c02), ruido_anormal(c02). true. | Hipótese mecânica sugerida porque foram observados vibração elevada e ruído anormal, conforme R02; esta é uma triagem inicial e não um laudo. | Hipótese identificada; depois Encaminhado para inspeção normal. Uma regra satisfeita. |
| C03, R03 | (B∧F∧N)→H. hipotese(c03,hidraulica,r03). | Ocorrência da bomba B1, tipo bomba, fluxo_reduzido(c03), ruido_anormal(c03). true. | Hipótese hidráulica sugerida porque a ocorrência é de uma bomba com fluxo reduzido e ruído anormal, conforme R03; esta é uma triagem inicial e não um laudo. | Hipótese identificada; depois Encaminhado para inspeção normal. Uma regra satisfeita. |
| C04, R02 e R04 | (V∧N)→M e (T∧V∧N)→(K∧I). hipotese(c04,H,R). | Temperatura, vibração e ruído de c04. Duas soluções: mecanica/r02 e condicao_critica/r04. | Hipótese mecânica sugerida por vibração e ruído, conforme R02, e condição crítica sugerida por temperatura, vibração e ruído, conforme R04; a inspeção é prioritária e esta é uma triagem inicial, não um laudo. | Hipóteses concorrentes; depois Encaminhado para inspeção prioritária. As duas provas permanecem disponíveis. |
| C05, tentativa R01 | (T∧C)→S. hipotese(c05,sobrecarga,r01). | Temperatura positiva; corrente explicitamente não elevada, sem fato corrente_elevada(c05). false. | Não foi possível sustentar sobrecarga por R01 porque corrente elevada não foi observada; isso não prova ausência de sobrecarga e esta é uma triagem inicial, não um laudo. | Triagem inconclusiva; depois Encaminhado para inspeção sem hipótese. Zero regras satisfeitas. |
| C06, tentativa R03 | (B∧F∧N)→H. hipotese(c06,hidraulica,r03). | Bomba com fluxo reduzido; ruído não informado, sem fato ruido_anormal(c06). false. | Não foi possível sustentar hipótese hidráulica por R03 porque ruído anormal não foi informado; ausência de prova não é prova de ausência da causa e esta é uma triagem inicial, não um laudo. | Triagem inconclusiva; depois Encaminhado para inspeção sem hipótese. Zero regras satisfeitas. |
| C07, R02, R03 e R04 | (V∧N)→M, (B∧F∧N)→H, (T∧V∧N)→(K∧I). hipotese(c07,H,R). | Bomba B1 com temperatura, vibração, ruído e fluxo reduzido. Três soluções. | Hipóteses mecânica e hidráulica e condição crítica são sugeridas pelos sintomas da bomba, conforme R02, R03 e R04; a condição crítica exige inspeção prioritária e todas são classificações de triagem inicial, não um laudo. | Hipóteses concorrentes; depois Encaminhado para inspeção prioritária. Mesmo critério do C04. |

A versão executável produz uma frase para cada prova usando `trilha/4`, além do encaminhamento. Não há divergência nos casos validados. Se aparecer divergência em outra entrada, a sequência de investigação é: conferir a fala original; reler a fórmula em português; verificar identificação da ocorrência e seus fatos; conferir cabeça e corpo da regra; examinar as portas do trace; revisar o evento e a transição. Nunca alterar uma regra para forçar o resultado pretendido.

## Etapa 10 Evolução da base

### Parte A Alteração de um fato

Caso escolhido: C06. Antes de executar, a previsão foi acrescentar ruido_anormal(c06) e passar de nenhum resultado a hidraulica/r03. B e F já estavam estabelecidos; N passa a estar estabelecido. A conjunção B∧F∧N torna-se satisfeita, e a triagem deixa de ser inconclusiva e passa a Hipótese identificada, seguida de Encaminhado para inspeção normal.

base_fato_alterado.pl contém a nova observação, sem mudar R01 a R04. A consulta `hipotese(c06,hidraulica,r03).` sucedeu. Não surgiram outras hipóteses porque seus demais requisitos continuam indisponíveis. A base original segue sem o fato de ruído em C06, preservando o resultado false.

### Parte B Regra nova

Fonte adicional autorizada pelo próprio enunciado: “A partir de agora, fluxo reduzido junto com corrente elevada em bomba também deve ser classificado como suspeita de obstrução.” A nova regra é R05: (B∧F∧C)→O, onde O significa hipótese de obstrução sustentada pela triagem. Não se alterou o significado de nenhum símbolo anterior.

```prolog
hipotese(Caso, obstrucao, r05) :-
    ocorrencia(Caso, Equipamento),
    equipamento(Equipamento, bomba),
    fluxo_reduzido(Caso),
    corrente_elevada(Caso).
```

Foram escritas cinco linhas executáveis para a regra de classificação, mais duas linhas executáveis de trilha para a explicação. Cabeçalho, comentários e linhas em branco não entram nessa contagem. Não foi necessário reescrever R01 a R04 nem o mecanismo de prova. A interface já consulta as categorias previstas, incluindo a categoria da evolução, e mantém a mesma contagem de provas e transições. A diferença declarativa é que um novo conhecimento pode ser acrescentado como cláusula, em vez de reescrever uma cadeia de decisões imperativas.

Predição antes da execução: somente acrescentar R05, mantendo os fatos originais, não deve gerar obstrução para C06 porque corrente elevada não está disponível. A consulta falhou como previsto em base_regra_nova.pl. Para verificar a condição positiva, base_regra_nova_teste.pl contém a entrada experimental de C06 com corrente elevada. Não foi acrescentado o ruído da Parte A: os experimentos são independentes. A previsão positiva era uma única hipótese obstrucao/r05, comprovada na execução, com Hipótese identificada e encaminhamento normal. O novo fato é uma entrada de teste explicitamente documentada, não um conhecimento inventado sobre o caso original.

## Etapa 11 Novo caso C07

C07 é uma ocorrência criada para a bomba B1, com temperatura elevada, vibração elevada, ruído anormal e fluxo reduzido. São usados somente equipamentos e sintomas já sustentados pela fonte original. A corrente não foi informada. Os quatro fatos de sintomas e ocorrencia(c07,bomba_b1) constam da base original.

Predição: R01 não é satisfeita porque falta corrente; R02 é satisfeita por V e N; R03 por B, F e N; R04 por T, V e N. Logo, a consulta genérica encontra três respostas, nessa ordem de busca: mecanica/r02, hidraulica/r03 e condicao_critica/r04. A execução confirmou as três respostas e os dois pedidos de próxima solução com `;`. A trilha retorna as evidências de cada regra.

A matriz da Etapa 9 contém a validação completa de C07. As três hipóteses são mantidas e a condição crítica fica primeiro na apresentação da interface. O estado de triagem é Hipóteses concorrentes, seguido de Encaminhado para inspeção prioritária. R05 não participa da versão original de C07 e continua sem prova na versão nova enquanto não houver corrente elevada.

## Etapa 12 Análise crítica

1. **Sintoma, regra e hipótese.** Sintoma é observação declarada para uma ocorrência. Regra é relação explícita que exige determinados fatos. Hipótese é conclusão sustentada pela aplicação da regra, não uma observação primária.

2. **Raciocínio do especialista e do motor.** A ligação de efeito a causa plausível é abdutiva. A aquisição de uma associação geral pode envolver indução, mas a transcrição não descreve como o especialista a obteve. O motor deduz a classificação a partir de fatos e regras já declarados. Uma prova computacional dessa classificação não garante a realidade física da causa.

3. **Limite da conclusão.** Os sintomas não são exclusivos de uma causa e as regras são simplificações pedagógicas. A finalidade é encaminhar um chamado, com explicação, para avaliação humana.

4. **Verdade vacuosa.** Na tabela de R04, antecedente falso torna a implicação verdadeira porque não existe uma obrigação ativada e descumprida nessa linha. Não se pode derivar K desse valor da fórmula nem concluir ¬K. A consulta verifica a disponibilidade dos requisitos positivos.

5. **Mais de uma regra.** C04 mantém as duas hipóteses e recebe prioridade por R04. C07 mantém três. Um sistema real poderia deixar a escolha diagnóstica em aberto para um técnico; a política de encaminhamento teria de ser definida pelo responsável. Não se inventou exclusão entre hipóteses.

6. **Representações da mesma regra.** A fala “temperatura alta junto com corrente alta” vira (T∧C)→S e o corpo com temperatura_elevada(Caso), corrente_elevada(Caso). A formalização perde nuances de linguagem, intensidade e simultaneidade física: os fatos representam o mesmo retrato de ocorrência, sem medição numérica ou verificação temporal real. Essa limitação é assumida, não resolvida com limiares inventados.

7. **Decisão mais difícil.** A frase “vibração alta sozinha não é suspeita mecânica” poderia ser lida como negação da causa. A interpretação adotada é insuficiência para provar R02. A leitura alternativa acrescentaria uma regra de negação não sustentada por O1 a O3 e poderia descartar uma causa real sem fundamento.

8. **Função da máquina.** A FSM controla a sequência do atendimento e distingue zero, uma e várias provas. Ela não sabe quais sintomas sustentam a hipótese; isso é responsabilidade da base. A base, por sua vez, não registra que uma inspeção física foi concluída.

9. **Consulta não demonstrável.** false é ausência de prova com a base disponível, segundo a presunção de mundo fechado. Não é uma afirmação definitiva sobre o mundo externo.

10. **C05 e C06.** C05 informa corrente não elevada e não tem o requisito de R01. C06 não informa ruído e não tem o requisito de R03. Falhar em um antecedente não prova a hipótese oposta nem uma regra independente de negação.

11. **Backtracking.** No C04, a busca retorna de R01 após falha da corrente, retoma depois da primeira resposta e retorna de R03 após falha do tipo bomba para tentar R04. Os vínculos provisórios são desfeitos. No C05 específico, não há alternativa útil nem Redo visível. Isso mostra busca e esgotamento de possibilidades, sem necessidade de inventar passos ausentes do trace.

12. **Valor da explicação.** Sem a trilha, o técnico receberia apenas um rótulo, sem saber quais observações e regras o sustentam, sem conseguir conferir a entrada nem localizar uma divergência. A trilha permite revisar a decisão e preserva a distinção entre triagem e laudo.

13. **Limitações.** A base é pequena, qualitativa e restrita aos três equipamentos didáticos; não mede sintomas, não estima probabilidades, não cobre compressor nem repara máquinas. Os fatos são estáticos durante cada sessão, e mudanças exigem carregar outra versão. Não há persistência de chamados, concorrência de usuários ou interface de coleta industrial. Esses recursos não foram exigidos e não mudam os resultados acadêmicos apresentados.

## Testes e conclusão

Foram executados testes reais com SWI-Prolog 10.0.2: C01 a C07; Parte A; Parte B sem mudança da entrada e com entrada positiva; comparação exaustiva dos quatro antecedentes em 64 combinações de seis condições (256 provas); conferência das 32 linhas da tabela de R04; as onze transições da FSM; rejeição de evento sem transição; e sessões com ponto e vírgula e trace.

O teste compara as provas de Prolog com um oráculo booleano independente, sem tratar `false` como diagnóstico negativo. O registro final da quantidade de verificações e das saídas está em evidencias/testes.txt e resultados.json. A revisão final compara o trabalho diretamente às doze etapas do enunciado e às orientações de regras.docx.

O protótipo atende ao escopo pedagógico: conhecimento explícito, prova rastreável, múltiplas hipóteses tratadas e controle do chamado separado da classificação. A apresentação de 45 minutos foi preparada para mostrar o raciocínio e executar consultas, com roteiro de demonstração e exemplos de arguição. A realização oral em 17/10 depende dos integrantes do grupo; nomes e divisão dos participantes não foram fornecidos e não foram inventados.

## Referências do trabalho

Fontes principais: AtividadeAvaliativa].pdf, páginas 1 a 9; regras.docx integral; Aula_01.pdf; Aula_02.pdf; Construindo Expressões.pdf; Maquinas_de_Estado (1).pdf; Aula01_Fundamentos_e_Contexto_Histórico_da_IA.pdf; PROLOG_PARTE_1.pdf. Não foi necessário acrescentar conhecimento de domínio de fontes externas. A noção abdutiva é usada para esclarecer a direção causal pedida no enunciado, sem acrescentar regra ao sistema.
