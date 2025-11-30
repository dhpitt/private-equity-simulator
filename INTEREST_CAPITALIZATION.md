# Interest Capitalization System

## Overview

When you can't afford to pay quarterly debt interest, the unpaid amount is automatically **capitalized into your debt** rather than causing a game over. This creates a realistic debt spiral mechanic.

---

## How It Works

### Quarterly Interest Payment

Every quarter, interest is calculated on your outstanding debt:

```python
quarterly_interest = total_debt × (annual_rate / 4)
```

**Example:** $50M debt at 7% annual rate = $875K quarterly interest

### Three Scenarios

#### 1. Can Afford Full Payment (Normal)

```
Cash: $10,000,000
Debt: $50,000,000
Interest Due: $875,000

Result:
✓ Pay $875,000 from cash
  Cash: $9,125,000
  Debt: $50,000,000 (unchanged)
```

#### 2. Can Afford Partial Payment

```
Cash: $500,000
Debt: $50,000,000
Interest Due: $875,000

Result:
✓ Pay $500,000 from cash
✓ Capitalize $375,000 into debt
⚠️ Reputation -2%

  Cash: $0
  Debt: $50,375,000
```

#### 3. Cannot Afford Any Payment

```
Cash: $0
Debt: $50,000,000
Interest Due: $875,000

Result:
✓ Capitalize all $875,000 into debt
⚠️ Reputation -2%

  Cash: $0
  Debt: $50,875,000
```

---

## Consequences

### Debt Spiral

Unpaid interest compounds your debt:

**Quarter 1:**
- Debt: $50M
- Interest: $875K
- Can't pay → Debt becomes $50.875M

**Quarter 2:**
- Debt: $50.875M
- Interest: $890K (more!)
- Can't pay → Debt becomes $51.765M

**Quarter 3:**
- Debt: $51.765M
- Interest: $906K (even more!)
- Can't pay → Debt becomes $52.671M

This can spiral out of control if cash flow remains negative!

### Reputation Impact

Each time you miss an interest payment:
- **Reputation decreases by 2%**
- Lower reputation = lower debt capacity
- Creates a vicious cycle

**Example:**
```
Start: 100% reputation → $130M debt capacity
Miss 1 payment: 98% reputation → $127M debt capacity  
Miss 5 payments: 90% reputation → $117M debt capacity
Miss 10 payments: 80% reputation → $104M debt capacity
```

---

## Strategic Implications

### Cash Management is Critical

You need positive cash flow to service debt:

**Healthy Portfolio:**
```
Q1: Generate $2M operating income
    Pay $875K interest
    Remaining: $1.125M (good!)
```

**Distressed Portfolio:**
```
Q1: Generate $0 operating income
    Owe $875K interest
    Shortfall: -$875K (BAD!)
```

### Leverage Limits

The system naturally limits over-leveraging:
- Miss payments → Debt grows
- Debt grows → Interest grows
- Interest grows → Harder to pay
- More missed payments → Reputation falls
- Lower reputation → Can't take more debt

### Recovery Strategies

If caught in a debt spiral:

1. **Emergency Exit**: Sell a company to raise cash
2. **Cost Cutting**: Improve margins on all companies
3. **Pray for Events**: Hope for positive market events
4. **Ride It Out**: Wait for companies to grow into debt

---

## In-Game Display

When you can't afford interest:

```
======================================================================
QUARTERLY INTEREST PAYMENT
======================================================================

Interest Due: $875,000
Your Cash: $500,000

You paid $500,000 from available cash.

⚠️  Insufficient cash! $375,000 in unpaid interest added to debt.
Total debt is now $50,375,000

📉 Reputation decreased by 2% for missing interest payment (now 98%)
======================================================================
```

---

## Comparison to Alternatives

### Why Not Game Over?

**Alternative 1: Instant Failure**
```
"You can't pay interest. Game Over!"
→ Too harsh, kills gameplay
```

**Alternative 2: Forced Asset Sales**
```
"Selling your best company to pay interest..."
→ Removes player agency
```

**Alternative 3: Capitalization (Current)**
```
"Interest added to debt. Spiral begins..."
→ Realistic, gives player chance to recover
→ Natural penalty through growing debt
→ Can still lead to eventual failure
```

### Real-World Parallel

This mirrors **Payment-in-Kind (PIK) debt** used in actual PE deals:
- If cash flow insufficient, interest "toggles" to PIK
- Interest added to principal
- Common in distressed/highly-leveraged situations
- Creates compound interest effect

---

## Example Scenarios

### Scenario 1: Overleveraged Early

**Q1:** Buy $10M company with $9M debt
- Cash: $0
- Debt: $9M
- Companies haven't generated income yet

**Q2:** Interest due: $158K
- Can't pay → Debt becomes $9.158M
- Reputation: 98%

**Q3:** Interest due: $160K
- Still no income → Debt becomes $9.318M
- Reputation: 96%

**Q4:** Companies perform well!
- Generate $500K operating income
- Pay $163K interest
- Remaining: $337K
- **Recovery begins!**

### Scenario 2: Market Crash

**Q8:** Portfolio was doing well
- Cash: $5M
- Debt: $30M

**Q9:** Market crash! Companies lose value
- Interest: $525K (can still pay)
- But portfolio value dropped 20%

**Q10:** Still recovering
- Cash: $1M
- Interest: $525K (can still pay)

**Q11:** Second bad quarter
- Cash: $100K
- Interest: $525K
- Can't pay → Debt spiral begins

### Scenario 3: Death Spiral

Player aggressively leverages with poor cash flow:

**Q5:** 
- Debt: $80M
- Interest: $1.4M/quarter
- Operating income: $500K/quarter
- Shortfall: -$900K

**Q6-Q10:** Missing $900K every quarter
- Debt grows $900K per quarter
- By Q10: Debt = $84.5M
- Interest now $1.48M
- Shortfall growing!

**Q15:** Debt = $95M, still growing
- Debt capacity maxed out
- Can't take more debt
- Must sell companies at fire-sale prices

---

## Configuration

Interest rates set in `config.py`:

```python
BASE_INTEREST_RATE = 0.05  # 5% base
DEBT_INTEREST_RATE_SPREAD = 0.02  # +2% for leverage

# Total debt rate = 7% annual
```

Reputation penalty:
```python
# In engine.py
self.player.adjust_reputation(-0.02)  # -2% per missed payment
```

---

## Tips for Players

### Avoid the Spiral

1. **Don't over-leverage early**: Leave cash buffer
2. **Build cash flow**: Buy profitable companies
3. **Monitor debt service**: Know your quarterly interest
4. **Keep reputation high**: Protects debt capacity
5. **Plan exits**: Sell before crisis hits

### If Caught in Spiral

1. **Immediate triage**: Sell worst-performing company
2. **Aggressive cost-cutting**: Improve all margins
3. **Stop acquisitions**: No new debt until stable
4. **Ride it out**: Growth may save you
5. **Accept failure**: Sometimes best to restart

---

## Summary

The interest capitalization system creates **realistic leverage dynamics**:

✅ **No instant game over** - gives chance to recover  
✅ **Natural consequences** - debt compounds  
✅ **Reputation impact** - limits future borrowing  
✅ **Realistic mechanic** - mirrors PIK debt  
✅ **Strategic depth** - cash management matters  
✅ **Recovery possible** - not automatic failure  

Leverage is powerful but dangerous. Manage your cash flow!

---

**Version**: 2.3  
**Added**: November 29, 2025  
**Feature**: Interest Capitalization  
**Impact**: High-stakes debt management

