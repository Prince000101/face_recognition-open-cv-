CREATE TABLE IF NOT EXISTS query (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT query_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_query_created_at ON query(created_at DESC);
CREATE INDEX idx_query_status ON query(status) WHERE status = 'active';
