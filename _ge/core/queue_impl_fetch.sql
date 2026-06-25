CREATE TABLE IF NOT EXISTS route (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT route_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_route_created_at ON route(created_at DESC);
CREATE INDEX idx_route_status ON route(status) WHERE status = 'active';
