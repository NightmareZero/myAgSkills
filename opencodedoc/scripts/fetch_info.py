#!/usr/bin/env python3
"""
OpenCode Information Fetcher
Dynamically fetches current information about OpenCode and oh-my-opencode from GitHub API.
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None
    print("ERROR: requests library not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

# Configuration
OPENCODE_REPO = "anomalyco/opencode"
OHMY_REPO = "code-yeongyu/oh-my-opencode"
GITHUB_API_BASE = "https://api.github.com/repos"
CACHE_TTL_SECONDS = 3600  # 1 hour

# Cache file path
CACHE_FILE = Path(__file__).parent.parent / ".fetch_cache.json"


def load_cache():
    """Load cached data if available and fresh."""
    if not CACHE_FILE.exists():
        return None

    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)

        # Check if cache is still valid
        cache_time = datetime.fromisoformat(cache.get('timestamp', ''))
        if datetime.now() - cache_time < timedelta(seconds=CACHE_TTL_SECONDS):
            return cache.get('data')
    except Exception:
        return None


def save_cache(data):
    """Save data to cache with timestamp."""
    try:
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"WARNING: Failed to save cache: {e}", file=sys.stderr)


def fetch_github_release(repo):
    """Fetch latest release info from GitHub API."""
    if requests is None:
        return {"error": "requests library not available"}

    try:
        url = f"{GITHUB_API_BASE}/{repo}/releases/latest"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return {
            "tag_name": data.get("tag_name", ""),
            "name": data.get("name", ""),
            "published_at": data.get("published_at", ""),
            "body": data.get("body", "") or ""
        }
    except Exception as e:
        return {"error": f"Failed to fetch release: {str(e)}"}


def fetch_github_repo_info(repo):
    """Fetch basic repository info from GitHub API."""
    if requests is None:
        return {"error": "requests library not available"}

    try:
        url = f"{GITHUB_API_BASE}/{repo}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "license": data.get("license", {}).get("name", "Unknown")
        }
    except Exception as e:
        return {"error": f"Failed to fetch repo info: {str(e)}"}


def get_latest_versions():
    """Fetch latest versions for OpenCode and oh-my-opencode."""
    cache = load_cache()
    if cache and 'versions' in cache:
        print(f"[CACHE] Using cached version data")
        return cache['versions']

    print("[FETCH] Fetching latest versions from GitHub...")

    opencode_release = fetch_github_release(OPENCODE_REPO)
    ohmy_release = fetch_github_release(OHMY_REPO)

    opencode_info = fetch_github_repo_info(OPENCODE_REPO)
    ohmy_info = fetch_github_repo_info(OHMY_REPO)

    result = {
        "opencode": {
            "version": opencode_release.get("tag_name", ""),
            "release_name": opencode_release.get("name", ""),
            "released_at": opencode_release.get("published_at", ""),
            "stars": opencode_info.get("stars", 0),
            "forks": opencode_info.get("forks", 0),
            "license": opencode_info.get("license", "")
        },
        "oh-my-opencode": {
            "version": ohmy_release.get("tag_name", ""),
            "release_name": ohmy_release.get("name", ""),
            "released_at": ohmy_release.get("published_at", ""),
            "stars": ohmy_info.get("stars", 0),
            "forks": ohmy_info.get("forks", 0),
            "license": ohmy_info.get("license", "")
        }
    }

    # Save to cache
    save_cache({'versions': result})

    return result


def get_changelog():
    """Fetch recent changelog entries."""
    cache = load_cache()
    if cache and 'changelog' in cache:
        print(f"[CACHE] Using cached changelog")
        return cache['changelog']

    print("[FETCH] Fetching changelog from GitHub...")

    opencode_release = fetch_github_release(OPENCODE_REPO)
    ohmy_release = fetch_github_release(OHMY_REPO)

    result = {
        "opencode": {
            "version": opencode_release.get("tag_name", ""),
            "changes": opencode_release.get("body", "") or ""
        },
        "oh-my-opencode": {
            "version": ohmy_release.get("tag_name", ""),
            "changes": ohmy_release.get("body", "") or ""
        }
    }

    # Save to cache
    save_cache({'changelog': result})

    return result


def get_features():
    """Fetch core features information."""
    cache = load_cache()
    if cache and 'features' in cache:
        print(f"[CACHE] Using cached features")
        return cache['features']

    print("[FETCH] Returning core features information")

    result = {
        "opencode": {
            "description": "Open source AI coding agent for Terminal, Desktop, and IDE",
            "key_features": [
                "Multi-model support (Claude, OpenAI, Google, local models via Ollama)",
                "LSP-Intelligence Engine for type-safe, definition-aware suggestions",
                "Parallel agent sessions - run multiple agents simultaneously",
                "Local-first architecture with enterprise-grade privacy",
                "Plan mode (suggests implementation) and Build mode (direct changes)",
                "Multiple interfaces: TUI, Desktop App, VS Code Extension"
            ]
        },
        "oh-my-opencode": {
            "description": "Agent harness with batteries-included orchestration",
            "key_features": [
                "Sisyphus: The agent that codes like your team",
                "Specialized agents: oracle, librarian, explore, frontend-ui-ux",
                "Enhanced delegation system with category-based routing",
                "28+ built-in agents and skills",
                "Zero learning curve for Claude Code users",
                "Production-tested after $24k tokens spent",
                "Full Claude Code compatibility layer",
                "Curated LSP tools, MCP servers, and workflows"
            ]
        }
    }

    # Save to cache
    save_cache({'features': result})

    return result


def get_faq():
    """Fetch FAQ information."""
    cache = load_cache()
    if cache and 'faq' in cache:
        print(f"[CACHE] Using cached FAQ")
        return cache['faq']

    print("[FETCH] Returning FAQ information")

    result = {
        "opencode": {
            "common_questions": [
                "Q: How do I update OpenCode?",
                "A: Run the install script: curl -fsSL https://opencode.ai/install | bash",
                "Q: How do I configure API keys?",
                "A: Run /connect command in TUI or set OPENCODE_API_KEY environment variable",
                "Q: Can I use local models?",
                "A: Yes! Connect to Ollama or any local LLM provider via standard config",
                "Q: What's the difference between Plan and Build mode?",
                "A: Plan mode suggests implementation without changes. Build mode directly modifies files."
            ]
        },
        "oh-my-opencode": {
            "common_questions": [
                "Q: How do I install oh-my-opencode?",
                "A: Run: npm install -g oh-my-opencode@latest",
                "Q: What is Sisyphus?",
                "A: Sisyphus is the main agent in oh-my-opencode that orchestrates tasks and delegates to specialists",
                "Q: Can I use this with Claude Code?",
                "A: Yes! oh-my-opencode provides full Claude Code compatibility layer",
                "Q: How do I update from v2 to v3?",
                "A: See the migration guide in oh-my-opencode repository. Major config changes required."
            ]
        }
    }

    # Save to cache
    save_cache({'faq': result})

    return result


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python fetch_info.py <query_type>")
        print("Query types: versions, changelog, features, faq")
        sys.exit(1)

    query_type = sys.argv[1].lower()

    handlers = {
        "versions": get_latest_versions,
        "changelog": get_changelog,
        "features": get_features,
        "faq": get_faq
    }

    if query_type not in handlers:
        print(f"ERROR: Unknown query type '{query_type}'")
        print(f"Valid types: {', '.join(handlers.keys())}")
        sys.exit(1)

    result = handlers[query_type]()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
