# AGENT OPERATIONS CHECKLIST

Use this checklist for EVERY code modification task.

---

## Pre-Operation Checklist

Before making ANY changes, agent must complete:

### 📋 Rule Verification
- [ ] Read Context/AGENT_RULES.md (all 20 rules)
- [ ] Read stock_prediction_project/copilot-instructions.md
- [ ] Read Context/SYSTEM_ENFORCEMENT.md
- [ ] Understand MANDATORY rules (1, 2, 3, 5, 8, 9)

### 🎯 Scope Definition
- [ ] Identified target file(s)
- [ ] Identified target function(s) or section(s)
- [ ] Determined change type (bug fix / feature / refactor / etc)
- [ ] Calculated exact line numbers
- [ ] Assessed risk level (LOW / MEDIUM / HIGH)

### 🔍 Locked File Check
- [ ] NOT modifying config.py
- [ ] NOT modifying requirements.txt
- [ ] NOT modifying .env files
- [ ] NOT modifying dataset files
- [ ] NOT modifying models/lstm_model.py (if locked)

### ✅ Rule Compliance Check
- [ ] Follows Rule 1 (Minimal Change)
- [ ] Follows Rule 2 (No Blind Loop)
- [ ] Follows Rule 3 (Preserve Working Code)
- [ ] Follows Rule 5 (Explicit Scope)
- [ ] Follows Rule 8 (File Boundaries)
- [ ] Follows Rule 9 (Backward Compatibility)

### 📝 Documentation
- [ ] CHANGE PLAN written (see template below)
- [ ] Risk assessment completed
- [ ] Alternative approaches considered

---

## CHANGE PLAN Template

```
CHANGE PLAN:

Target file: [exact absolute path]
Target function/section: [exact name or line range]
Change type: [bug fix | feature | refactor | optimization | etc]
Lines affected: [start-end]
Risk level: [LOW | MEDIUM | HIGH]

Reason: [why this change is needed]

Scope: [what will be modified / what will NOT be modified]

Dependencies: [other files that may be affected]

Backward compatibility: [will this break existing code?]

Verification:
- [ ] Minimal change principle
- [ ] Existing APIs preserved  
- [ ] No unnecessary refactoring
- [ ] Locked files untouched
- [ ] Syntax will be correct
```

---

## During Operation Checklist

### 🔧 Making Changes
- [ ] Using correct tool (replace_string_in_file / create_file / etc)
- [ ] Including 3-5 lines of context before/after target code
- [ ] Exact string matching verified
- [ ] Only one change per tool call (or using multi_replace for related changes)
- [ ] No unrelated code reformatting
- [ ] No extraneous whitespace changes

### ⚡ Optimization Focus
- [ ] Using multi_replace_string_in_file for multiple changes (token efficiency)
- [ ] Making targeted patches, not full rewrites
- [ ] Keeping responses concise
- [ ] Avoiding redundant analysis

### 🛡️ Safety Checks
- [ ] Verified target file exists
- [ ] Verified exact string match found
- [ ] Calculated line numbers are correct
- [ ] Will not modify unrelated code

---

## Post-Operation Checklist

### ✔️ Validation
- [ ] Changes applied successfully
- [ ] Syntax is correct
- [ ] No accidental modifications
- [ ] Test confirmed (if applicable)

### 📊 Reporting
- [ ] Confirmed what was changed
- [ ] Showed exact modifications
- [ ] Reported any errors encountered
- [ ] Provided summary of impact

### 📝 Documentation
- [ ] Documented changes in session memory (if complex)
- [ ] Added comments in code (if needed)
- [ ] Updated related documentation (if applicable)

---

## Error Handling Checklist

### ❌ If First Attempt Fails
- [ ] Analyzed error message
- [ ] Identified root cause
- [ ] Adjusted approach
- [ ] Retry once (second attempt)

### ❌ If Second Attempt Fails
- [ ] STOP (do not retry 3+ times)
- [ ] Print error clearly
- [ ] Explain what was attempted
- [ ] Suggest possible causes
- [ ] Request user instruction
- [ ] Wait for explicit guidance

### ⚠️ If Ambiguous or HIGH Risk
- [ ] STOP immediately
- [ ] Ask for clarification
- [ ] Do not proceed with assumptions
- [ ] Wait for user input

---

## Rule Override Checklist

If user requests override:

- [ ] Override is explicitly stated
- [ ] Rule number is specified (e.g., "OVERRIDE RULE 1")
- [ ] Reason is provided
- [ ] User understands consequences
- [ ] Proceed only after confirmation

---

## Token Efficiency Checklist

To minimize token usage:

- [ ] Using multi_replace_string_in_file for multiple changes
- [ ] Targeting exact code sections (not whole files)
- [ ] Providing concise responses
- [ ] Avoiding verbose explanations
- [ ] Not re-analyzing same code repeatedly
- [ ] Using file links instead of repeating code

---

## Special Scenarios

### ✅ Adding a New Model
- [ ] Create NEW file (don't modify existing models)
- [ ] Keep LSTM/existing models completely untouched
- [ ] Add imports to main.py only
- [ ] Add model selection parameter/logic
- [ ] Maintain backward compatibility (default to existing model)

### ✅ Bug Fix
- [ ] Minimal change to affected function only
- [ ] Don't refactor surrounding code
- [ ] Include 3-5 lines of context
- [ ] Try fix twice max
- [ ] Stop and report if 2nd attempt fails

### ✅ Feature Addition
- [ ] Add NEW functions/files
- [ ] Don't modify existing working code
- [ ] Maintain existing function signatures
- [ ] Ensure old code still works
- [ ] Update documentation if needed

### ❌ Refactoring (Without Request)
- [ ] NOT allowed unless explicitly requested
- [ ] NEVER rename variables without request
- [ ] NEVER reorganize imports without request
- [ ] NEVER restructure modules without request

---

## Quick Decision Tree

```
START: New task received
  ↓
├─ Is it a code change? 
│  ├─ YES → Go to SCOPE DEFINITION
│  └─ NO → Proceed with task
│
├─ SCOPE DEFINITION:
│  ├─ Read all 3 rule files ✓
│  ├─ Define exact target ✓
│  ├─ Write CHANGE PLAN ✓
│  ├─ Check locked files ✓
│  └─ Assess risk level ✓
│
├─ RISK ASSESSMENT:
│  ├─ If HIGH → STOP and ask user
│  ├─ If MEDIUM → Verify double, proceed carefully
│  └─ If LOW → Proceed
│
├─ RULE COMPLIANCE:
│  ├─ Violates mandatory rule? → STOP
│  ├─ All checks pass? → Proceed
│  └─ Unclear? → STOP and ask
│
├─ EXECUTE CHANGE:
│  ├─ Use exact string matching ✓
│  ├─ Include context lines ✓
│  ├─ Make single targeted change ✓
│  └─ Validate syntax ✓
│
├─ HANDLE ERRORS:
│  ├─ 1st failure → Try alternative
│  ├─ 2nd failure → STOP
│  └─ 3rd+ attempt → FORBIDDEN
│
└─ REPORT & COMPLETE:
   ├─ Show changes ✓
   ├─ Confirm success ✓
   ├─ Ask if needs more ✓
   └─ DONE

```

---

## Common Mistakes to Avoid

❌ **DON'T:**
- Rewrite entire files
- Skip CHANGE PLAN step
- Try same fix 3+ times
- Modify locked files
- Remove/optimize working code without request
- Change function signatures without request
- Refactor code without explicit request
- Use regex without context lines
- Make multiple unrelated changes
- Ignore ambiguous instructions

✅ **DO:**
- Make targeted patches
- Write CHANGE PLAN first
- Stop after 2 failed attempts
- Document changes clearly
- Verify scope is explicit
- Preserve working code
- Maintain backward compatibility
- Include 3-5 context lines
- Use multi_replace for efficiency
- Ask for clarification when unclear

---

**Print this checklist before every operation**
**Use it to verify all steps completed**
**Follow it strictly for all tasks**
