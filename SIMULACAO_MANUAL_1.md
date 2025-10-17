# Simulação Manual 1

**Data:** 17/10/2025  
**Tempo simulado:** T=0 até T=30 minutos  
**Método:** Três Fases

## Configuração

| Parâmetro | Distribuição | Fonte |
|-----------|--------------|-------|
| Tempo entre chegadas | Exponencial (média 5) | Tabela 3.6 |
| Tempo para encher | Normal (média 6, desvio 1) | Tabela 3.9 |
| Tempo para beber | Uniforme (5-8) | Tabela 3.8 |
| Tempo para lavar | 5 minutos (fixo) | - |
| Número de drinks | Uniforme (1-4) | Tabela 3.7 |
| Copos disponíveis | 10 | - |
| Garçonetes | 2 (G1, G2) | - |

## Trace da Simulação

### T=0
- **FASE C:** Cliente 1 chega
  - Início: T=0
  - Término: T=1 (tabela 3.6, valor=1)
  - Sede inicial: 4 drinks (tabela 3.7)

### T=1
- **FASE B:** Cliente 1 sai da fila de chegada
- **FASE C:** Cliente 1 com Garçonete 1 iniciam enchimento
  - Duração: 5 minutos (tabela 3.9)
  - Término: T=6
- **FASE C:** Cliente 2 chega
  - Duração na fila: 10 minutos (tabela 3.6)
  - Término: T=11
  - Sede inicial: 2 drinks (tabela 3.7)

### T=6
- **FASE B:** Cliente 1 termina enchimento com G1
- **FASE C:** Cliente 1 inicia bebida
  - Duração: 7 minutos (tabela 3.8)
  - Término: T=13

### T=11
- **FASE B:** Cliente 2 sai da fila de chegada
- **FASE C:** Cliente 2 com Garçonete 2 iniciam enchimento
  - Duração: 5 minutos (tabela 3.9)
  - Término: T=16
- **FASE C:** Cliente 3 chega
  - Duração na fila: 15 minutos (tabela 3.6)
  - Término: T=26
  - Sede inicial: 1 drink (tabela 3.7)

### T=13
- **FASE B:** Cliente 1 termina bebida
  - Sede restante: 3
  - Gera copo sujo
- **FASE C:** Garçonete 1 inicia lavagem
  - Duração: 5 minutos
  - Término: T=18

### T=16
- **FASE B:** Cliente 2 termina enchimento com G2
- **FASE C:** Cliente 2 inicia bebida
  - Duração: 7 minutos (tabela 3.8)
  - Término: T=23
- **FASE C:** Garçonete 2 inicia lavagem
  - Duração: 5 minutos
  - Término: T=21

### T=18
- **FASE B:** Garçonete 1 termina lavagem
- **FASE C:** Cliente 1 com G1 iniciam enchimento (2º drink)
  - Duração: 6 minutos (tabela 3.9)
  - Término: T=24

### T=21
- **FASE B:** Garçonete 2 termina lavagem

### T=23
- **FASE B:** Cliente 2 termina bebida
  - Sede restante: 1
  - Gera copo sujo
- **FASE C:** Garçonete 2 inicia lavagem
  - Duração: 5 minutos
  - Término: T=28

### T=24
- **FASE B:** Cliente 1 termina enchimento com G1 (2º drink)
- **FASE C:** Cliente 1 inicia bebida (2º drink)
  - Duração: 6 minutos (tabela 3.8)
  - Término: T=30
- **FASE C:** Garçonete 1 inicia lavagem
  - Duração: 5 minutos
  - Término: T=29

### T=26
- **FASE B:** Cliente 3 sai da fila de chegada
- **FASE C:** Cliente 4 chega
  - Duração na fila: 6 minutos (tabela 3.6)
  - Término: T=32
  - Sede inicial: 2 drinks (tabela 3.7)

### T=28
- **FASE B:** Garçonete 2 termina lavagem
- **FASE C:** Cliente 3 com G2 iniciam enchimento
  - Duração: 5 minutos (tabela 3.9)
  - Término: T=33

### T=29
- **FASE B:** Garçonete 1 termina lavagem
- **FASE C:** Cliente 2 com G1 iniciam enchimento (2º drink)
  - Duração: 5 minutos (tabela 3.9)
  - Término: T=34

### T=30 (fim)
- **FASE B:** Cliente 1 termina bebida (2º drink)
  - Sede restante: 2

## Métricas

### Tempos
- Tempo médio em fila: 8.00 minutos

### Garçonetes - Lavagem
| Garçonete | Tempo |
|-----------|-------|
| G1 | 10 min |
| G2 | 10 min |

### Garçonetes - Enchimento
| Garçonete | Tempo |
|-----------|-------|
| G1 | 16 min |
| G2 | 10 min |

### Ocupação
| Garçonete | Ocupada | Ociosa |
|-----------|---------|--------|
| G1 | 86.7% | 13.3% |
| G2 | 66.7% | 33.3% |

## Resumo

Clientes atendidos: 4 (C1, C2, C3, C4)

Estado dos clientes em T=30:
- C1: consumiu 2 de 4 drinks
- C2: consumiu 1 de 2 drinks
- C3: 0 de 1 drink (ainda enchendo)
- C4: 0 de 2 drinks (ainda na fila de chegada)

Estado do sistema em T=30:
- 8 copos limpos, 2 sujos
- 0 garçonetes disponíveis (ambas trabalhando)
- Filas: 0 chegada, 0 atendimento, 1 terminaram beber (C1)
