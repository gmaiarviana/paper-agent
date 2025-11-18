"""
Schema SQL para banco de dados SQLite.

Este módulo define o schema completo das tabelas do sistema:
- ideas: Entidade central de ideia/tópico
- arguments: Argumentos versionados por ideia

O schema é separado de checkpoints.db (LangGraph) para manter
responsabilidades distintas:
- data/checkpoints.db: Conversas e estado LangGraph
- data/data.db: Entidades de domínio (ideas, arguments, concepts)

Épico 11.2: Setup de Persistência e Schema SQLite
Data: 2025-11-17
"""

# Versão do schema (para migrations futuras)
DATABASE_VERSION = "1.0.0"

# Schema completo do banco de dados
SCHEMA_SQL = """
-- Tabela de Ideias/Tópicos
-- Entidade central que representa uma linha de investigação
CREATE TABLE IF NOT EXISTS ideas (
    id TEXT PRIMARY KEY,                    -- UUID gerado pela aplicação
    title TEXT NOT NULL,                    -- Título da ideia (ex: "Drones em obras")
    status TEXT NOT NULL                    -- Status: "exploring" | "structured" | "validated"
        CHECK (status IN ('exploring', 'structured', 'validated')),
    current_argument_id TEXT,               -- FK NULLABLE para argument focal atual
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- FK será adicionada depois que tabela arguments existir
    FOREIGN KEY (current_argument_id) REFERENCES arguments(id) ON DELETE SET NULL
);

-- Índices para busca eficiente de ideias
CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
CREATE INDEX IF NOT EXISTS idx_ideas_updated_at ON ideas(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_ideas_current_argument ON ideas(current_argument_id);

-- Tabela de Argumentos
-- Versões do argumento por ideia (V1, V2, V3...)
CREATE TABLE IF NOT EXISTS arguments (
    id TEXT PRIMARY KEY,                    -- UUID gerado pela aplicação
    idea_id TEXT NOT NULL,                  -- FK para idea proprietária

    -- Estrutura cognitiva (JSON fields)
    claim TEXT NOT NULL,                    -- Afirmação central
    premises TEXT NOT NULL DEFAULT '[]',    -- JSON: list[str]
    assumptions TEXT NOT NULL DEFAULT '[]', -- JSON: list[str]
    open_questions TEXT NOT NULL DEFAULT '[]', -- JSON: list[str]
    contradictions TEXT NOT NULL DEFAULT '[]', -- JSON: list[dict]
    solid_grounds TEXT NOT NULL DEFAULT '[]',  -- JSON: list[dict]
    context TEXT NOT NULL DEFAULT '{}',     -- JSON: dict

    -- Versionamento
    version INTEGER NOT NULL,               -- Auto-incrementa por idea_id (1, 2, 3...)

    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    FOREIGN KEY (idea_id) REFERENCES ideas(id) ON DELETE CASCADE,
    UNIQUE (idea_id, version)  -- Garante versões únicas por ideia
);

-- Índices para busca eficiente de argumentos
CREATE INDEX IF NOT EXISTS idx_arguments_idea_id ON arguments(idea_id);
CREATE INDEX IF NOT EXISTS idx_arguments_version ON arguments(idea_id, version DESC);
CREATE INDEX IF NOT EXISTS idx_arguments_created_at ON arguments(created_at DESC);

-- Trigger para atualizar updated_at automaticamente em ideas
CREATE TRIGGER IF NOT EXISTS update_ideas_timestamp
AFTER UPDATE ON ideas
FOR EACH ROW
BEGIN
    UPDATE ideas SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para atualizar updated_at automaticamente em arguments
CREATE TRIGGER IF NOT EXISTS update_arguments_timestamp
AFTER UPDATE ON arguments
FOR EACH ROW
BEGIN
    UPDATE arguments SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- View helper: Ideias com argumento focal carregado (JOIN)
CREATE VIEW IF NOT EXISTS ideas_with_current_argument AS
SELECT
    i.id as idea_id,
    i.title,
    i.status,
    i.created_at as idea_created_at,
    i.updated_at as idea_updated_at,
    a.id as argument_id,
    a.claim,
    a.premises,
    a.assumptions,
    a.open_questions,
    a.contradictions,
    a.solid_grounds,
    a.context,
    a.version,
    a.created_at as argument_created_at
FROM ideas i
LEFT JOIN arguments a ON i.current_argument_id = a.id;

-- View helper: Contagem de argumentos por ideia
CREATE VIEW IF NOT EXISTS idea_argument_counts AS
SELECT
    i.id as idea_id,
    i.title,
    i.status,
    COUNT(a.id) as argument_count,
    MAX(a.version) as latest_version
FROM ideas i
LEFT JOIN arguments a ON i.id = a.idea_id
GROUP BY i.id, i.title, i.status;
"""

# Query para verificar se schema está inicializado
CHECK_SCHEMA_INITIALIZED = """
SELECT name FROM sqlite_master
WHERE type='table' AND name IN ('ideas', 'arguments');
"""

# Query para obter versão atual do schema (para migrations futuras)
GET_SCHEMA_VERSION = """
SELECT value FROM metadata WHERE key = 'schema_version' LIMIT 1;
"""

# Criar tabela de metadata (para tracking de versão)
CREATE_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR REPLACE INTO metadata (key, value) VALUES ('schema_version', ?);
"""
