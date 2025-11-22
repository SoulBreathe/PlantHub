-- Tabela para armazenar os locais de cultivo
CREATE TABLE IF NOT EXISTS Locais (
    id_local INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    tipo TEXT,
    area_m2 REAL DEFAULT 0.0
);

-- Tabela para catálogo de espécies de plantas
CREATE TABLE IF NOT EXISTS Especies (
    id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_popular TEXT NOT NULL UNIQUE,
    nome_cientifico TEXT,
    instrucoes_rega TEXT,
    necessidade_sol TEXT,
    necessidade_poda TEXT,
    uso_adubos TEXT,
    epoca_plantio TEXT 
);

-- Tabela para plantas que o usuário possui
CREATE TABLE IF NOT EXISTS MinhasPlantas (
    id_planta INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_personalizado TEXT NOT NULL,
    data_plantio DATE,
    id_especie INTEGER NOT NULL,
    id_local INTEGER NOT NULL,
    FOREIGN KEY (id_especie) REFERENCES Especies(id_especie)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (id_local) REFERENCES Locais(id_local) 
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabela para agendar os cuidados (rega, adubação, etc...)
CREATE TABLE IF NOT EXISTS AgendaDeCuidados (
    id_agenda INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_tarefa TEXT NOT NULL,
    detalhes TEXT,
    data_agendada DATE NOT NULL CHECK (data_agendada >= date('now')),
    realizada INTEGER NOT NULL DEFAULT 0,
    id_planta INTEGER NOT NULL,
    FOREIGN KEY (id_planta) REFERENCES MinhasPlantas(id_planta)
);

-- Tabela para o diário de bordo de cada planta
CREATE TABLE IF NOT EXISTS DiarioDePlanta (
    id_diario INTEGER PRIMARY KEY AUTOINCREMENT,
    data_registro DATE NOT NULL,
    observacao TEXT NOT NULL,
    caminho_foto TEXT,
    id_planta INTEGER NOT NULL,
    FOREIGN KEY (id_planta) REFERENCES MinhasPlantas(id_planta)
);

-- Tabela para o catálogo de pragas e doenças
CREATE TABLE IF NOT EXISTS PragasDoencas (
    id_praga INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_comum TEXT NOT NULL UNIQUE,
    descricao TEXT,
    sintomas TEXT, 
    tratamento TEXT
);

-- Tabela para registrar quando uma planta foi afetada por uma praga
CREATE TABLE IF NOT EXISTS RegistroDePragas (
    id_registro_praga INTEGER PRIMARY KEY AUTOINCREMENT,
    data_identificacao DATE NOT NULL,
    status_tratamento TEXT,
    id_planta INTEGER NOT NULL,
    id_praga INTEGER NOT NULL,
    FOREIGN KEY (id_planta) REFERENCES MinhasPlantas(id_planta),
    FOREIGN KEY (id_praga) REFERENCES PragasDoencas(id_praga)
);

-- Tabela para as perguntas do assistente de diagnóstico 
CREATE TABLE IF NOT EXISTS DiagnosticoPerguntas (
    id_pergunta INTEGER PRIMARY KEY AUTOINCREMENT,
    texto_pergunta TEXT NOT NULL,
    ordem INTEGER NOT NULL UNIQUE
);

-- Tabela para as respostas possiveis de cada pergunta 
CREATE TABLE IF NOT EXISTS DiagnosticoRespostas (
    id_resposta INTEGER PRIMARY KEY AUTOINCREMENT,
    texto_resposta TEXT NOT NULL,
    id_pergunta INTEGER NOT NULL,
    FOREIGN KEY (id_pergunta) REFERENCES DiagnosticoPerguntas(id_pergunta)
);

-- Tabela que mapeia respostas a possiveis diagnosticos 
CREATE TABLE IF NOT EXISTS DiagnosticoMapeamento (
    id_resposta INTEGER NOT NULL,
    id_praga INTEGER NOT NULL,
    PRIMARY KEY (id_resposta, id_praga),
    FOREIGN KEY (id_resposta) REFERENCES DiagnosticoRespostas(id_resposta),
    FOREIGN KEY (id_praga) REFERENCES PragasDoencas(id_praga)
);