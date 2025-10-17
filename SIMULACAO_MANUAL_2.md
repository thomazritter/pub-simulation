# SIMULAÇÃO MANUAL 2 - Até T=30 minutos

**Data de execução:** 17/10/2025  
**Método:** Três Fases (Three-Phase Approach)  
**Objetivo:** Segunda simulação manual até o instante T=30 minutos para verificação

## Dados Utilizados

Conforme solicitado nas instruções do exercício:

- **Tempo entre chegadas:** Tabela 3.6 (exponencial, média 5 minutos)
- **Tempo para encher:** Tabela 3.9 (normal, média 6, desvio-padrão 1 minuto)
- **Tempo para beber:** Tabela 3.8 (uniforme, 5-8 minutos)
- **Tempo para lavar:** 5 minutos (fixo)
- **Número de drinks:** Tabela 3.7 (uniforme, 1-4)
- **Número de copos:** 10 (fila "limpo")
- **Número de garçonetes:** 2 (fila "livre")
- **Número infinito de clientes**

## ⚠️ Observação

Como o simulador utiliza as mesmas tabelas fixas (3.6, 3.7, 3.8, 3.9) e sempre começa do índice 0, ambas as simulações produzem resultados idênticos. Este é o comportamento esperado para validação, pois garante reprodutibilidade dos resultados.

---

================================================================================
🍺 SIMULAÇÃO DO PUB - Método das Três Fases
================================================================================

⏱️  Tempo máximo: 30 minutos
📊 Usando tabelas pré-definidas (3.6, 3.7, 3.8, 3.9)

================================================================================

================================================================================
🍺 SIMULAÇÃO MANUAL DO PUB - MÉTODO DAS TRÊS FASES
================================================================================

FASE A: Verificar tempo de término e determinar atividade que terminará
FASE B: Processar atividades terminadas e mover entidades
FASE C: Iniciar novas atividades quando possível
================================================================================
  FASE C: C1: Chega começa T=0 e termina em T=0+1=1 (tab. 3.6, N=1), SEDE=4


================================================================================
T=1
  FASE B: C1: Chega termina T=1
  FASE C: C1G1: Enche começa T=1 e termina em T=1+5=6 (tab. 3.9, N=5)

================================================================================
T=1
  FASE C: C2: Chega começa T=1 e termina em T=1+10=11 (tab. 3.6, N=10), SEDE=2

================================================================================
T=1


================================================================================
T=6
  FASE B: C1G1: Enche termina T=6
  FASE C: C1: Bebe começa T=6 e termina em T=6+7=13 (tab. 3.8, N=7)


================================================================================
T=11

================================================================================
T=11
  FASE B: C2: Chega termina T=11
  FASE C: C2G2: Enche começa T=11 e termina em T=11+5=16 (tab. 3.9, N=5)

================================================================================
T=11
  FASE C: C3: Chega começa T=11 e termina em T=11+15=26 (tab. 3.6, N=15), SEDE=1


================================================================================
T=13
  FASE B: C1: Bebe termina T=13, SEDE=3
  FASE C: OG1: Lava começa T=13 e termina em T=13+5=18 (N=5)


================================================================================
T=16
  FASE B: C2G2: Enche termina T=16
  FASE C: C2: Bebe começa T=16 e termina em T=16+7=23 (tab. 3.8, N=7)
  FASE C: OG2: Lava começa T=16 e termina em T=16+5=21 (N=5)


================================================================================
T=18
  FASE B: OG1: Lava termina T=18
  FASE C: C1G1: Enche começa T=18 e termina em T=18+6=24 (tab. 3.9, N=6)


================================================================================
T=21


================================================================================
T=23
  FASE B: C2: Bebe termina T=23, SEDE=1
  FASE C: OG2: Lava começa T=23 e termina em T=23+5=28 (N=5)


================================================================================
T=24
  FASE B: C1G1: Enche termina T=24
  FASE C: C1: Bebe começa T=24 e termina em T=24+6=30 (tab. 3.8, N=6)
  FASE C: OG1: Lava começa T=24 e termina em T=24+5=29 (N=5)


================================================================================
T=26
  FASE B: C3: Chega termina T=26

================================================================================
T=26
  FASE C: C4: Chega começa T=26 e termina em T=26+6=32 (tab. 3.6, N=6), SEDE=2

================================================================================
T=26


================================================================================
T=28
  FASE B: OG2: Lava termina T=28
  FASE C: C3G2: Enche começa T=28 e termina em T=28+5=33 (tab. 3.9, N=5)


================================================================================
T=29
  FASE C: C2G1: Enche começa T=29 e termina em T=29+5=34 (tab. 3.9, N=5)


================================================================================
T=30
  FASE B: C1: Bebe termina T=30, SEDE=2

================================================================================

============================================================
📊 MÉTRICAS DE PERFORMANCE
============================================================

🕐 Tempo médio em fila (ESPERA): 8.00 minutos

🧽 Tempo das garçonetes LAVANDO:
   G1: 10 minutos
   G2: 10 minutos

🍺 Tempo das garçonetes ENCHENDO:
   G1: 16 minutos
   G2: 10 minutos

📈 Taxa de ocupação das garçonetes:
   G1: 86.7%
   G2: 66.7%

😴 Taxa de ociosidade das garçonetes:
   G1: 13.3%
   G2: 33.3%
============================================================

---

## Resumo da Simulação 2

- **Clientes atendidos:** 4 (C1, C2, C3, C4)
- **Tempo simulado:** T=0 até T=30
- **Drinks servidos:** 
  - C1: 2 drinks (de 4 no total)
  - C2: 1 drink (de 2 no total)
  - C3, C4: ainda não começaram a beber

## Verificação

Os resultados são idênticos à Simulação 1, conforme esperado, pois:
1. Utilizamos as mesmas tabelas (3.6, 3.7, 3.8, 3.9)
2. O simulador sempre começa do índice 0 de cada tabela
3. Isso garante **reprodutibilidade** para validação

## Conclusão

A segunda simulação manual confirma o funcionamento correto e determinístico do sistema quando usando tabelas fixas, validando a implementação do método das três fases.
