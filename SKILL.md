---
name: inspect-script
description: >
  Run any script (Python, Bash, Shell, Node.js, Ruby, Perl) with full
  transparency before executing. Use this skill instead of calling Bash
  directly whenever writing and running a script at runtime. Triggers:
  executing a Python script, running a bash/shell script, invoking Node.js
  or Ruby scripts, writing a script to a temp file and running it, or any
  heredoc command containing script code. Always output WHAT/WHY/content/
  command before executing — ensures the user sees the full script even if
  they deny the permission prompt.
license: MIT
---

# inspect-script

Run any script with full transparency — always show what it does, why it's
needed, its full content, and the exact command before executing.

---

## The problem

When Claude writes and runs a script at runtime, users see a Bash permission
prompt but not the script content. If they deny, the script disappears. They
must approve or reject blind.

---

## Process

### Step 1 — Identify the script type

Detect the interpreter from the command:

| Interpreter | Detected by | Type label |
|-------------|-------------|------------|
| `python3`, `python` | interpreter name | Python |
| `bash`, `sh`, `zsh` | interpreter name | Bash / Shell |
| `node` | interpreter name | Node.js |
| `ruby` | interpreter name | Ruby |
| `perl` | interpreter name | Perl |

### Step 2 — Output the preview block

Before calling Bash, ALWAYS output this block:

```
── Script Preview ────────────────────────────────────────────
  Type    : <Python | Bash | Node.js | Ruby | Shell | Perl>
  What    : <one sentence — what this script does>
  Why     : <one sentence — why it is needed right now>

  Content :
    <full script content, verbatim>

  Command : <exact string passed to Bash>
─────────────────────────────────────────────────────────────
```

### Step 3 — Execute via Bash

After printing the preview, call Bash normally. The user still sees the
standard permission prompt — the preview adds visibility before they decide,
it does not replace the prompt.

---

## Rules

1. **Never skip the preview** — show it before every script execution, no exceptions
2. **WHAT and WHY must be task-specific** — not generic ("runs a script", "executes code")
3. **Show full content** — never truncate or summarise the script body
4. **Command must be verbatim** — copy the exact string that will be passed to Bash
5. **Applies to all script types** — Python, Bash, Shell, Node.js, Ruby, Perl, and any temp-file or heredoc pattern

---

## Script header convention

When writing scripts to temp files, always prepend these comment headers.
They make scripts self-documenting and are automatically extracted by the
companion hook.

**Python / Bash / Shell / Ruby / Perl:**
```
# WHAT: <one-line description of what this script does>
# WHY:  <one-line reason why it is needed for this task>
```

**Node.js / JavaScript:**
```
// WHAT: <one-line description of what this script does>
// WHY:  <one-line reason why it is needed for this task>
```

---

## Companion hook (optional)

For the embedded-in-prompt experience — script content shown inside the
Bash permission dialog itself — install the companion hook:

1. Copy `hooks/inspect_script.py` to your project's `.claude/hooks/`
2. Register it in `.claude/settings.json`:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "python3 .claude/hooks/inspect_script.py"
        }
      ]
    }
  ]
}
```

The hook fires automatically on every Bash command and prints script details
before the permission prompt appears. Exit code 0 — non-blocking.
