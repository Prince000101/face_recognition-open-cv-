CREATE TABLE IF NOT EXISTS helpers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT helpers_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_helpers_created_at ON helpers(created_at DESC);
CREATE INDEX idx_helpers_status ON helpers(status) WHERE status = 'active';
