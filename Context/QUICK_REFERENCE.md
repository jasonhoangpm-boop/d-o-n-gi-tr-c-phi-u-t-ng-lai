# QUICK REFERENCE - Agent Rules Summary

**Use this for quick lookup of all agent rules and enforcement**

---

## The 3 Core Rules (ALWAYS Follow)

### 1️⃣ **Minimal Change Principle** (Rule 1)
```
❌ WRONG: Rewrite entire file to add one line
✅ RIGHT: Add/modify just that one line with 3-5 lines context
```

### 2️⃣ **No Blind Fix Loop** (Rule 2)
```
Attempt 1: Try fix
Attempt 2: Try alternative fix
Attempt 3+: STOP and report error
```

### 3️⃣ **Preserve Working Code** (Rule 3)
```
❌ WRONG: Optimize/refactor working code without request
✅ RIGHT: Leave working code untouched unless explicitly requested
```

---

## Before Every Code Change

### Output CHANGE PLAN
```
CHANGE PLAN:
Target file: [path]
Target function: [name]
Change type: [type]
Lines affected: [range]
Risk level: [LOW/MEDIUM/HIGH]
```

### Check Locked Files
- ✅ Don't touch: config.py, requirements.txt, .env, datasets, models/lstm_model.py

### Verify No Violations
- ✅ Rule 1: Minimal?
- ✅ Rule 5: Scope explicit?
- ✅ Rule 8: File boundaries respected?
- ✅ Rule 9: Backward compatible?

---

## The 20 Rules at a Glance

| # | Rule | Brief | Critical? |
|---|------|-------|-----------|
| 1 | Minimal Change | Only modify required code | ⚠️ YES |
| 2 | No Blind Loop | Max 2 attempts, then STOP | ⚠️ YES |
| 3 | Preserve Code | Don't optimize without request | ⚠️ YES |
| 4 | Token Efficiency | Prefer patches over rewrites | Optional |
| 5 | Explicit Scope | Document changes clearly | ⚠️ YES |
| 6 | No Refactoring | Don't refactor without request | Optional |
| 7 | Maintain APIs | Keep function signatures | Optional |
| 8 | File Boundaries | Respect locked files | ⚠️ YES |
| 9 | Backward Compat | Keep old code working | ⚠️ YES |
| 10 | Single Fix | One problem per change | Required |
| 11 | Deterministic Debug | Find root cause, minimal fix | Required |
| 12 | No Over-Engineering | Don't add unnecessary complexity | Required |
| 13 | Model Stability | Don't change architecture auto | Required |
| 14 | Dataset Safety | Don't modify datasets | Required |
| 15 | Training Stability | Don't change training params | Required |
| 16 | Stop on Ambiguity | Ask for clarification | Required |
| 17 | Only Touch Tested Modules | Don't modify untested code | Required |
| 18 | Avoid Recursion | Don't create circular changes | Required |
| 19 | Prefer Reuse | Reuse existing code first | Required |
| 20 | Avoid Duplicates | No _v2, _new, _fixed versions | Required |

**CRITICAL (⚠️):** Cannot be overridden or disabled
**Required:** Strongly recommended, rarely overridden
**Optional:** Can be overridden with explicit request

---

## Override Instructions

```
OVERRIDE RULE [N]: [reason]

Example:
OVERRIDE RULE 1: I need to rewrite the entire training architecture

Only proceed with explicit override statement from user.
```

---

## Error Handling Flow

```
Error occurs
    ↓
Attempt 1: Try fix
    ↓ (still fails)
Attempt 2: Try alternative
    ↓ (still fails)
STOP (do not retry again)
    ↓
Output error clearly
Suggest root causes
Wait for user instruction
```

---

## Locked Files (DO NOT MODIFY)

```
✅ config.py
✅ requirements.txt
✅ .env
✅ Dataset files
✅ models/lstm_model.py (if locked)
```

**These require explicit user instruction to modify.**

---

## Flexible Files (Can Modify with Rules)

```
✅ models/ (can add new models)
✅ training/ (can add new training functions)
✅ utils/ (can add new utilities)
✅ main.py (can add selection logic)
✅ New files (can create)
```

**These follow minimal change principle and backward compatibility.**

---

## Common Operations

### ✅ Add New Model (CORRECT)
```
1. Create NEW file: models/transformer_model.py
2. Update main.py imports (minimal)
3. Add model selection parameter
4. Keep LSTM completely unchanged
```

### ❌ Add New Model (WRONG)
```
1. Modify StockLSTM to support both types
2. Refactor training code
3. Change function signatures
4. Rename variables
```

### ✅ Bug Fix (CORRECT)
```
1. Identify exact bug location
2. Make minimal fix
3. Include context lines
4. Test logic
5. Stop after 2 attempts if fails
```

### ❌ Bug Fix (WRONG)
```
1. Rewrite entire function
2. Refactor surrounding code
3. Change other variables
4. Keep retrying without limit
```

---

## Token Efficiency Tips

- ✅ Use `multi_replace_string_in_file` for multiple changes
- ✅ Target exact code sections
- ✅ Keep responses brief
- ✅ Use file links instead of copying code
- ❌ Don't rewrite entire files
- ❌ Don't provide verbose explanations

---

## Quick Decision Points

**Can I make this change?**
```
Is it a code modification?
├─ Read rule files ✓
├─ Define scope ✓
├─ Write CHANGE PLAN ✓
├─ Check locked files ✓
├─ Assess risk ✓
└─ Proceed if all pass, else STOP
```

**What if it fails?**
```
Try again once (2nd attempt)
├─ Works? → Done
└─ Still fails? → STOP, report error, wait for user
```

**What if scope is unclear?**
```
STOP immediately
├─ Ask for clarification
└─ Wait for user instruction
```

**What if risk is HIGH?**
```
STOP immediately
├─ Report why it's high risk
└─ Wait for user confirmation
```

---

## Rule Files Location

- **Master Rules:** Context/AGENT_RULES.md (20 rules)
- **Project Rules:** stock_prediction_project/copilot-instructions.md
- **Enforcement:** Context/SYSTEM_ENFORCEMENT.md
- **Checklist:** Context/OPERATIONS_CHECKLIST.md
- **Quick Ref:** This file

**Read all before starting work.**

---

## In Case of Doubt

1. ❓ Read the full rule from AGENT_RULES.md
2. ❓ Check the examples provided
3. ❓ Consult OPERATIONS_CHECKLIST.md
4. ❓ Ask user for clarification
5. ❓ STOP instead of guessing

**Never proceed on ambiguous instructions.**

---

## Verification Checklist (Copy & Use)

```
[ ] Rule files read
[ ] Scope defined clearly
[ ] CHANGE PLAN written
[ ] Locked files checked
[ ] Risk assessed
[ ] No mandatory rule violations
[ ] Minimal change principle applied
[ ] Existing APIs preserved
[ ] Backward compatibility maintained
[ ] Ready to proceed
```

**Print before every operation**

---

**STATUS:** ✅ ACTIVE
**All agents must read and follow these rules**
