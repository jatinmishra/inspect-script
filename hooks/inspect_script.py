#!/usr/bin/env python3
"""
inspect-script — PreToolUse hook for Claude Code
Shows script type, WHAT, WHY, and full content inside the Bash permission prompt.
Companion to the inspect-script skill (SKILL.md).

Registration in .claude/settings.json:
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/inspect_script.py" }]
      }
    ]
  }
"""

import json
import re
import sys
from pathlib import Path

INTERPRETERS = {
    "python3": "Python",
    "python": "Python",
    "bash": "Bash",
    "sh": "Shell",
    "zsh": "Shell",
    "node": "Node.js",
    "ruby": "Ruby",
    "perl": "Perl",
}

EXTENSIONS = {
    "python3": ["py"],
    "python": ["py"],
    "bash": ["sh", "bash"],
    "sh": ["sh"],
    "zsh": ["sh", "zsh"],
    "node": ["js", "mjs"],
    "ruby": ["rb"],
    "perl": ["pl"],
}


def detect(command):
    for key, name in INTERPRETERS.items():
        if re.search(rf'(?:^|\s|/)(?:{re.escape(key)})(?:\s|$)', command):
            return key, name
    return None, None


def extract_heredoc(command, interp):
    m = re.search(
        rf'(?:{re.escape(interp)})\s+<<\s*[\'"]?(\w+)[\'"]?\s*\n(.*?)\n\1',
        command,
        re.DOTALL,
    )
    return m.group(2) if m else None


def extract_inline(command, interp):
    m = re.search(
        rf'(?:{re.escape(interp)})\s+-[ce]\s+(?:\'(.*?)\'|"(.*?)")',
        command,
        re.DOTALL,
    )
    if m:
        return m.group(1) or m.group(2)
    return None


def extract_from_file(command, interp):
    for ext in EXTENSIONS.get(interp, []):
        m = re.search(rf'([\w/.\-]+\.{ext})\b', command)
        if m:
            p = Path(m.group(1))
            if p.exists():
                return p.read_text()
    return None


def get_what_why(content):
    what, why = "", ""
    if not content:
        return what, why
    for line in content.splitlines():
        clean = re.sub(r'^[#/\s]+', '', line).strip()
        if clean.upper().startswith("WHAT:"):
            what = clean[5:].strip()
        elif clean.upper().startswith("WHY:"):
            why = clean[4:].strip()
        if what and why:
            break
    return what, why


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    interp, lang = detect(command)

    if not interp:
        sys.exit(0)

    content = (
        extract_heredoc(command, interp)
        or extract_inline(command, interp)
        or extract_from_file(command, interp)
    )

    what, why = get_what_why(content)

    bar = "─" * 63
    out = [f"\n{bar}"]
    out.append(f"  Type    : {lang}")
    if what:
        out.append(f"  What    : {what}")
    if why:
        out.append(f"  Why     : {why}")
    if content:
        out.append("\n  Content :")
        for line in content.splitlines():
            out.append(f"    {line}")
    out.append(f"\n  Command : {command.strip().splitlines()[0]}")
    out.append(bar)

    print("\n".join(out))
    sys.exit(0)


if __name__ == "__main__":
    main()
