---
name: opencodedoc
description: "Query OpenCode and oh-my-opencode information dynamically including versions, features, updates, and FAQ. Auto-activates on keywords: 'opencode' and 'OpenCode文档'. Use when Claude needs to retrieve current information about OpenCode projects, version details, recent updates, or answer questions about usage and features."
---

# OpenCode Information Retrieval

Dynamically query current information about OpenCode and oh-my-opencode projects, including versions, features, updates, and FAQ.

## Overview

This skill provides up-to-date information about OpenCode (the open source AI coding agent) and oh-my-opencode (the agent harness built on top of OpenCode). All information is fetched dynamically from GitHub APIs and official documentation to ensure accuracy.

## Supported Query Types

Query this skill for 4 types of information:

### 1. Version Information
- Latest version numbers for OpenCode and oh-my-opencode
- Release dates and version history
- GitHub stars, forks, and license information

**Example queries:**
- "What's the latest OpenCode version?"
- "opencode version"
- "oh-my-opencode latest release"

### 2. Core Features
- Key capabilities of OpenCode (multi-model support, LSP integration, etc.)
- Main features of oh-my-opencode (Sisyphus agent, orchestration, etc.)
- Installation methods and supported platforms
- Available usage modes (TUI, Desktop, IDE)

**Example queries:**
- "What features does OpenCode have?"
- "OpenCode文档" (activates skill)
- "Tell me about oh-my-opencode"

### 3. Latest Updates
- Recent changelog entries
- Bug fixes and improvements
- New feature additions
- Breaking changes

**Example queries:**
- "What's new in the latest OpenCode release?"
- "Show me the latest oh-my-opencode updates"
- "opencode changelog"

### 4. FAQ
- Common questions and answers
- Troubleshooting tips
- Known issues and workarounds
- Best practices

**Example queries:**
- "How do I update OpenCode?"
- "Common OpenCode issues"
- "opencode FAQ"

## Data Sources

Information is fetched from:

**OpenCode:**
- GitHub API: `https://api.github.com/repos/anomalyco/opencode`
- Official Docs: `https://opencode.ai/docs`

**oh-my-opencode:**
- GitHub API: `https://api.github.com/repos/code-yeongyu/oh-my-opencode`
- GitHub Issues: For FAQ and common problems

## Usage

To use this skill, simply ask questions about OpenCode or oh-my-opencode using natural language. The skill will automatically activate on keywords:

- **Trigger words**: "opencode", "OpenCode文档"

**Example interactions:**

```
User: opencode version
Claude: [Skill activated] Fetching latest version...
       OpenCode v1.1.35 (released Jan 25, 2026)

User: What's new in OpenCode?
Claude: [Skill activated] Latest updates:
       - Desktop: Fixed reactive feedback loop, added line selection
       - Core: Added GitLab Duo model support

User: OpenCode文档
Claude: [Skill activated] Key Features:
       - Multi-model support (Claude, OpenAI, Google, local models)
       - LSP-Intelligence Engine for type-safe suggestions
       - Parallel agent sessions
```

## Output Format

The skill returns structured information in natural language format:

```
=== OpenCode ===
Latest: v1.1.35
Released: January 25, 2026
Stars: 86,866
Forks: 7,885
License: MIT

Recent Changes:
- Desktop: Fixed reactive feedback loop in global project cache sync
- Desktop: Added line selection functionality

=== oh-my-opencode ===
Latest: v3.0.1
Released: January 25, 2026
Stars: 23,501
Forks: 1,682

Recent Changes:
- Fix: Add missing name property in loadBuiltinCommands
- Refactor: Sync delegate_task schema with OpenCode Task tool
```

## Notes

- All data is fetched dynamically, not hardcoded
- Results are cached for 1 hour to respect API rate limits
- Information reflects the most current data available from GitHub
