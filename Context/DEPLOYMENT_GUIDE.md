# DEPLOYMENT GUIDE - Agent Rules System

**How to activate and maintain agent rules system**

---

## System Overview

This system enforces **20 mandatory rules** for all AI agent operations on this project.

**Components:**
1. **Context/AGENT_RULES.md** - Master rules file (20 rules)
2. **Context/SYSTEM_ENFORCEMENT.md** - Activation and enforcement
3. **Context/OPERATIONS_CHECKLIST.md** - Step-by-step procedures
4. **Context/QUICK_REFERENCE.md** - Fast lookup guide
5. **Context/AGENT_PROMPT_TEMPLATE.md** - Response templates
6. **Context/INDEX.md** - Navigation and guidance
7. **stock_prediction_project/copilot-instructions.md** - Project-specific rules

---

## Installation (Setup Instructions)

### Step 1: Verify All Files Exist

```bash
# In Context folder
✅ AGENT_RULES.md - 20 comprehensive rules
✅ SYSTEM_ENFORCEMENT.md - Enforcement configuration
✅ OPERATIONS_CHECKLIST.md - Operation procedures
✅ QUICK_REFERENCE.md - Quick lookup
✅ AGENT_PROMPT_TEMPLATE.md - Response templates
✅ INDEX.md - Navigation guide
✅ README.md - Project overview with rules

# In stock_prediction_project folder
✅ copilot-instructions.md - Project-specific rules
```

All files present? → Continue to Step 2

### Step 2: File Structure Check

```
Workspace Root (c:\Users\nhatm\Desktop\Đồ ÁN DL\)
├── Context/
│   ├── AGENT_RULES.md .................... ✓ Master rules
│   ├── SYSTEM_ENFORCEMENT.md ............. ✓ Enforcement
│   ├── OPERATIONS_CHECKLIST.md ........... ✓ Procedures
│   ├── QUICK_REFERENCE.md ............... ✓ Lookup
│   ├── AGENT_PROMPT_TEMPLATE.md ......... ✓ Templates
│   ├── INDEX.md ......................... ✓ Navigation
│   └── README.md ........................ ✓ Overview
│
└── stock_prediction_project/
    ├── copilot-instructions.md .......... ✓ Project rules
    ├── main.py .......................... ✓ Entry point
    ├── config.py ........................ ✓ Configuration
    └── models/
        ├── lstm_model.py ............... ✓ LSTM (LOCKED)
        └── transformer_model.py ........ ✓ Transformer (NEW)
```

### Step 3: Verify Activation Markers

Check each file for activation statement:

```bash
# Must contain:
grep -l "ACTIVATED" Context/*.md
grep -l "MANDATORY" Context/*.md
grep -l "✅ ACTIVE" Context/*.md
```

All files marked as active? → Continue to Step 4

### Step 4: Test Agent Compliance

Ask any agent to verify rules:

**Test Prompt:**
```
What are the 5 MANDATORY rules I must follow for any code change?
```

**Expected Response:**
```
The 5 mandatory rules are:
1. Minimal Change Principle (Rule 1)
2. No Blind Fix Loop (Rule 2)  
3. Preserve Working Code (Rule 3)
4. Explicit Scope Requirement (Rule 5)
5. Respect File Boundaries (Rule 8)

[Plus references to Context files]
```

If agent provides correct answer? → System is active ✅

---

## Default Activation

The system is **AUTOMATICALLY ACTIVE** by default for:

- ✅ GitHub Copilot (when reading context files)
- ✅ Claude Code (when working in workspace)
- ✅ Any AI agent (when context files are loaded)
- ✅ All code modification tasks
- ✅ All automation requests
- ✅ All feature additions

**No special activation required** - files themselves enforce compliance.

---

## How Agents Use These Files

### On First Request

Agent reads files in order:
1. **README.md** or **QUICK_REFERENCE.md** (quick overview)
2. **OPERATIONS_CHECKLIST.md** (pre-operation steps)
3. **AGENT_RULES.md** (detailed rules as needed)

### Before Code Change

Agent follows **OPERATIONS_CHECKLIST.md**:
1. Pre-operation verification
2. Write CHANGE PLAN
3. Check locked files
4. Verify compliance
5. Execute changes
6. Post-operation report

### On Error/Ambiguity

Agent refers to **SYSTEM_ENFORCEMENT.md**:
1. Identifies escalation condition
2. Stops after 2 attempts
3. Provides clear error report
4. Waits for user guidance

### Response Format

Agent uses **AGENT_PROMPT_TEMPLATE.md**:
- Consistent formatting
- Clear status updates
- Predictable structure
- Easy to verify compliance

---

## Enforcement Mechanisms

### Mandatory Rule Enforcement
These 6 rules CANNOT be bypassed:
```
✅ Rule 1: Minimal Change
✅ Rule 2: No Blind Loop  
✅ Rule 3: Preserve Code
✅ Rule 5: Explicit Scope
✅ Rule 8: File Boundaries
✅ Rule 9: Backward Compat
```

### Optional Rule Override
User can override with:
```
OVERRIDE RULE [N]: [reason]
```

Example:
```
OVERRIDE RULE 1: I need full file rewrite for architectural change
```

### Protected Files
Cannot be modified without explicit instruction:
- config.py
- requirements.txt
- .env
- Dataset files
- models/lstm_model.py

### Verification Steps
Before every change:
1. Document target file
2. Document target function
3. Specify change type
4. Write CHANGE PLAN
5. Verify no locked files
6. Check rule compliance
7. Execute changes
8. Report results

---

## Monitoring & Verification

### Daily Verification

```bash
# Verify rules are still active
grep "ACTIVATED\|MANDATORY\|✅ ACTIVE" Context/*.md | wc -l

# Should return: Multiple matches (7+ files with activation markers)
```

### Weekly Review

```bash
# Check that copilot-instructions.md exists
test -f stock_prediction_project/copilot-instructions.md

# Verify no files were accidentally modified
git status Context/

# Should show: No modifications (or only expected changes)
```

### Monthly Audit

- [ ] All 7 context files present and current
- [ ] copilot-instructions.md in project folder
- [ ] Activation markers present in all files
- [ ] No protected files accidentally modified
- [ ] All agent responses follow template format
- [ ] No rule violations in recent changes

---

## Maintenance Tasks

### Update Rules (When Needed)

**If updating a rule:**
1. Edit Context/AGENT_RULES.md
2. Update Context/QUICK_REFERENCE.md (if applies)
3. Update Context/OPERATIONS_CHECKLIST.md (if applies)
4. Update timestamp in all files
5. Verify deployment

**If adding a new rule:**
1. Add to Context/AGENT_RULES.md (Rule 21+)
2. Add to QUICK_REFERENCE.md table
3. Update SYSTEM_ENFORCEMENT.md if mandatory
4. Update timestamp
5. Notify users of new rule

### Archive Old Versions

```bash
# Keep in _archive subfolder
Context/_archive/
├── AGENT_RULES_v1.0.md (2026-01-15)
├── AGENT_RULES_v1.1.md (2026-03-20)
└── AGENT_RULES_v1.2.md (2026-04-23) ← Current
```

---

## Troubleshooting

### "Agent is not following rules"

**Check:**
1. Are context files in the workspace?
   ```bash
   test -f Context/AGENT_RULES.md
   ```
2. Does agent reference context files?
   - Ask: "What rules must you follow?"
   - If no mention of rules → Files not loaded

3. Are files properly formatted?
   ```bash
   grep "ACTIVATED" Context/*.md
   ```
   - If no matches → Files may be corrupted

**Fix:**
- Ensure all files exist
- Check file formatting (UTF-8 encoding)
- Have agent read specific file explicitly
- Test with: "Read Context/QUICK_REFERENCE.md"

### "Agent modifies locked files"

**Check:**
1. Is QUICK_REFERENCE.md listing locked files?
2. Does copilot-instructions.md mention file boundaries?
3. Did agent see the restrictions?

**Fix:**
- Have agent re-read QUICK_REFERENCE.md
- Show agent specific rule: "Show Rule 8: File Boundaries"
- Ask before each change: "Is this file locked?"

### "Agent doesn't output CHANGE_PLAN"

**Check:**
1. Is OPERATIONS_CHECKLIST.md accessible?
2. Did agent read pre-operation section?

**Fix:**
- Ask directly: "Output CHANGE_PLAN before proceeding"
- Reference template: "Use Context/AGENT_PROMPT_TEMPLATE.md"
- Have agent re-read OPERATIONS_CHECKLIST.md

### "Agent keeps retrying after 2 failures"

**Check:**
1. Is Rule 2 clear?
2. Did agent reference OPERATIONS_CHECKLIST.md error section?

**Fix:**
- Quote Rule 2 directly
- Ask: "What does Rule 2 say about failed attempts?"
- Show section: SYSTEM_ENFORCEMENT.md (escalation rules)

---

## Success Indicators

### Agent is Following Rules If:

✅ Outputs CHANGE_PLAN before modifications
✅ Mentions rule files in responses
✅ Stops after 2 failed attempts
✅ Avoids modifying locked files
✅ Preserves existing functions
✅ Makes minimal changes only
✅ Asks for clarification on ambiguous requests
✅ Uses template format for responses
✅ Reports changes clearly
✅ Respects backward compatibility

### System is Properly Deployed If:

✅ All 7 context files exist
✅ Files contain activation markers
✅ Files are readable and properly formatted
✅ Rules are enforced consistently
✅ Agents reference context files
✅ Protected files remain untouched
✅ Changes are minimal and targeted
✅ Backup/archive system in place
✅ Audit trail maintained
✅ Monthly reviews completed

---

## Emergency Procedures

### If Rules Are Not Being Followed

1. **STOP** - Do not proceed with changes
2. **VERIFY** - Check that context files exist
3. **REMIND** - Show agent the specific rule
4. **RELOAD** - Ask agent to re-read context files
5. **TEST** - Ask rule question to verify understanding
6. **PROCEED** - Only after compliance verified

### If Files Get Corrupted

```bash
# Restore from backup or git
git checkout Context/AGENT_RULES.md
git checkout Context/SYSTEM_ENFORCEMENT.md
# etc.

# Or re-create from this guide
```

### If New Agent Doesn't Know Rules

1. Attach all context files to conversation
2. Ask agent: "Read Context/QUICK_REFERENCE.md"
3. Test with: "What are the mandatory rules?"
4. Proceed only after correct answer

---

## Documentation Links

- **Getting Started:** Context/INDEX.md
- **Quick Rules:** Context/QUICK_REFERENCE.md
- **Step-by-Step:** Context/OPERATIONS_CHECKLIST.md
- **Full Details:** Context/AGENT_RULES.md
- **Enforcement:** Context/SYSTEM_ENFORCEMENT.md
- **Templates:** Context/AGENT_PROMPT_TEMPLATE.md
- **Project Rules:** stock_prediction_project/copilot-instructions.md

---

## Contact & Support

**Questions about rules?**
→ See: Context/QUICK_REFERENCE.md

**Need detailed explanation?**
→ See: Context/AGENT_RULES.md

**Don't know what to do?**
→ See: Context/OPERATIONS_CHECKLIST.md

**Quick lookup?**
→ See: Context/INDEX.md

**Need full understanding?**
→ Read all files in order listed in INDEX.md

---

## Deployment Checklist

- [ ] All 7 context files created
- [ ] All files contain activation markers
- [ ] Project rules file created (copilot-instructions.md)
- [ ] File structure verified
- [ ] Test agent comprehension
- [ ] Test locked file protection
- [ ] Test CHANGE_PLAN output
- [ ] Test error handling
- [ ] Backup system in place
- [ ] Archive folder ready (_archive)
- [ ] Monthly review schedule set
- [ ] Team notified of new system

All items checked? → **System is READY for deployment** ✅

---

**Deployment Date:** 2026-04-23
**System Version:** 1.0
**Status:** ✅ READY
**Last Updated:** 2026-04-23
