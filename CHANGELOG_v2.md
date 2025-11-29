# Private Equity Simulator - v2.0 Update

## Major System Overhaul: Dynamic Debt Financing

This update transforms PE Simulator from a capital-rich investment game into a realistic leverage-driven private equity experience.

---

## 🎯 Core Changes

### 1. Minimal Starting Capital
- **Old**: $10,000,000 starting capital
- **New**: $2,000,000 starting capital
- **Impact**: Debt financing is now **required** for almost all acquisitions

### 2. Dynamic Debt Capacity
- **Old**: Static $200M debt capacity
- **New**: Calculated based on net worth and reputation
- **Formula**: `base_capacity + (net_worth × 3.0 × reputation_factor)`

### 3. Reputation-Based Credit Access
- **Old**: Reputation only affected deal terms
- **New**: Reputation directly controls debt capacity (0.5x to 2.0x multiplier)
- **Impact**: Protecting reputation is now critical for growth

---

## 📊 How It Works

### Starting Position
```
Cash:              $2,000,000
Net Worth:         $2,000,000
Reputation:        100%
Debt Capacity:     $22,000,000
Available Capital: $24,000,000
```

**What This Means:**
- Can afford businesses valued up to $24M (with full leverage)
- Typical first acquisition: $2-5M (using 50-90% debt)
- 1-2 deals possible before needing to build net worth

### Growth Trajectory

**After 5 Quarters (Successful Path):**
```
Cash:              $5,000,000
Portfolio Value:   $15,000,000
Debt:              $8,000,000
Net Worth:         $12,000,000
Debt Capacity:     $82,000,000
Available Capital: $79,000,000
```

**After 10 Quarters (Strong Performance):**
```
Cash:              $10,000,000
Portfolio Value:   $40,000,000
Debt:              $15,000,000
Net Worth:         $35,000,000
Debt Capacity:     $220,000,000
Available Capital: $215,000,000
```

### Reputation Impact Example

**100% Reputation:**
```
Net Worth: $20M → Debt Capacity: $130M
```

**50% Reputation (Damaged):**
```
Net Worth: $20M → Debt Capacity: $85M  (-45M capacity!)
```

---

## 🎮 Strategic Implications

### Early Game: Bootstrapping Phase
**Quarters 1-5**

**Challenges:**
- Severely limited capital
- High leverage requirement (70-90% debt)
- Must choose deals carefully

**Best Practices:**
- Target $1-3M valuations
- Focus on stable, cash-generating businesses
- Avoid risky sectors
- Protect reputation at all costs

**Example First Deal:**
```
Target: "Mom's Pizza" - $2.5M valuation
Structure: $500K equity + $2M debt (80% leverage)
Remaining capacity: $20M
```

### Mid Game: Scale-Up Phase
**Quarters 6-12**

**Opportunities:**
- Growing net worth unlocks capacity
- Can pursue larger deals ($5-15M)
- Portfolio of 4-6 companies possible

**Best Practices:**
- Mix of debt and equity (40-60% debt)
- Exit winners to recycle capital
- Maintain 40-60% debt utilization
- Consider roll-up strategies

### Late Game: Empire Building
**Quarters 13-20**

**Power Moves:**
- $200M+ capacity available
- Multiple simultaneous large deals
- Roll-up strategies viable

**Best Practices:**
- Maximize leverage for final acquisitions
- Time exits to market cycles
- Focus on IRR optimization
- Prepare for endgame valuation

---

## 🎓 Key Strategic Concepts

### 1. The Leverage Ladder
```
Success → Net Worth ↑ → Debt Capacity ↑ → Bigger Deals → More Success
```

One great early deal can unlock exponential growth.

### 2. Reputation as Currency
Your reputation is your credit line. Damage it and you're locked out of growth opportunities.

**Reputation Gains:**
- Successful exits: +2-5%
- Strong operations: +1%/year
- Clean track record: Multiplier protection

**Reputation Losses:**
- Deal walkways: -2%
- Company crises: -3-5%
- Management conflicts: -1-3%

### 3. Debt Utilization Management
| Range | Status | Action |
|-------|--------|--------|
| 0-30% | Under-leveraged | Seek opportunities |
| 31-60% | Balanced | Maintain position |
| 61-80% | High | Consider de-leveraging |
| 81-100% | Critical | Must pay down |

### 4. Capital Recycling
- Don't hoard exits in cash
- Immediately redeploy into new deals
- Use debt capacity to bridge timing
- Compound returns through velocity

---

## 💡 Pro Tips

### 1. Start with High-EBITDA Businesses
EBITDA generates cash to service debt. Target 20%+ margins.

### 2. Use the 50/50 Rule
In early game, try to stay near 50% debt utilization. Leaves room for opportunistic deals.

### 3. Protect Reputation Early
One reputation hit in Q1 can cripple your entire game. Be conservative early.

### 4. Time Your Exits
Exit businesses after improving them but before crises. Use proceeds to deleverage and reposition.

### 5. Know Your Capacity
Always know your current debt capacity. It changes every quarter with net worth.

### 6. Layer Your Debt
- Early deals: High leverage (70-90%)
- Later deals: Moderate leverage (40-60%)
- This creates safer overall portfolio

---

## 🔧 Configuration Options

Want different difficulty? Edit `config.py`:

**Current Settings (Balanced):**
```python
STARTING_CAPITAL = 2_000_000
BASE_DEBT_CAPACITY = 10_000_000
DEBT_TO_NET_WORTH_RATIO = 3.0
REPUTATION_DEBT_MULTIPLIER = 2.0
```

**Easier:**
```python
STARTING_CAPITAL = 5_000_000          # More starting cash
BASE_DEBT_CAPACITY = 20_000_000       # Higher base capacity
DEBT_TO_NET_WORTH_RATIO = 4.0         # More leverage allowed
```

**Harder:**
```python
STARTING_CAPITAL = 1_000_000          # Very tight start
BASE_DEBT_CAPACITY = 5_000_000        # Limited base
DEBT_TO_NET_WORTH_RATIO = 2.0         # Conservative leverage
```

---

## 📈 Example Winning Strategy

### Quarter 1-2: Bootstrap
```
Deal 1: $2.5M local business
- Structure: 80% debt ($2M)
- Focus: Cash flow stability
- Result: +$3M net worth after improvement
```

### Quarter 3-5: Build Track Record
```
Deal 2: $4M business (with grown capacity)
- Structure: 60% debt ($2.4M)
- Focus: Margin improvement opportunity
- Result: +$5M net worth

Deal 3: $3M add-on acquisition
- Structure: 70% debt ($2.1M)
- Focus: Synergies with Deal 2
```

### Quarter 6-10: Scale
```
Exit Deal 1: Sell at $6M (2.4x return)
- Proceeds: $6M - $2M debt = $4M net
- Use to partially deleverage

Deal 4-5: Two $8M businesses
- Structure: 50% debt each
- Capacity: Now $150M+ available
```

### Quarter 11-15: Empire
```
Roll-up strategy: 3 businesses at $12M each
- Total: $36M deployed
- Portfolio: 7 companies, $80M+ value
- Net worth: $50M+
- Capacity: $300M+
```

### Quarter 16-20: Harvest
```
Strategic exits: Sell 4-5 best performers
- Time exits to market booms
- Final net worth: $150M+
- Return: 75x on starting capital!
- Grade: S (Legendary)
```

---

## 🎯 Success Metrics

### New Grading Considers Leverage

| Grade | Multiple | Description | Typical Strategy |
|-------|----------|-------------|------------------|
| S | 75x+ | Legendary | Aggressive leverage, perfect timing |
| A | 50x+ | Excellent | Heavy leverage, strong execution |
| B | 30x+ | Very Good | Balanced leverage, consistent wins |
| C | 15x+ | Good | Conservative leverage, slow growth |
| D | 5x+ | Modest | Minimal debt use, safe plays |
| F | <5x | Loss | Overleveraged or poor deals |

Starting with $2M makes achieving 50x+ (Grade A) a significant challenge!

---

## 🔄 Migration Notes

### For Existing Players

If you have a saved game (future feature):
- Old saves will use new debt capacity formula
- Previous debt amounts are preserved
- Capacity recalculated based on current net worth
- May find yourself suddenly at high utilization!

### For New Players

This is now the default experience. The old $10M starting capital was too easy.

---

## 📚 Related Documentation

- `DEBT_SYSTEM.md` - Full technical details of debt mechanics
- `ENHANCEMENTS.md` - Other recent improvements
- `QUICKSTART.md` - Updated tutorial for new system
- `README.md` - General game overview

---

## 🎉 Summary

The dynamic debt system makes PE Simulator a **true private equity game**:

✅ **Leverage is Essential** - Not optional anymore  
✅ **Reputation Matters** - Your track record is your currency  
✅ **Strategy Deepens** - Capital allocation becomes critical  
✅ **Risk Increases** - Overleveraging can destroy your fund  
✅ **Success Compounds** - Winners can build true empires  

This is the PE experience we always wanted to create!

---

**Version**: 2.0.0  
**Release Date**: November 29, 2025  
**Compatibility**: All previous games compatible

