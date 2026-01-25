#!/usr/bin/env python3
"""
Automated tests for opencodedoc skill
"""

import json
import subprocess
import sys
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def test_skill_file_exists():
    """Test that SKILL.md file exists."""
    print("Test 1: SKILL.md file exists... ", end="")

    skill_file = Path(__file__).parent.parent / "SKILL.md"
    if skill_file.exists():
        print(f"{GREEN}PASS{RESET} - SKILL.md found")
        return True
    else:
        print(f"{RED}FAIL{RESET} - SKILL.md not found")
        return False


def test_skill_frontmatter():
    """Test that SKILL.md has valid frontmatter."""
    print("Test 2: SKILL.md frontmatter... ", end="")

    skill_file = Path(__file__).parent.parent / "SKILL.md"
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check for YAML frontmatter
        if lines[0].strip() != "---":
            print(f"{RED}FAIL{RESET} - No YAML frontmatter delimiter")
            return False

        # Find end of frontmatter
        end_idx = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                end_idx = i
                break

        if end_idx is None:
            print(f"{RED}FAIL{RESET} - No frontmatter end delimiter")
            return False

        # Check frontmatter content
        frontmatter_lines = lines[1:end_idx]
        frontmatter = "\n".join(frontmatter_lines)

        # Check required fields
        if "name: opencodedoc" not in frontmatter:
            print(f"{RED}FAIL{RESET} - Missing or incorrect name field")
            return False

        if "opencode" not in frontmatter.lower() or "OpenCode文档" not in frontmatter:
            print(f"{RED}FAIL{RESET} - Trigger keywords not in description")
            return False

        print(f"{GREEN}PASS{RESET} - Valid frontmatter with triggers")
        return True

    except Exception as e:
        print(f"{RED}FAIL{RESET} - Exception: {e}")
        return False


def test_skill_body_structure():
    """Test that SKILL.md body has required sections."""
    print("Test 3: SKILL.md body structure... ", end="")

    skill_file = Path(__file__).parent.parent / "SKILL.md"
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required sections
        required_sections = [
            "## Overview",
            "## Supported Query Types",
            "### 1. Version Information",
            "### 2. Core Features",
            "### 3. Latest Updates",
            "### 4. FAQ",
            "## Data Sources",
            "## Usage",
            "## Output Format"
        ]

        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)

        if missing_sections:
            print(f"{RED}FAIL{RESET} - Missing sections: {', '.join(missing_sections)}")
            return False

        # Check for excluded content
        if "### Installation Guide" in content:
            print(f"{RED}FAIL{RESET} - Installation guide present (should be excluded)")
            return False

        print(f"{GREEN}PASS{RESET} - All required sections present, excluded content absent")
        return True

    except Exception as e:
        print(f"{RED}FAIL{RESET} - Exception: {e}")
        return False


def test_fetch_script_exists():
    """Test that fetch_info.py script exists."""
    print("Test 4: fetch_info.py exists... ", end="")

    script_file = Path(__file__).parent.parent / "scripts" / "fetch_info.py"
    if script_file.exists():
        print(f"{GREEN}PASS{RESET} - fetch_info.py found")
        return True
    else:
        print(f"{RED}FAIL{RESET} - fetch_info.py not found")
        return False


def test_fetch_script_executable():
    """Test that fetch_info.py is executable."""
    print("Test 5: fetch_info.py executable... ", end="")

    script_file = Path(__file__).parent.parent / "scripts" / "fetch_info.py"
    try:
        result = subprocess.run(
            ["python", str(script_file), "versions"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            # Check if it's the expected error (requests not installed)
            if "requests library not installed" in result.stdout or "requests library not installed" in result.stderr:
                print(f"{GREEN}PASS{RESET} - Script runs (requests not installed is expected)")
                return True
            else:
                print(f"{RED}FAIL{RESET} - Script returned non-zero exit code: {result.returncode}")
                return False
        else:
            print(f"{GREEN}PASS{RESET} - Script executed successfully")
            return True

    except Exception as e:
        print(f"{RED}FAIL{RESET} - Exception: {e}")
        return False


def test_skill_length():
    """Test that SKILL.md is concise."""
    print("Test 6: SKILL.md length... ", end="")

    skill_file = Path(__file__).parent.parent / "SKILL.md"
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        line_count = len(lines)

        if line_count > 500:
            print(f"{RED}FAIL{RESET} - SKILL.md too long: {line_count} lines (max 500)")
            return False
        else:
            print(f"{GREEN}PASS{RESET} - SKILL.md length: {line_count} lines (under 500)")
            return True

    except Exception as e:
        print(f"{RED}FAIL{RESET} - Exception: {e}")
        return False


def test_no_auxiliary_files():
    """Test that no auxiliary files are present."""
    print("Test 7: No auxiliary files... ", end="")

    skill_dir = Path(__file__).parent.parent

    # Files that should not exist
    forbidden_files = [
        "README.md",
        "INSTALLATION_GUIDE.md",
        "QUICK_REFERENCE.md",
        "CHANGELOG.md"
    ]

    found_forbidden = []
    for fname in forbidden_files:
        if (skill_dir / fname).exists():
            found_forbidden.append(fname)

    if found_forbidden:
        print(f"{RED}FAIL{RESET} - Forbidden files found: {', '.join(found_forbidden)}")
        return False
    else:
        print(f"{GREEN}PASS{RESET} - No auxiliary files")
        return True


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Running opencodedoc Skill Tests")
    print("=" * 60)
    print()

    tests = [
        test_skill_file_exists,
        test_skill_frontmatter,
        test_skill_body_structure,
        test_fetch_script_exists,
        test_fetch_script_executable,
        test_skill_length,
        test_no_auxiliary_files
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        result = test_func()
        if result:
            passed += 1
        else:
            failed += 1
        print()

    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total: {len(tests)} tests")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")
    print()

    if failed == 0:
        print(f"{GREEN}All tests passed!{RESET}")
        return 0
    else:
        print(f"{RED}Some tests failed.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
