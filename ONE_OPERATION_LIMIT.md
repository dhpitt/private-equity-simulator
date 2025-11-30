# One Operation Per Quarter System

## Overview

You can only perform **ONE operation per company per quarter**. This creates strategic prioritization decisions and prevents you from "fixing" all companies at once.

---

## How It Works

### Operation Limit

Each portfolio company can receive **exactly one** operational improvement per quarter:
- Cost Cutting
- CapEx Investment  
- Management Replacement
- Growth Strategy Change

Once operated, the company is **locked** until next quarter.

### Visual Indicators

In the **Operate Portfolio Companies** menu:

```
PORTFOLIO OPERATIONS
======================================================================

Note: You can only perform ONE operation per company per quarter.
Companies already operated on this quarter are marked with ✗

Company                     Sector              Revenue    Valuation
--------------------------------------------------------------------------
✓ Tony's Pizza             Food & Beverage     $1.2M      $8.5M
✗ Bob's Auto Repair [OPERATED]  Auto Services   $800K      $5.2M
✓ Sunshine Dental          Healthcare          $2.5M      $15M

Select a company to operate on:
  1. ✓ Tony's Pizza
  2. ✗ Bob's Auto Repair [OPERATED]
  3. ✓ Sunshine Dental
  4. Back to Main Menu
```

**Legend:**
- ✓ = Can operate this quarter
- ✗ = Already operated this quarter

### Attempting to Re-Operate

If you try to select an already-operated company:

```
⚠️  Bob's Auto Repair has already been operated on this quarter!
Advance to the next quarter to operate on them again.

Press Enter to continue...
```

### All Companies Operated

If you've operated on all companies:

```
⚠️  All companies have been operated on this quarter!
Advance to the next quarter to operate on them again.
```

---

## Strategic Implications

### Prioritization Required

With a 5-company portfolio and limited operations:

**Q1 Priorities:**
1. ⚡ **Emergency**: Fix failing company first
2. 💰 **High ROI**: Improve best performer
3. 📈 **Growth**: Boost promising startup
4. 🔧 **Maintenance**: Other companies wait
5. ⏸️ **Deferred**: Will operate next quarter

You **cannot** optimize all 5 companies simultaneously!

### Quarterly Planning

**Example Portfolio (5 companies):**

**Q1 Plan:**
- Company A: Cost-cutting (needs margin boost) ✓
- Company B: Deferred (stable, can wait)
- Company C: Deferred (performing well)
- Company D: CapEx (growth opportunity) ✓
- Company E: Mgmt replacement (failing CEO) ✓

**Operated: 3/5 companies**

**Q2 Plan:**
- Company A: Locked (operated in Q1)
- Company B: Now can operate ✓
- Company C: Now can operate ✓
- Company D: Locked (operated in Q1)
- Company E: Locked (operated in Q1)

This creates a **rotation system** for improvements.

### Scale Matters

The system's impact grows with portfolio size:

**Small Portfolio (2-3 companies):**
- Can operate on most each quarter
- Less strategic tension

**Medium Portfolio (5-7 companies):**
- Must prioritize carefully
- Some companies always waiting
- Good strategic depth

**Large Portfolio (10+ companies):**
- Can only touch half per quarter
- Requires careful planning
- Some may wait 2-3 quarters

---

## Tactical Considerations

### Timing Operations

**When to operate:**

1. **Crisis Management**: Operate immediately on failing companies
2. **Pre-Exit**: Boost metrics before selling
3. **High Impact**: When operation will move the needle most
4. **Market Timing**: Align with favorable market conditions

**When to wait:**

1. **Stable Performance**: Company doing fine, others need help more
2. **Recent Acquisition**: Give time to settle before operating
3. **Market Uncertainty**: Wait for clarity before investing
4. **Resource Constraints**: Need cash for operations

### Operation Sequencing

**Optimal sequence across quarters:**

**Q1:** Cost-cutting on 3 companies (quick wins)
**Q2:** CapEx on the cost-cut companies (now have margins for it)
**Q3:** Management replacement on underperformers
**Q4:** Growth strategy changes for exits

### Emergency Response

If a company enters crisis mid-quarter:

**Problem:** Company B is failing but already operated on this quarter!

**Options:**
1. ⏭️ **Wait it Out**: Endure one bad quarter, fix next quarter
2. 💰 **Exit Now**: Sell before it gets worse
3. 🤞 **Hope**: Maybe random event will help

No quick fixes available!

---

## Impact on Portfolio Management

### Natural Scale Limits

The system creates **natural portfolio size limits**:

**Too Large:**
- Can't keep up with operations needed
- Companies deteriorate while waiting
- Performance suffers

**Optimal:**
- Can operate on critical companies each quarter
- Maintain strong performance
- Strategic without overwhelming

**Too Small:**
- Wasting operational capacity
- Not enough diversification
- Foregone growth opportunities

### Encourages Exits

Companies waiting for operations may be better sold:

```
Company E Situation:
- Waiting 3 quarters for operation slot
- Performance declining while waiting
- Other companies higher priority

Decision: Sell now rather than let deteriorate
```

### Specialist Strategies

Enables different management approaches:

**Hands-Off Investor:**
- Buy stable, high-quality companies
- Minimal operations needed
- Larger portfolio possible

**Active Operator:**
- Buy distressed companies
- Intensive operations
- Smaller portfolio required

**Growth Investor:**
- High-growth companies
- Frequent strategy adjustments
- Medium portfolio with rotation

---

## Technical Implementation

### Company Tracking

```python
class Company:
    def __init__(self):
        self.last_operation_quarter = None
        self.operations_this_quarter = 0
    
    def can_operate(self, current_quarter: int) -> bool:
        """Check if company can be operated on this quarter."""
        return self.last_operation_quarter != current_quarter
    
    def mark_operated(self, current_quarter: int) -> None:
        """Mark that an operation was performed."""
        if self.last_operation_quarter != current_quarter:
            self.operations_this_quarter = 0
        self.last_operation_quarter = current_quarter
        self.operations_this_quarter += 1
```

### Quarterly Reset

```python
def advance_quarter(self):
    """Advance to next quarter."""
    for company in self.player.portfolio:
        company.simulate_quarter(market_conditions)
        company.reset_quarterly_operations()  # Reset for new quarter
```

### Menu Filtering

```python
def portfolio_operations_menu(player, current_quarter):
    """Show portfolio with operation availability."""
    for company in player.portfolio:
        can_operate = company.can_operate(current_quarter)
        status = "✓" if can_operate else "✗"
        print(f"{status} {company.name} {'[OPERATED]' if not can_operate else ''}")
```

---

## Examples

### Example 1: Growing Portfolio

**Year 1, Q1:**
- Portfolio: 2 companies
- Operations: Both companies operated ✓
- Result: Easy to manage

**Year 2, Q1:**
- Portfolio: 5 companies
- Operations: 3 operated, 2 deferred
- Result: Starting to feel constraint

**Year 3, Q1:**
- Portfolio: 8 companies
- Operations: 4 operated, 4 waiting
- Result: Must prioritize carefully

**Year 4, Q1:**
- Portfolio: 12 companies
- Operations: 6 operated, 6 waiting
- Result: Some companies waiting 2 quarters

### Example 2: Crisis Management

**Q5 Portfolio State:**
- Company A: Strong (operated Q4) → Wait
- Company B: Good (operated Q3) → Wait  
- Company C: **FAILING** (not operated since Q2) → OPERATE NOW
- Company D: Okay → Maybe operate
- Company E: Okay → Maybe operate

**Decision:** Must operate on Company C immediately, even though others could also benefit.

### Example 3: Exit Preparation

**Q10 - Planning to exit Company B in Q11:**

**Current Quarter (Q10):**
1. Cost-cutting on Company B → Boost margins
2. Other companies wait

**Next Quarter (Q11):**
- Company B metrics look great
- Ready to sell at premium
- Other companies finally get operations

**Strategic use** of the operation slot!

---

## Balancing the System

### Why One Operation?

**Prevents:**
- ❌ Mass optimization each quarter
- ❌ "Fix everything" gameplay
- ❌ Unlimited scaling
- ❌ Trivial management

**Creates:**
- ✅ Meaningful choices
- ✅ Strategic prioritization
- ✅ Portfolio size tradeoffs
- ✅ Engaging gameplay

### Alternative Limits Considered

**No Limit:**
- Operate on all companies every quarter
- No strategic depth
- **Rejected**

**Multiple Operations:**
- 2-3 operations per company per quarter
- More complex but less impactful
- **Rejected**

**One Operation (Current):**
- Clean, understandable
- High strategic impact
- **Implemented**

---

## Pro Tips

### 1. Plan Ahead
Know which companies you'll operate on next quarter before advancing.

### 2. Rotate Focus
Don't neglect any company for too long - performance will suffer.

### 3. Batch Similar Operations
Do all cost-cutting in one quarter, all CapEx in another.

### 4. Emergency Reserve
Keep 1-2 operation "slots" free for unexpected crises.

### 5. Pre-Exit Optimization
Always operate on a company the quarter before selling it.

### 6. Track Waiting Time
Companies waiting 3+ quarters need attention or should be sold.

### 7. Quality Over Quantity
Better to have 5 well-managed companies than 10 neglected ones.

---

## Summary

The one-operation-per-quarter system creates **meaningful portfolio management**:

✅ **Strategic Prioritization** - Can't optimize everything at once  
✅ **Natural Scale Limits** - Portfolio size has real consequences  
✅ **Rotation Management** - Must cycle through companies  
✅ **Crisis Decisions** - Emergency response requires sacrifice  
✅ **Exit Timing** - Optimize companies before selling  
✅ **Realistic Constraints** - Even PE firms have limited bandwidth  

It transforms portfolio management from "optimize all" to "choose wisely."

---

**Version**: 2.4  
**Added**: November 29, 2025  
**Feature**: Operation Limits  
**Impact**: Strategic depth for portfolio management

