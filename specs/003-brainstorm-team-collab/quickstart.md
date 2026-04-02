# Quickstart: Multi-Agent Collaborative Brainstorming

## Prerequisites

1. **Claude Code with Team mode enabled**:
   ```bash
   export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   ```

2. **spec-kit installed or development mode**:
   ```bash
   cd /path/to/spec-kit
   pip install -e .  # or: python -m specify_cli
   ```

## Basic Usage

### Standard Brainstorm (4 roles)

```bash
specify brainstorm "Build a real-time notification system"
```

### With Security Expert

```bash
specify brainstorm "Build a payment processing system" --with-security
```

## Workflow

1. **Provide your idea** - One sentence describing what you want to build
2. **Wait for proposals** - Each role generates their perspective (~5 min)
3. **Participate in debate** - Review challenges and provide decisions
4. **Receive spec.md** - Complete specification with appendix

## What to Expect

### Phase 1: Independent Proposals

Each role will independently analyze your idea and generate a proposal covering:
- Product Manager → User needs and business value
- Architect → System design and non-functional requirements
- Technical Expert → Technology choices and feasibility
- Test Expert → Acceptance criteria and testability
- Security Expert → (if flagged) Security and compliance

### Phase 2: Debate

The Devil's Advocate joins and challenges assumptions. You'll see:
- Counter-arguments from roles
- Multiple options with pros/cons for contested points
- Your role as final decision maker

### Phase 3: Output

- `spec.md` - Ready for `/speckit.plan`
- `brainstorm-appendix.md` - Full debate transcript (if needed)

## Troubleshooting

### "Team mode not enabled"

If you see a warning about Team mode:
- Ensure `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set
- Or use lite mode (sequential single-agent brainstorming)

### Long wait times

Role proposals typically complete within 5 minutes. If longer:
- Check network connection
- Verify Claude Code is properly authenticated
- Try with fewer roles (no `--with-security`)

### Want to stop early

Type `abort` or `cancel` to end the session. Your decisions up to that point will be preserved.
