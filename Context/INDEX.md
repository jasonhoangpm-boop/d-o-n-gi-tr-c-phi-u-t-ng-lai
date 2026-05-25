# CONTEXT INDEX - Complete Guide to Agent Rules

**File:** Context/INDEX.md
**Purpose:** Guide to all agent rule files and how to use them
**Status:** ✅ ACTIVE

---

## Files in Context Folder

### 1. **AGENT_RULES.md** (Master Rules File)
**What it contains:** 20 comprehensive rules for all agent operations

**When to use:**
- Before making ANY code changes
- Need full rule details
- Understanding specific rule requirements

**Key Sections:**
- Rules 1-20 with explanations
- Specific examples for each rule
- Failure handling procedures
- Default SAFE_PATCH_MODE enabled

**Read:** All 20 rules, especially CRITICAL ones (1, 2, 3, 5, 8, 9)

---

### 2. **SYSTEM_ENFORCEMENT.md** (Activation & Configuration)
**What it contains:** Global activation settings and enforcement mechanisms

**When to use:**
- Understanding how rules are enforced
- Learning enforcement matrix
- Checking agent-specific procedures

**Key Sections:**
- Global activation rules
- Mandatory vs optional rules
- Verification protocol (4-step process)
- Escalation rules (STOP conditions)
- Testing enforcement

**Read:** At least ACTIVATION and VERIFICATION PROTOCOL sections

---

### 3. **OPERATIONS_CHECKLIST.md** (Step-by-Step Checklist)
**What it contains:** Detailed checklist for every operation

**When to use:**
- Before starting ANY code modification
- Need to verify compliance
- Troubleshooting operations

**Key Sections:**
- Pre-operation checklist
- CHANGE PLAN template (required)
- During operation checklist
- Post-operation checklist
- Error handling checklist
- Special scenarios (adding models, bug fixes, features)
- Quick decision tree

**Read:** Pre-operation checklist before EVERY operation

---

### 4. **QUICK_REFERENCE.md** (Quick Lookup)
**What it contains:** Summary of rules for quick reference

**When to use:**
- Need quick rule lookup
- Can't remember specific rules
- Want rule summary with examples
- Need common operations guide

**Key Sections:**
- 3 core rules (most important)
- All 20 rules in table format
- Locked vs flexible files
- Common operations (correct vs wrong)
- Token efficiency tips
- Quick decision points

**Read:** When you need fast answers

---

### 5. **README.md** (Project Overview + Rules)
**What it contains:** Project description + agent rules summary

**When to use:**
- First time understanding project + rules
- Need project context
- Overview of enforcement

**Key Sections:**
- Stock prediction project description
- MANDATORY RULES section
- Before every code change requirements
- Locked vs flexible files
- Quick reference table

**Read:** If you're new to the project

---

## How to Use These Files

### Scenario 1: Starting a New Task
```
1. Read: QUICK_REFERENCE.md (3 core rules)
2. Read: OPERATIONS_CHECKLIST.md (pre-operation)
3. Write: CHANGE PLAN
4. Read: AGENT_RULES.md (relevant rules)
5. Proceed with VERIFICATION CHECKLIST
```

### Scenario 2: Making Code Changes
```
1. Read: OPERATIONS_CHECKLIST.md (pre-operation)
2. Write: CHANGE PLAN
3. Check: Locked files NOT included
4. Run: VERIFICATION CHECKLIST
5. Execute: Changes with minimal modification
6. Use: OPERATIONS_CHECKLIST.md (post-operation)
```

### Scenario 3: Debugging an Error
```
1. Read: AGENT_RULES.md (Rule 2: No Blind Loop)
2. Read: OPERATIONS_CHECKLIST.md (error handling)
3. Attempt: Fix (1st time)
4. If fails: Try alternative (2nd time)
5. If still fails: STOP and report using SYSTEM_ENFORCEMENT.md format
```

### Scenario 4: Need Rule Override
```
1. Read: SYSTEM_ENFORCEMENT.md (rule override section)
2. User: Explicitly states OVERRIDE RULE [N]: [reason]
3. Confirm: User has acknowledged consequences
4. Proceed: With override applied
```

### Scenario 5: Adding New Feature
```
1. Read: OPERATIONS_CHECKLIST.md (special scenarios)
2. Read: AGENT_RULES.md (Rule 9: Backward compatibility)
3. Design: Keep old code intact
4. Create: New files/functions only
5. Update: Imports minimally
```

---

## Rule Categories & Files

### For MANDATORY Rules (Cannot Bypass)
- Read: AGENT_RULES.md (Rules 1, 2, 3, 5, 8, 9)
- Verify: SYSTEM_ENFORCEMENT.md (mandatory section)
- Check: OPERATIONS_CHECKLIST.md (verification section)

### For Error Handling
- Read: AGENT_RULES.md (Rule 2)
- Use: SYSTEM_ENFORCEMENT.md (escalation rules)
- Follow: OPERATIONS_CHECKLIST.md (error handling)

### For Code Modifications
- Use: OPERATIONS_CHECKLIST.md (pre/during/post-operation)
- Reference: QUICK_REFERENCE.md (common operations)
- Details: AGENT_RULES.md (specific rules)

### For Decision Making
- Quick lookup: QUICK_REFERENCE.md (decision tree)
- Detailed: AGENT_RULES.md (full context)
- Checklist: OPERATIONS_CHECKLIST.md (verification)

---

## Reading Recommendations

### If You Have 2 Minutes
→ Read: QUICK_REFERENCE.md (3 core rules + decision tree)

### If You Have 5 Minutes
→ Read: OPERATIONS_CHECKLIST.md (pre-operation checklist)
→ Read: QUICK_REFERENCE.md (common operations)

### If You Have 15 Minutes
→ Read: OPERATIONS_CHECKLIST.md (all sections)
→ Read: SYSTEM_ENFORCEMENT.md (key sections)
→ Read: AGENT_RULES.md (critical rules 1, 2, 3, 5, 8, 9)

### If You Have 30+ Minutes
→ Read: All files in order:
1. README.md (project context)
2. QUICK_REFERENCE.md (rules overview)
3. OPERATIONS_CHECKLIST.md (detailed steps)
4. AGENT_RULES.md (complete rules)
5. SYSTEM_ENFORCEMENT.md (enforcement details)

---

## File Relationships

```
README.md ←─→ Project overview + rules summary
                ↓
QUICK_REFERENCE.md ←─→ Fast lookup, decision tree
                ↓
OPERATIONS_CHECKLIST.md ←─→ Step-by-step guide
                ↓
AGENT_RULES.md ←─→ Complete 20 rules
                ↓
SYSTEM_ENFORCEMENT.md ←─→ Implementation details
```

---

## Troubleshooting Guide

### "Which rule applies to my situation?"
→ Use: QUICK_REFERENCE.md (table of all rules)
→ Then: Read specific rule in AGENT_RULES.md

### "What should I do before modifying code?"
→ Use: OPERATIONS_CHECKLIST.md (pre-operation section)
→ Print and check off all items

### "How do I override a rule?"
→ Read: SYSTEM_ENFORCEMENT.md (rule override section)
→ Request: User must explicitly state override

### "What happens if my fix fails twice?"
→ Read: AGENT_RULES.md (Rule 2: No Blind Loop)
→ Use: SYSTEM_ENFORCEMENT.md (escalation format)
→ STOP and report error

### "Can I modify config.py?"
→ Answer: NO (unless explicit override)
→ Read: QUICK_REFERENCE.md (locked files)
→ Details: AGENT_RULES.md (Rule 8)

### "Can I refactor existing code?"
→ Answer: NO (unless explicitly requested)
→ Read: AGENT_RULES.md (Rule 3, 6)
→ Use: QUICK_REFERENCE.md (common mistakes)

---

## File Update Schedule

| File | Last Updated | Update Frequency |
|------|--------------|------------------|
| AGENT_RULES.md | 2026-04-23 | Monthly review |
| SYSTEM_ENFORCEMENT.md | 2026-04-23 | Quarterly |
| OPERATIONS_CHECKLIST.md | 2026-04-23 | Quarterly |
| QUICK_REFERENCE.md | 2026-04-23 | Quarterly |
| README.md | 2026-04-23 | As needed |
| INDEX.md (this) | 2026-04-23 | Quarterly |

---

## How Each Tool Should Use These Files

### GitHub Copilot
1. Read all files at conversation start
2. Output CHANGE PLAN for each modification
3. Refer to OPERATIONS_CHECKLIST.md
4. Stop and ask if ambiguous

### Claude Code
1. Load context from all files
2. Follow SYSTEM_ENFORCEMENT.md protocol
3. Use multi-tool approach for efficiency
4. Report using specified format

### Auto Agents (n8n, etc.)
1. Check rule file before each operation
2. Validate against enforcement matrix
3. Apply constraints automatically
4. Escalate HIGH risk to human

### Any Other Agent
1. Read all 5 files
2. Follow mandatory rules (1, 2, 3, 5, 8, 9)
3. Use OPERATIONS_CHECKLIST.md as guide
4. Refer to SYSTEM_ENFORCEMENT.md for edge cases

---

## Summary

| Need | Go To |
|------|-------|
| Quick rules | QUICK_REFERENCE.md |
| Step-by-step | OPERATIONS_CHECKLIST.md |
| All details | AGENT_RULES.md |
| Enforcement | SYSTEM_ENFORCEMENT.md |
| Project + rules | README.md |
| Navigation | This file (INDEX.md) |

---

## Final Checklist

Before working on any task:
- [ ] Read appropriate file(s) above
- [ ] Understand context
- [ ] Write CHANGE PLAN
- [ ] Verify no rule violations
- [ ] Execute with confidence

---

**Last Updated:** 2026-04-23
**Status:** ✅ ACTIVE
**All agents must review this index**
