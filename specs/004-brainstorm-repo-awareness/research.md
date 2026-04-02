# Research: Brainstorm仓库认知增强

## Decision 1: 仓库信息提取方案

**Decision**: 使用文件系统扫描提取关键信息

**Rationale**:
- 读取 README.md 获取项目概述
- 扫描根目录获取技术栈配置文件（package.json, pyproject.toml, go.mod等）
- 解析 .specify/ 目录获取 SDD 相关配置
- 扫描 docs/ 或 docs/*.md 获取架构文档

**Alternatives considered**:
- 使用 git log 分析（过于间接）
- 使用 AI 分析（延迟太高）

---

## Decision 2: 提案文件命名格式

**Decision**: `proposal-{number}-{short-name}-spec.md`

**Rationale**:
- 符合现有 spec-xxx-xxx 格式约定
- "proposal" 前缀明确标识文档性质
- 便于排序和检索

**Alternatives considered**:
- `spec-proposal-xxx`（不符合现有约定）
- `draft-xxx-spec.md`（"draft"不如"proposal"准确）

---

## Decision 3: 用户状态持久化

**Decision**: 使用本地配置文件存储认知状态

**Rationale**:
- 项目级配置存储在 .specify/awareness-state.json
- 包含：用户ID、最后确认时间、使用的模式、跳过次数

**Alternatives considered**:
- 环境变量（不适合持久化）
- 全球配置（不适合多项目场景）
