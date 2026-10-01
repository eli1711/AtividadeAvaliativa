"""Interface opcional: consulta o Prolog e aplica o controle do chamado."""
import argparse
import shutil
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ROTULOS = {"sobrecarga": "sobrecarga", "mecanica": "ocorrência mecânica",
           "hidraulica": "problema hidráulico", "condicao_critica": "condição crítica",
           "obstrucao": "obstrução"}
SINAIS = {"temperatura_elevada": "temperatura elevada", "corrente_elevada": "corrente elevada",
          "vibracao_elevada": "vibração elevada", "ruido_anormal": "ruído anormal",
          "fluxo_reduzido": "fluxo reduzido", "bomba": "equipamento do tipo bomba"}
REGRAS = [("sobrecarga", "r01"), ("mecanica", "r02"),
          ("hidraulica", "r03"), ("condicao_critica", "r04"), ("obstrucao", "r05")]


def executavel():
    caminho = shutil.which("swipl")
    if not caminho:
        alternativa = Path("C:/Program Files/swipl/bin/swipl.exe")
        if alternativa.exists():
            caminho = str(alternativa)
    if not caminho:
        raise RuntimeError("SWI-Prolog não encontrado. Instale-o e adicione swipl ao PATH.")
    return caminho


def consultar(base, objetivo, saida=False):
    resultado = subprocess.run([executavel(), "-q", "-s", str(base), "-g", objetivo,
                                "-t", "halt"], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=20)
    if resultado.stderr.strip():
        raise RuntimeError(resultado.stderr.strip())
    if resultado.returncode not in (0, 1):
        raise RuntimeError("Erro ao executar consulta Prolog.")
    return resultado.stdout.strip() if saida else resultado.returncode == 0


def avancar(estado, evento):
    objetivo = f"transicao({estado},{evento},Proximo),write(Proximo)"
    proximo = consultar(RAIZ / "prolog/maquina_estados.pl", objetivo, True)
    if not proximo:
        raise ValueError(f"Transição não definida: {estado}, {evento}")
    return proximo


def analisar(caso, versao="original"):
    arquivos = {"original": "base_original.pl", "fato": "base_fato_alterado.pl",
                "regra": "base_regra_nova.pl", "regra_teste": "base_regra_nova_teste.pl"}
    base = RAIZ / "prolog" / arquivos[versao]
    if caso not in {f"c{i:02}" for i in range(1, 8)}:
        raise ValueError("Informe um caso entre c01 e c07.")
    encontradas = []
    for hipotese, regra in REGRAS:
        objetivo = f"hipotese({caso},{hipotese},{regra})"
        if consultar(base, objetivo):
            evidencia = consultar(base, f"trilha({caso},{hipotese},{regra},E),write(E)", True)
            termos = evidencia.removeprefix("evidencias(").removesuffix(")").split(",")
            sinais = ", ".join(SINAIS[t] for t in termos)
            frase = (f"Hipótese de {ROTULOS[hipotese]} sugerida porque foram observados "
                     f"{sinais}, conforme a regra {regra.upper()}; "
                     "esta é uma triagem inicial e não um laudo.")
            encontradas.append({"hipotese": hipotese, "regra": regra, "frase": frase})
    eventos = {0: "nenhuma_regra_satisfeita", 1: "uma_regra_satisfeita"}
    evento = eventos.get(len(encontradas), "varias_regras_satisfeitas")
    estados = ["aguardando_ocorrencia"]
    estados.append(avancar(estados[-1], "ocorrencia_registrada"))
    estados.append(avancar(estados[-1], evento))
    # Prioridade de inspecao vem da fonte; conservar todas as hipoteses e
    # ordenar a critica primeiro e uma decisao de engenharia fora da KB.
    encontradas.sort(key=lambda h: h["hipotese"] != "condicao_critica")
    prioritario = any(h["hipotese"] == "condicao_critica" for h in encontradas)
    if not encontradas:
        mensagem = ("Não foi possível sustentar hipótese porque nenhuma regra teve "
                    "todas as suas condições estabelecidas pelos fatos disponíveis. "
                    "A ausência de prova não demonstra a hipótese oposta. "
                    "Esta é uma triagem inicial e não um laudo.")
        evento = "encaminhamento_sem_hipotese"
    else:
        mensagem = "\n".join(h["frase"] for h in encontradas)
        if len(encontradas) > 1:
            evento = "criterio_aplicado_prioritario" if prioritario else "criterio_aplicado_normal"
        else:
            evento = "encaminhamento_prioritario" if prioritario else "encaminhamento_normal"
    estados.append(avancar(estados[-1], evento))
    return {"caso": caso, "hipoteses": encontradas, "estados": estados,
            "prioridade": "prioritária" if prioritario else "normal", "mensagem": mensagem}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Triagem didática de manutenção por Prolog")
    parser.add_argument("caso", choices=[f"c{i:02}" for i in range(1, 8)])
    parser.add_argument("--versao", choices=["original", "fato", "regra", "regra_teste"], default="original")
    args = parser.parse_args()
    resposta = analisar(args.caso, args.versao)
    print(resposta["mensagem"])
    print("Estados: " + " -> ".join(resposta["estados"]))
    print("Encaminhamento: inspeção " + resposta["prioridade"])
