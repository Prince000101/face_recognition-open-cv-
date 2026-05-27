CREATE TABLE IF NOT EXISTS worker (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT worker_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_worker_created_at ON worker(created_at DESC);
CREATE INDEX idx_worker_status ON worker(status) WHERE status = 'active';
