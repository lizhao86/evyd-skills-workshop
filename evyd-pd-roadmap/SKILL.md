---
name: evyd-pd-roadmap
description: Modular EVYD PD roadmap operations for Feishu Bitable. Use when the user wants to collect roadmap ideas from conversation and write them into a specified Feishu Bitable, check for duplicate or overlapping roadmap rows, or assign roadmap planning fields such as Problem / Function / Value / Resource / startMonth.
---

# EVYD PD Roadmap

Operate EVYD PD roadmap data as a modular workflow.

Default source of truth: Feishu Bitable.
Default delivery artifact: structured export.

## Workflow modules

This skill has two modules.
Pick the module that matches the user's request.

### A. Collect + Write

Use when the user describes product scenarios in conversation and wants them written into a Feishu Bitable.

Read:
- `references/collection-write.md`

### B. Duplicate Check

Use when the user wants to inspect overlap, duplicates, or near-duplicate roadmap rows.

Read:
- `references/dedup-check.md`

Script available:
- `scripts/detect_duplicates.py`

Use the script for a first-pass duplicate scan when records are already available as JSON.
Treat script output as candidate duplicate groups, not final truth.
The user still decides whether to keep both, update the original, or merge.

## Shared operating rules

Canonical schema and mapping reference:
- `references/schema.md`

Read it when you need:
- field meaning
- Resource mapping
- startMonth planning canon


### 1. Always anchor on the target Bitable first when writing

If the user wants write-back behavior and has not specified the target Bitable, ask for it first.
Do not guess which Bitable to modify.

### 2. Skip empty rows

When reading roadmap rows, ignore rows where all meaningful planning fields are empty.
Do not export them.
Do not assign `startMonth` to them.

### 3. Separate enrichment from export

If the user asked to enrich roadmap data, update the Bitable first.
If the user asked only for export, do not mutate source data unless explicitly asked.

### 4. Retry Feishu Bitable operations once

If a Feishu Bitable read/write operation fails once, retry once before concluding permissions are broken.
Sharing and permission propagation can lag.

### 5. Keep roadmap fields disciplined

#### Problem
Write the actual product problem or operational gap.
Do not restate the solution as the problem.

#### Function
Write a single-function label, not a paragraph.

#### Value
Compress the value while keeping meaning readable.

#### Resource
Only include deep-collaboration teams outside the normal execution chain.
Preferred values include:
- `Medical`
- `Ops`
- `BD`
- `MOH`
- `Ops | BD`
- `Medical | Ops`
- `Ops | MOH | Medical`
- `-`

### 6. Plan `startMonth` using dependency logic

When asked to assign `startMonth`, act as both product lead and technical lead.

Use this default sequencing logic unless the user asks for a different planning style:
- Months 1-2: foundation
- Months 2-4: core AI and workflow loop
- Months 5-6: replication and operational scale
- Months 7-12: growth, incentives, brand, advanced engagement

Use these priorities:
1. foundation before dependencies
2. reusable capabilities before scenario-specific features
3. safety/governance before broad AI expansion
4. core workflow value before gamification and brand layers

## Current proven workflow

This skill is already proven for the following real pattern:
1. Read roadmap rows from Feishu Bitable
2. Fill `Problem`, `Function`, `Value`, `Resource`
3. Check duplicates
4. Assign `startMonth`

## Output quality bar

- Keep titles concise
- Keep problems concrete
- Keep values compressed but readable
- Keep collaborator arrays clean during export
- Never silently delete duplicates
- Never silently overwrite originals without user confirmation
- Never export empty rows
