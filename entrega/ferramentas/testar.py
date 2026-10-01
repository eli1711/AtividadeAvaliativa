"""Validação externa; a base Prolog utiliza somente fatos e regras simples."""
import itertools
import json
import subprocess
import tempfile
from pathlib import Path
from triagem import RAIZ, REGRAS, analisar, avancar, consultar, executavel

EVIDENCIAS = RAIZ / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)
total = 0


def verificar(condicao, descricao):
    global total
    if not condicao:
        raise AssertionError(descricao)
    total += 1


esperados = {"c01": {"r01"}, "c02": {"r02"}, "c03": {"r03"},
             "c04": {"r02", "r04"}, "c05": set(), "c06": set(),
             "c07": {"r02", "r03", "r04"}}
registros = []
for caso, regras in esperados.items():
    # Predicao fixada antes das chamadas ao interpretador.
    resposta = analisar(caso)
    verificar({h["regra"] for h in resposta["hipoteses"]} == regras, f"Hipóteses {caso}")
    estado = "triagem_inconclusiva" if not regras else (
        "hipotese_identificada" if len(regras) == 1 else "hipoteses_concorrentes")
    verificar(resposta["estados"][2] == estado, f"Estado {caso}")
    verificar(resposta["prioridade"] == ("prioritária" if "r04" in regras else "normal"), f"Prioridade {caso}")
    registros.append({"previsto": sorted(regras), "obtido": resposta})

verificar({h["regra"] for h in analisar("c06", "fato")["hipoteses"]} == {"r03"}, "Parte A")
verificar(analisar("c06", "regra")["hipoteses"] == [], "R05 sem corrente continua inconclusiva")
verificar({h["regra"] for h in analisar("c06", "regra_teste")["hipoteses"]} == {"r05"}, "Parte B positiva")

base = (RAIZ / "prolog/base_original.pl").read_text(encoding="utf-8")
# Para todas as 64 combinacoes de B,T,V,N,C,F, o oraculo booleano
# independente testa o antecedente de cada uma das quatro regras.
predicados = ["temperatura_elevada", "vibracao_elevada", "ruido_anormal", "corrente_elevada", "fluxo_reduzido"]
with tempfile.TemporaryDirectory() as pasta:
    arquivo = Path(pasta) / "combinacao.pl"
    for B, T, V, N, C, F in itertools.product([False, True], repeat=6):
        fatos = "\nocorrencia(cteste, bomba_b1).\n" if B else "\nocorrencia(cteste, motor_m1).\n"
        # Inserir fatos antes de sua primeira clausula mantem predicados contiguos.
        texto = base
        texto = texto.replace("ocorrencia(c01,", fatos.strip() + "\nocorrencia(c01,")
        for nome, valor in zip(predicados, [T, V, N, C, F]):
            if valor:
                texto = texto.replace(nome + "(c", nome + "(cteste).\n" + nome + "(c", 1)
        arquivo.write_text(texto, encoding="utf-8")
        previsoes = [T and C, V and N, B and F and N, T and V and N]
        for (categoria, regra), previsto in zip(REGRAS[:4], previsoes):
            observado = consultar(arquivo, f"hipotese(cteste,{categoria},{regra})")
            verificar(observado == previsto, f"Combinação {B,T,V,N,C,F} {regra}")

# A implicacao completa de R04 tem 5 variaveis e 32 linhas.
linhas = []
for T, V, N, K, I in itertools.product([True, False], repeat=5):
    antecedente = T and V and N
    consequente = K and I
    implicacao = (not antecedente) or consequente
    linhas.append([T,V,N,K,I,antecedente,consequente,implicacao])
verificar(len(linhas) == 32, "Tabela completa R04")
verificar(sum(l[5] for l in linhas) == 4, "Antecedente verdadeiro em 4 linhas")
verificar(sum(l[7] for l in linhas) == 29, "Implicação verdadeira em 29 linhas")

arestas = [
 ("aguardando_ocorrencia", "ocorrencia_registrada", "em_triagem"),
 ("em_triagem", "nenhuma_regra_satisfeita", "triagem_inconclusiva"),
 ("em_triagem", "uma_regra_satisfeita", "hipotese_identificada"),
 ("em_triagem", "varias_regras_satisfeitas", "hipoteses_concorrentes"),
 ("hipotese_identificada", "encaminhamento_normal", "encaminhado_para_inspecao"),
 ("hipotese_identificada", "encaminhamento_prioritario", "encaminhado_para_inspecao"),
 ("hipoteses_concorrentes", "criterio_aplicado_normal", "encaminhado_para_inspecao"),
 ("hipoteses_concorrentes", "criterio_aplicado_prioritario", "encaminhado_para_inspecao"),
 ("triagem_inconclusiva", "coleta_complementar", "em_triagem"),
 ("triagem_inconclusiva", "encaminhamento_sem_hipotese", "encaminhado_para_inspecao"),
 ("encaminhado_para_inspecao", "inspecao_finalizada", "encerrado")]
for origem, evento, destino in arestas:
    verificar(avancar(origem,evento) == destino, f"FSM {origem}, {evento}")
try:
    avancar("em_triagem", "inspecao_finalizada")
except ValueError:
    verificar(True, "Transição inválida rejeitada")
else:
    verificar(False, "Transição inválida aceita")

# Registros reais do REPL e do trace, incluindo o pedido de proxima solucao.
sessoes = {
 "consultas_c01_c07.txt": "hipotese(c01,sobrecarga,r01).\nhipotese(c02,mecanica,r02).\nhipotese(c03,hidraulica,r03).\nhipotese(c04,H,R).\n;\nhipotese(c05,sobrecarga,r01).\nhipotese(c06,hidraulica,r03).\nhipotese(c07,H,R).\n;\n;\nhalt.\n",
 "trace_sucesso_c04.txt": "leash(-all).\ntrace.\nhipotese(c04,H,R).\n;\nnotrace.\nhalt.\n",
 "trace_falha_c05.txt": "leash(-all).\ntrace.\nhipotese(c05,sobrecarga,r01).\nnotrace.\nhalt.\n"}
for nome, entrada in sessoes.items():
    proc = subprocess.run([executavel(),"-q","-s",str(RAIZ / "prolog/base_original.pl")],
                          input=entrada, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding="utf-8", errors="replace", timeout=20)
    verificar(proc.returncode == 0 and "ERROR:" not in proc.stdout, nome)
    (EVIDENCIAS / nome).write_text("ENTRADA\n"+entrada+"\nSAÍDA REAL\n"+proc.stdout, encoding="utf-8")

(EVIDENCIAS / "resultados.json").write_text(json.dumps({"verificacoes":total,"casos":registros,"tabela_r04":linhas},ensure_ascii=False,indent=2),encoding="utf-8")
(EVIDENCIAS / "testes.txt").write_text(f"{total} verificações aprovadas.\nSWI-Prolog real, 7 casos, duas evoluções, 256 avaliações de antecedentes, 32 linhas da tabela-verdade, 11 transições e rejeição de evento inválido.\n",encoding="utf-8")
print(f"{total} verificações aprovadas.")
