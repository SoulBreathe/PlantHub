import sqlite3
from typing import Optional

class DatabaseService: 
    _instance: Optional['DatabaseService'] = None
    _connection: Optional[sqlite3.Connection] = None

    DATABASE_PATH = 'database/Horta.db'
    SCHEMA_PATH = 'database/schema.sql'

    def __new__(cls):
        """
        Implementa o padrao Singleton para garantir uma única instância de classe.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.connect()
        return cls._instance
    
    def connect(self) -> None:
        """
        Estabelece a conexão com o banco de dados e cria as tabelas se não existirem. 
        """
        if self._connection is None:
            try: 
                self._connection = sqlite3.connect(self.DATABASE_PATH)
                print("Conexão com o banco de dados estabelecida com sucesso.")
                self._create_database()
            except sqlite3.Error as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                self._connection = None

    def _create_database(self) -> None:
        """
        Método privado para ler o arquivo schema.sql e criar as tabelas.
        """
        if self._connection:
            try: 
                print("Verificando e criando tabelas se necessário...")
                with open(self.SCHEMA_PATH, 'r') as f:
                    schema_script = f.read()
                self._connection.executescript(schema_script)
                self._connection.commit()
                print("Tabelas criadas com sucesso.")
            except FileNotFoundError:
                print(f"Erro: Arquivo de schema não encontrado em {self.SCHEMA_PATH}")
            except sqlite3.Error as e:
                print(f"Erro ao executar o script de schema: {e}")

    def get_connection(self) -> sqlite3.Connection:
        """
        Retorna a conexão ativa com o banco de dados. 
        Lança uma exceção se a conexão não estiver estabelecida.
        """
        if self._connection is None:
            raise ConnectionError("A conexão com o baco de dados não foi estabelecidade.")
        return self._connection
    
    def close_connection(self) -> None:
        """
        Fecha a conexão com o banco de dados se estiver aberta.
        """
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Conexão com o banco de dados fechada.")