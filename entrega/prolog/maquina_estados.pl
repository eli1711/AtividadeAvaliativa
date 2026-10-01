% Controle do chamado separado das regras de triagem.
% O chamador informa o evento depois de consultar TODAS as solucoes.
estado_inicial(aguardando_ocorrencia).
estado_final(encerrado).

transicao(aguardando_ocorrencia, ocorrencia_registrada, em_triagem).
transicao(em_triagem, nenhuma_regra_satisfeita, triagem_inconclusiva).
transicao(em_triagem, uma_regra_satisfeita, hipotese_identificada).
transicao(em_triagem, varias_regras_satisfeitas, hipoteses_concorrentes).
transicao(hipotese_identificada, encaminhamento_normal, encaminhado_para_inspecao).
transicao(hipotese_identificada, encaminhamento_prioritario, encaminhado_para_inspecao).
transicao(hipoteses_concorrentes, criterio_aplicado_normal, encaminhado_para_inspecao).
transicao(hipoteses_concorrentes, criterio_aplicado_prioritario, encaminhado_para_inspecao).
transicao(triagem_inconclusiva, coleta_complementar, em_triagem).
transicao(triagem_inconclusiva, encaminhamento_sem_hipotese, encaminhado_para_inspecao).
transicao(encaminhado_para_inspecao, inspecao_finalizada, encerrado).
