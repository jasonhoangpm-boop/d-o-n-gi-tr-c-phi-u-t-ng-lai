# SYSTEM ENFORCEMENT - Agent Rules Activation

**File Purpose:** Define and activate default behavioral rules for all AI agents

**Last Updated:** 2026-04-23
**Status:** ✅ ACTIVE

---

## Global Activation Rules

These settings apply to **ALL** agent operations in this workspace:

### Security & Safety
```
SAFE_MODE = TRUE                    # Never bypass safety checks
MINIMAL_CHANGE_MODE = TRUE          # Only modify required code
REQUIRE_EXPLICIT_SCOPE = TRUE       # Must document changes
VALIDATE_BEFORE_MODIFY = TRUE       # Verify target files exist
```

### Change Management
```
MAX_FIX_ATTEMPTS = 2                # Stop retrying after 2 fails
REQUIRE_CHANGE_PLAN = TRUE          # Must output CHANGE PLAN first
PRESERVE_WORKING_CODE = TRUE        # Don't optimize working functions
PATCH_OVER_REWRITE = TRUE           # Prefer small changes
```

### File Boundaries
```
LOCK_FILE_CONFIG = TRUE             # Protect config.py
LOCK_FILE_REQUIREMENTS = TRUE       # Protect requirements.txt
LOCK_FILE_ENV = TRUE                # Protect .env files
LOCK_FILE_DATASETS = TRUE           # Protect data files
```

### Token Efficiency
```
MINIMIZE_TOKENS = TRUE              # Optimize for low token usage
PREFER_DIFFS = TRUE                 # Show diffs, not full files
AVOID_REDUNDANT_ANALYSIS = TRUE     # Don't re-analyze same code
CONCISE_COMMUNICATION = TRUE        # Keep responses brief
```

---

## Mandatory Rule Set

**Rules that CANNOT be disabled:**

1. ✅ **Rule 1: Minimal Change Principle** 
   - Always active
   - No exceptions

2. ✅ **Rule 2: No Blind Fix Loop**
   - Max 2 attempts enforced
   - Automatic STOP on 3rd failure

3. ✅ **Rule 3: Preserve Working Code**
   - No unauthorized optimization
   - No refactoring without request

4. ✅ **Rule 5: Explicit Scope Requirement**
   - Must document changes
   - STOP if scope unclear

5. ✅ **Rule 8: Respect File Boundaries**
   - Locked files protected
   - Requires explicit override

6. ✅ **Rule 9: Backward Compatibility**
   - Maintain existing APIs
   - Keep function signatures

---

## Optional Enhancements (Can Disable with Override)

These rules can be overridden with explicit user instruction:

- Rule 4: Token Efficiency
- Rule 6: No Unrequested Refactoring
- Rule 7: Maintain Existing APIs
- Rule 10+: Other rules

**Override Format:**
```
OVERRIDE RULE [N]: [reason for override]
```

---

## Verification Protocol

Every code modification requires:

**Step 1: Plan**
```
CHANGE PLAN:

Target file: [path]
Target function: [name]
Change type: [type]
Lines affected: [range]
Risk level: [LOW/MEDIUM/HIGH]
```

**Step 2: Check** (Before executing)
- [ ] Scope is explicit and clear
- [ ] Minimal change principle applied
- [ ] Working code not modified
- [ ] Existing APIs preserved
- [ ] Backward compatibility maintained
- [ ] Locked files not touched

**Step 3: Execute** (Only if all checks pass)
- Apply changes
- Validate syntax

**Step 4: Report** (After completion)
- Confirm changes applied
- Show what was changed
- Summary of impact

---

## Escalation Rules

### STOP Conditions (Automatic Halt)

Agent MUST stop immediately if:

1. ❌ Scope is ambiguous
2. ❌ Risk level is HIGH
3. ❌ 2 fix attempts failed
4. ❌ Would violate a mandatory rule
5. ❌ Instruction contradicts rules
6. ❌ Locked file would be modified
7. ❌ Working code would be changed

### Error Reporting

When STOP occurs, agent MUST output:
```
SAFE STOP TRIGGERED

Reason: [specific reason]

Current status: [what was attempted]

Suggested actions:
1. [action 1]
2. [action 2]

Awaiting user instruction...
```

---

## Rule Combination Matrix

### Scenario: Bug Fix
- ✅ Rule 1: Minimal change (YES)
- ✅ Rule 2: Try 2 times (YES)
- ✅ Rule 3: Don't break working code (YES)
- ✅ Rule 5: Document scope (YES)
- ✅ Rule 8: Respect boundaries (YES)

### Scenario: Add New Feature
- ✅ Rule 1: Minimal change (YES - only new code)
- ✅ Rule 5: Explicit scope (YES - new file/function)
- ✅ Rule 9: Backward compatibility (YES - keep old APIs)
- ❌ Rule 6: No refactoring (NO - don't touch old code)

### Scenario: Add New Model
- ✅ Create new file (YES - follow Rule 9)
- ✅ Keep LSTM untouched (YES - follow Rule 3)
- ✅ Update imports only (YES - follow Rule 1)
- ✅ Add selection logic (YES - follow Rule 9)

---

## Related Configuration Files

Files that define these rules:

1. **Context/AGENT_RULES.md** - Master rule definitions
2. **stock_prediction_project/copilot-instructions.md** - Project-specific rules
3. **This file** - Activation and enforcement settings

All must be consulted together.

---

## Enforcement Mechanism

### For GitHub Copilot
- Always follow rules
- Output CHANGE PLAN before modifications
- Stop on mandatory rule violations

### For Auto Agents
- Load rules before each operation
- Verify against rule set
- Apply constraints automatically

### For Claude Code
- Read rule files from context
- Validate against enforcement matrix
- Report violations explicitly

### For All Agents
- Check rule file before any code change
- Document changes per protocol
- Escalate ambiguities to user

---

## Testing Enforcement

Before deploying changes, verify:

```bash
# 1. Check copilot-instructions.md exists
test -f stock_prediction_project/copilot-instructions.md

# 2. Check AGENT_RULES.md exists  
test -f Context/AGENT_RULES.md

# 3. Verify files have activation section
grep -q "ACTIVATED" Context/AGENT_RULES.md
```

---

## Audit Trail

Track all agent operations:

- **Change Plan Required:** Yes
- **Scope Documentation:** Yes
- **Risk Assessment:** Yes
- **Validation Checklist:** Yes
- **Error Handling:** Yes

---

**Last Sync:** 2026-04-23
**Version:** 1.0
**Status:** ✅ ACTIVE

All agents must read and follow this file.
