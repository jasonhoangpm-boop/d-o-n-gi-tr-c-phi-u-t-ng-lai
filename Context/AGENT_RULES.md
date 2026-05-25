# AGENT_RULES.md

## Strict Rules for AI Automation Agents

This file defines **strict behavioral rules** for AI agents (Copilot, Claude Code, Auto Agents, n8n AI nodes, etc.) working in this repository.

The goal is to:

* Prevent unnecessary code changes
* Reduce token waste
* Avoid repeated fixing loops
* Maintain stable project behavior
* Ensure deterministic automation

Agents MUST follow these rules at all times.

---

# CORE PRINCIPLES

## Rule 1 — Minimal Change Principle

The agent MUST:

* Modify only the **exact code section** required
* Avoid rewriting entire files
* Avoid reformatting unrelated code
* Avoid restructuring modules unless explicitly requested

NEVER:

* Rewrite working functions
* Replace full files unnecessarily
* Introduce new architecture without approval

---

## Rule 2 — No Blind Fix Loop

If an error persists after **2 attempts**, the agent MUST:

1. Stop automatic fixing
2. Print error clearly
3. Suggest possible root causes
4. Wait for human instruction

NEVER:

* Keep retrying blindly
* Generate multiple versions of same logic
* Stack patches on patches

Maximum retry attempts:

```
MAX_FIX_ATTEMPTS = 2
```

---

## Rule 3 — Preserve Working Code

If code executes successfully:

DO NOT:

* Optimize it
* Refactor it
* Simplify it
* Improve style
* Rename variables

Unless explicitly requested.

Working code is considered **locked**.

---

## Rule 4 — Token Efficiency Mode

Agent must optimize for **low token usage**.

Allowed:

* Targeted patch
* Small code diff
* Inline fixes

Not allowed:

* Full file regeneration
* Verbose explanation logs
* Repeated re-analysis of same code

Target:

```
Prefer PATCH over REWRITE
```

---

## Rule 5 — Explicit Scope Requirement

Before modifying code, agent must identify:

* Target file
* Target function
* Exact change

Example format:

```
Target file: models/lstm_model.py  
Target function: forward()  
Change type: bug fix  
```

If scope is unclear:

STOP.

Do not modify code.

---

## Rule 6 — No Unrequested Refactoring

Agent MUST NOT:

* Change architecture
* Rename classes
* Move files
* Merge modules
* Split modules

Unless user explicitly requests:

```
"refactor"
"optimize architecture"
"restructure"
```

---

## Rule 7 — Maintain Existing APIs

Agent must preserve:

* Function names
* Function signatures
* Input/output format

Do not change:

```
def train_model(X, y)
```

into:

```
def train(data)
```

unless explicitly requested.

---

## Rule 8 — Respect File Boundaries

Agent MUST NOT modify:

```
config.py
requirements.txt
.env
dataset files
```

Unless explicitly instructed.

These files are considered **sensitive**.

---

## Rule 9 — Log Before Modify

Before making changes, agent must output:

```
CHANGE PLAN:

File: ______
Reason: ______
Lines affected: ______
Risk level: LOW | MEDIUM | HIGH
```

If risk level:

```
HIGH
```

Agent must STOP.

---

## Rule 10 — Single Responsibility Fix

Each modification must solve:

```
ONE problem only
```

Do not combine:

* bug fix
* optimization
* refactor

in one change.

---

# DEBUGGING RULES

## Rule 11 — Deterministic Debugging

Agent must:

1. Identify root cause
2. Modify minimal code
3. Re-test logic mentally

NOT:

* Try random fixes
* Add redundant conditions
* Add defensive hacks blindly

---

## Rule 12 — No Over-Engineering

Agent must not:

* Add new abstraction layers
* Add unused helper functions
* Add complex class hierarchies

Unless strictly required.

---

# MODEL-SPECIFIC RULES

(For LSTM / Transformer Projects)

## Rule 13 — Do Not Change Model Architecture Automatically

Agent MUST NOT modify:

```
LSTM layer count
Hidden size
Transformer heads
Embedding dimensions
```

Unless explicitly requested.

These are **experimental parameters**, not bug fixes.

---

## Rule 14 — Dataset Safety

Agent MUST NOT:

* Modify dataset
* Normalize twice
* Shuffle dataset unintentionally

Unless explicitly instructed.

---

## Rule 15 — Training Stability

Agent MUST NOT:

* Change optimizer
* Change loss function
* Change learning rate

Without instruction.

---

# AUTOMATION SAFETY RULES

## Rule 16 — Stop on Ambiguity

If instruction is unclear:

STOP.

Ask:

```
Clarify target file and expected behavior.
```

Do not guess.

---

## Rule 17 — Do Not Touch Untested Modules

If module is not executed in current flow:

DO NOT modify it.

---

## Rule 18 — Avoid Recursive Changes

Agent must not:

* Modify file A
* Which triggers modification in file B
* Which returns to file A

This creates infinite loops.

---

# PERFORMANCE RULES

## Rule 19 — Prefer Reuse

Before creating new code:

Check:

* existing functions
* existing utilities
* existing modules

Reuse first.

---

## Rule 20 — Avoid Duplicate Code

Agent MUST NOT create:

```
train_model_v2
train_model_new
train_model_fixed
```

Instead:

Fix original function.

---

# FAILURE HANDLING

If agent cannot safely proceed:

Output:

```
SAFE STOP TRIGGERED

Reason:
_________

Suggested Actions:
1. _______
2. _______
```

Do not modify code.

---

# FINAL LOCK RULE

If file contains:

```
# LOCKED
```

Agent MUST:

```
READ ONLY
NO MODIFICATION
```

---

# EXECUTION MODE

Default mode:

```
SAFE_PATCH_MODE = TRUE
```

Meaning:

* Only minimal patches
* No file rewrite
* No architecture change
* No speculative fixes

---

---

# ACTIVATION: DEFAULT AGENT ENFORCEMENT

**STATUS: ✅ ACTIVATED - MANDATORY FOR ALL OPERATIONS**

These rules are **DEFAULT and ALWAYS ACTIVE** for:
- ✅ All code modifications
- ✅ All file operations  
- ✅ All automation tasks
- ✅ All feature additions
- ✅ All bug fixes
- ✅ All code reviews
- ✅ All refactoring work
- ✅ All optimization tasks

## No Exceptions
**These rules apply to EVERY agent operation on this project.**

No agent may bypass, ignore, or selectively apply these rules.

---

## Rule Override Requirement

To temporarily override any rule, the user MUST:

1. State rule number explicitly
2. Provide clear justification
3. Acknowledge consequences

**Example override request:**
```
OVERRIDE RULE 1: I need full file rewrite because of structural incompatibility
```

Without explicit override, **follow all rules strictly.**

---

## Verification Checklist

Before EVERY code change, agent MUST verify:

- [ ] Rule 1: Minimal change principle applied
- [ ] Rule 5: Explicit scope documented
- [ ] Rule 7: Existing APIs preserved
- [ ] Rule 8: Sensitive files untouched
- [ ] Rule 9: Backward compatibility maintained
- [ ] Rule 10: Changes validated

If ANY checkbox fails: **STOP and report issue**

---

## Related Files

- **Primary Rules:** This file (AGENT_RULES.md)
- **Project-Specific Instructions:** stock_prediction_project/copilot-instructions.md
- **Context Reference:** Context/AGENT_RULES.md

All must be read and followed together.

---

# END OF RULES
