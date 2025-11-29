# Narrative System - Business Decision Consequences

## Overview

Every major business decision now has **sector-specific narrative consequences** that bring the game to life. Instead of generic "margins improved," you'll see exactly *how* costs were cut and what the consequences are.

---

## Cost-Cutting Narratives

### How It Works

When you implement cost-cutting measures, the system:
1. **Selects intensity level** based on your chosen percentage (0-100%)
2. **Generates sector-specific narrative** describing the actual cuts
3. **Shows immediate consequences** of your decision
4. **Applies financial and reputation impacts**

### Intensity Levels

**Low Intensity (0-33%):**
- Minor operational changes
- Minimal employee/customer impact
- Safe improvements with predictable results

**Medium Intensity (34-66%):**
- Significant operational changes
- Noticeable impact on employees and customers
- Higher risk of morale/quality issues

**High Intensity (67-100%):**
- Aggressive, dramatic cuts
- Major impact on everyone involved
- High risk of long-term damage

---

## Sector-Specific Examples

### Food & Beverage

**Low Intensity:**
- "You direct management to switch to generic brand ingredients"
- "You eliminate free employee meals"
- "You reduce portion sizes by 10%"

**Medium Intensity:**
- "You lay off 15% of kitchen staff during off-peak hours"
- "You replace the espresso machine with instant coffee"
- "You eliminate all garnishes and presentation elements"

**High Intensity:**
- "You replace all meat with 'mystery meat' of dubious origin"
- "You switch to single-ply toilet paper (customers notice)"
- "You require dishwashers to reuse water for multiple loads"

### Healthcare

**Low Intensity:**
- "You switch to generic medications whenever possible"
- "You reduce magazine subscriptions in the waiting room"
- "You dim the lights in non-critical areas"

**Medium Intensity:**
- "You reduce nursing staff by 15%"
- "You switch to cheaper, scratchier patient gowns"
- "You require doctors to see 20% more patients per day"

**High Intensity:**
- "You direct management to use bedpans made of cardboard" 
- "You replace anesthesiologists with 'a wooden stick to bite on'"
- "You install coin-operated vending machines for basic supplies"

### Auto Services

**Low Intensity:**
- "You switch to generic oil and fluids"
- "You eliminate free car washes with service"
- "You switch to cheaper, imported parts"

**Medium Intensity:**
- "You require mechanics to work faster (quality drops)"
- "You switch to refurbished parts only"
- "You eliminate diagnostic scanning - guessing now"

**High Intensity:**
- "You use duct tape as a 'temporary permanent fix'"
- "You eliminate all safety inspections"
- "You eliminate the lift - everything on jack stands now"

### Personal Services

**Low Intensity:**
- "You switch to cheaper product lines"
- "You reduce appointment times by 15%"
- "You eliminate complimentary beverages"

**Medium Intensity:**
- "You eliminate air conditioning to save costs"
- "You switch to 'bring your own towel' policy"
- "You require stylists to purchase their own supplies"

**High Intensity:**
- "You require clients to wash their own hair"
- "You switch to kitchen scissors for haircuts"
- "You use '2-in-1' product for everything"

---

## Consequences System

### Immediate Consequences

Each decision generates a consequence message:

**Low Intensity:**
- "Employees grumble but accept the changes"
- "Minor efficiency losses but margins improve"
- "Short-term pain for long-term gain"

**Medium Intensity:**
- "Employee morale drops noticeably"
- "Some customers start complaining"
- "Quality metrics show slight decline"
- "Turnover increases among skilled workers"

**High Intensity:**
- "Mass employee exodus begins"
- "Customer complaints surge dramatically"
- "Quality plummets - reviews turn negative"
- "Several key employees quit immediately"
- "Long-term damage to brand reputation"

### Reputation Impact

High-intensity cost-cutting (>70%) can damage your reputation:
- **Medium intensity**: Rare reputation hits (30% chance)
- **High intensity**: Frequent reputation hits (50% chance, 1-3% decrease)
- **Reputation loss** reduces your debt capacity!

### Morale Impact

Aggressive cost-cutting hurts employee morale:
- **Medium intensity**: 30% chance of additional growth penalty
- **High intensity**: 50% chance of significant growth penalty
- **Effect**: Extra -0.01 to -0.03 quarterly growth rate

---

## In-Game Display

When you implement cost-cutting, you'll see:

```
======================================================================
COST-CUTTING ACTION
======================================================================

📋 ACTION TAKEN:
   You replace the espresso machine with instant coffee

⚠️  IMMEDIATE CONSEQUENCE:
   Employee morale drops noticeably

💰 FINANCIAL IMPACT:
   • EBITDA Margin: +5.2%
   • Growth Rate: -1.0%

😞 MORALE IMPACT:
   Additional growth penalty from poor employee morale

📉 REPUTATION IMPACT:
   Your reputation decreased by 2.0%
   (Now at 98%)

⚠️  WARNING: Aggressive cost-cutting may have long-term consequences!
======================================================================
```

---

## Strategic Implications

### When to Use Low Intensity
- Company is profitable but could be more efficient
- Want safe, predictable margin improvement
- Building long-term sustainable business
- High-reputation fund protecting track record

### When to Use Medium Intensity
- Company needs significant improvement
- Acceptable to take some risks
- Short-term hold (will exit soon)
- Can absorb some reputation hit

### When to Use High Intensity
- Company in crisis - desperate measures needed
- Planning to flip quickly
- Don't care about reputation (risky!)
- Final quarter - no long-term consequences

### Best Practices

1. **Match intensity to timeline**: Short hold = can be aggressive
2. **Consider sector**: Healthcare/food cuts are riskier
3. **Protect reputation early game**: You need debt capacity
4. **Diversify impact**: Don't max intensity on all companies
5. **Watch compound effects**: Multiple aggressive cuts = exodus

---

## Technical Details

### File Structure

**Data:**
- `/data/narratives.json` - All narrative text by sector and intensity

**Code:**
- `/simulation/narratives.py` - Narrative generator
- `/simulation/portfolio_ops.py` - Applies narratives to operations
- `/game/engine.py` - Displays formatted output

### Adding New Narratives

Edit `/data/narratives.json`:

```json
{
  "cost_cutting_narratives": {
    "Your Sector": {
      "low_intensity": [
        "Your narrative here",
        "Another option here"
      ],
      "medium_intensity": [...],
      "high_intensity": [...]
    }
  }
}
```

### Future Expansion

This system can be extended to:
- **Capex investment narratives** (what gets built/improved)
- **Management replacement stories** (why they left, who replaced them)
- **Growth strategy narratives** (how roll-ups/expansion executed)
- **Exit deal stories** (who bought, why, bidding war details)

---

## Examples from Gameplay

### Example 1: Conservative Pizza Shop Owner

```
Company: Main Street Pizza (Food & Beverage)
Action: 25% intensity cost-cutting

ACTION: You direct management to switch to generic brand ingredients
CONSEQUENCE: Employees grumble but accept the changes
RESULT: +3.5% margin, -0.5% growth, no reputation hit
```

### Example 2: Aggressive Healthcare Turnaround

```
Company: Quick Urgent Care (Healthcare)  
Action: 85% intensity cost-cutting

ACTION: You direct management to use bedpans made of cardboard
CONSEQUENCE: Customer complaints surge dramatically
RESULT: +11.2% margin, -1.7% growth, -2.5% reputation
WARNING: Long-term damage to brand reputation
```

### Example 3: Tech Company Optimization

```
Company: Premium IT Services (Technology)
Action: 40% intensity cost-cutting

ACTION: You eliminate work-from-home options
CONSEQUENCE: Turnover increases among skilled workers
RESULT: +5.8% margin, -0.8% growth, minor morale impact
```

---

## Summary

The narrative system transforms cold financial decisions into **vivid, memorable stories**:

✅ **Sector-specific** - Pizza shops ≠ hospitals  
✅ **Intensity-scaled** - Severity matches your choice  
✅ **Consequential** - Decisions have real trade-offs  
✅ **Humorous** - Keeps gameplay entertaining  
✅ **Strategic** - Forces you to think about costs  

This makes every cost-cutting decision feel **meaningful and memorable**!

---

**Version**: 2.1  
**Added**: November 29, 2025  
**Applies to**: All business sectors

