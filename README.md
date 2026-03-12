# Webplode Marketplace

A Claude Code plugin marketplace with curated skills for AI-powered workflows.

## Installation

```bash
claude plugin add /path/to/webplode-marketplace
```

## Skills

### prompt-leverage

Strengthen a raw user prompt into an execution-ready instruction set. Automatically detects task type (coding, research, writing, review, planning, analysis), infers intensity level, and adds structured scaffolding for better execution.

**Usage:**

Invoke as a skill in Claude Code:
```
/webplode-marketplace:prompt-leverage
```

Or use the Python script directly:
```bash
python skills/prompt-leverage/scripts/augment_prompt.py "your raw prompt here"
```

**Framework blocks applied selectively:**
- Objective, Context, Work Style, Tool Rules, Output Contract, Verification, Done Criteria

**Output modes:**
- Inline upgrade, Upgrade + rationale, Template extraction, Hook spec

## License

MIT
