# Tasks: Brainstorm仓库认知增强

## Task List

### Phase 1: 模板修改

- [ ] **T-001**: 修改 `templates/commands/brainstorm.md`
  - 添加 `--mode {full|quick}` 参数处理
  - 添加 `--skip-awareness` 参数处理
  - 添加仓库认知交互阶段
  - 添加状态持久化逻辑

### Phase 2: 状态管理

- [ ] **T-002**: 创建 `.specify/awareness-state.json` 状态文件
  - 实现用户确认状态读写
  - 实现跳过计数

### Phase 3: 提案标识

- [ ] **T-003**: 修改 spec 生成逻辑
  - 文件名添加 `proposal-` 前缀
  - Status 字段设为 "Proposal"

### Phase 4: 测试

- [ ] **T-004**: 添加单元测试
  - 测试认知阶段流程
  - 测试跳过逻辑
  - 测试状态持久化

### Phase 5: 文档

- [ ] **T-005**: 更新 README
  - 说明新增参数
  - 添加使用示例
