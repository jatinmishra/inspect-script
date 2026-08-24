# inspect-script

**Claude runs scripts. You approve them blind.**

Every time Claude writes and executes a script at runtime, you see a bare filename and a binary choice. No script. No explanation. No context.

If you say **Yes** — you've just approved code you haven't read.  
If you say **No** — the script is gone. You'll never know what it was going to do.

This happens multiple times in a single Claude Code session. And until now, there was no fix.

---

## Before & After

### Without inspect-script

> A script with bunch of code only.

<img width="861" height="804" alt="Thash command" src="https://github.com/user-attachments/assets/1769f959-0d3f-412e-bd6f-314c5f8921dc" />


---

### With the Skill

> Script type, what it does, why it's needed, and full content — shown as a preview block above the permission prompt.

<img width="821" height="513" alt="• — Script Preview -" src="https://github.com/user-attachments/assets/f203c542-1864-4f17-ad70-b1a1a6a56fbd" />


---

### With the Hook *(optional)*

> Same information, but embedded directly inside the permission dialog itself.

<img width="871" height="829" src="https://github.com/user-attachments/assets/5c92889e-edf9-4ca0-87ae-0605b259e9b0" />


---

## Why this matters

Scripts Claude runs at runtime are real code executing on your machine. They can read files, write to disk, call external services, process sensitive data, or do things you never intended.

The current Claude Code UX gives you zero visibility into any of this. You're expected to trust a temp filename.

**inspect-script is the missing layer** between Claude's intent and your approval. It enforces transparency at the moment it matters most — before execution, not after.

---

## Coverage

Works across every script type Claude commonly uses:

| Type | Detected forms |
|------|---------------|
| Python | `python3 script.py`, heredoc, `-c "..."` |
| Bash / Shell | `bash script.sh`, `sh`, `zsh`, heredoc |
| Node.js | `node script.js`, `-e "..."` |
| Ruby | `ruby script.rb`, `-e "..."` |
| Perl | `perl script.pl` |

Handles heredocs, temp files written then executed, and inline `-c` / `-e` arguments.

---

## Installation

```bash
git clone https://github.com/jatinmishra/inspect-script
cp inspect-script/SKILL.md /your/project/.claude/skills/inspect-script.md
```

That's it. Claude picks it up automatically — no slash command, no config, no restart.

### Optional: embedded-in-prompt hook

For script content shown directly inside the permission dialog (the third screenshot above), install the companion hook:

```bash
mkdir -p /your/project/.claude/hooks
cp inspect-script/hooks/inspect_script.py /your/project/.claude/hooks/
```

Then add this to your project's `.claude/settings.json`:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "python3 /absolute/path/to/.claude/hooks/inspect_script.py"
        }
      ]
    }
  ]
}
```

Use an absolute path in the hook command — relative paths break when Claude changes directories during a session.

---

## Two layers, one goal

| Layer | Mechanism | What you see |
|-------|-----------|--------------|
| **Skill** | Claude outputs a preview block before calling Bash | Formatted summary above the permission prompt |
| **Hook** *(optional)* | `PreToolUse` fires on every Bash command | Script content embedded inside the permission dialog |

Install both for maximum visibility. The skill alone already solves the core problem.

---

## Project structure

```
inspect-script/
├── SKILL.md                ← skill entry point (read by Claude Code)
├── README.md
├── LICENSE.txt
├── hooks/
│   └── inspect_script.py  ← companion PreToolUse hook
└── .gitignore
```

---

## License

MIT — see `LICENSE.txt`
