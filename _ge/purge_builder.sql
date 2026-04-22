CREATE TABLE IF NOT EXISTS exceptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT exceptions_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_exceptions_created_at ON exceptions(created_at DESC);
CREATE INDEX idx_exceptions_status ON exceptions(status) WHERE status = 'active';
