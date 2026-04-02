# Quickstart: Split Brainstorm Output

**Feature**: 005-proposal-separation

## Quickstart Notes

本改进为**工作流/流程变更**，无需安装步骤。

### 使用方式

1. **Brainstorm 阶段**
   ```
   /speckit.brainstorm <idea>
   ```
   生成:
   - `spec.proposal.md` - 用户故事
   - `plan.proposal.md` - 技术方案
   - `brainstorm-appendix.md` - 完整辩论

2. **Specify 阶段**
   ```
   /speckit.specify
   ```
   读取 `spec.proposal.md`，生成最终 `spec.md`

3. **Plan 阶段**
   ```
   /speckit.plan
   ```
   结合 `plan.proposal.md` 做技术分析

### 无需配置

- 无需安装依赖
- 无需环境变量
- 无需权限配置
