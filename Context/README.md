# Stock Price Prediction using Deep Learning

## Objective
This project predicts stock prices using deep learning models.

## Technologies
- Python
- PyTorch
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

## Dataset
Historical stock data including:
- Open
- High
- Low
- Close
- Volume

## Model
- LSTM neural network
- CNN
- Predict next day closing price

## Workflow

1. Load data
2. Preprocess data
3. Create sequences
4. Train model
5. Evaluate model
6. Visualize results

---

## ⚠️ AGENT RULES - MANDATORY FOR ALL OPERATIONS

**Status: ✅ ACTIVATED AND ENFORCED**

All AI agents (GitHub Copilot, Claude, Auto Agents, etc.) MUST follow the rules defined in:

- **AGENT_RULES.md** - 20 mandatory rules for all operations
- **Context/** - Contains enforcement rules and verification protocols

### Key Enforcement Points

1. **Minimal Changes Only** - Modify only required code sections
2. **No Blind Fixes** - Max 2 retry attempts, then STOP
3. **Preserve Working Code** - No unrequested optimization/refactoring
4. **Token Efficiency** - Prefer patches over rewrites
5. **Explicit Scope** - Document target file, function, exact change
6. **Respect File Boundaries** - Don't modify config.py, requirements.txt, .env
7. **Backward Compatibility** - Keep existing APIs and functions intact

### Before Every Code Change

Agents must output:
```
CHANGE PLAN:

Target file: [exact path]
Target function: [exact name]
Change type: [bug fix | feature | refactor]
Lines affected: [line range]
Risk level: [LOW | MEDIUM | HIGH]
```

If unclear or risk is HIGH: **STOP and report**

### Override Rules

User can bypass a rule with explicit instruction:
```
OVERRIDE RULE [N]: [reason]
```

Example:
```
OVERRIDE RULE 1: I need full file rewrite for architectural changes
```

**Without explicit override: all rules apply strictly.**

### Locked Files (No Modifications)

- ✅ `config.py`
- ✅ `requirements.txt`
- ✅ `.env` / environment files
- ✅ Dataset files
- ✅ `models/lstm_model.py` (existing working model)

### Flexible Files (Can Modify with Rules)

- ✅ `models/` - Add new model files
- ✅ `training/` - Add new training functions
- ✅ `main.py` - Add model selection logic
- ✅ `utils/` - Add new utilities

### Quick Reference: 20 Core Rules

| # | Rule | Enforcement |
|---|------|---|
| 1 | Minimal Change | ⚠️ CRITICAL |
| 2 | No Blind Loop | ⚠️ CRITICAL |
| 3 | Preserve Code | ⚠️ CRITICAL |
| 5 | Explicit Scope | ⚠️ CRITICAL |
| 8 | File Boundaries | ⚠️ CRITICAL |
| 9 | Backward Compat | ⚠️ CRITICAL |
| 4 | Token Efficiency | Required |
| 6 | No Refactoring | Required |
| 7 | Maintain APIs | Required |
| 10+ | Others | All required |

**Read AGENT_RULES.md for complete details.**