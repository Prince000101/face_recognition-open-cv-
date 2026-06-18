CREATE TABLE IF NOT EXISTS middleware (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT middleware_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_middleware_created_at ON middleware(created_at DESC);
CREATE INDEX idx_middleware_status ON middleware(status) WHERE status = 'active';
