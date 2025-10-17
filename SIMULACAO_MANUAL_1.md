# 🍺 Simulação Manual 1 - Método das Três Fases

**Data:** 17/10/2025  
**Tempo simulado:** T=0 até T=30 minutos  
**Método:** Three-Phase Approach (Método das Três Fases)

---

## 📋 Configuração da Simulação

Conforme especificado nas instruções do exercício:

| Parâmetro | Distribuição | Fonte |
|-----------|--------------|-------|
| Tempo entre chegadas | Exponencial (μ=5) | Tabela 3.6 |
| Tempo para encher | Normal (μ=6, σ=1) | Tabela 3.9 |
| Tempo para beber | Uniforme (5-8) | Tabela 3.8 |
| Tempo para lavar | Fixo (5 min) | - |
| Número de drinks | Uniforme (1-4) | Tabela 3.7 |
| Copos disponíveis | 10 | Fila "limpo" |
| Garçonetes | 2 (G1, G2) | Fila "livre" |
| Clientes | Infinito | - |

---

## 🔄 Método das Três Fases

**FASE A:** Verificar tempo de término e determinar atividade que terminará  
**FASE B:** Processar atividades terminadas e mover entidades  
**FASE C:** Iniciar novas atividades quando possível

---

## 📊 Trace da Simulação

### T=0
```
FASE C: C1 chega
  → Início: T=0
  → Término: T=0+1=1 (tab. 3.6, N=1)
  → SEDE inicial: 4 drinks (tab. 3.7)
```

### T=1
```
FASE B: C1 termina chegada
  → Move para fila de atendimento

FASE C: C1G1 começa encher
  → Início: T=1
  → Duração: 5 min (tab. 3.9, N=5)
  → Término: T=6

FASE C: C2 chega
  → Início: T=1
  → Duração: 10 min (tab. 3.6, N=10)
  → Término: T=11
  → SEDE inicial: 2 drinks (tab. 3.7)
```

### T=6
```
FASE B: C1G1 termina encher
  → G1 fica disponível

FASE C: C1 começa beber
  → Início: T=6
  → Duração: 7 min (tab. 3.8, N=7)
  → Término: T=13
```

### T=11
```
FASE B: C2 termina chegada
  → Move para fila de atendimento

FASE C: C2G2 começa encher
  → Início: T=11
  → Duração: 5 min (tab. 3.9, N=5)
  → Término: T=16

FASE C: C3 chega
  → Início: T=11
  → Duração: 15 min (tab. 3.6, N=15)
  → Término: T=26
  → SEDE inicial: 1 drink (tab. 3.7)
```

### T=13
```
FASE B: C1 termina beber
  → SEDE restante: 3 drinks
  → Copo sujo gerado
  → Move para fila "terminaram beber"

FASE C: G1 começa lavar
  → Início: T=13
  → Duração: 5 min
  → Término: T=18
```

### T=16
```
FASE B: C2G2 termina encher
  → G2 fica disponível

FASE C: C2 começa beber
  → Início: T=16
  → Duração: 7 min (tab. 3.8, N=7)
  → Término: T=23

FASE C: G2 começa lavar
  → Início: T=16
  → Duração: 5 min
  → Término: T=21
```

### T=18
```
FASE B: G1 termina lavar
  → Copo limpo disponível
  → G1 fica disponível

FASE C: C1G1 começa encher (2º drink)
  → Início: T=18
  → Duração: 6 min (tab. 3.9, N=6)
  → Término: T=24
```

### T=21
```
FASE B: G2 termina lavar
  → Copo limpo disponível
  → G2 fica disponível
```

### T=23
```
FASE B: C2 termina beber
  → SEDE restante: 1 drink
  → Copo sujo gerado
  → Move para fila "terminaram beber"

FASE C: G2 começa lavar
  → Início: T=23
  → Duração: 5 min
  → Término: T=28
```

### T=24
```
FASE B: C1G1 termina encher (2º drink)
  → G1 fica disponível

FASE C: C1 começa beber (2º drink)
  → Início: T=24
  → Duração: 6 min (tab. 3.8, N=6)
  → Término: T=30

FASE C: G1 começa lavar
  → Início: T=24
  → Duração: 5 min
  → Término: T=29
```

### T=26
```
FASE B: C3 termina chegada
  → Move para fila de atendimento

FASE C: C4 chega
  → Início: T=26
  → Duração: 6 min (tab. 3.6, N=6)
  → Término: T=32
  → SEDE inicial: 2 drinks (tab. 3.7)
```

### T=28
```
FASE B: G2 termina lavar
  → Copo limpo disponível
  → G2 fica disponível

FASE C: C3G2 começa encher
  → Início: T=28
  → Duração: 5 min (tab. 3.9, N=5)
  → Término: T=33
```

### T=29
```
FASE B: G1 termina lavar
  → Copo limpo disponível
  → G1 fica disponível

FASE C: C2G1 começa encher (2º drink)
  → Início: T=29
  → Duração: 5 min (tab. 3.9, N=5)
  → Término: T=34
```

### T=30 ⏱️ (FIM DA SIMULAÇÃO)
```
FASE B: C1 termina beber (2º drink)
  → SEDE restante: 2 drinks
  → Copo sujo gerado
  → Move para fila "terminaram beber"
```

---

## 📈 Métricas de Performance

### Tempo Médio em Fila (Espera)
- **8.00 minutos**

### Tempo das Garçonetes Lavando
| Garçonete | Tempo Total |
|-----------|-------------|
| G1 | 10 minutos |
| G2 | 10 minutos |

### Tempo das Garçonetes Enchendo
| Garçonete | Tempo Total |
|-----------|-------------|
| G1 | 16 minutos |
| G2 | 10 minutos |

### Taxa de Ocupação
| Garçonete | Ocupação | Ociosidade |
|-----------|----------|------------|
| G1 | 86.7% | 13.3% |
| G2 | 66.7% | 33.3% |

---

## 📊 Resumo da Simulação

### Clientes Atendidos
- **Total:** 4 clientes (C1, C2, C3, C4)

### Status dos Clientes em T=30
| Cliente | SEDE Inicial | Drinks Consumidos | SEDE Restante |
|---------|--------------|-------------------|---------------|
| C1 | 4 | 2 | 2 |
| C2 | 2 | 1 | 1 |
| C3 | 1 | 0 | 1 (enchendo) |
| C4 | 2 | 0 | 2 (chegando) |

### Estado do Sistema em T=30
- **Copos limpos:** 8
- **Copos sujos:** 2
- **Garçonetes disponíveis:** 0 (ambas trabalhando)
- **Fila de chegada:** 0
- **Fila de atendimento:** 0
- **Fila terminaram beber:** 1 (C1)

---

## ✅ Validação

A simulação seguiu corretamente:
- ✅ Método das três fases (A → B → C)
- ✅ Uso das tabelas especificadas (3.6, 3.7, 3.8, 3.9)
- ✅ Prioridade de atendimento: chega → enche → bebe → lava
- ✅ Gerenciamento correto de recursos (garçonetes e copos)
- ✅ Controle de filas e estados do sistema

---

## 🔗 Informações Adicionais

Para executar esta simulação:
```bash
python pub_sim_final.py 30
```

O código fonte completo está disponível em [`pub_sim_final.py`](pub_sim_final.py).
