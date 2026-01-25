# OpenCode Info Skill Creation

## Context

### Original Request
创建一个skill用于查询关于opencode、oh-my-opencode的信息，包括用法、版本、更新等等。当用户明确询问opencode相关信息时激活。

### Interview Summary
**Key Discussions**:
- Skill file location: `D:\Documents\Projects\myAgSkills\opencodedoc\SKILL.md` (standard SKILL.md format)
- Skill name: opencodedoc
- Information categories to include: Version info, Core features, Latest updates, FAQ (Installation guide excluded)
- Update mechanism: Dynamic fetching via GitHub API and webfetch (not static data)
- Trigger keywords: "opencode", "OpenCode文档"
- Test strategy: Automated testing required

**Research Findings**:
- OpenCode latest: v1.1.35 (Jan 25, 2026), 86,866 stars, MIT license
- oh-my-opencode latest: v3.0.1 (Jan 25, 2026), 23,501 stars, stable release
- Relationship: oh-my-opencode is an agent harness built on top of OpenCode core
- Both projects have active development with recent releases
- OpenCode provides core AI coding agent platform
- oh-my-opencode adds enhanced agent orchestration (Sisyphus)

### Metis Review
**Note**: Metis consultation was unavailable due to technical error. Gaps addressed in self-review below.

---

## Work Objectives

### Core Objective
Create a SKILL.md file that dynamically queries OpenCode and oh-my-opencode information (versions, features, updates, FAQ) and auto-activates on specific keywords.

### Concrete Deliverables
- `D:\Documents\Projects\myAgSkills\opencodedoc\SKILL.md` - Skill definition file
- Automated test suite to verify skill functionality

### Definition of Done
- [ ] SKILL.md file exists with proper metadata and structure
- [ ] Dynamic information fetching implemented (GitHub API + webfetch)
- [ ] Supports queries for versions, features, updates, FAQ
- [ ] Triggers on "opencode" or "OpenCode文档" keywords
- [ ] All automated tests pass
- [ ] Manual verification: Skill can be loaded and queries return accurate info

### Must Have
- Standard SKILL.md format (matches OpenCode skill specifications)
- Dynamic data fetching (no hardcoded version numbers)
- Support for both OpenCode and oh-my-opencode
- 4 information categories: versions, features, updates, FAQ
- Trigger word activation
- Automated tests with passing results

### Must NOT Have (Guardrails)
- Hardcoded version numbers or data (must be dynamic)
- Installation guide category (user excluded this)
- Additional categories beyond the 4 specified
- Manual update procedures (must be automated)
- External dependencies beyond standard tools (curl, webfetch)

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: UNKNOWN (need to verify)
- **User wants tests**: YES (Automated testing)
- **Framework**: TBD (verify existing test infrastructure)

### Test Infrastructure Check
**Note**: Test infrastructure status unknown. Plan includes verification step in Task 1.

### Test Approach
Since automated testing is required, the plan includes:
1. Test infrastructure verification
2. If no framework exists: Set up minimal testing framework
3. Create test cases for each information category
4. Verify dynamic fetching works
5. Verify trigger keyword activation

---

## Task Flow

```
Task 1: Verify environment → Task 2: Create SKILL.md (standard format) → Task 3: Create fetch script
                                                           ↓
Task 4: Create tests → Task 5: Run tests → Task 6: Manual verification
```

## Parallelization

| Group | Tasks | Reason |
|-------|-------|--------|
| N/A | None | Sequential dependency chain |

---

## TODOs

- [ ] 1. Verify environment and test infrastructure

  **What to do**:
  - Check current directory structure exists: `D:\Documents\Projects\myAgSkills\opencodedoc\`
  - Search for existing test framework (package.json test scripts, *.test.*, *.spec.*)
  - Verify .sisyphus/ directory structure
  - Document test infrastructure findings

  **Must NOT do**:
  - Install test frameworks if not explicitly needed (Task 3 will handle)
  - Modify any files in this task (read-only verification)

  **Parallelizable**: NO (must complete first)

  **References**:

  **Pattern References**: None needed for this task

  **API/Type References**: None

  **Test References**: None yet (this task finds them)

  **Documentation References**:
  - Project structure conventions (based on directory exploration)
  - Testing best practices (if framework found)

  **External References**:
  - Testing frameworks comparison: bun test, vitest, jest, pytest (if needed later)

  **WHY Each Reference Matters**:
  - Understanding existing infrastructure prevents framework conflicts
  - Ensures compatibility with project conventions

  **Acceptance Criteria**:

  **Manual Execution Verification**:
  - [ ] Directory exists: `ls D:\Documents\Projects\myAgSkills\opencodedoc\` → shows .sisyphus/ subdirectory
  - [ ] Test framework check: `ls *.test.* *.spec.* 2>/dev/null` → report findings
  - [ ] Config check: `cat package.json 2>/dev/null | grep -i test` → report findings
  - [ ] Document findings in plan execution notes

  **Evidence Required**:
  - [ ] Terminal output showing directory structure
  - [ ] Terminal output showing test file search results
  - [ ] Terminal output showing package.json test scripts (if exists)

  **Commit**: NO

---

- [ ] 2. Create SKILL.md with standard format and metadata

  **What to do**:
  - Create `D:\Documents\Projects\myAgSkills\opencodedoc\SKILL.md` following standard format
  - **Frontmatter (YAML)**:
    ```yaml
    ---
    name: opencodedoc
    description: "Query OpenCode and oh-my-opencode information dynamically including versions, features, updates, and FAQ. Auto-activates on keywords: 'opencode' and 'OpenCode文档'. Use when Claude needs to retrieve current information about OpenCode projects, version details, recent updates, or answer questions about usage and features."
    ---
    ```
  - **Body (Markdown)**:
    - Overview of skill purpose
    - How to use the skill
    - Supported query types (4 categories)
    - Data sources and fetching logic
    - Output format examples
  - Keep SKILL.md concise (< 500 lines, < 5k words)
  - Use progressive disclosure: Keep essential info in body, detailed info in references if needed
  - No bundled resources needed (this is an informational skill)

  **Must NOT do**:
  - Hardcode version numbers or data in SKILL.md
  - Include installation guide category (excluded by user)
  - Create categories beyond 4 specified
  - Make SKILL.md verbose or include unnecessary documentation
  - Include auxiliary files (README, INSTALL, etc.)

  **Parallelizable**: NO (depends on Task 1 for environment understanding)

  **References**:

  **Pattern References**:
  - SKILL.md format from examples:
    - `C:\Users\night\OneDrive\Script\skills\mytime\SKILL.md`
    - `C:\Users\night\OneDrive\Script\skills\skill-creator\SKILL.md`
    - `C:\Users\night\OneDrive\Script\skills\code-module\SKILL.md`

  **API/Type References**:
  - Standard SKILL.md frontmatter: `name`, `description` (required only)
  - Body structure: Markdown instructions and guidance

  **Test References**: None yet (Task 4 will create)

  **Documentation References**:
  - SKILL format specification (from skill-creator examples)
  - Progressive disclosure principle (keep SKILL.md < 500 lines)

  **External References**:
  - SKILL examples in `C:\Users\night\OneDrive\Script\skills\` directory

  **WHY Each Reference Matters**:
  - Correct SKILL.md format ensures skill loads properly
  - Frontmatter `description` is the primary trigger mechanism
  - Conciseness prevents context window bloat

  **Acceptance Criteria**:

  **If TDD (tests enabled)**:
  - [ ] Test file created: `SKILL.test.md` or equivalent
  - [ ] Test validates: Frontmatter format (name, description), body structure
  - [ ] Test passes: Framework reports PASS

  **Manual Execution Verification**:
  - [ ] File created: `ls D:\Documents\Projects\myAgSkills\opencodedoc\SKILL.md` → file exists
  - [ ] Frontmatter validation: `head -n 5 SKILL.md` → contains YAML frontmatter with name and description
  - [ ] Description check: Frontmatter contains "opencode" and "OpenCode文档" triggers
  - [ ] Body validation: `cat SKILL.md` → contains overview, usage, supported query types
  - [ ] Length check: `wc -l SKILL.md` → < 500 lines
  - [ ] No auxiliary files: `ls D:\Documents\Projects\myAgSkills\opencodedoc\` → only SKILL.md exists

  **Evidence Required**:
  - [ ] Terminal output showing file creation
  - [ ] File content displayed showing frontmatter and body
  - [ ] Line count verification

  **Commit**: NO

---

- [ ] 3. Create fetch script for dynamic information retrieval

  **What to do**:
  - Create `scripts/fetch_info.py` for dynamic data fetching
  - Define data sources:
    - OpenCode: GitHub API `https://api.github.com/repos/anomalyco/opencode`
    - oh-my-opencode: GitHub API `https://api.github.com/repos/code-yeongyu/oh-my-opencode`
    - OpenCode docs: `https://opencode.ai/docs`
  - Implement fetch functions:
    - `get_latest_versions()`: Fetch from GitHub releases API
    - `get_changelog()`: Fetch release notes from GitHub
    - `get_features()`: Parse features from documentation (or hardcode for now)
    - `get_faq()`: Parse FAQ from docs or GitHub issues
  - Implement caching with 1-hour TTL to respect API rate limits
  - Output JSON format for easy parsing by skill
  - Error handling for network failures and API errors

  **Must NOT do**:
  - Hardcode version numbers in script
  - Cache for extended periods (keep data fresh)
  - Skip error handling

  **Parallelizable**: NO (depends on Task 2 SKILL.md structure)

  **References**:

  **Pattern References**: None yet (first implementation in this project)

  **API/Type References**:
  - GitHub REST API: `https://docs.github.com/en/rest`
  - Python `requests` or `urllib` for HTTP requests
  - JSON output format

  **Test References**: None yet

  **Documentation References**:
  - GitHub REST API documentation
  - Python HTTP libraries documentation

  **External References**:
  - GitHub API examples for Python

  **WHY Each Reference Matters**:
  - Standard HTTP libraries ensure cross-platform compatibility
  - JSON output is easy for Claude to parse and format

  **Acceptance Criteria**:

  **If TDD (tests enabled)**:
  - [ ] Test file created: `scripts/fetch_info.test.py` or equivalent
  - [ ] Test covers: All 4 fetch functions, error handling, caching
  - [ ] Mock API responses in tests
  - [ ] Test passes: All tests green

  **Manual Execution Verification**:
  - [ ] Script created: `ls scripts/fetch_info.py` → file exists
  - [ ] Version fetch test: `python scripts/fetch_info.py versions` → returns JSON with versions
  - [ ] Changelog test: `python scripts/fetch_info.py updates` → returns changelog
  - [ ] Error handling: Test with invalid network → graceful error message
  - [ ] Caching test: Run twice, second call uses cache
  - [ ] Output format: `python scripts/fetch_info.py` → returns valid JSON

  **Evidence Required**:
  - [ ] Terminal output showing script execution
  - [ ] Sample JSON output displayed
  - [ ] Caching behavior verified

  **Commit**: NO

---

- [ ] 4. Create automated test suite

  **What to do**:
  - Set up test framework if not present (based on Task 1 findings):
    - Preferred: bun test (if Bun is installed)
    - Alternative: vitest (if Node project)
    - Fallback: Simple shell script tests
  - Create test file: `SKILL.test.md` or equivalent
  - Test cases:
    1. Skill file exists and is readable
    2. Skill metadata is valid (name, description present)
    3. Trigger keywords match specification
    4. Version fetching returns correct format
    5. Changelog fetching returns data
    6. Error handling works for failed requests
    7. Cache mechanism reduces API calls
  - Make tests runnable with standard command

  **Must NOT do**:
  - Create tests for features not in scope (installation guide, etc.)
  - Skip error handling tests
  - Hardcode test data for dynamic features

  **Parallelizable**: NO (depends on Task 3 fetch implementation)

  **References**:

  **Pattern References**:
  - Existing test files in project (if found in Task 1)
  - Test structure from Task 1 findings

  **API/Type References**: None

  **Test References**: None (this task creates them)

  **Documentation References**:
  - bun test documentation (if used): https://bun.sh/docs/cli/test
  - vitest documentation (if used): https://vitest.dev/
  - Testing best practices for OpenCode skills

  **External References**:
  - Testing patterns for API clients
  - Mock data examples for testing

  **WHY Each Reference Matters**:
  - Consistent test structure matches project conventions
  - Proper test framework usage ensures reliability

  **Acceptance Criteria**:

  **Manual Execution Verification**:
  - [ ] Test file exists: `ls SKILL.test.*` → file exists
  - [ ] Test command exists: Document how to run tests
  - [ ] All tests pass: Run test command → 0 failures
  - [ ] Test coverage: All 4 categories covered by tests

  **Evidence Required**:
  - [ ] Terminal output showing test file listing
  - [ ] Terminal output showing test execution with results
  - [ ] Test command documented

  **Commit**: NO

---

- [ ] 5. Run automated tests and fix failures

  **What to do**:
  - Run all tests using framework command
  - Verify all tests pass
  - If tests fail:
    - Identify failure cause
    - Fix code (SKILL.md or fetch logic)
    - Re-run tests until all pass
  - Document test results

  **Must NOT do**:
  - Skip failing tests
  - Reduce test coverage to pass
  - Modify acceptance criteria to pass tests

  **Parallelizable**: NO (depends on Task 4 tests)

  **References**:

  **Pattern References**: None (standard test execution)

  **API/Type References**: None

  **Test References**: Tests created in Task 4

  **Documentation References**:
  - Test framework documentation (for interpreting results)
  - Debugging strategies for failing tests

  **External References**: None

  **WHY Each Reference Matters**:
  - Proper test execution ensures skill works as specified
  - All passing tests validate implementation correctness

  **Acceptance Criteria**:

  **Manual Execution Verification**:
  - [ ] Test command run: Document command used
  - [ ] All tests pass: Output shows "PASS" or 0 failures
  - [ ] Test count: Output shows all planned tests executed
  - [ ] If failures exist: Document fix and re-run until 0 failures

  **Evidence Required**:
  - [ ] Terminal output showing test command execution
  - [ ] Terminal output showing final test results (all pass)
  - [ ] Documentation of any test fixes applied

  **Commit**: NO

---

- [ ] 6. Manual verification and final validation

  **What to do**:
  - Verify SKILL.md follows standard format:
    - Frontmatter has `name` and `description` fields
    - Description includes triggers "opencode" and "OpenCode文档"
    - Body is concise and well-structured
  - Test skill discovery and activation:
    - Verify frontmatter loads properly
    - Description accurately describes skill purpose
  - Test fetch script functionality:
    - Run `python scripts/fetch_info.py versions`
    - Run `python scripts/fetch_info.py updates`
    - Verify all 4 query types work
  - Validate output format:
    - JSON output is parseable
    - All 4 categories return correct data
  - Verify no hardcoded data:
    - Check script fetches from live APIs
    - Version numbers are current (v1.1.35, v3.0.1)

  **Must NOT do**:
  - Accept SKILL.md that doesn't follow standard format
  - Skip testing all 4 information categories
  - Accept hardcoded version numbers

  **Parallelizable**: NO (depends on Task 5 tests passing)

  **References**:

  **Pattern References**:
  - Example SKILL.md files from `C:\Users\night\OneDrive\Script\skills\`

  **API/Type References**:
  - Standard SKILL.md frontmatter format
  - JSON output structure from fetch script

  **Test References**: Tests from Task 4 and Task 5

  **Documentation References**:
  - SKILL.md format specification (from examples)

  **External References**:
  - Current OpenCode and oh-my-opencode releases (to verify data accuracy)

  **WHY Each Reference Matters**:
  - Manual verification catches issues tests miss
  - Format compliance ensures skill loads in OpenCode

  **Acceptance Criteria**:

  **Manual Execution Verification**:
  - [ ] SKILL.md format check: `head -n 10 SKILL.md` → shows YAML frontmatter
  - [ ] Frontmatter validation: Contains `name: opencodedoc`
  - [ ] Description check: Contains "opencode" and "OpenCode文档" triggers
  - [ ] Body structure: Has overview, usage, query types sections
  - [ ] Conciseness: `wc -l SKILL.md` → < 500 lines
  - [ ] No auxiliary files: `ls .` → only SKILL.md and scripts/
  - [ ] Fetch script test: `python scripts/fetch_info.py versions` → returns JSON
  - [ ] Version verification: Output shows v1.1.35 and v3.0.1
  - [ ] All categories tested: versions, features, updates, FAQ all work
  - [ ] Dynamic data confirmed: Versions match current GitHub releases

  **Evidence Required**:
  - [ ] File listing showing SKILL.md and scripts/ directory
  - [ ] SKILL.md frontmatter displayed
  - [ ] Fetch script output for each query type
  - [ ] Comparison of fetched versions with current GitHub releases
  - [ ] Documentation of all verification steps

  **Commit**: NO

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 2 | `feat(skill): create opencodedoc SKILL.md with metadata` | SKILL.md | Manual review of file content |
| 3 | `feat(skill): implement dynamic info fetching for opencode and oh-my-opencode` | SKILL.md, fetch logic files | Run tests |
| 4 | `test(skill): add automated tests for opencodedoc skill` | SKILL.test.* | Run test command |
| 6 | `docs(skill): add verification documentation for opencodedoc skill` | VERIFICATION.md | Manual review |

---

## Success Criteria

### Verification Commands

```bash
# Verify skill directory structure
ls -la D:\Documents\Projects\myAgSkills\opencodedoc\
# Expected: SKILL.md, scripts/ (with fetch_info.py)

# Verify SKILL.md format
head -n 10 D:\Documents\Projects\myAgSkills\opencodedoc\SKILL.md
# Expected: YAML frontmatter with name and description

# Verify fetch script exists
ls -la D:\Documents\Projects\myAgSkills\opencodedoc\scripts\
# Expected: fetch_info.py

# Test fetch script (dynamic data)
python D:\Documents\Projects\myAgSkills\opencodedoc\scripts\fetch_info.py versions
# Expected: JSON with latest versions (v1.1.35, v3.0.1)

# Verify data is fresh (not hardcoded)
grep -r "v1.1.35\|v3.0.1" D:\Documents\Projects\myAgSkills\opencodedoc\ --include="*.py"
# Expected: No hardcoded versions (only fetched from API)

# Run automated tests
# Framework dependent, e.g.:
python -m pytest D:\Documents\Projects\myAgSkills\opencodedoc\tests\
# or
bun test D:\Documents\Projects\myAgSkills\opencodedoc\tests\
```

### Final Checklist
- [ ] SKILL.md exists with standard format (YAML frontmatter + markdown body)
- [ ] Frontmatter contains `name: opencodedoc`
- [ ] Frontmatter description includes triggers: "opencode", "OpenCode文档"
- [ ] Body includes: overview, usage, supported query types
- [ ] SKILL.md is concise (< 500 lines, < 5k words)
- [ ] scripts/fetch_info.py exists and is executable
- [ ] Fetch script returns JSON format
- [ ] All 4 query types supported: versions, features, updates, FAQ
- [ ] Installation guide NOT included (excluded per user request)
- [ ] No hardcoded version data in any files
- [ ] Fetch script implements error handling
- [ ] Caching implemented with 1-hour TTL
- [ ] All automated tests pass (0 failures)
- [ ] Manual verification confirms dynamic fetching works
- [ ] SKILL.md follows progressive disclosure (essential info only)
- [ ] No auxiliary files (README, INSTALL, etc.)
