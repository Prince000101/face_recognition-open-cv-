CREATE TABLE IF NOT EXISTS form (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT form_status_check CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX idx_form_created_at ON form(created_at DESC);
CREATE INDEX idx_form_status ON form(status) WHERE status = 'active';
