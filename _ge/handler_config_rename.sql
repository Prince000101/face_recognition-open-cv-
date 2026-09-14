CREATE TABLE IF NOT EXISTS modal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT modal_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_modal_created_at ON modal(created_at DESC);
CREATE INDEX idx_modal_status ON modal(status) WHERE status = 'active';
