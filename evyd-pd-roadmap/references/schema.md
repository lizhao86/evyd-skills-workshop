# Roadmap Schema Reference

Use this reference when you need the canonical field model for the EVYD PD roadmap workflow.

## 1. Working Bitable schema

Preferred working columns in Feishu Bitable:
- `Name`
- `Module`
- `Problem`
- `Function`
- `Description`
- `Value`
- `Resource`
- `startMonth`

### Field intent

#### `Name`
Owner / proposer / row author.
Used as export `author`.

#### `Module`
Product or domain grouping.
Examples:
- `Routines`
- `DTx`
- `HCP`
- `VC`
- `PHR`
- `基础设施层`
- `运营与数据层`

#### `Problem`
Short statement of the current product problem, gap, or difficulty.

#### `Function`
Single-feature label.
Short, atomic, and feature-oriented.

#### `Description`
Richer description of what the item actually does.
Can contain a short feature bundle if the roadmap row is intentionally grouped.

#### `Value`
Condensed value statement.
Should preserve benefit but avoid long repetitive structure.

#### `Resource`
Deep-collaboration team dependency only.
Do not use this field as a catch-all participant list.

#### `startMonth`
Execution start month from `1` to `12`.
Numeric field.

## 2. Enrichment rules

### Problem rule
Write the problem from the present-state gap.

Good:
- Users cannot log in with email
- AI lacks clear safety boundaries
- Campaign setup is too slow

Bad:
- Build email login
- Create AI memory
- Add campaign templates

### Function rule
Keep it as one short label.

Good:
- Multi-channel unified login
- AI long-term memory
- Campaign template launch

Bad:
- Support users to log in with email and OTP
- AI memory + proactive care + knowledge sync

### Value rule
Compress, but do not hollow it out.
Keep the main business/product benefit.

### Resource rule
Only include domain-side teams needing ongoing collaboration.

## 3. Resource mapping canon

### Allowed common values
- `Medical`
- `Ops`
- `BD`
- `MOH`
- `-`

### Multi-team formatting in Bitable
Use pipe-separated values:
- `Ops | BD`
- `Medical | Ops`
- `Ops | MOH | Medical`

### Mapping guidance

Use `Medical` for:
- clinical logic
- DTx
- consultation safety
- risk alerts
- local clinical knowledge
- disease-specific intervention logic

Use `Ops` for:
- enterprise workflows
- campaign operations
- support operations
- channel operations
- merchant operations
- content operation / knowledge maintenance

Use `BD` for:
- merchant partnership
- external partner onboarding
- commercial resource access

Use `MOH` for:
- public-health outputs
- policy-facing reporting
- government collaboration

Use `-` when:
- the item is foundational and does not need extra domain team dependency

## 4. startMonth planning canon

Plan months using dependency logic, not source order.

### Default annual shape
- Months 1-2: foundation
- Months 2-4: core AI and workflow loop
- Months 5-6: replication and scale
- Months 7-12: growth, incentives, brand, advanced engagement

### Priority ladder
1. foundation before dependencies
2. shared capability before single scenario
3. safety/governance before broad AI expansion
4. core workflow before gamification
5. growth and branding later unless explicitly prioritized

### Typical month buckets

#### Month 1
- auth foundation
- shared records/logging
- knowledge backend
- capability registry
- master data
- shared health profile data

#### Month 2
- AI safety
- general consultation assistant
- long-term memory
- local clinical knowledge
- patient summary foundations

#### Months 3-4
- DTx support loop
- risk alerts
- feedback systems
- HCP/VC/C-end/Dr-end assistants
- proactive care
- insights query
- AI patient summary

#### Months 5-6
- reusable frameworks
- cross-scenario replication
- specialist assistants
- QMS / VC optimization
- reporting automation

#### Months 7-12
- enterprise tools
- challenge operations
- merchant rewards
- incentives
- avatar / Oyen / brand layers

## 5. Empty row rule

Rows with no meaningful planning content are invalid working rows.

Skip rows when all core fields are empty:
- `Module`
- `Problem`
- `Function`
- `Description`
- `Value`
- `Name`

Do not enrich them.
Do not export them.
Do not assign `startMonth` to them.
