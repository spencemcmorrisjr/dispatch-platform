
-- Enable UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ======================
-- TENANTS
-- ======================
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    subscription_plan TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================
-- USERS
-- ======================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_tenant_id ON users(tenant_id);

-- ======================
-- DRIVERS
-- ======================
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    cdl_number TEXT,
    cdl_expiration DATE,
    medical_card_expiration DATE,
    availability_status TEXT DEFAULT 'available',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_drivers_tenant_id ON drivers(tenant_id);

-- ======================
-- TRUCKS
-- ======================
CREATE TABLE trucks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    vin TEXT,
    plate_number TEXT,
    registration_expiration DATE,
    insurance_expiration DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_trucks_tenant_id ON trucks(tenant_id);

-- ======================
-- LOADS
-- ======================
CREATE TABLE loads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    driver_id UUID REFERENCES drivers(id),
    truck_id UUID REFERENCES trucks(id),
    pickup_location TEXT,
    delivery_location TEXT,
    status TEXT DEFAULT 'created',
    revenue_amount NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_loads_tenant_id ON loads(tenant_id);

-- ======================
-- INVOICES
-- ======================
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    load_id UUID REFERENCES loads(id) ON DELETE SET NULL,
    issue_date DATE,
    due_date DATE,
    subtotal_amount NUMERIC(12,2),
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_invoices_tenant_id ON invoices(tenant_id);

-- ======================
-- COMPLIANCE RECORDS
-- ======================
CREATE TABLE compliance_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    type TEXT NOT NULL,
    expiration_date DATE,
    status TEXT DEFAULT 'valid',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_compliance_tenant_id ON compliance_records(tenant_id);
