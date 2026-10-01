import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
const root='C:/Users/Microsoft/Desktop/Atividade';
process.env.RUNTIME_NODE_MODULES='C:/Users/Microsoft/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const skill='C:/Users/Microsoft/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const build=path.join(root,'.analise/slides');
await fs.mkdir(build,{recursive:true});
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const p=Presentation.create({slideSize:{width:1280,height:720}});
const slides=[];
function text(slide,value,x,y,w,h,size=32,bold=false,color='#172e43',font='Arial') {
 const shape=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 shape.text=value;shape.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none'};
 return shape;
}
function add(title,lines,notes,code=false){
 const s=p.slides.add();s.background.fill='#FFFFFF';
 text(s,title,65,40,1150,105,44,true);
 if(lines) lines.forEach((line,i)=>text(s,line,70,170+i*105,1140,90,code?29:32,false,'#172e43',code?'Consolas':'Arial'));
 text(s,String(slides.length+1),1175,665,40,25,18,false,'#687b8b');
 s.speakerNotes.textFrame.setText(notes+'\nFontes: AtividadeAvaliativa].pdf e regras.docx. Consulte Dossie.md para a validação e evidências de execução.');
 slides.push(s);return s;
}
function table(s,values,widths,y=170,height=400,size=28){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:70,top:y,width:1140,height,columnWidths:widths,values});
 t.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({textStyle:{typeface:'Arial',fontSize:size,color:'#172e43'},margins:{left:10,right:10,top:8,bottom:8},anchor:'center'});
 for(let c=0;c<values[0].length;c++){t.getCell(0,c).fill='#e1ebf3';t.getCell(0,c).text.style={typeface:'Arial',fontSize:size,bold:true,color:'#172e43'};}
 t.borders.assign({style:'solid',fill:'#bdcad5',width:1});return t;
}

let s=add('Projeto Manutenção Inteligente',null,'Abertura. Apresentar a Situação de Aprendizagem 02 e a integração das duas UCs. Explicar que o material acompanha uma demonstração real.');
text(s,'Sistema especialista para triagem\nde manutenção industrial',70,200,1120,180,50,true);
text(s,'Indústria Atlas\nLógica para IA e Sistemas Baseados em Conhecimento',70,430,1120,120,29);
text(s,'Apresentação técnica de 45 minutos',70,595,1100,40,26);

add('Objetivo e alcance',[
 'Sintomas observados sustentam hipóteses iniciais e justificadas.',
 'O chamado evolui por estados explícitos até a inspeção.',
 'As regras são pedagógicas e não constituem laudo ou procedimento real.'
], 'Bloco 1: quatro minutos nos slides 1 a 3. Dar um exemplo de observação e de classificação. Não inventar causas reais ou reparos. Fonte: enunciado, p. 1 e 2.');

s=add('Ambiente e tarefa cognitiva',null,'Distinguir o ambiente físico da representação. O retrato do caso é estático, discreto e processado deterministicamente. MYCIN aproxima-se pela tarefa e arquitetura. Fonte curricular: aula de Fundamentos, p. 8 e 11.');
table(s,[['Ambiente físico','Representação do protótipo'],['Parcialmente observável','Somente os sintomas relatados'],['Dinâmico e contínuo','Retrato estático com categorias discretas'],['Causa incerta','Prova determinística de uma classificação'],['Tarefa diagnóstica inicial','Referência de arquitetura: MYCIN']],[490,650],170,440,28);

add('Fonte de conhecimento',[
 'R01: temperatura elevada e corrente elevada sustentam sobrecarga.',
 'R02: vibração elevada e ruído anormal sustentam hipótese mecânica.',
 'R03: em bomba, fluxo reduzido e ruído sustentam hipótese hidráulica.',
 'R04: temperatura, vibração e ruído sustentam condição crítica e prioridade.'
], 'Bloco 2: seis minutos nos slides 4 a 6. Mostrar a transcrição da página 2. Explicar que R01 a R04 são produtos da extração, não uma tabela entregue pronta.');

add('Decisões de modelagem',[
 'A repetição reforça a conjunção de todos os sinais de cada regra.',
 '“Vibração sozinha” significa insuficiência de suporte para R02.',
 'Compressor com falta de óleo fica sem regra: a fonte não o cobre.',
 'Nenhuma ausência de prova vira uma regra de negação.'
], 'Comparar a leitura como insuficiência com a leitura alternativa de negação universal. Relacionar às orientações O1 a O3. Fonte: enunciado, p. 2 a 4.');

add('Separação de ocorrências',[
 'C01, C02 e C05 usam o mesmo motor, mas possuem observações distintas.',
 'Cada sintoma recebe o identificador do caso, como temperatura_elevada(c01).',
 'A variável Caso conecta somente fatos da mesma ocorrência.'
], 'Explicar o erro que ocorreria se todos os sintomas fossem registrados em motor_m1: o C05 receberia corrente do C01 e vibração e ruído do C02. Mostrar a seção de fatos da base.');

add('Formalização de R01 e R04',[
 'R01: (T ∧ C) → S',
 'R04: (T ∧ V ∧ N) → (K ∧ I)',
 'K é a classificação crítica. I é o encaminhamento prioritário.',
 'A regra exige todos os sinais, sem provar uma causa física definitiva.'
], 'Bloco 3: cinco minutos nos slides 7 e 8. Usar o método de seis passos e a tradução reversa da aula Construindo Expressões. Definir T,V,N,C,S,K,I antes de substituir valores.');

add('Tabela-verdade de R04',[
 'Cinco proposições distintas produzem 32 combinações.',
 'O antecedente é verdadeiro em 4 linhas.',
 'A implicação é verdadeira em 29 e falsa em 3 linhas.',
 'Antecedente falso não ativa a obrigação e não descarta a hipótese.'
], 'Abrir a tabela completa do dossiê. Explicar que K e I são independentes na enumeração semântica, e por isso há quatro linhas com T,V,N verdadeiros. As três violações têm K ou I falso. Não confundir verdade vacuosa com derivação.');

s=add('Conjunto de conflito do C04',null,'Bloco 4: seis minutos nos slides 9 a 11. Antes da consulta, pedir a previsão do público. As hipóteses são compatíveis. A prioridade é da fonte; a preservação e ordenação são decisões de engenharia.');
table(s,[['Regra','Condições provadas','Resultado'],['R02','Vibração e ruído','Hipótese mecânica'],['R04','Temperatura, vibração e ruído','Condição crítica e prioridade']],[150,510,480],180,270,29);
text(s,'As duas provas permanecem disponíveis. A condição crítica orienta a prioridade.',70,495,1140,115,31);

add('Quantidade de regras e estado do chamado',[
 'Zero provas: Triagem inconclusiva.',
 'Uma prova: Hipótese identificada.',
 'Mais de uma prova: Hipóteses concorrentes.',
 'O encaminhamento preserva a trilha e a prioridade exigida por R04.'
], 'Explicar que “duas hipóteses” não pode pular o estado de concorrência. Separar estado de classificação e estado posterior de encaminhamento. A FSM não é um diagnóstico.');

s=add('Máquina de estados do chamado',null,'Diagrama editável dos sete estados mínimos. As transições normal e prioritária estão detalhadas no dossiê e no arquivo Prolog. O evento inspecao_finalizada é informado externamente. Coleta complementar retorna à triagem.');
function node(label,x,y,w=300,h=60){
 const n=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:'#edf3f8',line:{fill:'#31465a',width:1.5}});
 n.text=label;n.text.style={typeface:'Arial',fontSize:25,color:'#172e43',alignment:'center',verticalAlignment:'middle',autoFit:'none'};return n;
}
function conn(a,b,from='bottom',to='top'){s.shapes.connect(a,b,{kind:'elbow',fromSide:from,toSide:to,line:{fill:'#31465a',width:2},tail:{type:'arrow'}});}
const a=node('Aguardando ocorrência',490,155);
const t=node('Em triagem',490,265);
const z=node('Triagem inconclusiva',65,395);
const u=node('Hipótese identificada',490,395);
const m=node('Hipóteses concorrentes',905,395);
const e=node('Encaminhado para inspeção',485,555,330);
const f=node('Encerrado',960,555,245);
conn(a,t);conn(t,z);conn(t,u);conn(t,m);conn(z,e);conn(u,e);conn(m,e);conn(e,f,'right','left');conn(z,t,'left','left');
text(s,'registrada',805,223,270,32,23);
text(s,'n = 0',100,327,200,33,23);text(s,'n = 1',550,327,180,33,23);text(s,'n > 1',995,327,180,33,23);
text(s,'encaminhar sem\nhipótese',230,458,235,60,23);text(s,'encaminhar',660,463,190,40,23);text(s,'aplicar critério',855,463,190,40,23);
text(s,'inspeção\nfinalizada',825,510,135,58,21);
text(s,'Coleta complementar retorna à triagem. Inicial: Aguardando ocorrência. Final: Encerrado.',65,637,1150,40,22);

add('Base declarativa em Prolog',[
 'hipotese(Caso, sobrecarga, r01) :-',
 '    temperatura_elevada(Caso),\n    corrente_elevada(Caso).',
 'Fatos descrevem sintomas. A regra produz a hipótese.',
 'A base não usa listas, recursão, corte ou negação.'
], 'Bloco 5: dez minutos nos slides 12 a 15. Mostrar o código real. Explicar cabeça, corpo e variável compartilhada. Fonte curricular: PROLOG_PARTE_1, p. 14 a 21.',true);

add('Consultas de sucesso e falha',[
 'hipotese(c01, sobrecarga, r01).     Resultado previsto: true.',
 'hipotese(c05, sobrecarga, r01).     Resultado previsto: false.',
 'C01 tem os dois sintomas. C05 informa corrente não elevada.',
 'false significa que a base não forneceu uma prova.'
], 'Executar as duas consultas ao vivo, só depois da predição. Distinguir informação negativa de corrente de ausência de ruído no C06. Não apresentar false como laudo negativo.',true);

add('Trace e unificação no C04',[
 'R01: temperatura sucede e corrente falha.',
 'R02: vibração e ruído sucedem. Primeira resposta.',
 'O pedido ; retoma a busca. R03 falha no tipo bomba.',
 'R04 sucede. Segunda resposta: condição crítica.'
], 'Executar leash(-all), trace e hipotese(c04,H,R), pedindo a segunda resposta com ;. Mostrar constante com constante, variável com termo e estrutura com estrutura. Explicar desfazer os vínculos de H e R. Comparar com trace_sucesso_c04.txt.');

add('Portas do trace e busca',[
 'Call: tentativa de um objetivo. Exit: prova encontrada.',
 'Fail: tentativa sem prova. Redo: retomada para alternativa.',
 'Cláusulas de cima para baixo, objetivos da esquerda para a direita.',
 'C05 específico não mostra Redo. C04 demonstra as quatro portas.'
], 'Abrir trace_falha_c05.txt ou gerar ao vivo. Explicar que a consulta específica de sobrecarga/r01 não possui outra cabeça que possa provar o objetivo. A indexação pode evitar tentativas inúteis, sem alterar os resultados.');

s=add('Validação cruzada dos seis casos',null,'Bloco 6: seis minutos nos slides 16 a 18. Mostrar um caso completo em cinco níveis: fonte, fórmula, Prolog, motor e estado. A matriz detalhada no dossiê contém frases e todos os fatos.');
table(s,[['Caso','Regras provadas','Estado após a triagem'],['C01','R01','Hipótese identificada'],['C02','R02','Hipótese identificada'],['C03','R03','Hipótese identificada'],['C04','R02 e R04','Hipóteses concorrentes'],['C05','Nenhuma','Triagem inconclusiva'],['C06','Nenhuma','Triagem inconclusiva']],[150,310,680],165,440,27);

add('Evoluções independentes da base',[
 'Parte A: ruído acrescentado a C06 permite provar R03.',
 'Parte B: R05 exige bomba, fluxo reduzido e corrente elevada.',
 'Só acrescentar R05 não muda C06 sem corrente informada.',
 'Na entrada positiva da Parte B, C06 sustenta obstrução por R05.'
], 'Preservar a base original e usar uma sessão para cada versão. Prever antes de consultar. Mostrar base_regra_nova.pl e base_regra_nova_teste.pl, sem misturar com o ruído da Parte A. Cinco linhas da regra de classificação e duas da trilha.');

add('Novo caso C07',[
 'Bomba B1 com temperatura, vibração, ruído e fluxo reduzido.',
 'Previsão: R02, R03 e R04. A corrente não foi informada.',
 'A consulta retorna três hipóteses, com dois pedidos de próxima solução.',
 'Hipóteses concorrentes e encaminhamento para inspeção prioritária.'
], 'Executar hipotese(c07,H,R) com dois pedidos ;. Relacionar cada resposta aos fatos e à origem das regras. Mostrar a frase de cada trilha e a matriz C07.');

add('Raciocínio e limites da conclusão',[
 'Efeito observado para causa possível é inferência abdutiva.',
 'Indução pode construir associações. A transcrição não descreve essa aquisição.',
 'O motor deduz a classificação usando fatos e regras já declarados.',
 'Mundo fechado: ausência de prova não demonstra ausência da causa.'
], 'Bloco 7: quatro minutos nos slides 19 e 20. O enunciado solicita três formas estudadas, mas nenhuma descreve precisamente a inversão causal. Explicar a aproximação indutiva e a distinção, sem acrescentar conhecimento de domínio.');

add('Resultados e demonstração final',[
 '298 verificações aprovadas com SWI-Prolog real.',
 'Sete casos, evoluções, 256 provas de antecedentes e onze transições.',
 'Cada hipótese mantém sua regra e os sintomas que a sustentam.',
 'Uma mudança de fato exige nova previsão antes da consulta.'
], 'Quatro minutos reservados para arguição ou dinâmica final. Propor remover temperatura de C04: permanece R02 e desaparece R04. Perguntar o novo estado antes de demonstrar. Sem arguição, usar o tempo para essa atividade, respeitando 40 a 50 minutos. Registros: evidencias/testes.txt e resultados.json.');

const candidate=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
await fs.mkdir(path.join(root,'.analise/final_deck'),{recursive:true});
const revision=Date.now();
const final=path.join(root,`.analise/final_deck/Apresentacao_${revision}.pptx`);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,
 pythonExecutable:'C:/Users/Microsoft/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',... [3,9,16].flatMap(n=>['--require-native-table-slide',String(n)])],
 fontPolicy:{basis:'design',families:['Arial','Consolas']},
 requiredNativeTableOwnerSlides:[3,9,16],verifyArtifactToolImport:true,
 receiptPath:path.join(build,`validation-${revision}.json`)});
for(let i=0;i<slides.length;i++){
 const blob=await p.export({slide:slides[i],format:'png',scale:1});
 await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));
}
console.log(`Apresentação finalizada: ${slides.length} slides.`);
await fs.copyFile(final,path.join(root,'entrega/apresentacao/Apresentacao.pptx'));
