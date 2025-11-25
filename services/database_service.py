import os
import sqlite3
from typing import List, Optional

# Imports dos Models
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
        self._seed_initial_data()  # Popula a base fixa

    def connect(self) -> None:
        if self._connection is None:
            try:
                # check_same_thread=False é vital para Flet
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
        """Insere dados fixos (Espécies/Pragas) se as tabelas estiverem vazias."""
        if not self._connection:
            return
        cursor = self._connection.cursor()

        # 1. Seed Espécies
        cursor.execute("SELECT COUNT(*) FROM Especies")
        if cursor.fetchone()[0] == 0:
            print("Populando Espécies base...")
            especies_base = [
                (
                    "Hortelã",
                    "Mentha sp.",
                    "Diária",
                    "Sombra parcial",
                    "Regular",
                    "Orgânico",
                    "Todo ano",
                ),
                (
                    "Tomate",
                    "Solanum lycopersicum",
                    "Regular",
                    "Sol Pleno",
                    "Regular",
                    "Rico em Potássio",
                    "Primavera",
                ),
                (
                    "Manjericão",
                    "Ocimum basilicum",
                    "Moderada",
                    "Sol Pleno",
                    "Poda floral",
                    "Orgânico",
                    "Verão",
                ),
            ]
            cursor.executemany(
                """
                INSERT INTO Especies (nome_popular, nome_cientifico, instrucoes_rega, necessidade_sol, necessidade_poda, uso_adubos, epoca_plantio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                especies_base,
            )
            self._connection.commit()

        # 2. Seed Pragas
        cursor.execute("SELECT COUNT(*) FROM PragasDoencas")
        if cursor.fetchone()[0] == 0:
            print("Populando Pragas base...")
            pragas_base = [
                (
                    "Pulgão",
                    "Pequenos insetos verdes/pretos.",
                    "Folhas amarelas e enroladas.",
                    "Óleo de Neem.",
                    "assets/pragas/pulgao.png",
                ),
                (
                    "Cochonilha",
                    "Manchas brancas algodonosas.",
                    "Planta pegajosa e fraca.",
                    "Cotonete com álcool.",
                    "assets/pragas/cochonilha.png",
                ),
            ]
            cursor.executemany(
                """
                INSERT INTO PragasDoencas (nome_comum, descricao, sintomas, tratamento, foto_exemplo)
                VALUES (?, ?, ?, ?, ?)
            """,
                pragas_base,
            )
            self._connection.commit()

    def get_connection(self) -> sqlite3.Connection:
        if self._connection is None:
            self.connect()
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    # =========================================================================
    #  MÉTODOS CRUD (Locais, Plantas, Agenda, etc.)
    # =========================================================================

    # --- AGENDA ---
    def get_agenda_pendente(self) -> List[TarefaAgenda]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM AgendaDeCuidados WHERE realizada = 0 ORDER BY data_agendada"
        )
        return [TarefaAgenda(*row) for row in cursor.fetchall()]

    def add_tarefa_agenda(self, t: TarefaAgenda):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO AgendaDeCuidados (tipo_tarefa, detalhes, data_agendada, realizada, id_planta)
            VALUES (?, ?, ?, ?, ?)""",
            (t.tipo_tarefa, t.detalhes, t.data_agendada, int(t.realizada), t.id_planta),
        )
        conn.commit()
        t.id_agenda = cur.lastrowid

    def marcar_tarefa_realizada(self, id_agenda: int):
        self.get_connection().execute(
            "UPDATE AgendaDeCuidados SET realizada = 1 WHERE id_agenda = ?",
            (id_agenda,),
        ).commit()

    # --- DIAGNÓSTICO ---
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
            """
            SELECT p.* FROM DiagnosticoMapeamento m
            JOIN PragasDoencas p ON m.id_praga = p.id_praga
            WHERE m.id_resposta = ?
        """,
            (id_resposta,),
        )
        row = cur.fetchone()
        return Praga(*row) if row else None

    # --- DIÁRIO ---
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
        cur.execute(
            "INSERT INTO DiarioDePlanta (data_registro, observacao, caminho_foto, id_planta) VALUES (?, ?, ?, ?)",
            (d.data_registro, d.observacao, d.caminho_foto, d.id_planta),
        )
        conn.commit()

    # --- ESPÉCIES ---
    def get_all_especies(self) -> List[Especie]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM Especies ORDER BY nome_popular")
        return [Especie(*r) for r in cur.fetchall()]

    def add_especie(self, e: Especie):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Especies (nome_popular, nome_cientifico, instrucoes_rega, necessidade_sol, necessidade_poda, uso_adubos, epoca_plantio)
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
            conn.commit()
            e.id_especie = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Espécie '{e.nome_popular}' já existe.")

    # --- LOCAIS ---
    def get_all_locais(self) -> List[Local]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM Locais ORDER BY nome")
        return [Local(*r) for r in cur.fetchall()]

    def add_local(self, l: Local):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Locais (nome, descricao, tipo, area_m2) VALUES (?, ?, ?, ?)",
                (l.nome, l.descricao, l.tipo, l.area_m2),
            )
            conn.commit()
            l.id_local = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Local '{l.nome}' já existe.")

    # --- PLANTAS ---
    def get_all_plantas(self) -> List[Planta]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM MinhasPlantas ORDER BY nome_personalizado")
        return [Planta(*r) for r in cur.fetchall()]

    def get_plantas_completas(self) -> List[PlantaCompleta]:
        cur = self.get_connection().cursor()
        cur.execute(
            """
            SELECT mp.id_planta, mp.nome_personalizado, e.nome_popular, l.nome, mp.data_plantio
            FROM MinhasPlantas mp
            LEFT JOIN Especies e ON mp.id_especie = e.id_especie
            LEFT JOIN Locais l ON mp.id_local = l.id_local
            ORDER BY mp.nome_personalizado ASC
        """
        )
        # Nota: Ajuste os índices aqui se PlantaCompleta tiver campos diferentes dos retornados
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

    # --- PRAGAS & REGISTROS ---
    def get_all_pragas(self) -> List[Praga]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT * FROM PragasDoencas ORDER BY nome_comum")
        return [Praga(*r) for r in cur.fetchall()]

    def add_registro_praga(self, r: RegistroPraga):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO RegistroDePragas (data_identificacao, status_tratamento, id_planta, id_praga) VALUES (?, ?, ?, ?)",
            (r.data_identificacao, r.status_tratamento, r.id_planta, r.id_praga),
        )
        conn.commit()
