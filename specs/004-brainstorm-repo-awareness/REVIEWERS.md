# Reviewers Guide: Brainstorm仓库认知增强

## Feature Summary

增强 brainstorm 命令，在提案准备前增加仓库认知阶段，确保架构师和技术专家对项目有足够了解。

## Key Changes

1. **新增参数**:
   - `--mode {full|quick}`: 完整模式/快速模式
   - `--skip-awareness`: 跳过认知阶段（需历史确认）

2. **新增文件**:
   - `.specify/awareness-state.json`: 用户认知状态持久化

3. **修改文件**:
   - `templates/commands/brainstorm.md`: 添加认知阶段
   - `templates/spec-template.md`: 支持Proposal状态

## Review Checklist

### 功能完整性
- [ ] 认知阶段正确展示仓库信息
- [ ] 跳过机制仅对已确认用户有效
- [ ] 提案文件正确标记为Proposal

### 代码质量
- [ ] 向后兼容（现有brainstorm用户不受影响）
- [ ] 错误处理完善
- [ ] 测试覆盖充分

### 用户体验
- [ ] 交互流程清晰
- [ ] 帮助文档准确
- [ ] 快速模式信息充足但不冗余

## 测试场景

| 场景 | 预期行为 |
|------|----------|
| 新用户执行brainstorm | 必须完成完整认知阶段 |
| 已确认用户执行brainstorm | 可选择跳过 |
| 选择快速模式 | 仅展示核心信息 |
| 仓库信息缺失 | 展示可用信息+警告 |

## 联系人

- **PM**: @zhoudaiyu
- **技术负责人**: @zhoudaiyu
