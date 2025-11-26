import os
import sqlite3
from typing import List, Optional
from datetime import date

# --- Imports dos Models ---
from models.agenda import TarefaAgenda
from models.diario import EntradaDiario
from models.especie import Especie
from models.local import Local
from models.pergunta import PerguntaDiagnostico
from models.planta import Planta
from models.planta_completa import PlantaCompleta
from models.praga import Praga
from models.registro_praga import RegistroPraga
from models.resposta import RespostaDiagnostico
from database.seeds import popular_banco


class DatabaseService:
    _instance: Optional["DatabaseService"] = None
    _connection: Optional[sqlite3.Connection] = None

    # Caminhos absolutos
    DATABASE_PATH = os.path.join(os.getcwd(), "database", "Horta.db")
    SCHEMA_PATH = os.path.join(os.getcwd(), "database", "schema.sql")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicia conexão, cria tabelas e popula dados base se necessário."""
        os.makedirs(os.path.dirname(self.DATABASE_PATH), exist_ok=True)
        self.connect()
        self._seed_initial_data()

    def connect(self) -> None:
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(
                    self.DATABASE_PATH, check_same_thread=False
                )
                self._connection.execute("PRAGMA foreign_keys = ON;")
                self._create_database()
            except sqlite3.Error as e:
                print(f"Erro BD: {e}")
                self._connection = None

    def _create_database(self) -> None:
        if self._connection and os.path.exists(self.SCHEMA_PATH):
            with open(self.SCHEMA_PATH, "r", encoding="utf-8") as f:
                self._connection.executescript(f.read())
            self._connection.commit()

    def _seed_initial_data(self):
        """Chama o arquivo externo de seeds para popular dados fixos."""
        if not self._connection:
            return

        try:
            popular_banco(self._connection)
        except Exception as e:
            print(f"Erro ao popular seeds: {e}")

    def get_connection(self) -> sqlite3.Connection:
        if self._connection is None:
            self.connect()
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    # =========================================================================
    #  1. AGENDA (COMPLETA: Abas, Dashboard, Edição)
    # =========================================================================

    def get_agenda_futura(self) -> List[TarefaAgenda]:
        hoje = date.today().strftime("%Y-%m-%d")
        cur = self.get_connection().cursor()
        cur.execute(
            "SELECT * FROM AgendaDeCuidados WHERE realizada = 0 AND data_agendada >= ? ORDER BY data_agendada ASC",
            (hoje,),
        )
        return [TarefaAgenda(*row) for row in cur.fetchall()]

    def get_agenda_atrasada(self) -> List[TarefaAgenda]:
        hoje = date.today().strftime("%Y-%m-%d")
        cur = self.get_connection().cursor()
        cur.execute(
            "SELECT * FROM AgendaDeCuidados WHERE realizada = 0 AND data_agendada < ? ORDER BY data_agendada ASC",
            (hoje,),
        )
        return [TarefaAgenda(*row) for row in cur.fetchall()]

    # Mantido para compatibilidade se alguma view antiga chamar
    def get_agenda_pendente(self) -> List[TarefaAgenda]:
        return self.get_agenda_futura() + self.get_agenda_atrasada()

    def get_estatisticas_agenda(self) -> dict:
        hoje = date.today().strftime("%Y-%m-%d")
        cur = self.get_connection().cursor()
        pendentes = cur.execute(
            "SELECT COUNT(*) FROM AgendaDeCuidados WHERE realizada = 0 AND data_agendada >= ?",
            (hoje,),
        ).fetchone()[0]
        atrasadas = cur.execute(
            "SELECT COUNT(*) FROM AgendaDeCuidados WHERE realizada = 0 AND data_agendada < ?",
            (hoje,),
        ).fetchone()[0]
        concluidas = cur.execute(
            "SELECT COUNT(*) FROM AgendaDeCuidados WHERE realizada = 1"
        ).fetchone()[0]
        return {
            "pendentes": pendentes,
            "atrasadas": atrasadas,
            "concluidas": concluidas,
        }

    def add_tarefa_agenda(self, t: TarefaAgenda):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO AgendaDeCuidados (tipo_tarefa, detalhes, data_agendada, realizada, id_planta)
                       VALUES (?, ?, ?, ?, ?)""",
            (t.tipo_tarefa, t.detalhes, t.data_agendada, int(t.realizada), t.id_planta),
        )
        conn.commit()
        t.id_agenda = cur.lastrowid

    def marcar_tarefa_realizada(self, id_agenda: int):
        from datetime import date

        hoje = date.today().strftime("%Y-%m-%d")

        conn = self.get_connection()

        conn.execute(
            """
            UPDATE AgendaDeCuidados 
            SET realizada = 1, data_conclusao = ? 
            WHERE id_agenda = ?
        """,
            (hoje, id_agenda),
        )

        conn.commit()

    def get_tarefa_por_id(self, id_agenda: int) -> Optional[TarefaAgenda]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM AgendaDeCuidados WHERE id_agenda = ?", (id_agenda,))
        row = cur.fetchone()
        return TarefaAgenda(*row) if row else None

    def update_tarefa_agenda(self, t: TarefaAgenda):
        conn = self.get_connection()
        conn.execute(
            """
            UPDATE AgendaDeCuidados 
            SET tipo_tarefa = ?, detalhes = ?, data_agendada = ?, id_planta = ? 
            WHERE id_agenda = ?
        """,
            (t.tipo_tarefa, t.detalhes, t.data_agendada, t.id_planta, t.id_agenda),
        )
        conn.commit()

    def delete_tarefa_agenda(self, id_agenda: int):
        conn = self.get_connection()
        conn.execute("DELETE FROM AgendaDeCuidados WHERE id_agenda = ?", (id_agenda,))
        conn.commit()

    # =========================================================================
    #  2. DIAGNÓSTICO
    # =========================================================================
    def get_pergunta_por_ordem(self, ordem: int) -> Optional[PerguntaDiagnostico]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM DiagnosticoPerguntas WHERE ordem = ?", (ordem,))
        row = cur.fetchone()
        return PerguntaDiagnostico(*row) if row else None

    def get_respostas_por_pergunta(self, id_pergunta: int) -> List[RespostaDiagnostico]:
        cur = self.get_connection().cursor()
        cur.execute(
            "SELECT * FROM DiagnosticoRespostas WHERE id_pergunta = ?", (id_pergunta,)
        )
        return [RespostaDiagnostico(*r) for r in cur.fetchall()]

    def verificar_diagnostico(self, id_resposta: int) -> Optional[Praga]:
        cur = self.get_connection().cursor()
        cur.execute(
            """SELECT p.* FROM DiagnosticoMapeamento m
                       JOIN PragasDoencas p ON m.id_praga = p.id_praga
                       WHERE m.id_resposta = ?""",
            (id_resposta,),
        )
        row = cur.fetchone()
        return Praga(*row) if row else None

    # =========================================================================
    #  3. DIÁRIO
    # =========================================================================
    def get_diario_por_planta(self, id_planta: int) -> List[EntradaDiario]:
        cur = self.get_connection().cursor()
        cur.execute(
            "SELECT * FROM DiarioDePlanta WHERE id_planta = ? ORDER BY data_registro DESC",
            (id_planta,),
        )
        return [EntradaDiario(*r) for r in cur.fetchall()]

    def add_entrada_diario(self, d: EntradaDiario):
        conn = self.get_connection()
        cur = conn.cursor()
        # CORRIGIDO: 5 parâmetros
        cur.execute(
            "INSERT INTO DiarioDePlanta (data_registro, titulo, observacao, caminho_foto, id_planta) VALUES (?, ?, ?, ?, ?)",
            (d.data_registro, d.titulo, d.observacao, d.caminho_foto, d.id_planta),
        )
        conn.commit()
        d.id_diario = cur.lastrowid
        return d

    # =========================================================================
    #  4. ESPÉCIES
    # =========================================================================
    def get_all_especies(self) -> List[Especie]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM Especies ORDER BY nome_popular")
        return [Especie(*r) for r in cur.fetchall()]

    def add_especie(self, e: Especie):
        try:
            cur = self.get_connection().cursor()
            cur.execute(
                """INSERT INTO Especies (nome_popular, nome_cientifico, instrucoes_rega, necessidade_sol, necessidade_poda, uso_adubos, epoca_plantio)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    e.nome_popular,
                    e.nome_cientifico,
                    e.instrucoes_rega,
                    e.necessidade_sol,
                    e.necessidade_poda,
                    e.uso_adubos,
                    e.epoca_plantio,
                ),
            )
            self.get_connection().commit()
            e.id_especie = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Espécie '{e.nome_popular}' já existe.")

    # =========================================================================
    #  5. LOCAIS
    # =========================================================================
    def get_all_locais(self) -> List[Local]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM Locais ORDER BY nome")
        return [Local(*r) for r in cur.fetchall()]

    def add_local(self, l: Local):
        try:
            cur = self.get_connection().cursor()
            cur.execute(
                "INSERT INTO Locais (nome, descricao, tipo, area_m2) VALUES (?, ?, ?, ?)",
                (l.nome, l.descricao, l.tipo, l.area_m2),
            )
            self.get_connection().commit()
            l.id_local = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Local '{l.nome}' já existe.")

    # =========================================================================
    #  6. PLANTAS (COMPLETO: Update, Delete, GetById)
    # =========================================================================
    def get_all_plantas(self) -> List[Planta]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM MinhasPlantas ORDER BY nome_personalizado")
        return [Planta(*r) for r in cur.fetchall()]

    def get_plantas_completas(self) -> List[PlantaCompleta]:
        cur = self.get_connection().cursor()
        cur.execute(
            """SELECT mp.id_planta, mp.nome_personalizado, e.nome_popular, l.nome, mp.data_plantio
                       FROM MinhasPlantas mp
                       LEFT JOIN Especies e ON mp.id_especie = e.id_especie
                       LEFT JOIN Locais l ON mp.id_local = l.id_local
                       ORDER BY mp.nome_personalizado ASC"""
        )
        return [
            PlantaCompleta(
                id_planta=r[0],
                nome_personalizado=r[1],
                nome_popular=r[2] or "-",
                nome_local=r[3] or "-",
                data_plantio=r[4],
            )
            for r in cur.fetchall()
        ]

    def add_planta(self, p: Planta):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO MinhasPlantas (nome_personalizado, data_plantio, id_especie, id_local) VALUES (?, ?, ?, ?)",
            (p.nome_personalizado, p.data_plantio, p.id_especie, p.id_local),
        )
        conn.commit()
        p.id_planta = cur.lastrowid

    def get_planta_por_id(self, id_planta: int) -> Optional[Planta]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM MinhasPlantas WHERE id_planta = ?", (id_planta,))
        row = cur.fetchone()
        return Planta(*row) if row else None

    def update_planta(self, p: Planta):
        self.get_connection().execute(
            """
            UPDATE MinhasPlantas SET nome_personalizado = ?, data_plantio = ?, id_especie = ?, id_local = ? WHERE id_planta = ?
        """,
            (
                p.nome_personalizado,
                p.data_plantio,
                p.id_especie,
                p.id_local,
                p.id_planta,
            ),
        ).commit()

    def delete_planta(self, id_planta: int):
        conn = self.get_connection()
        conn.execute("DELETE FROM DiarioDePlanta WHERE id_planta = ?", (id_planta,))
        conn.execute("DELETE FROM AgendaDeCuidados WHERE id_planta = ?", (id_planta,))
        conn.execute("DELETE FROM MinhasPlantas WHERE id_planta = ?", (id_planta,))
        conn.commit()

    # =========================================================================
    #  7. PRAGAS & REGISTROS
    # =========================================================================
    def get_all_pragas(self) -> List[Praga]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM PragasDoencas ORDER BY nome_comum")
        return [Praga(*r) for r in cur.fetchall()]

    def add_praga(self, p: Praga):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO PragasDoencas (nome_comum, descricao, sintomas, tratamento, foto_exemplo) VALUES (?, ?, ?, ?, ?)",
                (p.nome_comum, p.descricao, p.sintomas, p.tratamento, p.foto_exemplo),
            )
            conn.commit()
            p.id_praga = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Praga '{p.nome_comum}' já existe.")

    def add_registro_praga(self, r: RegistroPraga):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO RegistroDePragas (data_identificacao, status_tratamento, id_planta, id_praga) VALUES (?, ?, ?, ?)",
            (r.data_identificacao, r.status_tratamento, r.id_planta, r.id_praga),
        )
        conn.commit()

    # =========================================================================
    #  8. DASHBOARD HOME
    # =========================================================================
    def get_resumo_dashboard(self) -> dict:
        cur = self.get_connection().cursor()
        qtd_plantas = cur.execute("SELECT COUNT(*) FROM MinhasPlantas").fetchone()[0]
        qtd_locais = cur.execute("SELECT COUNT(*) FROM Locais").fetchone()[0]
        qtd_agenda = cur.execute(
            "SELECT COUNT(*) FROM AgendaDeCuidados WHERE realizada = 0"
        ).fetchone()[0]
        qtd_diario = cur.execute("SELECT COUNT(*) FROM DiarioDePlanta").fetchone()[0]
        return {
            "plantas": qtd_plantas,
            "locais": qtd_locais,
            "agenda": qtd_agenda,
            "diario": qtd_diario,
        }
