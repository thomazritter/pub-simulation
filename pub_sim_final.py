import pandas as pd
import heapq
import sys

# =============================================================================
# TABELAS DE DADOS (Extraídas das imagens do exercício)
# =============================================================================

# Tabela 3.6 - Distribuição exponencial, média 5 (Tempo entre chegadas sucessivas)
TABELA_3_6 = [
    1, 10, 15, 6, 2, 2, 2, 1, 11, 0,
    5, 13, 6, 0, 11, 5, 1, 20, 4, 12,
    3, 2, 8, 1, 1, 3, 1, 2, 10, 5,
    5, 11, 1, 1, 20, 7, 6, 10, 4, 23,
    1, 12, 2, 7, 1, 4, 4, 1, 3, 0,
    5, 3, 2, 6
]

# Tabela 3.7 - Distribuição uniforme, mínimo 1 e máximo 4 (Número de drinks)
TABELA_3_7 = [
    4, 2, 1, 2, 2, 1, 2, 2, 1, 2,
    4, 1, 3, 3, 4, 4, 1, 2, 4, 1,
    2, 1, 1, 2, 2, 3, 2, 1, 1, 2,
    1, 2, 4, 4, 1, 3, 2, 1, 2, 1,
    2, 4, 2, 3, 2, 4, 1, 1, 4, 3,
    4, 2, 4, 4, 3, 3, 3, 3, 3, 1,
    4, 1, 1, 1, 4, 2
]

# Tabela 3.8 - Distribuição uniforme, mínimo 5 e máximo 8 (Tempo para beber)
TABELA_3_8 = [
    7, 7, 6, 7, 7, 8, 8, 6, 8, 8,
    8, 7, 8, 5, 8, 8, 6, 5, 5, 5,
    7, 6, 7, 8, 6, 7, 5, 5, 7, 6,
    8, 6, 5, 7, 6, 8, 7, 8, 7, 7,
    6, 8, 5, 6, 8, 6, 8, 5, 5, 5,
    8, 6, 5, 5, 5, 6, 8, 5, 8, 6,
    6, 8, 8, 5, 7
]

# Tabela 3.9 - Distribuição normal, média 6 e desvio-padrão 1 (Tempo para encher)
TABELA_3_9 = [
    5, 5, 6, 5, 5, 5, 6, 6, 6, 6,
    3, 5, 7, 5, 6, 6, 7, 6, 7, 7,
    6, 5, 5, 6, 6, 6, 5, 4, 4, 5, 4,
    6, 6, 5, 6, 7, 7, 6, 5, 4, 6,
    6, 4, 6, 7, 7, 7, 6, 6, 6, 6,
    5, 6, 6, 5, 6, 6, 6, 6, 6
]

# =============================================================================
# ESTRUTURAS DE DADOS
# =============================================================================

class Cliente:
    def __init__(self, id, tempo_chegada, sede_inicial):
        self.id = id
        self.tempo_chegada = tempo_chegada
        self.sede_inicial = sede_inicial  # sede inicial (preservada)
        self.sede_restante = sede_inicial  # drinks que ainda quer beber

class Evento:
    def __init__(self, tempo, tipo, cliente=None, garconete=None, duracao=None, tabela_info=None):
        self.tempo = tempo
        self.tipo = tipo  # "chegada", "sair_fila_chegada", "encher_fim", "beber_fim", "lavar_fim"
        self.cliente = cliente
        self.garconete = garconete
        self.duracao = duracao  # Duração da atividade (para trace)
        self.tabela_info = tabela_info  # Info da tabela usada (tab X.X, N=X)
    
    def __lt__(self, other):
        return self.tempo < other.tempo

# =============================================================================
# SIMULADOR DO PUB
# =============================================================================

class SimuladorPUB:
    def __init__(self, tempo_max, 
                 tabela_chegadas=None, 
                 tabela_drinks=None, 
                 tabela_beber=None, 
                 tabela_encher=None):
        # Configuração básica
        self.tempo_max = tempo_max
        self.tempo_atual = 0
        
        # Tabelas de dados (com defaults das imagens)
        self.tabela_chegadas = tabela_chegadas if tabela_chegadas else TABELA_3_6
        self.tabela_drinks = tabela_drinks if tabela_drinks else TABELA_3_7
        self.tabela_beber = tabela_beber if tabela_beber else TABELA_3_8
        self.tabela_encher = tabela_encher if tabela_encher else TABELA_3_9
        
        # Índices para tabelas (ciclam quando chegam ao fim)
        self.idx_chegadas = 0
        self.idx_drinks = 0
        self.idx_beber = 0
        self.idx_encher = 0
        
        # Recursos do pub
        self.copos_limpos = 10
        self.copos_sujos = 0
        self.garconetes_disponiveis = ["G1", "G2"]
        
        # Filas do sistema
        self.fila_chegada = []        # Clientes esperando para entrar no pub (máx 1)
        self.fila_atendimento = []    # Clientes prontos para serem atendidos
        self.fila_terminaram_beber = []  # Clientes que terminaram de beber (aguardando próximo copo)
        
        # Controle de clientes
        self.clientes = []
        self.proximo_id_cliente = 1
        
        # Sistema de eventos
        self.fila_eventos = []
        self.log_simulacao = []
        self.trace_tres_fases = []  # Log formatado para o método das três fases

    # =============================================================================
    # DISTRIBUIÇÕES DE TEMPO (Usando tabelas)
    # =============================================================================
    
    def gerar_tempo_espera_fila_chegada(self):
        """Tempo entre chegadas sucessivas (Tabela 3.6 - exponencial, média 5)"""
        valor = self.tabela_chegadas[self.idx_chegadas]
        self.idx_chegadas = (self.idx_chegadas + 1) % len(self.tabela_chegadas)
        return valor
    
    def gerar_tempo_encher_copo(self):  
        """Tempo para encher copo (Tabela 3.9 - normal, média 6, desvio 1)"""
        valor = self.tabela_encher[self.idx_encher]
        self.idx_encher = (self.idx_encher + 1) % len(self.tabela_encher)
        return valor
    
    def gerar_tempo_beber(self):   
        """Tempo para beber (Tabela 3.8 - uniforme, 5-8)"""
        valor = self.tabela_beber[self.idx_beber]
        self.idx_beber = (self.idx_beber + 1) % len(self.tabela_beber)
        return valor
    
    def gerar_tempo_lavar_copo(self):   
        """Tempo para lavar copo (fixo, 5)"""
        return 5
    
    def gerar_sede_inicial(self):   
        """Sede inicial do cliente (Tabela 3.7 - uniforme, 1-4)"""
        valor = self.tabela_drinks[self.idx_drinks]
        self.idx_drinks = (self.idx_drinks + 1) % len(self.tabela_drinks)
        return valor

    # =============================================================================
    # SISTEMA DE LOG
    # =============================================================================
    
    def registrar_evento(self, evento, detalhe=""):
        """Registra um evento no log da simulação"""
        estado = f"Fila chegada={len(self.fila_chegada)}, Fila atendimento={len(self.fila_atendimento)}, Fila terminaram beber={len(self.fila_terminaram_beber)}, Copos limpos={self.copos_limpos}, sujos={self.copos_sujos}, Garç disponíveis={self.garconetes_disponiveis}"
        self.log_simulacao.append({
            "T": self.tempo_atual, 
            "Evento": evento, 
            "Detalhe": detalhe, 
            "Estado": estado
        })
    
    def registrar_trace_fase(self, fase, mensagem):
        """Registra uma linha no trace formatado das três fases"""
        self.trace_tres_fases.append({
            "T": self.tempo_atual,
            "Fase": fase,
            "Mensagem": mensagem
        })
    
    def calcular_metricas(self):
        """Calcula métricas de performance da simulação"""
        metricas = {}
        
        # 1. Tempo médio em fila (ESPERA)
        tempos_espera = []
        for evento in self.log_simulacao:
            if "ESPERA FILA CHEGADA" in evento['Evento']:
                # Extrair tempo de espera do detalhe
                detalhe = evento['Detalhe']
                if "espera" in detalhe and "min" in detalhe:
                    try:
                        tempo_espera = int(detalhe.split("espera ")[1].split(" min")[0])
                        tempos_espera.append(tempo_espera)
                    except:
                        pass
        
        metricas['tempo_medio_fila'] = sum(tempos_espera) / len(tempos_espera) if tempos_espera else 0
        
        # 2. Tempo das garçonetes ocupadas (LAVANDO e ENCHENDO)
        # Rastrear períodos de ocupação para cada garçonete
        g1_periodos = []
        g2_periodos = []
        
        for evento in self.log_simulacao:
            if evento['Evento'] == 'LAVAR INICIA':
                detalhe = evento['Detalhe']
                if 'G1' in detalhe:
                    try:
                        tempo_fim = int(detalhe.split('G1 até ')[1])
                        g1_periodos.append((evento['T'], tempo_fim, 'LAVAR'))
                    except:
                        pass
                elif 'G2' in detalhe:
                    try:
                        tempo_fim = int(detalhe.split('G2 até ')[1])
                        g2_periodos.append((evento['T'], tempo_fim, 'LAVAR'))
                    except:
                        pass
            
            elif evento['Evento'] == 'ENCHER INICIA':
                detalhe = evento['Detalhe']
                if 'G1' in detalhe:
                    try:
                        tempo_fim = int(detalhe.split('G1 para')[1].split(' até ')[1])
                        g1_periodos.append((evento['T'], tempo_fim, 'ENCHER'))
                    except:
                        pass
                elif 'G2' in detalhe:
                    try:
                        tempo_fim = int(detalhe.split('G2 para')[1].split(' até ')[1])
                        g2_periodos.append((evento['T'], tempo_fim, 'ENCHER'))
                    except:
                        pass
        
        # Calcular tempos totais por atividade
        metricas['g1_lavando_total'] = sum([tempo_fim - tempo_inicio for tempo_inicio, tempo_fim, atividade in g1_periodos if atividade == 'LAVAR'])
        metricas['g2_lavando_total'] = sum([tempo_fim - tempo_inicio for tempo_inicio, tempo_fim, atividade in g2_periodos if atividade == 'LAVAR'])
        metricas['g1_enchendo_total'] = sum([tempo_fim - tempo_inicio for tempo_inicio, tempo_fim, atividade in g1_periodos if atividade == 'ENCHER'])
        metricas['g2_enchendo_total'] = sum([tempo_fim - tempo_inicio for tempo_inicio, tempo_fim, atividade in g2_periodos if atividade == 'ENCHER'])
        
        # 3. Taxa de ocupação das garçonetes (tempo total ocupado / tempo total da simulação)
        g1_total_ocupado = metricas['g1_lavando_total'] + metricas['g1_enchendo_total']
        g2_total_ocupado = metricas['g2_lavando_total'] + metricas['g2_enchendo_total']
        
        metricas['g1_taxa_ocupacao'] = (g1_total_ocupado / self.tempo_max) * 100
        metricas['g2_taxa_ocupacao'] = (g2_total_ocupado / self.tempo_max) * 100
        
        # 4. Taxa de ociosidade das garçonetes
        metricas['g1_taxa_ociosidade'] = 100 - metricas['g1_taxa_ocupacao']
        metricas['g2_taxa_ociosidade'] = 100 - metricas['g2_taxa_ocupacao']
        
        # 5. Número de clientes atendidos
        metricas['clientes_atendidos'] = len(self.clientes)
        
        # 6. Número total de eventos
        metricas['total_eventos'] = len(self.log_simulacao)
        
        return metricas

    def imprimir_metricas(self, metricas):
        """Imprime as métricas de performance no console"""
        print("\n" + "="*60)
        print("📊 MÉTRICAS DE PERFORMANCE")
        print("="*60)
        
        print(f"\n🕐 Tempo médio em fila (ESPERA): {metricas['tempo_medio_fila']:.2f} minutos")
        
        print(f"\n🧽 Tempo das garçonetes LAVANDO:")
        print(f"   G1: {metricas['g1_lavando_total']} minutos")
        print(f"   G2: {metricas['g2_lavando_total']} minutos")
        
        print(f"\n🍺 Tempo das garçonetes ENCHENDO:")
        print(f"   G1: {metricas['g1_enchendo_total']} minutos")
        print(f"   G2: {metricas['g2_enchendo_total']} minutos")
        
        print(f"\n📈 Taxa de ocupação das garçonetes:")
        print(f"   G1: {metricas['g1_taxa_ocupacao']:.1f}%")
        print(f"   G2: {metricas['g2_taxa_ocupacao']:.1f}%")
        
        print(f"\n😴 Taxa de ociosidade das garçonetes:")
        print(f"   G1: {metricas['g1_taxa_ociosidade']:.1f}%")
        print(f"   G2: {metricas['g2_taxa_ociosidade']:.1f}%")
        
        print("="*60)
    
    def imprimir_trace_tres_fases(self):
        """Imprime o trace formatado no estilo do método das três fases"""
        print("\n" + "="*80)
        print("🍺 SIMULAÇÃO MANUAL DO PUB - MÉTODO DAS TRÊS FASES")
        print("="*80)
        print("\nFASE A: Verificar tempo de término e determinar atividade que terminará")
        print("FASE B: Processar atividades terminadas e mover entidades")
        print("FASE C: Iniciar novas atividades quando possível")
        print("="*80)
        
        tempo_anterior = -1
        for entrada in self.trace_tres_fases:
            # Separador visual quando o tempo muda
            if entrada['T'] != tempo_anterior and tempo_anterior != -1:
                print()
            tempo_anterior = entrada['T']
            
            # Formatação por fase
            if entrada['Fase'] == 'A':
                print(f"\n{'='*80}")
                print(f"T={entrada['T']}")
            elif entrada['Fase'] == 'B':
                print(f"  FASE B: {entrada['Mensagem']}")
            elif entrada['Fase'] == 'C':
                print(f"  FASE C: {entrada['Mensagem']}")
        
        print("\n" + "="*80)

    def salvar_log_markdown(self, nome_arquivo="log_simulacao.md"):
        """Salva o log da simulação em um arquivo Markdown formatado"""
        metricas = self.calcular_metricas()
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("# 🍺 LOG DA SIMULAÇÃO DO PUB\n\n")
            f.write(f"**Tempo máximo:** {self.tempo_max} minutos\n")
            f.write(f"**Total de eventos:** {metricas['total_eventos']}\n")
            f.write(f"**Clientes atendidos:** {metricas['clientes_atendidos']}\n\n")
            
            f.write("## 📊 RESUMO DA SIMULAÇÃO\n\n")
            f.write("| Tempo | Evento | Detalhe | Estado |\n")
            f.write("|-------|--------|---------|--------|\n")
            
            for evento in self.log_simulacao:
                f.write(f"| {evento['T']} | {evento['Evento']} | {evento['Detalhe']} | {evento['Estado']} |\n")
            
            f.write("\n## 📈 ESTATÍSTICAS\n\n")
            
            # Contar tipos de eventos
            tipos_eventos = {}
            for evento in self.log_simulacao:
                tipo = evento['Evento']
                tipos_eventos[tipo] = tipos_eventos.get(tipo, 0) + 1
            
            f.write("### Eventos por Tipo:\n\n")
            for tipo, count in tipos_eventos.items():
                f.write(f"- **{tipo}:** {count} ocorrências\n")
            
            f.write("\n### Clientes:\n\n")
            for cliente in self.clientes:
                f.write(f"- **Cliente {cliente.id}:** Chegou em T={cliente.tempo_chegada}, Sede inicial={cliente.sede_inicial}\n")
            
            f.write("\n## 📊 MÉTRICAS DE PERFORMANCE\n\n")
            f.write("### Tempo médio em fila (ESPERA):\n")
            f.write(f"- **Tempo médio:** {metricas['tempo_medio_fila']:.2f} minutos\n\n")
            
            f.write("### Tempo das garçonetes ocupadas:\n")
            f.write("#### LAVANDO:\n")
            f.write(f"- **G1:** {metricas['g1_lavando_total']} minutos\n")
            f.write(f"- **G2:** {metricas['g2_lavando_total']} minutos\n\n")
            
            f.write("#### ENCHENDO:\n")
            f.write(f"- **G1:** {metricas['g1_enchendo_total']} minutos\n")
            f.write(f"- **G2:** {metricas['g2_enchendo_total']} minutos\n\n")
            
            f.write("### Taxa de ocupação das garçonetes:\n")
            f.write(f"- **G1:** {metricas['g1_taxa_ocupacao']:.1f}%\n")
            f.write(f"- **G2:** {metricas['g2_taxa_ocupacao']:.1f}%\n\n")
            
            f.write("### Taxa de ociosidade das garçonetes:\n")
            f.write(f"- **G1:** {metricas['g1_taxa_ociosidade']:.1f}%\n")
            f.write(f"- **G2:** {metricas['g2_taxa_ociosidade']:.1f}%\n\n")
            
            f.write(f"---\n*Simulação gerada em {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}*\n")
        
        print(f"✅ Log salvo em: {nome_arquivo}")
        
        # Também imprimir as métricas no console
        self.imprimir_metricas(metricas)

    # =============================================================================
    # SISTEMA DE EVENTOS
    # =============================================================================
    
    def agendar_evento(self, tempo, tipo, cliente=None, garconete=None):
        """Agenda um evento para ser processado no futuro"""
        if tempo <= self.tempo_max:
            heapq.heappush(self.fila_eventos, Evento(tempo, tipo, cliente, garconete))

    # =============================================================================
    # MÉTODO DAS TRÊS FASES
    # =============================================================================
    
    def executar_simulacao(self):
        """Executa a simulação usando o método das três fases"""
        # Cliente chega imediatamente no T=0
        self._processar_chegada_cliente()
        
        while self.fila_eventos:
            # FASE A: Avançar relógio para próximo evento
            evento = heapq.heappop(self.fila_eventos)
            self.tempo_atual = evento.tempo
            if self.tempo_atual > self.tempo_max:
                break
            
            # Registrar FASE A
            self.registrar_trace_fase('A', f"T={self.tempo_atual}")
            
            # FASE B: Processar apenas o evento atual
            self._processar_evento(evento)
            
            # FASE C: Tentar iniciar novas atividades
            self._tentar_iniciar_atividades()
        
        return pd.DataFrame(self.log_simulacao)
    
    def _processar_evento(self, evento):
        """Processa um evento individual"""
        if evento.tipo == "chegada":
            self._processar_chegada_cliente()
        elif evento.tipo == "sair_fila_chegada":
            self._processar_saida_fila_chegada(evento)
        elif evento.tipo == "encher_fim":
            self._processar_fim_encher_copo(evento)
        elif evento.tipo == "beber_fim":
            self._processar_fim_beber(evento)
        elif evento.tipo == "lavar_fim":
            self._processar_fim_lavar_copo(evento)
        
        # Após processar qualquer evento, tenta lavar copos (seguindo ordem: chega → enche → bebe → lava)
        self._tentar_lavar_copos()
    
    def _tentar_iniciar_atividades(self):
        """Tenta iniciar novas atividades na ordem de prioridade: chega → enche → bebe → lava"""
        # Atividades já são iniciadas nos métodos específicos de processamento de eventos
        pass

    # =============================================================================
    # PROCESSAMENTO DE EVENTOS
    # =============================================================================
    
    def _processar_chegada_cliente(self):
        """Processa chegada de um cliente na fila de chegada"""
        # Só permite 1 cliente na fila de chegada por vez
        if len(self.fila_chegada) == 0:
            sede = self.gerar_sede_inicial()
            cliente = Cliente(self.proximo_id_cliente, self.tempo_atual, sede)
            cliente_id = self.proximo_id_cliente
            self.proximo_id_cliente += 1
            self.clientes.append(cliente)
            self.fila_chegada.append(cliente)
            self.registrar_evento("CHEGADA", f"Cliente {cliente.id} (sede={cliente.sede_restante})")
            
            # Cliente fica na fila de chegada por um tempo
            tempo_espera = self.gerar_tempo_espera_fila_chegada()
            tempo_fim = self.tempo_atual + tempo_espera
            self.agendar_evento(tempo_fim, "sair_fila_chegada", cliente=cliente)
            self.registrar_evento("ESPERA FILA CHEGADA", f"Cliente {cliente.id} espera {tempo_espera} min")
            
            # Trace FASE C: Cliente chega
            self.registrar_trace_fase('C', f"C{cliente_id}: Chega começa T={self.tempo_atual} e termina em T={self.tempo_atual}+{tempo_espera}={tempo_fim} (tab. 3.6, N={tempo_espera}), SEDE={sede}")
            
            # Agenda próxima chegada para o momento que este cliente sair da fila
            self.agendar_evento(tempo_fim, "chegada")
    
    def _processar_saida_fila_chegada(self, evento):
        """Processa cliente saindo da fila de chegada para fila de atendimento"""
        cliente = evento.cliente
        self.fila_chegada.remove(cliente)
        self.fila_atendimento.append(cliente)
        self.registrar_evento("SAI FILA CHEGADA", f"Cliente {cliente.id} vai para atendimento")
        
        # Trace FASE B
        self.registrar_trace_fase('B', f"C{cliente.id}: Chega termina T={self.tempo_atual}")
        
        # Imediatamente tenta atender o cliente (se houver recursos)
        self._tentar_atender_clientes()
        
        # Imediatamente agenda a próxima chegada para o mesmo instante
        # Isso garante que o próximo cliente chegue no mesmo momento
        self.agendar_evento(self.tempo_atual, "chegada")

    def _processar_fim_encher_copo(self, evento):
        """Processa fim do enchimento de copo"""
        garconete = evento.garconete
        cliente = evento.cliente
        self.garconetes_disponiveis.append(garconete)
        self.registrar_evento("ENCHER TERMINA", f"{garconete} terminou Cliente {cliente.id}")
        
        # Trace FASE B
        self.registrar_trace_fase('B', f"C{cliente.id}{garconete}: Enche termina T={self.tempo_atual}")
        
        # Cliente começa a beber
        tempo_beber = self.gerar_tempo_beber()
        fim_beber = self.tempo_atual + tempo_beber
        self.agendar_evento(fim_beber, "beber_fim", cliente=cliente)
        self.registrar_evento("BEBER INICIA", f"Cliente {cliente.id} até {fim_beber}")
        
        # Trace FASE C
        self.registrar_trace_fase('C', f"C{cliente.id}: Bebe começa T={self.tempo_atual} e termina em T={self.tempo_atual}+{tempo_beber}={fim_beber} (tab. 3.8, N={tempo_beber})")

    def _processar_fim_beber(self, evento):
        """Processa fim de beber"""
        cliente = evento.cliente
        cliente.sede_restante -= 1
        self.copos_sujos += 1
        self.registrar_evento("BEBER TERMINA", f"Cliente {cliente.id}, sede={cliente.sede_restante}")
        
        # Trace FASE B
        self.registrar_trace_fase('B', f"C{cliente.id}: Bebe termina T={self.tempo_atual}, SEDE={cliente.sede_restante}")
        
        if cliente.sede_restante > 0:
            # Cliente vai para fila dos que terminaram de beber (aguarda próximo copo)
            self.fila_terminaram_beber.append(cliente)
            self.registrar_evento("FILA TERMINARAM BEBER", f"Cliente {cliente.id} aguarda próximo copo")
        else:
            # Cliente sai do sistema
            self.registrar_evento("SAÍDA", f"Cliente {cliente.id} saiu")

    def _processar_fim_lavar_copo(self, evento):
        """Processa fim da lavagem de copo"""
        garconete = evento.garconete
        if self.copos_sujos > 0:
            self.copos_limpos += 1
            self.copos_sujos -= 1
            self.registrar_evento("LAVAR TERMINA", f"{garconete} lavou 1 copo")
            
            # Trace FASE B
            self.registrar_trace_fase('B', f"O{garconete}: Lava termina T={self.tempo_atual}")
        
        self.garconetes_disponiveis.append(garconete)
        
        # Após lavar, tenta atender clientes (incluindo os que terminaram de beber)
        self._tentar_atender_clientes()

    # =============================================================================
    # INICIAÇÃO DE ATIVIDADES
    # =============================================================================
    
    def _tentar_atender_clientes(self):
        """Tenta atender clientes seguindo ordem: chega → enche → bebe → lava"""
        # 1. PRIORIDADE: Atender clientes da fila de chegada (chega → enche)
        while (self.fila_atendimento and 
               self.garconetes_disponiveis and 
               self.copos_limpos > 0):
            
            cliente = self.fila_atendimento.pop(0)
            garconete = self.garconetes_disponiveis.pop(0)
            self.copos_limpos -= 1
            
            tempo_encher = self.gerar_tempo_encher_copo()
            fim_encher = self.tempo_atual + tempo_encher
            self.agendar_evento(fim_encher, "encher_fim", cliente=cliente, garconete=garconete)
            self.registrar_evento("ENCHER INICIA", f"{garconete} para Cliente {cliente.id} até {fim_encher}")
            
            # Trace FASE C
            self.registrar_trace_fase('C', f"C{cliente.id}{garconete}: Enche começa T={self.tempo_atual} e termina em T={self.tempo_atual}+{tempo_encher}={fim_encher} (tab. 3.9, N={tempo_encher})")
        
        # 2. SEGUNDA PRIORIDADE: Atender clientes que terminaram de beber (bebe → enche)
        while (self.fila_terminaram_beber and 
               self.garconetes_disponiveis and 
               self.copos_limpos > 0):
            
            cliente = self.fila_terminaram_beber.pop(0)
            garconete = self.garconetes_disponiveis.pop(0)
            self.copos_limpos -= 1
            
            tempo_encher = self.gerar_tempo_encher_copo()
            fim_encher = self.tempo_atual + tempo_encher
            self.agendar_evento(fim_encher, "encher_fim", cliente=cliente, garconete=garconete)
            self.registrar_evento("ENCHER INICIA", f"{garconete} para Cliente {cliente.id} até {fim_encher}")
            
            # Trace FASE C
            self.registrar_trace_fase('C', f"C{cliente.id}{garconete}: Enche começa T={self.tempo_atual} e termina em T={self.tempo_atual}+{tempo_encher}={fim_encher} (tab. 3.9, N={tempo_encher})")

    def _tentar_lavar_copos(self):
        """Tenta lavar copos sujos (seguindo ordem de prioridade: chega → enche → bebe → lava)"""
        # Lavagem pode acontecer mesmo com clientes na fila, mas com prioridade menor
        if (self.copos_sujos > 0 and self.garconetes_disponiveis):
            
            garconete = self.garconetes_disponiveis.pop(0)
            tempo_lavar = self.gerar_tempo_lavar_copo()
            fim_lavar = self.tempo_atual + tempo_lavar
            self.agendar_evento(fim_lavar, "lavar_fim", garconete=garconete)
            self.registrar_evento("LAVAR INICIA", f"{garconete} até {fim_lavar}")
            
            # Trace FASE C
            self.registrar_trace_fase('C', f"O{garconete}: Lava começa T={self.tempo_atual} e termina em T={self.tempo_atual}+{tempo_lavar}={fim_lavar} (N={tempo_lavar})")

# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    # Argumentos padrão
    tempo_max = 30
    
    # Parse argumentos da linha de comando
    if len(sys.argv) > 1:
        try:
            tempo_max = int(sys.argv[1])
        except ValueError:
            print("Uso: python pub_sim_final.py [tempo_max]")
            print("Exemplo: python pub_sim_final.py 50")
            sys.exit(1)
    
    print("="*80)
    print("🍺 SIMULAÇÃO DO PUB - Método das Três Fases")
    print("="*80)
    print(f"\n⏱️  Tempo máximo: {tempo_max} minutos")
    print("📊 Usando tabelas pré-definidas (3.6, 3.7, 3.8, 3.9)")
    print("\n" + "="*80)
    
    # Criar e executar simulador
    simulador = SimuladorPUB(tempo_max=tempo_max)
    log = simulador.executar_simulacao()
    
    # Imprimir trace das três fases
    simulador.imprimir_trace_tres_fases()
    
    # Imprimir e salvar métricas
    metricas = simulador.calcular_metricas()
    simulador.imprimir_metricas(metricas)
    
    # Salvar log detalhado em arquivo Markdown
    simulador.salvar_log_markdown("log_simulacao_pub.md")
    
    print("\n✅ Simulação concluída com sucesso!")
    print(f"📄 Log detalhado salvo em: log_simulacao_pub.md")
