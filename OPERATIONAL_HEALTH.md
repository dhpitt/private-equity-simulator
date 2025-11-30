# Operational Health System

## Overview

Companies now have an **Operational Health** metric (0-100%) that represents the long-term viability and strength of their operations. This creates strategic tension between short-term profit maximization and long-term sustainability.

---

## How It Works

### Initial Health

Companies start with **varied health** based on their fundamentals:

**Formula:**
```python
Base = 50% + (Manager Competence × 40%)
Margin Bonus = (EBITDA Margin - 10%) × 50%
Growth Bonus = max(0, Growth Rate) × 200%
Random = ±5%

Initial Health = Base + Bonuses (clamped to 50-100%)
```

**Examples:**
```
Excellent Company:
  Manager: 90% competent
  Margin: 30%
  Growth: +5%
  → Health: 95-100%

Average Company:
  Manager: 60% competent
  Margin: 20%
  Growth: +2%
  → Health: 75-85%

Struggling Company:
  Manager: 40% competent
  Margin: 12%
  Growth: -1%
  → Health: 50-60%
```

### Health Changes Over Time

**DAMAGES Health:**
1. **Cost-Cutting** (up to -25% per action)
   - Moderate (50%): -7.5% health
   - Aggressive (70%): -17.5% health
   - Extreme (90%): -22.5% health

**IMPROVES Health:**
1. **CapEx Investment** (up to +15%)
   - Based on investment/revenue ratio
   - $1M into $2M revenue company: +5% health

2. **Growth Strategies** (varies by type)
   - Roll-up: +5% to +12% health
   - Expansion: +3% to +8% health
   - Diversification: +2% to +6% health

3. **Management Replacement** (up to +20%)
   - Only if new manager is better
   - Proportional to competence improvement

4. **Natural Recovery** (+1% per quarter)
   - Gradual healing if left alone
   - Takes 20 quarters to fully recover from severe damage

---

## Effects of Low Health

### Performance Impact

Low health affects company performance during quarterly simulation:

**Growth Penalty:**
```
Health 100%: No penalty
Health 70%:  -15% growth multiplier
Health 50%:  -25% growth multiplier  
Health 30%:  -35% growth multiplier
```

**Increased Volatility:**
```
Health < 70%: Volatility increases
  - More likely to have bad quarters
  - Less predictable performance
  - Higher downside risk
```

**Example:**
```
Company with 40% health:
  Base Growth: +5% per quarter
  Health Penalty: -30% (reduces to +3.5%)
  Volatility: 2x normal (more swings)
  
→ Grows slower and less reliably
```

### Visual Indicators

**Portfolio Display:**
```
Portfolio Companies
┏━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ # ┃ Name     ┃ Return ┃ Health ┃
┃ 1 ┃ Pizza    ┃ +50.0% ┃    95% ┃  ← Green (Healthy)
┃ 2 ┃ Tech     ┃ +10.0% ┃    55% ┃  ← Yellow (Degraded)
┃ 3 ┃ Retail   ┃ -25.0% ┃  35% ⚠️ ┃  ← Red (Critical!)
```

**Color Coding:**
- 🟢 **Green (80-100%)**: Healthy operations
- 🟡 **Yellow (60-80%)**: Degraded but manageable
- 🟠 **Orange (40-60%)**: Concerning, needs attention
- 🔴 **Red (<40%)**: Critical condition with ⚠️ warning

---

## Strategic Implications

### The Cost-Cutting Dilemma

**Short-term thinking:**
```
Q1: Aggressive cost-cutting (80%)
  + Margin: 20% → 32%  ✓
  + EBITDA: $200K → $320K  ✓
  - Health: 90% → 70%  ⚠️
  - Growth: 5% → 3%

Q2: Company performs worse
  - Health penalty reduces growth
  - Higher volatility
  - Value growth slows

Q5: Company struggling
  - Health: 55% (from repeated cuts)
  - Growth: Severely limited
  - Hard to sell at premium
```

**Long-term thinking:**
```
Q1: CapEx investment ($500K)
  + Health: 80% → 85%  ✓
  + Growth: 5% → 6%  ✓
  - Cash: Down $500K temporarily

Q4: Company thriving
  + Health: 90% (recovered + investment)
  + Growth: Strong and reliable
  + Value: Much higher
  + Exit: Premium valuation
```

### Recovery Strategies

**If Health is Critical (<50%):**

1. **Stop Cost-Cutting Immediately**
   - No more damage to health
   - Let natural recovery begin

2. **Invest in CapEx**
   - +5-15% health per investment
   - Multiple investments stack

3. **Replace Management**
   - Better manager = better health
   - +10-20% if good upgrade

4. **Pursue Growth Strategy**
   - Roll-up: +5-12% health
   - Strengthens operations

5. **Wait It Out**
   - +1% per quarter naturally
   - Slow but steady recovery

**Example Recovery:**
```
Q1: Health at 40% (critical)
Q2: CapEx $1M → Health 47%
Q3: Natural recovery → Health 48%
Q4: Roll-up strategy → Health 56%
Q5: Natural recovery → Health 57%
Q8: Management replacement → Health 72%
Q12: Back to healthy → Health 85%
```

### Strategic Depth

**Trade-offs:**

**Option A: Extract Value (Risky)**
```
Buy → Cost-cut aggressively → Sell quickly
  ✓ High immediate returns
  ✗ Health destroyed
  ✗ Hard to hold long-term
  ✗ Lower exit multiples due to poor health
```

**Option B: Build Value (Safe)**
```
Buy → Invest in CapEx → Build health → Sell at premium
  ✓ Sustainable growth
  ✓ Healthy company
  ✓ Premium exit valuation
  ✗ Longer hold period
  ✗ More capital tied up
```

**Option C: Balanced (Optimal?)**
```
Buy → Moderate cost-cutting → Invest profits → Maintain health → Exit
  ✓ Margin improvement
  ✓ Health maintained
  ✓ Good returns
  ✓ Flexibility
```

---

## In-Game Experience

### Cost-Cutting Display

```
COST-CUTTING ACTION
======================================================================

📋 ACTION TAKEN:
   You direct management to use bedpans made of cardboard

⚠️  IMMEDIATE CONSEQUENCE:
   Patients complain vigorously

💰 FINANCIAL IMPACT:
   • EBITDA Margin: +8.5%
   • Growth Rate: -1.6%

🏥 OPERATIONAL HEALTH:
   • Health Decreased: -20.0%
   • Current Health: 65%
   ⚠️  WARNING: Company health degraded
   • Higher volatility in performance
   • Reduced growth potential

⚠️  WARNING: Aggressive cost-cutting causes lasting operational damage!
   Health recovers slowly (1% per quarter) - plan accordingly.
======================================================================
```

### CapEx Investment Display

```
Invested $1,000,000 in growth initiatives.
Growth rate increased by 5.2%.
Operational health improved by 5.0%.

After Transaction:
  Remaining Cash: $500,000
  Total Debt: $3,500,000
  Company Health: 85% ✓
```

### Portfolio View

```
Portfolio Companies
┏━━━┳━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ # ┃ Name        ┃ P&L   ┃ Return┃ Health ┃
┃ 1 ┃ Healthy Co  ┃ +$2M  ┃ +40%  ┃    92% ┃ ← Green
┃ 2 ┃ Cut Co      ┃ +$1M  ┃ +15%  ┃    58% ┃ ← Yellow
┃ 3 ┃ Damaged Co  ┃ -$500K┃ -10%  ┃  35% ⚠️ ┃ ← Red
```

---

## Game Balance

### Why This Matters

**Before Operational Health:**
- Cost-cutting was always optimal
- No downside to aggressive extraction
- Short-termism rewarded

**With Operational Health:**
- Cost-cutting has lasting consequences
- Must balance short vs. long term
- Investment becomes attractive
- Strategic diversity emerges

### Difficulty Progression

**Early Game (Low Reputation):**
- Limited capital
- Tempted to cost-cut to boost margins
- Must resist for long-term health

**Mid Game (Building):**
- More capital available
- Can invest in health
- Portfolio quality matters

**Late Game (Mature):**
- High-health companies command premiums
- Low-health companies hard to exit
- Health determines final score

---

## Technical Implementation

### Company Model

```python
class Company:
    def __init__(self, ...):
        self.operational_health = self._calculate_initial_health()
    
    def _calculate_initial_health(self) -> float:
        """Initialize health based on fundamentals."""
        mgmt_contribution = 0.5 + (self.manager.competence * 0.4)
        margin_bonus = (self.ebitda_margin - 0.10) * 0.5
        growth_bonus = max(0, self.growth_rate) * 2.0
        return max(0.5, min(1.0, mgmt_contribution + margin_bonus + growth_bonus))
    
    def simulate_quarter(self, market_conditions):
        """Health affects performance."""
        health_penalty = (1.0 - self.operational_health) * 0.5
        growth_factor *= (1.0 - health_penalty)
        
        if self.operational_health < 0.7:
            volatility_factor *= (1.0 + (0.7 - self.operational_health) * 2.0)
        
        # Natural recovery
        if self.operational_health < 1.0:
            self.operational_health = min(1.0, self.operational_health + 0.01)
```

### Portfolio Operations

```python
def apply_cost_cutting(company, intensity):
    """Damages health."""
    health_damage = intensity * 0.15
    if intensity > 0.7:
        health_damage = intensity * 0.25
    company.operational_health -= health_damage

def apply_capex_investment(company, amount):
    """Improves health."""
    health_improvement = min(0.15, (amount/revenue) * 0.10)
    company.operational_health += health_improvement

def pursue_acquisition_strategy(company, strategy):
    """Improves health."""
    health_improvement = random.uniform(0.02, 0.12)  # Varies by strategy
    company.operational_health += health_improvement
```

---

## Examples

### Example 1: Death Spiral

**Q1:** Buy company at 85% health
- Cost-cut aggressively (80%) → Health: 65%
- Margins look great!

**Q2:** Performance disappoints
- Health penalty kicks in
- Cost-cut again (70%) → Health: 48%

**Q3:** Company struggles
- Growth severely limited
- High volatility
- Value declining
- Cost-cut desperately (90%) → Health: 25% ⚠️

**Q5:** Crisis
- Company barely functional
- Can't sell (no buyers want it)
- Trapped in failing asset

### Example 2: Sustainable Growth

**Q1:** Buy company at 75% health
- Moderate cost-cutting (40%) → Health: 69%
- Margins improved slightly

**Q2:** Invest profits
- CapEx $500K → Health: 73%
- Growth accelerating

**Q4:** Continued investment
- Another CapEx $800K → Health: 81%
- Strong performance

**Q6:** Roll-up strategy
- Acquire competitors → Health: 90%
- Market leader status

**Q8:** Premium exit
- High health = premium multiple
- Strong returns realized

### Example 3: Turnaround

**Q1:** Buy distressed company
- Initial health: 52%
- Cheap valuation opportunity

**Q2:** Stop the bleeding
- No cost-cutting
- Natural recovery → Health: 53%

**Q3:** Start investing
- CapEx $1M → Health: 60%
- Management replacement → Health: 72%

**Q6:** Transformation
- Roll-up strategy → Health: 82%
- Now a healthy business

**Q10:** Successful exit
- Turned around completely
- High returns on distressed buy

---

## Configuration

### Health Parameters

**In `models/company.py`:**
```python
# Initial health range
MIN_INITIAL_HEALTH = 0.5  # 50%
MAX_INITIAL_HEALTH = 1.0  # 100%

# Natural recovery rate
NATURAL_HEALTH_RECOVERY = 0.01  # 1% per quarter
```

**In `simulation/portfolio_ops.py`:**
```python
# Cost-cutting damage
MODERATE_DAMAGE = intensity * 0.15
AGGRESSIVE_DAMAGE = intensity * 0.25

# Investment improvements
CAPEX_HEALTH_BOOST = min(0.15, ratio * 0.10)
MGMT_HEALTH_BOOST = competence_delta * 0.20
STRATEGY_HEALTH_BOOST = 0.02 to 0.12
```

### Performance Impact

**In `models/company.py`:**
```python
# Growth penalty from low health
health_penalty = (1.0 - operational_health) * 0.5

# Volatility increase from low health
if operational_health < 0.7:
    volatility_multiplier = 1.0 + (0.7 - operational_health) * 2.0
```

---

## Strategic Patterns

### Pattern 1: Extract and Exit

**Goal:** Quick returns, short hold
**Strategy:**
- Buy cheap
- Aggressive cost-cutting
- Accept health damage
- Exit before it matters

**Risk:** May not find buyer if health too low

### Pattern 2: Build and Hold

**Goal:** Long-term value creation
**Strategy:**
- Buy quality
- Invest in CapEx
- Maintain high health
- Hold for steady growth

**Risk:** Capital tied up longer

### Pattern 3: Turnaround

**Goal:** Distressed investing
**Strategy:**
- Buy damaged companies (low health)
- Stop cost-cutting
- Heavy CapEx investment
- Restore health
- Exit at premium

**Risk:** Requires capital and time

### Pattern 4: Balanced

**Goal:** Optimal risk/return
**Strategy:**
- Moderate cost-cutting initially
- Reinvest savings into CapEx
- Maintain health above 70%
- Exit when multiple expands

**Risk:** None, but requires discipline

---

## Pro Tips

### 1. Check Health Before Buying
- High health = premium price but stable
- Low health = discount but risky
- Factor into valuation

### 2. Don't Over-Cut
- One aggressive cut = okay
- Repeated cuts = death spiral
- Monitor health closely

### 3. Invest Profits
- Use CapEx to restore health
- Reinvestment creates virtuous cycle
- Healthy companies grow faster

### 4. Exit Timing
- High health = better exit multiples
- Don't wait until health critical
- Plan exits 2-3 quarters ahead

### 5. Portfolio Mix
- Some high-health (stable)
- Some low-health (turnaround opportunities)
- Diversify health risk

### 6. Natural Recovery
- Sometimes best to do nothing
- +1% per quarter adds up
- Patience can pay off

### 7. Health Floors
- Never let health drop below 30%
- Critical threshold for viability
- Very hard to recover from <30%

---

## Warning Thresholds

### Display Warnings

**During Cost-Cutting:**
```
Intensity > 70%:
  "⚠️  WARNING: Aggressive cost-cutting causes lasting operational damage!
   Health recovers slowly (1% per quarter) - plan accordingly."

Health < 50% after action:
  "⚠️  CRITICAL: Company health below 50%!
   • Increased volatility and downside risk
   • Reduced growth potential
   • Risk of operational failure"
```

**In Portfolio View:**
```
Health < 40%:
  Company displayed in RED with ⚠️ symbol
  Visual warning of critical condition
```

---

## Summary

The Operational Health system adds **strategic depth**:

✅ **Initialization**: Companies start with varied health (50-100%)  
✅ **Degradation**: Cost-cutting damages health (up to -25%)  
✅ **Improvement**: Investments restore health (multiple methods)  
✅ **Impact**: Low health hurts growth and increases risk  
✅ **Recovery**: Natural healing +1% per quarter  
✅ **Display**: Color-coded health in portfolio view  
✅ **Save/Load**: Health persists across saves  

**Key Insight:** Short-term profit extraction comes at the cost of long-term viability. You must balance immediate returns with sustainable operations!

---

**Version**: 2.6  
**Added**: November 30, 2025  
**Feature**: Operational Health System  
**Impact**: Long-term consequences for all decisions

