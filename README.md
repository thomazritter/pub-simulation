# 🍺 Simulação do Pub - Método das Três Fases

Simulação de um pub usando o **Método das Três Fases** (Three-Phase Approach) implementado em Python.

## ⚡ Quick Start

```bash
# 1. Clone o repositório
git clone <repository-url>
cd pub_sim

# 2. Configure o ambiente
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute!
python pub_sim_final.py
```

**Pronto!** A simulação rodará até T=30 minutos e exibirá os resultados no console.

## 📂 Simulações Manuais Incluídas

Este repositório contém **duas simulações manuais completas** até T=30 minutos, conforme solicitado nas instruções do exercício:

- **[SIMULACAO_MANUAL_1.md](SIMULACAO_MANUAL_1.md)** - Primeira simulação manual detalhada
- **[SIMULACAO_MANUAL_2.md](SIMULACAO_MANUAL_2.md)** - Segunda simulação manual detalhada

Ambas as simulações utilizam o método das três fases e seguem rigorosamente as tabelas especificadas (3.6, 3.7, 3.8, 3.9), demonstrando o funcionamento correto do sistema.

## 📋 Descrição

Este projeto simula o funcionamento de um pub com as seguintes características:

- **Clientes**: Chegam ao pub e possuem uma "sede" inicial (número de drinks que desejam)
- **Garçonetes**: 2 garçonetes (G1 e G2) que enchem copos e lavam copos sujos
- **Copos**: 10 copos limpos no início, que precisam ser lavados após uso
- **Atividades**: 
  - Chegar (cliente entra na fila de chegada)
  - Encher (garçonete enche um copo para o cliente)
  - Beber (cliente consome o drink)
  - Lavar (garçonete lava copos sujos)

## 🎯 Características da Simulação

### Método das Três Fases

A simulação implementa o método das três fases:

1. **FASE A**: Verificar o tempo de término e determinar qual atividade terminará
2. **FASE B**: Processar atividades que terminaram e mover entidades entre filas
3. **FASE C**: Iniciar novas atividades quando recursos estiverem disponíveis

### Tabelas de Dados

O simulador usa tabelas pré-definidas (baseadas nas imagens do exercício):

- **Tabela 3.6**: Tempo entre chegadas sucessivas (distribuição exponencial, média 5)
- **Tabela 3.7**: Número de drinks por cliente (distribuição uniforme, 1-4)
- **Tabela 3.8**: Tempo para beber (distribuição uniforme, 5-8)
- **Tabela 3.9**: Tempo para encher copo (distribuição normal, média 6, desvio 1)
- **Tempo para lavar**: Fixo em 5 minutos

## 🚀 Como Usar

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação e Execução - Passo a Passo

#### Opção 1: Usando Ambiente Virtual (Recomendado) ⭐

Esta é a melhor opção pois isola as dependências do projeto.

**Passo 1:** Clone o repositório
```bash
git clone <repository-url>
cd pub_sim
```

**Passo 2:** Crie um ambiente virtual
```bash
python3 -m venv venv
```

**Passo 3:** Ative o ambiente virtual
```bash
# No Linux/Mac:
source venv/bin/activate

# No Windows (PowerShell):
venv\Scripts\Activate.ps1

# No Windows (CMD):
venv\Scripts\activate.bat
```

Você verá `(venv)` no início da linha de comando quando estiver ativado.

**Passo 4:** Instale as dependências
```bash
pip install -r requirements.txt
```

**Passo 5:** Execute a simulação
```bash
# Simulação padrão (T=30 minutos)
python pub_sim_final.py

# Ou especifique um tempo customizado
python pub_sim_final.py 50
```

**Passo 6:** Desative o ambiente virtual quando terminar
```bash
deactivate
```

#### Opção 2: Instalação Global (Mais Rápido)

Se você prefere não usar ambiente virtual:

**Passo 1:** Clone o repositório
```bash
git clone <repository-url>
cd pub_sim
```

**Passo 2:** Instale as dependências globalmente
```bash
pip3 install pandas
```

**Passo 3:** Execute a simulação
```bash
python3 pub_sim_final.py 30
```

#### Opção 3: Execução Direta (Se já instalou)

Se você já tem o ambiente configurado:

```bash
# Com venv ativado:
python pub_sim_final.py 30

# Ou diretamente com o Python do venv:
venv/bin/python pub_sim_final.py 30

# No Windows:
venv\Scripts\python.exe pub_sim_final.py 30
```

### Argumentos da Linha de Comando

```bash
python pub_sim_final.py [TEMPO_MAX]
```

- `TEMPO_MAX` (opcional): Tempo máximo de simulação em minutos
  - Padrão: 30 minutos
  - Exemplo: `python pub_sim_final.py 50` → simula até T=50

## 📊 Saídas

A simulação gera três tipos de saída:

### 1. Trace das Três Fases (Console)

Mostra o progresso da simulação passo a passo no formato do método das três fases:

```
================================================================================
T=1
  FASE B: C1: Chega termina T=1
  FASE C: C1G1: Enche começa T=1 e termina em T=1+5=6 (tab. 3.9, N=5)
================================================================================
T=1
  FASE C: C2: Chega começa T=1 e termina em T=1+10=11 (tab. 3.6, N=10), SEDE=2
```

### 2. Métricas de Performance (Console)

Exibe estatísticas da simulação ao final:

```
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
```

### 3. Log Detalhado (Arquivo Markdown)

Salvo automaticamente em `log_simulacao_pub.md`, contém:
- Todos os eventos com timestamps
- Estado do sistema em cada momento
- Estatísticas completas
- Lista de clientes atendidos
- Contadores de eventos por tipo

## ⚠️ Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'pandas'"

**Causa:** pandas não está instalado no ambiente Python que você está usando.

**Solução:**
```bash
# Se usando venv, ative-o primeiro:
source venv/bin/activate  # Mac/Linux
# ou
venv\Scripts\activate     # Windows

# Depois instale:
pip install pandas
```

### Erro: "command not found: python"

**Causa:** Python não está no PATH ou precisa usar `python3`.

**Solução:**
```bash
# Tente com python3:
python3 pub_sim_final.py

# Ou verifique se Python está instalado:
python3 --version
```

### Venv não ativa no Windows

**Causa:** PowerShell pode bloquear execução de scripts.

**Solução:**
```powershell
# Execute como administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Depois ative novamente:
venv\Scripts\Activate.ps1
```

### Arquivo log_simulacao_pub.md não foi criado

**Causa:** Erro de permissão ou simulação foi interrompida.

**Solução:**
- Verifique se tem permissão de escrita na pasta
- Execute a simulação até o final (aguarde "Simulação concluída")
- O arquivo é recriado a cada execução

## 📁 Estrutura do Código

```
pub_sim_final.py
├── Tabelas de dados (TABELA_3_6, 3_7, 3_8, 3_9)
├── Classe Cliente
├── Classe Evento  
├── Classe SimuladorPUB
│   ├── __init__: Inicialização com tabelas configuráveis
│   ├── Métodos de geração (usando tabelas)
│   ├── Sistema de log e trace
│   ├── Cálculo de métricas
│   ├── Método das três fases
│   └── Processamento de eventos
└── Execução principal (com CLI)
```

## 🔧 Customização

Você pode customizar as tabelas de dados passando-as como parâmetros ao criar o simulador:

```python
simulador = SimuladorPUB(
    tempo_max=30,
    tabela_chegadas=[1, 2, 3, 4, ...],
    tabela_drinks=[1, 2, 3, 4, ...],
    tabela_beber=[5, 6, 7, 8, ...],
    tabela_encher=[5, 6, 7, ...],
)
```

## 📝 Exemplos de Uso

### Simulação até T=30 minutos (padrão):
```bash
python pub_sim_final.py
```

### Simulação até T=100 minutos:
```bash
python pub_sim_final.py 100
```

## 📚 Referências

Este projeto implementa os conceitos de simulação de eventos discretos usando o método das três fases, baseado em exercícios de simulação e modelagem.

## ✅ Validação

O código foi validado comparando os resultados com simulações manuais até T=30 minutos, verificando:
- ✓ Ordem correta dos eventos
- ✓ Estados do sistema (filas, recursos)
- ✓ Cálculo correto dos tempos
- ✓ Métricas de performance

## 📄 Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

