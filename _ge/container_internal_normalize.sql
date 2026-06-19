CREATE TABLE IF NOT EXISTS cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT cache_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_cache_created_at ON cache(created_at DESC);
CREATE INDEX idx_cache_status ON cache(status) WHERE status = 'active';
