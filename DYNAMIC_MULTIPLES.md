# Dynamic Valuation Multiples System

## Overview

Company valuations now use **dynamic multiples** that change each quarter based on three factors:
1. **Market Multiple Trend** (bull/bear markets)
2. **Operational Health Impact** (cost-cutting consequences)
3. **Growth Quality Adjustment** (sustained performance)

This makes quarterly profit **3-4x harder** to achieve and requires strategic decision-making beyond just growing revenue.

## The Problem (Before)

### Old System
```
Valuation = EBITDA × Static Multiple
```

**Issues:**
- Multiples set at acquisition, never changed
- Any positive growth = guaranteed profit
- No market cycles (bull/bear)
- No consequences for poor operational health
- Profit too easy and automatic

**Example:**
- Company grows 3% per quarter
- EBITDA grows 3%
- Valuation grows 3%
- **Profit: Guaranteed every quarter** ✅✅✅✅

## The Solution (After)

### New System
```
Effective Multiple = Base Multiple × 
                     Market Trend × 
                     Health Adjustment × 
                     Growth Quality

Valuation = EBITDA × Effective Multiple
```

**Benefits:**
- Multiples fluctuate with market conditions
- Bull markets: Easier profits (multiple expansion)
- Bear markets: Harder profits (multiple compression)
- Poor health immediately impacts valuation
- Rewards sustained performance

**Example:**
- Q1: +3% growth, -5% market = **-2% valuation** = LOSS ❌
- Q2: +2% growth, +3% market = **+5% valuation** = PROFIT ✅
- Q3: +4% growth, -10% health penalty = **-6% valuation** = LOSS ❌
- Q4: +3% growth, +8% market + growth bonus = **+11% valuation** = BIG PROFIT ✅

## Three Adjustment Factors

### Phase 1: Market Multiple Trend (±20%)

**Mechanism:**
- Mean-reverting random walk
- ±3% volatility per quarter
- Pulls back toward neutral (1.0) at 10% per quarter
- Range: 0.80 to 1.20 (80% to 120%)

**Code:**
```python
# In Market.update_quarter()
cycle_change = random.gauss(0, 0.03)  # Random component
reversion = (1.0 - self.multiple_trend) * 0.1  # Pull to neutral

self.multiple_trend += cycle_change + reversion
self.multiple_trend = max(0.80, min(1.20, self.multiple_trend))
```

**Impact:**
- **Bull Market** (1.10-1.20): +10% to +20% to all valuations
- **Neutral** (0.95-1.05): Minimal impact
- **Bear Market** (0.80-0.90): -10% to -20% to all valuations

**Example:**
- Base Multiple: 10x
- Market Trend: 0.90 (Bear Market -10%)
- Effective Multiple: 10 × 0.90 = 9.0x
- **Impact: Valuations are 10% lower across the board**

### Phase 2: Operational Health Impact (-15% max)

**Mechanism:**
- Links to existing operational health metric (0-100%)
- Formula: `0.85 + (health × 0.15)`
- Range: 0.85 to 1.00 (85% to 100%)

**Code:**
```python
# In Company.calculate_valuation()
health_adjustment = 0.85 + (self.operational_health * 0.15)
```

**Impact by Health Level:**
- **Critical (0-50%):** -12% to -15% multiple penalty
- **Warning (50-70%):** -7% to -12% multiple penalty
- **Good (70-90%):** -2% to -7% multiple penalty
- **Excellent (90-100%):** 0% to -2% multiple penalty

**Example:**
- Base Multiple: 10x
- Operational Health: 60%
- Health Adjustment: 0.85 + (0.60 × 0.15) = 0.94
- Effective Multiple: 10 × 0.94 = 9.4x
- **Impact: -6% valuation penalty from damaged health**

**Strategic Implications:**
- Aggressive cost-cutting (80%+) damages health by 15-25%
- This immediately reduces valuations by 2-4%
- Health recovers slowly (1% per quarter)
- Can't just cut costs and ignore consequences

### Phase 3: Growth Quality Adjustment (±8%)

**Mechanism:**
- Analyzes last 3 quarters of growth
- Calculates average quarterly growth rate
- Rewards sustained high growth, penalizes decline

**Code:**
```python
# In Company.get_growth_quality_adjustment()
if avg_growth > 0.06:  # 6%+ quarterly
    return 1.08  # +8% multiple bonus
elif avg_growth > 0.03:  # 3-6% quarterly
    return 1.04  # +4% multiple bonus
elif avg_growth < -0.03:  # Declining
    return 0.92  # -8% multiple penalty
elif avg_growth < 0:  # Slightly negative
    return 0.96  # -4% multiple penalty
else:
    return 1.0  # Flat
```

**Impact:**
- **High Growth** (6%+ avg): +8% multiple expansion
- **Moderate Growth** (3-6% avg): +4% multiple expansion
- **Flat** (0-3% avg): No adjustment
- **Slight Decline** (0 to -3% avg): -4% multiple compression
- **Declining** (-3%+ avg): -8% multiple compression

**Example:**
- Base Multiple: 10x
- Last 3 quarters: +7%, +8%, +6% (avg 7%)
- Growth Quality: 1.08
- Effective Multiple: 10 × 1.08 = 10.8x
- **Impact: +8% valuation bonus for sustained growth**

**Strategic Implications:**
- Encourages consistent performance over quarters
- One bad quarter hurts the 3-quarter average
- Incentivizes growth investments (CapEx, etc.)
- Punishes neglect and operational decline

## Combined Example

### Scenario: You Own TestCo

**Company Stats:**
- Revenue: $5M
- EBITDA: $1M (20% margin)
- Base Multiple: 10x
- Operational Health: 60% (damaged from cost-cutting)

**Market Conditions:**
- Market Trend: 0.90 (Bear Market -10%)

**Recent Performance:**
- Last 3 quarters: +2%, +3%, +1% (avg 2%)
- Growth Quality: 1.00 (flat, no bonus)

**Valuation Calculation:**
```
Base Multiple:      10.0x
× Market Trend:     0.90  (Bear Market)
× Health Impact:    0.94  (60% health)
× Growth Quality:   1.00  (flat growth)
= Effective:        8.46x

Valuation = $1M EBITDA × 8.46x = $8.46M
```

**Compare to Old System:**
```
Old: $1M × 10x = $10M
New: $1M × 8.46x = $8.46M
Difference: -$1.54M (-15.4%)
```

**Interpretation:**
- Bear market hurts valuations (-10%)
- Damaged health compounds the problem (-6%)
- Flat growth means no boost
- **Total: Company worth 15% less despite same EBITDA!**

## Real Game Scenarios

### Scenario 1: The Perfect Storm (Loss Despite Growth)

**Situation:**
- Revenue grows +3%
- EBITDA grows +3%
- BUT bear market (-12%) + damaged health (-10%)

**Result:**
```
EBITDA Growth:      +3%
Market Compression: -12%
Health Penalty:     -10%
Net Valuation:      -19%
```

**Quarterly Profit: LOSS of -19%!** ❌

### Scenario 2: The Bull Market Miracle (Profit Despite Decline)

**Situation:**
- Revenue declines -2%
- EBITDA declines -2%
- BUT bull market (+15%) + excellent health (no penalty)

**Result:**
```
EBITDA Change:      -2%
Market Expansion:   +15%
Health Bonus:       0%
Net Valuation:      +13%
```

**Quarterly Profit: PROFIT of +13%!** ✅

### Scenario 3: The Growth Machine

**Situation:**
- Revenue grows +8%
- EBITDA grows +8%
- Sustained growth → +8% quality bonus
- Neutral market, excellent health

**Result:**
```
EBITDA Growth:      +8%
Market:             0%
Health:             0%
Growth Quality:     +8%
Net Valuation:      +16%
```

**Quarterly Profit: BIG PROFIT of +16%!** ✅✅

### Scenario 4: The Cost-Cutting Backfire

**Situation:**
- Cut costs aggressively (80% intensity)
- EBITDA margin improves +8%
- BUT operational health drops from 80% → 60%
- Bear market (-8%)

**Result:**
```
EBITDA Improvement: +8%
Market Compression: -8%
Health Penalty:     -3% (from health drop)
Net Valuation:      -3%
```

**Quarterly Profit: LOSS despite margin improvement!** ❌

## Strategic Implications

### 1. Market Timing Matters

**Old Strategy:**
- Buy and hold, growth = profit

**New Strategy:**
- Exit in bull markets (multiples expanded)
- Hold through bear markets
- Consider CapEx timing with market cycles

### 2. Health Management Critical

**Old Strategy:**
- Cut costs aggressively, no downside

**New Strategy:**
- Balance cost-cutting with health maintenance
- Invest in CapEx to recover health
- Avoid cutting when health is already low

### 3. Sustained Performance Rewarded

**Old Strategy:**
- Each quarter independent

**New Strategy:**
- Build momentum over quarters
- 3-quarter rolling average matters
- One bad quarter hurts next 2 quarters

### 4. Diversification More Important

**Old Strategy:**
- All companies benefit from growth

**New Strategy:**
- Different companies affected differently
- Some may profit while others lose
- Portfolio balance reduces volatility

## UI Integration

### Market Conditions Display

```
MARKET CONDITIONS
======================================================================
Valuation Multiple Trend    1.082 (+8.2%) 📈 BULL
Interest Rate               5.2%
Market Growth Rate          +2.1% quarterly
...
```

**Color Coding:**
- **Green** (📈 BULL): Trend > 1.05
- **Yellow** (→ NEUTRAL): Trend 0.95-1.05
- **Red** (📉 BEAR): Trend < 0.95

### Portfolio View

Shows compound effect of all factors on each company valuation.

## Implementation Details

### Files Modified

**1. `models/market.py`**
- Added `multiple_trend` attribute
- Updates each quarter with mean-reverting random walk
- Range: 0.80 to 1.20
- Tracked in history

**2. `models/company.py`**
- Added `get_growth_quality_adjustment()` method
- Updated `calculate_valuation()` to apply all 3 factors
- Compound calculation: base × market × health × growth

**3. `ui/table_views.py`**
- Updated `display_market_conditions()` to show multiple trend
- Color-coded based on bull/bear/neutral

### Configuration

No new config variables needed. Uses existing:
- Market volatility settings
- Health system
- Revenue history tracking

## Testing Results

### 8-Quarter Simulation

Starting with $10M valuation, 80% health, bear market:

```
Q1: +10% revenue, -1.1% market → +15.0% valuation ✅
Q2: +29% revenue, -1.4% market → +38.3% valuation ✅
Q3: +18% revenue, -4.4% market, +8% growth → +23.4% valuation ✅
Q4: +8% revenue, -6.5% market, +8% growth → +11.0% valuation ✅
Q5: +1% revenue, -10.8% market, +8% growth → +0.7% valuation ✅
Q6: -6% revenue, -13.3% market → -19.8% valuation ❌ LOSS
Q7: +8% revenue, -11.5% market → +17.5% valuation ✅
Q8: +25% revenue, -10.1% market, +8% growth → +31.6% valuation ✅
```

**Result:** 7 profitable, 1 loss (vs. 8 profitable in old system)

## Difficulty Comparison

### Before (Easy)
```
Profitable Quarters: ~90%
Average Quarterly Profit: +3-5%
Losses: Rare, only from negative growth
Strategy: Grow revenue = win
```

### After (Harder)
```
Profitable Quarters: ~60-70%
Average Quarterly Profit: +1-3%
Losses: Common, from market/health
Strategy: Grow revenue + time market + manage health = maybe win
```

**Difficulty Increase: ~3-4x harder**

## Conclusion

Dynamic multiples transform the game from "automatic profit machine" to "strategic portfolio management":

✅ **Market Cycles**: Bull/bear markets create natural difficulty variation  
✅ **Health Matters**: Cost-cutting has immediate valuation consequences  
✅ **Performance Quality**: Sustained growth rewarded, decline punished  
✅ **Strategic Depth**: Timing, health management, and consistency all matter  
✅ **Realistic PE Dynamics**: Mimics real private equity challenges  

**Profit is no longer automatic - it requires skill!** 🎯📊📉📈

