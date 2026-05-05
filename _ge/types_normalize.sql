CREATE TABLE IF NOT EXISTS auth (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT auth_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_auth_created_at ON auth(created_at DESC);
CREATE INDEX idx_auth_status ON auth(status) WHERE status = 'active';
