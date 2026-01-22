---
name: code-module
description: 'Generate a tree-structured module overview with functional summaries for codebases. Use when user says: "init-modules" OR requests to: (1) Understand the structure of a codebase, (2) Generate a hierarchical view of directories/modules with their purposes, (3) Create modules.md documentation with tree structure and concise function descriptions, (4) Summarize module functionality from leaf directories upward. Triggered by init-modules command.'
---

# Code Module Analysis

## Overview

Analyzes a codebase directory structure and generates a hierarchical modules.md document with tree view and concise functional summaries for each module.

## Workflow

### 阶段 1：生成骨架 (Skeleton Generation)

**目标**：先创建完整的目录结构和占位符，用户可以立即查看项目结构。

#### 1.1 构建目录树

使用 `find` 或 `bash` 命令发现当前目录的所有目录，排除常见的忽略模式：

```bash
# 获取所有目录作为树结构
find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*' | sort
```

构建 markdown 树结构，使用：
- `├── ` 表示有后续兄弟节点
- `└── ` 表示组中最后一个项目
- 根据深度层级正确缩进

#### 1.2 生成初始 modules.md

创建或覆盖 `modules.md`，包含：

```markdown
# Modules

## Directory Structure

<完整的树形结构，从根目录开始>

## Module Descriptions

<完整路径> - [待分析]
<完整路径> - [待分析]
...

<!-- Last Update: [时间戳] | Processing: Initializing -->
```

**格式规范：**
- **Directory Structure 部分**：
  - 树形结构显示
  - 使用 `├──` 和 `└──` 表示层级关系
  - 不在树中使用完整路径（仅目录名）

- **Module Descriptions 部分**：
  - 每个目录使用**完整路径**（从根目录开始）
  - 例如：`myproject/src/api/auth/ - [待分析]`
  - 按字母顺序排列
  - 描述在连字符后，用空格分隔

- **进度头**（在文件末尾）：
  - 格式：`<!-- Last Update: [时间] | Processing: [当前处理目录] -->`
  - 初始状态：`<!-- Last Update: [INIT] | Processing: Initializing -->`

### 阶段 2：增量填充 (Incremental Population)

**目标**：逐个分析目录并实时更新，提供进度反馈。

#### 2.1 识别叶子目录

从树中识别叶子目录（没有子目录的目录）：

```bash
# 查找不包含其他目录的目录
find . -type d -exec sh -c 'find "$1" -maxdepth 1 -type d | wc -l | grep -q "^1$"' _ {} \;
```

#### 2.2 分析叶子模块（批处理）

对于每个叶子目录：
1. 列出所有代码文件（扩展名：.py, .js, .ts, .tsx, .java, .go, .rs, .cpp, .c, .cs, 等）
2. 使用 `read` 工具读取文件内容
3. 分析功能：
   - 从文件名和代码结构识别主要目的
   - 查找类/函数定义、导入语句和关键逻辑
   - 提取核心功能
4. 生成功能描述（10~50 个中文字符）
   - 聚焦主要目的
   - 使用现在时动词（如 "handles", "manages", "processes"）
   - 具体但简短

**示例摘要：**
- "用户认证与权限管理模块"
- "通用工具函数与辅助类库"
- "RESTful API 接口与路由处理"
- "数据模型与实体定义层"

**批量更新策略：**
- 每处理 5 个叶子目录后，批量更新 modules.md
- 更新进度头中的时间戳和当前处理目录
- 继续直到所有叶子目录完成

#### 2.3 分层向上传播（按层级）

对于非叶子目录：
1. **按层级从深到浅处理**：
   - 从最深的层级开始（叶子目录的父目录）
   - 每处理完一层，再处理上一层

2. **等待所有子目录完成**：
   - 只有当某个目录的所有子目录都有描述后，才处理该目录
   - 确保向上传播基于完整的子目录信息

3. **合并子目录摘要**：
   - 如果所有子目录服务于相似目的 → 使用该目的
   - 如果子目录有不同目的 → 使用统称
   - 描述长度：10~50 个中文字符
   - 保持层级性（如 "Auth module" 用于 "login", "register" 等子目录）

**示例：**
```
auth/
  ├── login/      → "Login handlers"
  └── register/   → "Registration handlers"
                → "Auth module"
```

4. **批量更新**：
   - 每处理完 5 个父目录，批量更新 modules.md
   - 更新进度头
   - 继续直到根目录

#### 2.4 完成

1. 移除进度头（`<!-- Last Update... -->`）
2. 确认所有目录都有描述
3. 报告完成状态

## Constraints

- **Summary length**: 10~50 个中文字符（保留明确英文缩写）
- **Bottom-up analysis**: Always start with leaf directories, then propagate upward
- **Code-aware**: Base summaries on actual code content, not just directory names
- **Markdown tree**: Use proper tree symbols (├──, └──) with correct indentation
- **Batch update**: Update modules.md every 5 directories analyzed
- **Progress tracking**: Always update progress header during analysis
- **Full paths**: Use complete paths (e.g., `myproject/src/api/`) in Module Descriptions section
- **Propagate timing**: Only propagate summary upward after all children are complete

## When to Use

**This skill requires EXPLICIT user invocation.**

Use this skill ONLY when:
- User says "init-modules" command
- User explicitly requests to generate or create modules documentation
- User explicitly asks to analyze codebase structure and summarize modules
- User explicitly requests module overview or tree structure generation

**DO NOT auto-invoke** this skill for any other reason, even when analyzing codebases for other purposes.

## Process Notes

- Always read actual code files before summarizing
- Skip common directories: node_modules, .git, __pycache__, .venv, dist, build
- For large files, focus on: imports, class definitions, main functions, comments
- If directory has no code files, mark as "Configuration" or "Empty"
- Use complete paths (e.g., `myproject/src/api/`) in Module Descriptions section
- Update modules.md every 5 directories analyzed for progress tracking
- Remove progress header when analysis is complete
