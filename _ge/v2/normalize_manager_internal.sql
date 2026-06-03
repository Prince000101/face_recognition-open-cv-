CREATE TABLE IF NOT EXISTS queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT queue_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_queue_created_at ON queue(created_at DESC);
CREATE INDEX idx_queue_status ON queue(status) WHERE status = 'active';
