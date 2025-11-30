# Tax System

## Overview

A simple but impactful **capital gains tax** system that applies when selling companies. Tax rates vary by difficulty mode, making hard mode even more challenging by taking a larger bite out of your profits.

## How It Works

### Capital Gains Tax

**Applied When:** Selling a portfolio company at a profit

**Formula:**
```
Capital Gain = Sale Price - Purchase Price
Tax Owed = Capital Gain × Tax Rate (if gain > 0)
Net Proceeds = Sale Price - Tax Owed
```

**Key Rules:**
- Only taxes **gains**, not losses
- Applied immediately at exit
- Cash proceeds reduced by tax amount
- Total taxes tracked for endgame summary

### Tax Rates by Difficulty

| Difficulty | Era Name | Tax Rate | Keep % |
|------------|----------|----------|--------|
| Easy | Obama Era | 15% | 85% |
| Medium | Reagan Era | 20% | 80% |
| Hard | Brandon Era | 35% | 65% |

## Examples

### Profitable Exit - Easy Mode (Obama Era)

**Scenario:**
- Purchase Price: $10,000,000
- Sale Price: $15,000,000
- Capital Gain: $5,000,000

**Tax Calculation:**
```
Tax Owed = $5,000,000 × 15% = $750,000
Net Proceeds = $15,000,000 - $750,000 = $14,250,000
Effective Gain = $4,250,000 (42.5% return)
```

**Display:**
```
Buyer offers: $15,000,000
Your acquisition price: $10,000,000
Profit/Loss: $5,000,000 (+50.0%)

💸 Capital Gains Tax (15%): $750,000
Net Proceeds (after tax): $14,250,000

Accept this offer? (y/n)
```

### Profitable Exit - Hard Mode (Brandon Era)

**Scenario:**
- Purchase Price: $10,000,000
- Sale Price: $15,000,000
- Capital Gain: $5,000,000

**Tax Calculation:**
```
Tax Owed = $5,000,000 × 35% = $1,750,000
Net Proceeds = $15,000,000 - $1,750,000 = $13,250,000
Effective Gain = $3,250,000 (32.5% return)
```

**Display:**
```
Buyer offers: $15,000,000
Your acquisition price: $10,000,000
Profit/Loss: $5,000,000 (+50.0%)

💸 Capital Gains Tax (35%): $1,750,000
Net Proceeds (after tax): $13,250,000

Accept this offer? (y/n)
```

**Impact:** Hard mode loses **$1,000,000 more** to taxes than easy mode!

### Loss Exit - All Modes

**Scenario:**
- Purchase Price: $10,000,000
- Sale Price: $8,000,000
- Capital Gain: -$2,000,000 (loss)

**Tax Calculation:**
```
Tax Owed = $0 (no tax on losses)
Net Proceeds = $8,000,000
```

**Display:**
```
Buyer offers: $8,000,000
Your acquisition price: $10,000,000
Profit/Loss: $-2,000,000 (-20.0%)

Accept this offer? (y/n)

...

Net Proceeds: $8,000,000 (no tax on loss)
```

## Comparative Impact

### Same Deal, Different Difficulties

**Selling a company bought for $10M:**

| Sale Price | Easy (15%) | Medium (20%) | Hard (35%) |
|------------|------------|--------------|------------|
| $15M (+50%) | $4.25M gain | $4.00M gain | $3.25M gain |
| $20M (+100%) | $8.50M gain | $8.00M gain | $6.50M gain |
| $30M (+200%) | $17.00M gain | $16.00M gain | $13.00M gain |
| $8M (-20%) | -$2M loss (no tax) | -$2M loss (no tax) | -$2M loss (no tax) |

**Observations:**
- Hard mode loses **2.33x more** to taxes than easy mode
- On a $20M profit, hard mode pays **$1.75M more** in taxes
- Losses are never taxed (realistic tax treatment)

### Multi-Exit Game

**Scenario: 5 successful exits over 20 quarters**

**Easy Mode (15% tax):**
```
Exit 1: Buy $5M → Sell $8M → Gain $3M → Tax $450K
Exit 2: Buy $8M → Sell $12M → Gain $4M → Tax $600K
Exit 3: Buy $10M → Sell $18M → Gain $8M → Tax $1.2M
Exit 4: Buy $15M → Sell $25M → Gain $10M → Tax $1.5M
Exit 5: Buy $20M → Sell $35M → Gain $15M → Tax $2.25M

Total Taxes: $6.0M
Total Gains: $40M
After-Tax Gains: $34M (85% kept)
```

**Hard Mode (35% tax):**
```
Exit 1: Buy $5M → Sell $8M → Gain $3M → Tax $1.05M
Exit 2: Buy $8M → Sell $12M → Gain $4M → Tax $1.4M
Exit 3: Buy $10M → Sell $18M → Gain $8M → Tax $2.8M
Exit 4: Buy $15M → Sell $25M → Gain $10M → Tax $3.5M
Exit 5: Buy $20M → Sell $35M → Gain $15M → Tax $5.25M

Total Taxes: $14.0M
Total Gains: $40M
After-Tax Gains: $26M (65% kept)
```

**Difference:** Hard mode pays **$8M more** in taxes over the game! This is huge when starting with just $2M.

## Strategic Implications

### 1. Exit Timing More Critical

**Before Taxes:**
- Exit when valuation is favorable
- Simple profitability calculation

**After Taxes:**
- Must factor in tax hit to net proceeds
- Holding longer might be worth it to get better multiples
- 35% tax on mediocre exit might be worse than waiting

### 2. Difficulty Choice Matters Long-Term

**Easy Mode Advantage:**
- Keep 85% of gains
- More capital to reinvest
- Snowball effect over multiple exits
- Can afford more aggressive exits

**Hard Mode Challenge:**
- Lose 35% of every gain
- Less capital to reinvest
- Must be selective about exits
- Need higher multiples to compensate

### 3. Loss Realization

**No tax on losses = strategic opportunity:**
- Can exit losing investments without tax penalty
- Cut losses early in hard mode
- Tax-advantaged way to free up capital

### 4. Hold vs Sell Calculations

**Example Decision:**

Company bought for $10M, now worth $12M:

**Easy Mode (15% tax):**
- Gain: $2M
- Tax: $300K
- Net: $1.7M
- Decision: Decent gain, might sell

**Hard Mode (35% tax):**
- Gain: $2M
- Tax: $700K
- Net: $1.3M
- Decision: Small net gain, probably hold for better price

## UI Experience

### Exit Dialog (Before Taxes)
```
EXIT INVESTMENT
======================================================================

Buyer offers: $15,000,000
Your acquisition price: $10,000,000
Profit/Loss: $5,000,000 (+50.0%)

Accept this offer? (y/n)
```

### Exit Dialog (After Taxes - Easy Mode)
```
EXIT INVESTMENT
======================================================================

Buyer offers: $15,000,000
Your acquisition price: $10,000,000
Profit/Loss: $5,000,000 (+50.0%)

💸 Capital Gains Tax (15%): $750,000
Net Proceeds (after tax): $14,250,000

Accept this offer? (y/n)
```

### Exit Confirmation
```
Investment exited successfully!
Gross Proceeds: $15,000,000
Taxes Paid: $750,000
Net Proceeds: $14,250,000
```

### Endgame Summary
```
FINANCIAL PERFORMANCE:
  Starting Capital:     $    2,000,000
  Final Net Worth:      $  250,000,000
  Total Return:         $  248,000,000
  
  Return Multiple:            125.00x
  Annualized Return:           215.3%

PORTFOLIO:
  Companies Owned:                  3
  Portfolio Value:      $  200,000,000
  Total Deals:                     15
  
TAXES:
  Capital Gains Tax Rate:          15%
  Total Taxes Paid:     $   12,500,000
  
REPUTATION:                      85.5%
```

## Difficulty Comparison - Full Game

### Scenario: Same Exits, Different Tax Rates

**Portfolio Performance:**
- 10 exits over 20 quarters
- Total gains: $50M

**Easy Mode (Obama Era - 15% tax):**
```
Total Gains:      $50,000,000
Total Taxes:      $ 7,500,000
After-Tax Gains:  $42,500,000
```

**Medium Mode (Reagan Era - 20% tax):**
```
Total Gains:      $50,000,000
Total Taxes:      $10,000,000
After-Tax Gains:  $40,000,000
```

**Hard Mode (Brandon Era - 35% tax):**
```
Total Gains:      $50,000,000
Total Taxes:      $17,500,000
After-Tax Gains:  $32,500,000
```

**Tax Difference:**
- Easy vs Hard: **$10M less** in hard mode
- This $10M could fund 5 more acquisitions!

## Implementation Details

### Files Modified

**1. `config.py`**
- Added `capital_gains_tax_rate` to each difficulty setting
- Easy: 15%, Medium: 20%, Hard: 35%

**2. `models/player.py`**
- Added `total_taxes_paid` tracker
- Added `calculate_capital_gains_tax()` method
- Added `pay_taxes()` method

**3. `game/engine.py`**
- Updated `exit_investment()` to calculate and apply taxes
- Shows tax before confirmation
- Displays gross and net proceeds

**4. `ui/screens.py`**
- Updated difficulty selection to show tax rates
- Updated endgame summary to show total taxes paid
- Tax rate displayed in final results

### Code Structure

```python
# Calculate tax
tax_owed = player.calculate_capital_gains_tax(sale_price, purchase_price)

# Apply tax
if tax_owed > 0:
    player.pay_taxes(tax_owed)

# Track total
player.total_taxes_paid  # Cumulative across all exits
```

## Design Decisions

### Why Capital Gains Tax (Not Income Tax)?

**Capital Gains:**
- ✅ Simple to understand
- ✅ Only applies on exits (clear trigger)
- ✅ Realistic for PE funds
- ✅ Strategic timing component

**Income Tax (Rejected):**
- ❌ More complex (what's income vs. unrealized gains?)
- ❌ Would need to track quarterly
- ❌ Harder to explain
- ❌ Would make quarterly profit calculation confusing

### Why No Tax on Losses?

**Realistic:**
- Real tax systems allow loss deductions
- Can't tax negative gains
- Encourages cutting losing investments

**Gameplay:**
- Doesn't punish failure twice
- Allows strategic loss realization
- Already hard to make money in hard mode

### Why Vary by Difficulty?

**Reinforces Theme:**
- Obama Era: Pro-business, lower taxes
- Reagan Era: Moderate, balanced
- Brandon Era: High taxes, tough environment

**Gameplay Impact:**
- Significant (2.33x difference)
- Makes hard mode meaningfully harder
- Adds to cumulative difficulty increase

## Conclusion

The tax system adds:

✅ **Realism** - Capital gains taxes are real  
✅ **Difficulty Scaling** - 15% to 35% across modes  
✅ **Strategic Depth** - Exit timing more critical  
✅ **Long-term Impact** - Compounds over multiple exits  
✅ **Simplicity** - Only on profitable exits, easy to understand  

**In Brandon Era, the government takes 35% of your wins!** 💸🏛️

Combined with volatile markets, frequent crises, and dynamic multiples, hard mode is now truly hardcore.

**Obama Era:** Keep 85% of gains → More capital → Easier scaling  
**Reagan Era:** Keep 80% of gains → Balanced challenge  
**Brandon Era:** Keep 65% of gains → Brutal compounding difficulty  

The tax system doesn't just make profit harder - it makes **reinvestment** harder, which makes **scaling** harder, which makes reaching S-tier ($10B+) significantly more challenging! 🎯

