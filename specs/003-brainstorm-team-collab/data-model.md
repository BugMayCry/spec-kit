# Data Model: Multi-Agent Collaborative Brainstorming

**Status**: Minimal - This feature is a workflow extension, not a data storage system

## Entity Definitions

The spec defines three conceptual entities that are used during the brainstorming session but do not require persistent storage:

### Proposal

**Purpose**: Structured output from each role containing their analysis

| Field | Type | Description |
|-------|------|-------------|
| role | string | Role identifier (pm, architect, tech, test, security) |
| content | markdown | Role's structured proposal in markdown format |
| key_points | list[string] | 3-5 main points from the proposal |
| risks | list[string] | Identified risks or concerns |
| questions | list[string] | Open questions for other roles |

**Note**: Proposal is generated in-memory during proposal phase, output as part of appendix.

### Decision

**Purpose**: Final choice made by Product Owner on contested points

| Field | Type | Description |
|-------|------|-------------|
| topic | string | The contested topic being decided |
| choice | string | Selected option (A, B, or custom) |
| rationale | string | (optional) Reason for the choice |

**Note**: Decisions are recorded in spec.md Decisions Log section and appendix.

### DebateRecord

**Purpose**: Chronological transcript of all messages exchanged

| Field | Type | Description |
|-------|------|-------------|
| timestamp | ISO datetime | When the message was sent |
| from | string | Sender role or "user" |
| to | string | Recipient role, "all", or "user" |
| type | string | Message type (proposal, debate, counter_argument, etc.) |
| payload | object | Message content |

**Note**: Kept in runtime memory, output as appendix at session end. Not persisted.

## Data Flow

```
User Idea → Proposal Collection → Debate → Decisions → spec.md + Appendix
                ↓
           team-config.json (runtime only, gitignored)
```

## Storage

| Data | Storage | Location |
|------|---------|----------|
| team-config.json | Runtime memory | `.specify/team-config.json` (gitignored) |
| Proposals | Memory → Appendix | Output as markdown |
| Decisions | Memory → spec.md | Written to Decisions Log |
| Debate transcript | Memory → Appendix | Output as markdown |

No persistent data storage beyond spec output.
