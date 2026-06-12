---
name: MD to HTML (lib-based, with mermaid)
description: 使用 Python markdown 库将 Markdown 文件转换为美观 HTML。LLM 先处理 ASCII 流程图（转成 Mermaid 语法），再调用脚本做确定性转换。触发场景：用户要求将 md/markdown 转成 html、生成带流程图的网页、转换文档格式为可浏览的 HTML。
---

# MD to HTML (lib-based)

使用 `markdown` Python 库将 `.md` 文件转换为独立的、可在浏览器中打开的 HTML 文件。保留所有文本内容（零丢失），支持 Mermaid 流程图渲染，代码块干净无多余标签。

## 工作流程

### Step 1: LLM 处理 ASCII 流程图

读取源文件，检查代码块中的 ASCII 艺术流程图（包含 `│ ├ └ ─ →` 等字符）。将 ASCII 流程图手动重写为 ` ```mermaid ` 块。如果源文件中已有 ` ```mermaid ` 块则跳过。

### Step 2: 安装依赖（首次）

```bash
uv pip install --system markdown
```

### Step 3: 运行脚本

```bash
python scripts/convert.py <输入文件.md> [输出文件.html]
```

- 不指定输出路径 → 源文件同目录（同名 `.html`）
- 输出目录自动创建

### 脚本做了什么

1. **提取 ` ```mermaid ` 块** → 替换为占位符
2. **转换 markdown → HTML** → 使用 `markdown` 库（`extra` + `toc` + `smarty` 扩展），**不用 codehilite/Pygments**（避免 span 污染代码块）
3. **恢复 Mermaid div** → 将 mermaid 代码插入 `<div class="mermaid">`
4. **生成完整 HTML** → 带微信绿主题 CSS
5. **验证** → 统计标题数、表格行数、mermaid 块数

### 验证报告示例

```
[OK] Output: path/to/output.html

Validation:
  | headings:    src 28 / html 28  [PASS]
  | table rows:  src 12 / html 12  [PASS]
  | mermaid:     [PASS] (2 blocks)
```

## 与旧版 md-to-html-mermaid 的区别

| 对比项 | 旧版（LLM 手动拼接） | 新版（库 + 脚本） |
|--------|-------------------|-----------------|
| 转换方式 | Claude 逐段写 HTML 标签 | `markdown` 库确定性解析 |
| 文本完整性 | **有丢失风险** | **100% 保留** |
| 代码块 | 纯色深底 | 纯色深底，无 span 污染 |
| Mermaid 流程图 | LLM 手动转 | LLM 手动转 + 脚本渲染 |
| 稳定性 | 每次可能不同 | 相同输入 → 相同输出 |
| 验证 | grep 数标题/表格 | 同 |

## CSS 样式特点

- 微信绿主题色（`#07c160`）
- 代码块深底浅字（`#1e1e1e` / `#d4d4d4`）
- 表格斑马纹、圆角容器
- 响应式（`viewport` meta 标签）
- Mermaid 流程图居中渲染
- 提示框：`.note`（绿色）、`.warning`（黄色）
