-- Adicionar coluna foto_url na tabela vacas
ALTER TABLE vacas ADD COLUMN IF NOT EXISTS foto_url TEXT;

-- Adicionar índice para melhor performance (opcional)
CREATE INDEX IF NOT EXISTS idx_vacas_foto_url ON vacas(foto_url);
