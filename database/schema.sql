-- 1. Locais
CREATE TABLE IF NOT EXISTS Locais (
    id_local INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    tipo TEXT, -- 'interno', 'externo', etc.
    area_m2 REAL DEFAULT 0.0,
    foto_capa TEXT
);

-- 2. Espécies (Base de Conhecimento)
CREATE TABLE IF NOT EXISTS Especies (
    id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_popular TEXT NOT NULL UNIQUE,
    nome_cientifico TEXT,
    instrucoes_rega TEXT,
    necessidade_sol TEXT,
    necessidade_poda TEXT,
    uso_adubos TEXT,
    epoca_plantio TEXT,
    foto_exemplo TEXT
);

-- 3. Minhas Plantas
CREATE TABLE IF NOT EXISTS MinhasPlantas (
    id_planta INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_personalizado TEXT NOT NULL,
    data_plantio DATE,
    id_especie INTEGER NOT NULL,
    id_local INTEGER NOT NULL,
    status TEXT DEFAULT 'ativa',
    foto_principal TEXT,
    FOREIGN KEY (id_especie) REFERENCES Especies(id_especie),
    FOREIGN KEY (id_local) REFERENCES Locais(id_local)
);

-- 4. Diário
CREATE TABLE IF NOT EXISTS DiarioDePlanta (
    id_diario INTEGER PRIMARY KEY AUTOINCREMENT,
    data_registro DATE NOT NULL,
    titulo TEXT,
    observacao TEXT NOT NULL,
    caminho_foto TEXT,
    id_planta INTEGER NOT NULL,
    FOREIGN KEY (id_planta) REFERENCES MinhasPlantas(id_planta)
);

-- 5. Agenda
CREATE TABLE IF NOT EXISTS AgendaDeCuidados (
    id_agenda INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_tarefa TEXT NOT NULL,
    detalhes TEXT,
    data_agendada DATE NOT NULL,
    data_conclusao DATE,
    realizada INTEGER NOT NULL DEFAULT 0, -- 0: False, 1: True
    id_planta INTEGER NOT NULL,
    FOREIGN KEY (id_planta) REFERENCES MinhasPlantas(id_planta)
);

-- 6. Pragas (Base de Conhecimento)
CREATE TABLE IF NOT EXISTS PragasDoencas (
    id_praga INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_comum TEXT NOT NULL UNIQUE,
    descricao TEXT,
    sintomas TEXT,
    tratamento TEXT,
    foto_exemplo TEXT
);

-- 7. Registro de Ocorrências (Histórico)
CREATE TABLE IF NOT EXISTS RegistroDePragas (
    id_registro_praga INTEGER PRIMARY KEY AUTOINCREMENT,
    data_identificacao DATE NOT NULL,
    data_resolucao DATE,
    status_tratamento TEXT,
    id_planta INTEGER NOT NULL,
    id_praga INTEGER NOT NULL,
    FOREIGN KEY (id_planta) REFERENCES MinhasPlantas(id_planta),
    FOREIGN KEY (id_praga) REFERENCES PragasDoencas(id_praga)
);

-- 8, 9, 10. Tabelas de Lógica de Diagnóstico
CREATE TABLE IF NOT EXISTS DiagnosticoPerguntas (
    id_pergunta INTEGER PRIMARY KEY AUTOINCREMENT,
    texto_pergunta TEXT NOT NULL,
    ordem INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS DiagnosticoRespostas (
    id_resposta INTEGER PRIMARY KEY AUTOINCREMENT,
    texto_resposta TEXT NOT NULL,
    id_pergunta INTEGER NOT NULL,
    id_proxima_pergunta INTEGER,
    FOREIGN KEY (id_pergunta) REFERENCES DiagnosticoPerguntas(id_pergunta),
    FOREIGN KEY (id_proxima_pergunta) REFERENCES DiagnosticoPerguntas(id_pergunta)
);

CREATE TABLE IF NOT EXISTS DiagnosticoMapeamento (
    id_resposta INTEGER NOT NULL,
    id_praga INTEGER NOT NULL,
    PRIMARY KEY (id_resposta, id_praga),
    FOREIGN KEY (id_resposta) REFERENCES DiagnosticoRespostas(id_resposta),
    FOREIGN KEY (id_praga) REFERENCES PragasDoencas(id_praga)
);