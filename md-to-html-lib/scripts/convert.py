#!/usr/bin/env python3
"""
Convert Markdown to styled HTML using the 'markdown' library.
Features:
  - Uses markdown lib for deterministic conversion (zero text loss)
  - Extracts ```mermaid blocks for Mermaid.js rendering
  - Clean code blocks (no Pygments span soup)
  - ASCII flowcharts are handled by the LLM before calling this script
"""

import re
import sys
import markdown
from pathlib import Path


def convert(md_path: str, html_path: str | None = None):
    md_file = Path(md_path)
    if not md_file.exists():
        print(f"[ERROR] File not found: {md_file}")
        sys.exit(1)

    html_file = Path(html_path) if html_path else md_file.with_suffix(".html")
    src = md_file.read_text(encoding="utf-8")

    # Step 1: Extract ```mermaid blocks, replace with placeholders
    mermaid_blocks = []

    def save_mermaid(m):
        idx = len(mermaid_blocks)
        code = m.group(1)
        mermaid_blocks.append(code)
        return f'<div class="mermaid-placeholder" data-idx="{idx}"></div>'

    src = re.sub(r'```mermaid\s*\n(.*?)```', save_mermaid, src, flags=re.DOTALL)

    # Step 2: Convert markdown → HTML (no codehilite, clean <pre><code>)
    body = markdown.markdown(src, extensions=[
        "markdown.extensions.extra",
        "markdown.extensions.toc",
        "markdown.extensions.smarty",
    ])

    # Step 3: Restore mermaid blocks
    def restore_mermaid(m):
        idx = int(m.group(1))
        code = mermaid_blocks[idx]
        return f'<div class="mermaid">\n{code}\n</div>'

    body = re.sub(
        r'<div class="mermaid-placeholder" data-idx="(\d+)"></div>',
        restore_mermaid,
        body,
    )

    # Step 4: Build full HTML
    title = md_file.stem
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        .container {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 2em; margin-bottom: 30px; color: #1a1a1a; border-bottom: 2px solid #07c160; padding-bottom: 10px; }}
        h2 {{ font-size: 1.5em; margin-top: 40px; margin-bottom: 20px; color: #2c3e50; border-left: 4px solid #07c160; padding-left: 12px; }}
        h3 {{ font-size: 1.2em; margin-top: 30px; margin-bottom: 15px; color: #34495e; }}
        p  {{ margin-bottom: 15px; }}
        ul, ol {{ margin: 15px 0; padding-left: 30px; }}
        li {{ margin-bottom: 8px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #f0faf4; font-weight: 600; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9em; }}
        pre {{ background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 8px; overflow-x: auto; margin: 20px 0; line-height: 1.5; }}
        pre code {{ background: none; padding: 0; color: inherit; font-size: 0.9em; }}
        blockquote {{ background: #f0faf4; border-left: 4px solid #07c160; padding: 15px 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }}
        blockquote p {{ margin: 0; }}
        hr {{ border: none; border-top: 1px solid #eee; margin: 40px 0; }}
        .mermaid {{ background: #fafafa; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; }}
        .toc {{ background: #f8f9fa; padding: 20px 30px; border-radius: 8px; margin: 20px 0; }}
        .toc ul {{ list-style: none; padding-left: 0; }}
        .toc a {{ color: #07c160; text-decoration: none; }}
        .toc a:hover {{ text-decoration: underline; }}
        .note {{ background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 15px 0; border-radius: 0 8px 8px 0; }}
        .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; border-radius: 0 8px 8px 0; }}
        strong {{ color: #1a1a1a; }}
    </style>
</head>
<body>
    <div class="container">
{body}
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>
"""

    # ── Write ──
    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.write_text(html, encoding="utf-8")
    print(f"[OK] Output: {html_file}")

    # ── Validation (exclude fenced code blocks) ──
    src_no_fence = re.sub(r'```\w*\s*\n.*?```', '', src, flags=re.DOTALL)
    md_h = len(re.findall(r'^#{1,3} ', src_no_fence, re.MULTILINE))
    html_h = len(re.findall(r'<h[1-3][^>]*>', html))
    md_tr = len(re.findall(r'^\|', src, re.MULTILINE)) - len(re.findall(r'^\|:?-+:?\|', src, re.MULTILINE))
    html_tr = html.count('<tr>')
    mermaid_ok = 'class="mermaid"' in html

    ok, fail = "[PASS]", "[FAIL]"
    print()
    print("Validation:")
    print(f"  | headings:    src {md_h:>2} / html {html_h:>2}  {ok if md_h == html_h else fail}")
    print(f"  | table rows:  src {md_tr:>2} / html {html_tr:>2}  {ok if md_tr == html_tr else fail}")
    print(f"  | mermaid:     {ok if mermaid_ok else fail} ({len(mermaid_blocks)} blocks)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input.md> [output.html]")
        sys.exit(1)
    md_input = sys.argv[1]
    html_output = sys.argv[2] if len(sys.argv) > 2 else None
    convert(md_input, html_output)
