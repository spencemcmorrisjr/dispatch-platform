# Dispatch Platform — MVP Scope (90-Day Build)

## Objective
Launch a revenue-generating multi-tenant dispatch SaaS for 1–25 truck fleets.

---

## Core Modules (MVP)

### 1. Multi-Tenant Authentication
- Tenant creation
- User roles (Owner, Dispatcher, Driver)
- JWT auth
- Strict tenant_id enforcement

---

### 2. Loads
- Create load
- Assign driver
- Update status
- Revenue amount
- Margin calculation (deterministic)

---

### 3. Drivers
- Driver profile
- CDL & medical expiration tracking
- Availability status

---

### 4. Trucks
- Truck profile
- Registration & insurance tracking

---

### 5. Compliance
- Unified compliance_records table
- Expiration tracking
- Expiring/expired alerts

---

### 6. Invoicing
- Generate invoice from load
- Track payment status
- Overdue detection

---

### 7. Basic Automation
- Compliance expiring → alert
- Invoice overdue → alert
- Load delivered → create invoice

---

## Not Included in MVP
- AI models
- Advanced routing optimization
- Full general ledger
- Sharding/microservices
- Enterprise SLA features

---

## Definition of MVP Complete
- Fleet can manage loads inside system
- Compliance alerts prevent expiration
- Invoices generated and tracked
- Basic profit per load visible
