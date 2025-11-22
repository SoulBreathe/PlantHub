import sqlite3
from typing import List, Optional
from models.local import Local
from models.especie import Especie
from models.planta import Planta
from models.diario import EntradaDiario
from models.agenda import TarefaAgenda
from models.planta_completa import PlantaCompleta
from models.praga import Praga
from models.registro_praga import RegistroPraga
from models.pergunta import PerguntaDiagnostico
from models.resposta import RespostaDiagnostico


class DatabaseService:
    _instance: Optional["DatabaseService"] = None
    _connection: Optional[sqlite3.Connection] = None

    DATABASE_PATH = "database/Horta.db"
    SCHEMA_PATH = "database/schema.sql"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.connect()
        return cls._instance

    def connect(self) -> None:
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(self.DATABASE_PATH)
                self._connection.execute("PRAGMA foreign_keys = ON;")
                print("Conexão com o banco de dados estabelecida com sucesso.")
                self._create_database()
            except sqlite3.Error as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                self._connection = None

    def _create_database(self) -> None:
        if self._connection:
            try:
                print("Verificando e criando tabelas se necessário...")
                with open(self.SCHEMA_PATH, "r") as f:
                    schema_script = f.read()
                self._connection.executescript(schema_script)
                self._connection.commit()
                print("Tabelas criadas com sucesso.")
            except FileNotFoundError:
                print(f"Erro: Arquivo de schema não encontrado em {self.SCHEMA_PATH}")
            except sqlite3.Error as e:
                print(f"Erro ao executar o script de schema: {e}")

    def get_connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise ConnectionError(
                "A conexão com o banco de dados não foi estabelecida."
            )
        return self._connection

    def close_connection(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Conexão com o banco de dados fechada.")

    # === Locais ===
    def get_all_locais(self) -> List[Local]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_local, nome, descricao, tipo, area_m2 
            FROM Locais 
            ORDER BY nome
        """
        )
        return [
            Local(
                id_local=row[0],
                nome=row[1],
                descricao=row[2],
                tipo=row[3] or "outro",
                area_m2=row[4] or 0.0,
            )
            for row in cursor.fetchall()
        ]

    def add_local(self, local: Local) -> Local:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Locais (nome, descricao, tipo, area_m2) VALUES (?, ?, ?, ?)",
                (local.nome, local.descricao, local.tipo, local.area_m2),
            )
            conn.commit()
            new_id = cursor.lastrowid
            return Local(
                id_local=new_id,
                nome=local.nome,
                descricao=local.descricao,
                tipo=local.tipo,
                area_m2=local.area_m2,
            )
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                raise ValueError(f"Local '{local.nome}' já existe.")
            raise

    # === Espécies ===
    def get_all_especies(self) -> List[Especie]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_especie, nome_popular, nome_cientifico, instrucoes_rega,
                   necessidade_sol, necessidade_poda, uso_adubos, epoca_plantio
            FROM Especies
            ORDER BY nome_popular
        """
        )
        return [
            Especie(
                id_especie=row[0],
                nome_popular=row[1],
                nome_cientifico=row[2],
                instrucoes_rega=row[3],
                necessidade_sol=row[4],
                necessidade_poda=row[5],
                uso_adubos=row[6],
                epoca_plantio=row[7],
            )
            for row in cursor.fetchall()
        ]

    def add_especie(self, especie: Especie) -> Especie:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Especies (
                    nome_popular, nome_cientifico, instrucoes_rega,
                    necessidade_sol, necessidade_poda, uso_adubos, epoca_plantio
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    especie.nome_popular,
                    especie.nome_cientifico,
                    especie.instrucoes_rega,
                    especie.necessidade_sol,
                    especie.necessidade_poda,
                    especie.uso_adubos,
                    especie.epoca_plantio,
                ),
            )
            conn.commit()
            new_id = cursor.lastrowid
            return Especie(
                id_especie=new_id,
                nome_popular=especie.nome_popular,
                nome_cientifico=especie.nome_cientifico,
                instrucoes_rega=especie.instrucoes_rega,
                necessidade_sol=especie.necessidade_sol,
                necessidade_poda=especie.necessidade_poda,
                uso_adubos=especie.uso_adubos,
                epoca_plantio=especie.epoca_plantio,
            )
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                raise ValueError(f"Espécie '{especie.nome_popular}' já existe.")
            raise

    # === MinhasPlantas ===
    def get_all_plantas(self) -> List[Planta]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_planta, nome_personalizado, data_plantio, id_especie, id_local
            FROM MinhasPlantas
            ORDER BY nome_personalizado
        """
        )
        return [
            Planta(
                id_planta=row[0],
                nome_personalizado=row[1],
                data_plantio=row[2],
                id_especie=row[3],
                id_local=row[4],
            )
            for row in cursor.fetchall()
        ]

    def add_planta(self, planta: Planta) -> Planta:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO MinhasPlantas (nome_personalizado, data_plantio, id_especie, id_local)
            VALUES (?, ?, ?, ?)
        """,
            (
                planta.nome_personalizado,
                planta.data_plantio,
                planta.id_especie,
                planta.id_local,
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return Planta(
            id_planta=new_id,
            nome_personalizado=planta.nome_personalizado,
            data_plantio=planta.data_plantio,
            id_especie=planta.id_especie,
            id_local=planta.id_local,
        )

    def get_plantas_completas(self) -> List[PlantaCompleta]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                mp.id_planta,
                mp.nome_personalizado,
                e.nome_popular,
                l.nome AS nome_local,
                mp.data_plantio
            FROM MinhasPlantas mp
            LEFT JOIN Especies e ON mp.id_especie = e.id_especie
            LEFT JOIN Locais l ON mp.id_local = l.id_local
            ORDER BY mp.nome_personalizado ASC
        """
        )
        rows = cursor.fetchall()
        return [
            PlantaCompleta(
                id_planta=row[0],
                nome_personalizado=row[1],
                nome_popular=row[2] or "—",
                nome_local=row[3] or "—",
                data_plantio=row[4],
            )
            for row in rows
        ]

    # === Diário ===
    def get_diario_por_planta(self, id_planta: int) -> List[EntradaDiario]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_diario, data_registro, observacao, caminho_foto, id_planta
            FROM DiarioDePlanta
            WHERE id_planta = ?
            ORDER BY data_registro DESC
        """,
            (id_planta,),
        )
        return [
            EntradaDiario(
                id_diario=row[0],
                data_registro=row[1],
                observacao=row[2],
                caminho_foto=row[3],
                id_planta=row[4],
            )
            for row in cursor.fetchall()
        ]

    def add_entrada_diario(self, entrada: EntradaDiario) -> EntradaDiario:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO DiarioDePlanta (data_registro, observacao, caminho_foto, id_planta)
            VALUES (?, ?, ?, ?)
        """,
            (
                entrada.data_registro,
                entrada.observacao,
                entrada.caminho_foto,
                entrada.id_planta,
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return EntradaDiario(
            id_diario=new_id,
            data_registro=entrada.data_registro,
            observacao=entrada.observacao,
            caminho_foto=entrada.caminho_foto,
            id_planta=entrada.id_planta,
        )

    # === Agenda ===
    def get_agenda_pendente(self) -> List[TarefaAgenda]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_agenda, tipo_tarefa, detalhes, data_agendada, realizada, id_planta
            FROM AgendaDeCuidados
            WHERE realizada = 0
            ORDER BY data_agendada
        """
        )
        return [
            TarefaAgenda(
                id_agenda=row[0],
                tipo_tarefa=row[1],
                detalhes=row[2],
                data_agendada=row[3],
                realizada=bool(row[4]),
                id_planta=row[5],
            )
            for row in cursor.fetchall()
        ]

    def add_tarefa_agenda(self, tarefa: TarefaAgenda) -> TarefaAgenda:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO AgendaDeCuidados (tipo_tarefa, detalhes, data_agendada, realizada, id_planta)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                tarefa.tipo_tarefa,
                tarefa.detalhes,
                tarefa.data_agendada,
                int(tarefa.realizada),
                tarefa.id_planta,
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return TarefaAgenda(
            id_agenda=new_id,
            tipo_tarefa=tarefa.tipo_tarefa,
            detalhes=tarefa.detalhes,
            data_agendada=tarefa.data_agendada,
            realizada=tarefa.realizada,
            id_planta=tarefa.id_planta,
        )

    # === Pragas ===
    def get_all_pragas(self) -> List[Praga]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_praga, nome_comum, descricao, sintomas, tratamento
            FROM PragasDoencas
            ORDER BY nome_comum
        """
        )
        return [
            Praga(
                id_praga=row[0],
                nome_comum=row[1],
                descricao=row[2],
                sintomas=row[3],
                tratamento=row[4],
            )
            for row in cursor.fetchall()
        ]

    # === Diagnóstico ===
    def get_perguntas_ordenadas(self) -> List[PerguntaDiagnostico]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_pergunta, text_pergunta, ordem
            FROM DiagnosticoPerguntas
            ORDER BY ordem
        """
        )
        return [
            PerguntaDiagnostico(
                id_pergunta=row[0],
                texto_pergunta=row[1],
                ordem=row[2],
            )
            for row in cursor.fetchall()
        ]

    def get_respostas_por_pergunta(self, id_pergunta: int) -> List[RespostaDiagnostico]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_resposta, texto_resposta, id_pergunta
            FROM DiagnosticoRespostas
            WHERE id_pergunta = ?
            ORDER BY id_resposta
        """,
            (id_pergunta,),
        )
        return [
            RespostaDiagnostico(
                id_resposta=row[0],
                texto_resposta=row[1],
                id_pergunta=row[2],
            )
            for row in cursor.fetchall()
        ]
