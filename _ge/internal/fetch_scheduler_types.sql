CREATE TABLE IF NOT EXISTS config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT config_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_config_created_at ON config(created_at DESC);
CREATE INDEX idx_config_status ON config(status) WHERE status = 'active';
