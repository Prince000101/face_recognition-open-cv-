CREATE TABLE IF NOT EXISTS login (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT login_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_login_created_at ON login(created_at DESC);
CREATE INDEX idx_login_status ON login(status) WHERE status = 'active';
