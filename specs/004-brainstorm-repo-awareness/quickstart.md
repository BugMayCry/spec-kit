# Quickstart: Brainstorm仓库认知增强

## 修改概述

1. **Brainstorm命令增强**
   - 新增 `--mode {full|quick}` 参数
   - 新增 `--skip-awareness` 参数
   - 新增仓库认知交互阶段

2. **提案标识**
   - 文件名格式：`proposal-{number}-{short-name}-spec.md`
   - Status字段：`Proposal`

## 交互流程

```
用户执行 /speckit.brainstorm <idea>

    v
[仓库认知阶段]
    |
    +-- 完整模式 --> 展示所有信息 --> 用户确认 --> 继续
    |
    +-- 快速模式 --> 展示核心信息 --> 用户确认 --> 继续
    |
    +-- 跳过（已确认用户）--> 直接继续

    v
[提案生成阶段]
    |
    v
[生成 proposal-xxx-xxx-spec.md]
```

## 验证方式

```bash
# 查看提案文件标识
grep "Status.*Proposal" specs/*/proposal-*-spec.md

# 验证跳过功能
/specit.brainstorm --skip-awareness "新功能"
```
