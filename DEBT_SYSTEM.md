# Dynamic Debt Capacity System

## Overview

The game now features a realistic, dynamic debt capacity system that makes debt management a core strategic element. Players start with minimal capital and must leverage their reputation and net worth to access debt financing.

---

## Key Changes

### 1. Minimal Starting Capital
```python
STARTING_CAPITAL = $2,000,000  # Down from $10M
```

**Impact:**
- Most acquisitions require debt financing
- Forces players to carefully manage leverage
- Creates realistic progression from bootstrapping to scaling

### 2. Dynamic Debt Capacity Formula

Debt capacity is no longer static. It's calculated each time based on:

```python
debt_capacity = base_capacity + (net_worth × leverage_ratio × reputation_factor)
```

**Components:**
- **Base Capacity**: $10M (minimum access to capital markets)
- **Net Worth Multiplier**: 3.0x (can borrow up to 3x net worth)
- **Reputation Factor**: 0.5 to 2.0 (scales with reputation)
- **Minimum Capacity**: $5M (floor to ensure playability)

### 3. Reputation Impact

Reputation now directly affects borrowing power:

| Reputation | Reputation Factor | Impact on Capacity |
|------------|------------------|-------------------|
| 0% (lowest) | 0.5x | Severely limited debt access |
| 50% | 1.25x | Moderate borrowing capacity |
| 100% (highest) | 2.0x | Maximum leverage available |

**Formula:**
```python
reputation_factor = 0.5 + (reputation × 1.5)
```

---

## Debt Capacity Examples

### Starting Position
```
Cash: $2,000,000
Net Worth: $2,000,000
Reputation: 100%
───────────────────────────
Debt Capacity: $22,000,000
  = $10M base
  + ($2M × 3.0 × 2.0)
  = $10M + $12M
  
Available Capital: $24,000,000
```

### After First Successful Deal
```
Cash: $5,000,000
Portfolio Value: $8,000,000
Debt: $3,000,000
Net Worth: $10,000,000
Reputation: 100%
───────────────────────────
Debt Capacity: $70,000,000
  = $10M base
  + ($10M × 3.0 × 2.0)
  = $10M + $60M

Available Capital: $72,000,000
```

### After Building Track Record
```
Cash: $15,000,000
Portfolio Value: $35,000,000
Debt: $10,000,000
Net Worth: $40,000,000
Reputation: 100%
───────────────────────────
Debt Capacity: $250,000,000
  = $10M base
  + ($40M × 3.0 × 2.0)
  = $10M + $240M

Available Capital: $255,000,000
```

### With Damaged Reputation
```
Cash: $15,000,000
Portfolio Value: $35,000,000
Debt: $10,000,000
Net Worth: $40,000,000
Reputation: 50%
───────────────────────────
Debt Capacity: $160,000,000
  = $10M base
  + ($40M × 3.0 × 1.25)
  = $10M + $150M

Available Capital: $165,000,000
```

---

## Strategic Implications

### Early Game (Quarters 1-5)

**Challenge:** Limited capital forces careful selection
- Starting capital: $2M cash
- Available capital: ~$24M (with $22M debt capacity)
- Can afford: 1-2 small businesses with heavy leverage

**Strategy:**
- Target smallest businesses ($1-3M valuations)
- Use 70-90% debt financing
- Focus on stable cash flow to service debt
- Avoid risky bets early - damaged reputation hurts severely

**Key Metrics to Watch:**
- Debt utilization (try to stay under 50% early on)
- Quarterly interest payments (ensure positive cash flow)
- Net worth growth (drives future capacity)

### Mid Game (Quarters 6-12)

**Opportunity:** Growing capacity enables larger deals
- As net worth grows, debt capacity multiplies
- Successful exits recycle capital
- Reputation maintained = maximum leverage

**Strategy:**
- Scale into larger acquisitions ($5-15M range)
- Use mix of equity and debt (40-60% debt)
- Consider refinancing old deals
- Build portfolio of 4-6 companies

### Late Game (Quarters 13-20)

**Power:** Significant leverage available
- Net worth of $30-50M+ unlocks $200M+ capacity
- Can pursue roll-up strategies
- Multiple simultaneous acquisitions possible

**Strategy:**
- Optimize exits before game end
- Max out leverage on final acquisitions
- Focus on IRR maximization
- Time exits to market cycles

---

## Reputation Management

### How Reputation Changes

**Positive Factors:**
- Successful exits at good multiples: +2-5%
- Clean operational record: +1% per year
- Portfolio company performance: +0.5% per breakthrough

**Negative Factors:**
- Failed negotiations: -2% per walkaway
- Company crises: -3-5% per major crisis
- Debt defaults: -10% (if implemented)
- Management conflicts: -1-3%

### Reputation Strategy

**Protect Your Reputation:**
1. **Honor Commitments** - Don't walk away from too many deals
2. **Manage Actively** - Address crises immediately
3. **Build Track Record** - Successful exits build credibility
4. **Service Debt** - Never miss interest payments

**Recovery from Low Reputation:**
- Takes time (8-12 quarters typically)
- Requires consistent performance
- Focus on smaller, safer deals
- Avoid risky leverage until reputation recovers

---

## Debt Utilization Tracking

### New UI Elements

**Main Menu Display:**
```
Debt: $8,000,000 / $22,000,000 (36% utilized)
```

**Player Summary:**
```
Debt:            $8,000,000
Debt Capacity:   $22,000,000
Debt Utilization: 36.4%
```

### Utilization Thresholds

| Utilization | Risk Level | Recommendation |
|-------------|-----------|----------------|
| 0-30% | Low | Safe to take more debt |
| 31-60% | Moderate | Balanced position |
| 61-80% | High | Consider paying down |
| 81-100% | Critical | At max capacity |

---

## Mathematical Details

### Debt Capacity Calculation

```python
def get_debt_capacity(self) -> float:
    net_worth = self.compute_net_worth()
    
    # Reputation factor: 0.5 to 2.0
    reputation_factor = 0.5 + (self.reputation * 1.5)
    
    # Net worth capacity
    nw_capacity = max(0, net_worth) * 3.0 * reputation_factor
    
    # Total capacity
    total = 10_000_000 + nw_capacity
    
    # Ensure minimum
    return max(5_000_000, total)
```

### Why This Works

1. **Scales with Success**: Growing net worth enables bigger deals
2. **Reputation Matters**: Protects downside of bad reputation
3. **Positive Feedback**: Success → Net Worth → Capacity → More Success
4. **Risk Management**: Over-leveraging hurts if deals go bad
5. **Realistic**: Mirrors real-world credit markets

---

## Configuration Options

All parameters can be tuned in `config.py`:

```python
STARTING_CAPITAL = 2_000_000           # Starting cash
BASE_DEBT_CAPACITY = 10_000_000        # Base credit line
DEBT_TO_NET_WORTH_RATIO = 3.0          # Leverage multiple
REPUTATION_DEBT_MULTIPLIER = 2.0       # Max reputation boost
MIN_DEBT_CAPACITY = 5_000_000          # Floor for capacity
```

**Suggested Difficulty Levels:**

**Easy Mode:**
```python
STARTING_CAPITAL = 5_000_000
BASE_DEBT_CAPACITY = 20_000_000
DEBT_TO_NET_WORTH_RATIO = 4.0
```

**Current (Balanced):**
```python
STARTING_CAPITAL = 2_000_000
BASE_DEBT_CAPACITY = 10_000_000
DEBT_TO_NET_WORTH_RATIO = 3.0
```

**Hard Mode:**
```python
STARTING_CAPITAL = 1_000_000
BASE_DEBT_CAPACITY = 5_000_000
DEBT_TO_NET_WORTH_RATIO = 2.0
```

---

## Tips for Success

### 1. Start Small, Grow Fast
- First deal: aim for $2-4M valuation
- Use 80% debt, 20% equity
- Build net worth quickly to unlock capacity

### 2. Manage Leverage Wisely
- Keep utilization under 60% when possible
- Leave room for opportunistic deals
- Don't max out early - leave buffer

### 3. Protect Reputation
- Reputation = Credit = Opportunity
- One bad reputation hit can severely limit capacity
- Worth paying extra to maintain good standing

### 4. Time Your Exits
- Exit winners to build net worth
- Recycle capital into new deals
- Use exit proceeds to pay down debt

### 5. Compound Capacity
- Net worth growth → Capacity growth → Bigger deals → More net worth
- Virtuous cycle is key to success
- One great early deal can unlock entire game

---

## Comparison to Old System

| Aspect | Old System | New System |
|--------|-----------|------------|
| Starting Cash | $10M | $2M |
| Debt Capacity | Static $200M | Dynamic $22M+ |
| First Deal | No debt needed | Debt required |
| Reputation Impact | Deal terms only | Debt capacity & terms |
| Late Game | Capacity limited | Capacity grows with success |
| Strategy Depth | Simple | Complex leverage management |

---

## Summary

The dynamic debt capacity system transforms the game from a simple investment simulator into a realistic leverage-based private equity game where:

✅ **Capital is Scarce** - Must earn every dollar of capacity  
✅ **Reputation Matters** - Bad decisions have lasting consequences  
✅ **Strategy Deepens** - Leverage management becomes core gameplay  
✅ **Success Compounds** - Winners can scale dramatically  
✅ **Risk Increases** - Over-leveraging can cripple your fund  

This creates a much more engaging and realistic PE experience!

