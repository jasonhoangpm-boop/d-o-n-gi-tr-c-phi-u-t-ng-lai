# Copilot Instructions - Default Agent Rules

**These rules MUST be followed for ALL agent operations on this project.**

---

## MANDATORY RULES (Apply to every task, no exceptions)

### Rule 1: Minimal Change Principle
- Modify **ONLY** the exact code section required
- Avoid rewriting entire files
- Avoid reformatting unrelated code
- Avoid restructuring modules unless explicitly requested

**NEVER:**
- Rewrite working functions
- Replace full files unnecessarily
- Introduce new architecture without approval

---

### Rule 2: No Blind Fix Loop
If an error persists after **2 attempts**:
1. Stop automatic fixing
2. Print error clearly
3. Suggest possible root causes
4. Wait for human instruction

**NEVER:**
- Keep retrying blindly
- Generate multiple versions of same logic
- Stack patches on patches

**MAX_FIX_ATTEMPTS = 2**

---

### Rule 3: Preserve Working Code
If code executes successfully:

**DO NOT:**
- Optimize it
- Refactor it
- Simplify it
- Improve style
- Rename variables

Unless explicitly requested.

**Working code is LOCKED.**

---

### Rule 4: Token Efficiency Mode
Optimize for **low token usage**.

**Allowed:**
- Targeted patch
- Small code diff
- Inline fixes

**NOT allowed:**
- Full file regeneration
- Verbose explanation logs
- Repeated re-analysis of same code

**Prefer: PATCH over REWRITE**

---

### Rule 5: Explicit Scope Requirement
Before modifying code, identify:
- Target file
- Target function/class
- Exact change type (bug fix, feature, refactor, etc.)

**Example format:**
```
CHANGE PLAN:

Target file: models/lstm_model.py  
Target function: forward()  
Change type: bug fix  
Lines affected: 42-47
Risk level: LOW
```

**If scope is unclear: STOP. Do NOT modify code.**

---

### Rule 6: No Unrequested Refactoring
**MUST NOT:**
- Change architecture
- Rename classes
- Move files
- Merge modules
- Split modules
- Change function signatures

Unless user explicitly requests:
- "refactor"
- "optimize architecture"
- "restructure"
- "rename"

---

### Rule 7: Maintain Existing APIs
Preserve:
- Function names
- Function signatures
- Input/output format

**DO NOT change:**
```python
def train_model(X, y)
```
into:
```python
def train(data)
```

Unless explicitly requested.

---

### Rule 8: Respect File Boundaries
**MUST NOT modify:**
- `config.py`
- `requirements.txt`
- `.env`
- Dataset files
- Lock files

Unless explicitly instructed.

**These files are SENSITIVE.**

---

### Rule 9: Backward Compatibility
When adding new features:
- Keep old functions/methods intact
- Maintain old function signatures
- Create NEW functions instead of modifying existing ones
- Ensure old code still works

---

### Rule 10: Change Validation
Before finalizing changes:

1. ✅ Verify target file is correct
2. ✅ Check exact string match for replacement
3. ✅ Include 3-5 lines of context before/after
4. ✅ Confirm no unrelated code is modified
5. ✅ Validate syntax if code was changed

**NEVER execute changes without validation.**

---

## BEST PRACTICES

### For Code Changes:
- Use `multi_replace_string_in_file` for multiple simultaneous changes
- Use `replace_string_in_file` for single changes
- Use `create_file` only for NEW files, never to edit existing files

### For File Operations:
- Always use absolute file paths
- Check file exists before reading
- Validate paths match the workspace structure

### For Error Handling:
- If error after 2 fixes: STOP and report clearly
- Provide context about what was attempted
- Suggest root causes
- Wait for explicit user instruction

### For Communication:
- Report CHANGE PLAN before modifying
- Keep responses concise
- Use file links when referencing code locations
- Never make assumptions about unclear requirements

---

## SCOPE BOUNDARIES

### Locked (NO CHANGES):
- `models/lstm_model.py` ← Existing working LSTM model
- `config.py` ← Configuration file
- `requirements.txt` ← Dependencies

### Flexible (Can Add/Modify):
- `models/` ← Can add new model files (e.g., `transformer_model.py`)
- `training/` ← Can add new training functions
- `utils/` ← Can add new utility functions
- `main.py` ← Can add model selection logic
- New files ← Can create supporting modules

---

## EXAMPLE: ADDING A NEW MODEL

✅ **CORRECT APPROACH (following rules):**
1. Create NEW file: `models/transformer_model.py`
2. Add import in `main.py` (minimal change)
3. Add model selection parameter to `run_pipeline()`
4. Keep `StockLSTM` completely untouched

❌ **INCORRECT APPROACH (violates rules):**
1. Modify `StockLSTM` to support both architectures
2. Rename existing functions
3. Refactor training code
4. Change config values

---

## ACTIVATION

**These rules are ACTIVE by default for:**
- All code modifications
- All file operations
- All automation tasks
- All feature additions
- All bug fixes

**No exceptions. Follow these rules FIRST, always.**

---

## APPROVAL OVERRIDE

To temporarily override a rule, user MUST explicitly state:
```
OVERRIDE RULE [number]: [reason]
```

Example:
```
OVERRIDE RULE 6: I need to refactor the training pipeline
```

Without explicit override, **follow all rules strictly**.
