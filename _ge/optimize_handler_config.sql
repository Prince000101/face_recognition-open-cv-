CREATE TABLE IF NOT EXISTS validator (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT validator_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_validator_created_at ON validator(created_at DESC);
CREATE INDEX idx_validator_status ON validator(status) WHERE status = 'active';
