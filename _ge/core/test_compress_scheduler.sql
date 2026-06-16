CREATE TABLE IF NOT EXISTS migration (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT migration_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_migration_created_at ON migration(created_at DESC);
CREATE INDEX idx_migration_status ON migration(status) WHERE status = 'active';
