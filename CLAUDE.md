# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**spec-kit** is a toolkit for Spec-Driven Development (SDD) - a methodology where specifications drive implementation generation. The `specify` CLI bootstraps new projects with templates, slash commands, and workflows for AI-assisted spec-driven development.

## Commands

### Install & Run
```bash
# Install locally for development
uv pip install -e .

# Run CLI directly
python -m specify_cli

# Or after installation
specify --help
```

### Development
```bash
# Lint markdown files (CI checks)
markdownlint-cli2 '**/*.md'

# Full lint (GitHub Actions runs this)
```

### Testing
```bash
# Run a single test file
python -m pytest tests/test_file.py -v
```

## Architecture

### Source Structure
- `src/specify_cli/__init__.py` - Main CLI entry point (~1200 lines). Contains:
  - `AGENT_CONFIG` - Dict mapping CLI tool names to agent metadata (folder, install_url, requires_cli)
  - `StepTracker` - Rich-based progress tracker with live refresh
  - `init()` command - Downloads templates from GitHub releases, extracts, initializes git
  - `check()` command - Detects installed tools (git, claude, gemini, etc.)
  - Helper functions for git operations, SSL/HTTP, JSON merging, script permissions

### Templates (`templates/`)
Templates are packaged into zip files per AI agent (e.g., `spec-kit-template-claude-sh.zip`) and downloaded from GitHub releases during `specify init`. Key templates:
- `commands/*.md` - Slash command implementations (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, etc.)
- `spec-template.md`, `plan-template.md`, `tasks-template.md` - SDD workflow document templates

### Release Packaging
- GitHub release assets are created by `.github/workflows/scripts/create-release-packages.sh`
- Each agent has its own zip with agent-specific command files
- Release workflow: `.github/workflows/release.yml`

## Agent Integration

The CLI supports 14+ AI agents (Claude, Gemini, Copilot, Cursor, Qwen, Codex, Windsurf, etc.). Each agent type:
- Has a folder convention (`.claude/`, `.cursor/`, `.windsurf/`, etc.)
- Uses either Markdown or TOML command format
- May require CLI tool check (`cursor-agent`, `claude`) or be IDE-based only (`copilot`)

Adding a new agent requires updates to:
1. `AGENT_CONFIG` in `__init__.py`
2. `create-release-packages.sh` script
3. `create-github-release.sh` script
4. Both bash and PowerShell agent context scripts

See `AGENTS.md` for the full integration guide.

## Key Patterns

- **SSL/TLS**: Uses `truststore` for cross-platform SSL context with `httpx`
- **GitHub API**: Token from `GH_TOKEN`/`GITHUB_TOKEN` env vars or `--github-token` flag
- **Cross-platform**: Handles Windows (PowerShell) vs POSIX (bash/zsh) script variants
- **Progress UI**: `StepTracker` with Rich `Live` for animated terminal progress
