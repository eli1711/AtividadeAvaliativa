% Projeto Manutencao Inteligente - versao original.
% Cada sintoma refere-se a uma ocorrencia, nao ao equipamento acumulado.

% EQUIPAMENTOS E OCORRENCIAS
equipamento(motor_m1, motor).
equipamento(bomba_b1, bomba).
equipamento(ventilador_v1, ventilador).
ocorrencia(c01, motor_m1).
ocorrencia(c02, motor_m1).
ocorrencia(c03, bomba_b1).
ocorrencia(c04, ventilador_v1).
ocorrencia(c05, motor_m1).
ocorrencia(c06, bomba_b1).
ocorrencia(c07, bomba_b1).

% SINTOMAS OBSERVADOS
temperatura_elevada(c01).
temperatura_elevada(c04).
temperatura_elevada(c05).
temperatura_elevada(c07).
corrente_elevada(c01).
vibracao_elevada(c02).
vibracao_elevada(c04).
vibracao_elevada(c07).
ruido_anormal(c02).
ruido_anormal(c03).
ruido_anormal(c04).
ruido_anormal(c07).
% Parte A: nova observacao no C06.
ruido_anormal(c06).
fluxo_reduzido(c03).
fluxo_reduzido(c06).
fluxo_reduzido(c07).
% C05 informa corrente nao elevada: nao declaramos corrente_elevada(c05).
% C06 originalmente nao informava ruido; a Parte A acrescenta essa observacao.

% REGRAS EXTRAIDAS DA FONTE - R01 A R04
hipotese(Caso, sobrecarga, r01) :-
    temperatura_elevada(Caso),
    corrente_elevada(Caso).

hipotese(Caso, mecanica, r02) :-
    vibracao_elevada(Caso),
    ruido_anormal(Caso).

hipotese(Caso, hidraulica, r03) :-
    ocorrencia(Caso, Equipamento),
    equipamento(Equipamento, bomba),
    fluxo_reduzido(Caso),
    ruido_anormal(Caso).

hipotese(Caso, condicao_critica, r04) :-
    temperatura_elevada(Caso),
    vibracao_elevada(Caso),
    ruido_anormal(Caso).

% TRILHA DE EXPLICACAO - termos estruturados, sem listas
trilha(Caso, sobrecarga, r01, evidencias(temperatura_elevada, corrente_elevada)) :-
    hipotese(Caso, sobrecarga, r01).
trilha(Caso, mecanica, r02, evidencias(vibracao_elevada, ruido_anormal)) :-
    hipotese(Caso, mecanica, r02).
trilha(Caso, hidraulica, r03, evidencias(bomba, fluxo_reduzido, ruido_anormal)) :-
    hipotese(Caso, hidraulica, r03).
trilha(Caso, condicao_critica, r04, evidencias(temperatura_elevada, vibracao_elevada, ruido_anormal)) :-
    hipotese(Caso, condicao_critica, r04).
