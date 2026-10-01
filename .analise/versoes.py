from pathlib import Path
p=Path('entrega/prolog/base_original.pl')
s=p.read_text(encoding='utf-8')
s=s.replace('temperatura_elevada(c05).','temperatura_elevada(c05).\ntemperatura_elevada(c07).').replace('vibracao_elevada(c04).','vibracao_elevada(c04).\nvibracao_elevada(c07).')
p.write_text(s,encoding='utf-8')
a=s.replace('ruido_anormal(c07).','ruido_anormal(c07).\n% Parte A: nova observacao no C06.\nruido_anormal(c06).').replace('% C06 nao informa ruido: nao declaramos ruido_anormal(c06).','% C06 originalmente nao informava ruido; a Parte A acrescenta essa observacao.')
Path('entrega/prolog/base_fato_alterado.pl').write_text(a,encoding='utf-8')
r='''% R05 - mudanca fornecida na Etapa 10 Parte B.
hipotese(Caso, obstrucao, r05) :-
    ocorrencia(Caso, Equipamento),
    equipamento(Equipamento, bomba),
    fluxo_reduzido(Caso),
    corrente_elevada(Caso).

'''
b=s.replace('% TRILHA DE EXPLICACAO',r+'% TRILHA DE EXPLICACAO')
b+='''\n% Trilha da nova regra.
trilha(Caso, obstrucao, r05, evidencias(bomba, fluxo_reduzido, corrente_elevada)) :-
    hipotese(Caso, obstrucao, r05).
'''
Path('entrega/prolog/base_regra_nova.pl').write_text(b,encoding='utf-8')
btest=b.replace('corrente_elevada(c01).','corrente_elevada(c01).\n% Entrada positiva da Parte B: observacao de corrente no C06.\ncorrente_elevada(c06).')
Path('entrega/prolog/base_regra_nova_teste.pl').write_text(btest,encoding='utf-8')
Path('entrega/prolog/entrada_experimento_b.pl').unlink()
