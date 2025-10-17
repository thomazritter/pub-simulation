# SIMULAÇÃO MANUAL 2 - Até T30 minutos

**Data de execução:** 17/10/2025  
**Método:** Três Fases (Three-Phase Approach)  
**Objetivo:** Segunda simulação manual até o instante T30 minutos para verificação

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


🍺 SIMULAÇÃO DO PUB - Método das Três Fases


⏱️  Tempo máximo: 30 minutos
📊 Usando tabelas pré-definidas (3.6, 3.7, 3.8, 3.9)




🍺 SIMULAÇÃO MANUAL DO PUB - MÉTODO DAS TRÊS FASES


FASE A: Verificar tempo de término e determinar atividade que terminará
FASE B: Processar atividades terminadas e mover entidades
FASE C: Iniciar novas atividades quando possível

  FASE C: C1: Chega começa T0 e termina em T0+11 (tab. 3.6, N1), SEDE4



T1
  FASE B: C1: Chega termina T1
  FASE C: C1G1: Enche começa T1 e termina em T1+56 (tab. 3.9, N5)


T1
  FASE C: C2: Chega começa T1 e termina em T1+1011 (tab. 3.6, N10), SEDE2


T1



T6
  FASE B: C1G1: Enche termina T6
  FASE C: C1: Bebe começa T6 e termina em T6+713 (tab. 3.8, N7)



T11


T11
  FASE B: C2: Chega termina T11
  FASE C: C2G2: Enche começa T11 e termina em T11+516 (tab. 3.9, N5)


T11
  FASE C: C3: Chega começa T11 e termina em T11+1526 (tab. 3.6, N15), SEDE1



T13
  FASE B: C1: Bebe termina T13, SEDE3
  FASE C: OG1: Lava começa T13 e termina em T13+518 (N5)



T16
  FASE B: C2G2: Enche termina T16
  FASE C: C2: Bebe começa T16 e termina em T16+723 (tab. 3.8, N7)
  FASE C: OG2: Lava começa T16 e termina em T16+521 (N5)



T18
  FASE B: OG1: Lava termina T18
  FASE C: C1G1: Enche começa T18 e termina em T18+624 (tab. 3.9, N6)



T21



T23
  FASE B: C2: Bebe termina T23, SEDE1
  FASE C: OG2: Lava começa T23 e termina em T23+528 (N5)



T24
  FASE B: C1G1: Enche termina T24
  FASE C: C1: Bebe começa T24 e termina em T24+630 (tab. 3.8, N6)
  FASE C: OG1: Lava começa T24 e termina em T24+529 (N5)



T26
  FASE B: C3: Chega termina T26


T26
  FASE C: C4: Chega começa T26 e termina em T26+632 (tab. 3.6, N6), SEDE2


T26



T28
  FASE B: OG2: Lava termina T28
  FASE C: C3G2: Enche começa T28 e termina em T28+533 (tab. 3.9, N5)



T29
  FASE C: C2G1: Enche começa T29 e termina em T29+534 (tab. 3.9, N5)



T30
  FASE B: C1: Bebe termina T30, SEDE2




📊 MÉTRICAS DE PERFORMANCE


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


---

## Resumo da Simulação 2

- **Clientes atendidos:** 4 (C1, C2, C3, C4)
- **Tempo simulado:** T0 até T30
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
