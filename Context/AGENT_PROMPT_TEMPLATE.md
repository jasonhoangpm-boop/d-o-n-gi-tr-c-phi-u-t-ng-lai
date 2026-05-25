# AGENT PROMPT TEMPLATE

**Use this template when starting ANY new task**

---

## Task Initialization Protocol

Use this template as your first response to any new task:

---

## INITIALIZATION CHECK

```
AGENT RULE VERIFICATION - [TASK NAME]

✅ Status: READY TO PROCEED
⏱️ Time: 2026-04-23

Reading Context Files:
[1/5] Context/README.md ................... ✓ Loaded
[2/5] Context/QUICK_REFERENCE.md ......... ✓ Loaded
[3/5] Context/AGENT_RULES.md ............. ✓ Loaded
[4/5] Context/SYSTEM_ENFORCEMENT.md ...... ✓ Loaded
[5/5] Context/OPERATIONS_CHECKLIST.md .... ✓ Loaded

All mandatory rules verified:
✅ Rule 1: Minimal Change Principle
✅ Rule 2: No Blind Fix Loop (max 2 attempts)
✅ Rule 3: Preserve Working Code
✅ Rule 5: Explicit Scope Requirement
✅ Rule 8: Respect File Boundaries
✅ Rule 9: Backward Compatibility

Locked files identified:
✅ config.py - PROTECTED
✅ requirements.txt - PROTECTED
✅ .env - PROTECTED
✅ Dataset files - PROTECTED
✅ models/lstm_model.py - PROTECTED

Ready to receive task.
```

---

## For Code Modification Tasks

**Use this additional template:**

```
CHANGE PLAN:

Target file: [absolute path]
Target function/section: [exact name or line numbers]
Change type: [bug fix | feature | refactor | optimization | other]
Lines affected: [start-end or N/A]
Risk level: [LOW | MEDIUM | HIGH]

Reason for change:
[Why this change is needed]

Scope boundary:
WILL MODIFY: [what changes]
WILL NOT MODIFY: [what stays same]

Dependencies:
[Other files affected, or "None"]

Backward compatibility:
[Will this break existing code? YES/NO - explain]

Verification checklist:
- [ ] Minimal change principle applied
- [ ] Existing APIs preserved
- [ ] No unnecessary refactoring
- [ ] Locked files untouched
- [ ] Working code not modified
- [ ] Syntax will be correct

Status: AWAITING CONFIRMATION TO PROCEED
```

---

## For Complex Tasks

**Use this expanded template:**

```
TASK ANALYSIS:

Task Type: [code change | debugging | feature | refactor | other]
Complexity: [LOW | MEDIUM | HIGH]
Estimated Attempts: [how many fixes expected?]

Rules Review:
✅ All mandatory rules (1,2,3,5,8,9) understood
✅ Locked files identified
✅ Flexible files identified
✅ Risk factors assessed

Execution Plan:
1. [First step]
2. [Second step]
3. [Third step]

Error Handling:
- Attempt 1: [strategy]
- Attempt 2: [alternative]
- If both fail: STOP and report

Documentation:
- Changes will be minimal and targeted
- Context lines included (3-5 before/after)
- Syntax validation required
- Post-operation report provided

Status: READY TO PROCEED
```

---

## For Ambiguous or HIGH-Risk Tasks

**STOP and use this template:**

```
CLARIFICATION REQUIRED

Task: [name]
Clarity Level: AMBIGUOUS | HIGH RISK

Issue:
[Describe what's unclear or risky]

Questions for user:
1. [Question 1]
2. [Question 2]
3. [Question 3]

Suggested approaches:
A) [Option A]
B) [Option B]
C) [Option C]

Awaiting user guidance before proceeding.

Related rule: [which rule applies - e.g., "Rule 5: Explicit Scope"]
```

---

## Before Starting Work

Copy and adapt this checklist:

```
PRE-OPERATION VERIFICATION:

Task received: ✓
Task understood: ✓ / ❌ [need clarification]
Risk assessed: ✓ 
Scope defined: ✓ / ❌ [need clarification]
Rules reviewed: ✓
Locked files checked: ✓
Flexible files identified: ✓
CHANGE PLAN written: ✓
All verifications passed: ✓

READY TO PROCEED: YES / NO [need clarification]

If NO - explain issue and wait for user guidance.
```

---

## During Execution

Use this running format:

```
EXECUTING: [Task Name]

Step 1/N: [Description]
Status: IN PROGRESS
Time: 2026-04-23 XX:XX

Making change to: [file path]
Line range: [lines]
Reason: [why this change]
Impact: [what else might be affected]

Executing change...
✓ Change applied successfully

Validation:
✓ Syntax correct
✓ No unintended modifications
✓ File saved

Step 2/N: [Description]
...
```

---

## Error Handling During Execution

Use this format:

```
ERROR ENCOUNTERED:

Step: [which step]
Error type: [type of error]
Error message: [full message]

Analysis:
[Detailed explanation]

Attempted fix (Attempt 1/2):
[What was tried]
Result: [Success / Failed]

If failed - attempting alternative (Attempt 2/2):
[Alternative approach]
Result: [Success / Failed]

If still failing:
STOPPING EXECUTION - Rule 2 (No Blind Loop) triggered

Issue: [What went wrong]
Possible causes:
1. [Cause 1]
2. [Cause 2]
3. [Cause 3]

Suggested next steps:
1. [Suggestion 1]
2. [Suggestion 2]

Awaiting user instruction.
```

---

## Post-Operation Report

Use this template:

```
OPERATION COMPLETED

Task: [name]
Duration: [time]
Status: ✅ SUCCESS / ❌ PARTIAL / ⚠️ STOPPED

Changes made:
✓ [Change 1]
✓ [Change 2]
[etc]

Files modified:
- [file 1] (lines X-Y)
- [file 2] (lines A-B)

Verification:
✓ All changes applied
✓ No unintended modifications
✓ Syntax validated
✓ Locked files untouched
✓ Backward compatibility maintained

Summary:
[Brief summary of what was done]

Next steps:
[What's next, or "Task complete"]

Status: READY FOR NEXT TASK
```

---

## Error/STOP Report

Use this format:

```
OPERATION STOPPED

Task: [name]
Reason: [why stopped]

Attempts made: [N/2]

Current status:
[What was accomplished]
[What needs to be done]

Issue:
[Detailed description]

Possible causes:
1. [Cause 1]
2. [Cause 2]

Suggestions:
1. [Suggestion 1]
2. [Suggestion 2]

Related rule: [Rule N - description]

Awaiting user guidance.
```

---

## Rule Reference Quick Links

- Rule 1 (Minimal): Changes to single files only
- Rule 2 (2 attempts): Stop after 2 fails
- Rule 3 (Preserve): Don't touch working code
- Rule 5 (Scope): Document exactly what changes
- Rule 8 (Boundaries): Protect locked files
- Rule 9 (Compat): Keep existing functions

Full details: Context/AGENT_RULES.md

---

## Example: Adding a New Model

```
TASK: Add Transformer model to stock prediction system

INITIALIZATION CHECK:
✅ All rules loaded
✅ Context verified
✅ Scope defined

CHANGE PLAN:

Target file: models/transformer_model.py (NEW)
Target function: StockTransformer class (NEW)
Change type: feature addition
Risk level: LOW

Scope boundary:
WILL MODIFY:
- Create new file: models/transformer_model.py
- Update main.py imports (minimal)
- Add model parameter to run_pipeline()

WILL NOT MODIFY:
- models/lstm_model.py (keep unchanged)
- config.py (keep unchanged)
- training/train.py (add new function only)

Dependencies: Requires PyTorch Transformer

Backward compatibility:
✓ YES - default model remains LSTM
✓ Old code still works
✓ New feature is optional

Verification:
✓ Minimal change (only new code + minimal updates)
✓ Existing APIs preserved (train_model unchanged)
✓ No working code modified
✓ Locked files untouched

Status: READY TO EXECUTE

[Execute changes here...]

OPERATION COMPLETED:
✓ New model file created
✓ Main.py updated with import
✓ Model selection added
✓ LSTM model completely untouched
✓ Backward compatibility verified

Status: TASK COMPLETE
```

---

## Copy-Paste Ready Sections

### Section 1: Task Start
```
AGENT RULES VERIFICATION

✅ Rules loaded: All 5 context files
✅ Task: [TASK NAME]
✅ Complexity: [LOW/MEDIUM/HIGH]
✅ Ready to proceed

Status: INITIALIZED
```

### Section 2: Change Plan
```
CHANGE PLAN:

Target file: [PATH]
Target function: [NAME]
Change type: [TYPE]
Risk level: [LEVEL]

Status: AWAITING VERIFICATION
```

### Section 3: Execution Start
```
EXECUTING CHANGES

Step 1/N: [STEP]
Status: IN PROGRESS

[Make changes...]

✓ Complete
```

### Section 4: Error Stop
```
STOPPING - Rule 2 Triggered

Attempts: 2/2
Issue: [ISSUE]

Awaiting user instruction.
```

### Section 5: Completion
```
✅ OPERATION COMPLETED

Changes: [SUMMARY]
Status: SUCCESS

Ready for next task.
```

---

## Frequently Used Phrases

**When starting:**
- "AGENT RULES VERIFIED - READY TO PROCEED"
- "All mandatory rules loaded and understood"

**When in doubt:**
- "CLARIFICATION REQUIRED - STOPPING"
- "Ambiguous instruction - requesting guidance"

**After success:**
- "OPERATION COMPLETED SUCCESSFULLY"
- "All changes applied and verified"

**After error:**
- "STOPPING - Rule 2 (No Blind Loop) triggered"
- "Awaiting user instruction to proceed"

---

**Usage:** Copy relevant sections into your response
**Purpose:** Ensure consistent rule application
**Update Frequency:** Quarterly
**Status:** ✅ ACTIVE
