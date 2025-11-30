# Reputation and Quote Systems

## Overview

Two new game systems have been added:
1. **Low Starting Reputation** - You must prove yourself through profits
2. **Inspirational Quotes** - Dumb motivational messages during quarter transitions

---

## 1. Reputation System

### Starting Low

Players now start with **20% reputation** instead of 100%:

```python
STARTING_REPUTATION = 0.20  # Start at bottom, prove yourself!
```

### Building Reputation Through Profits

Reputation increases/decreases based on **quarterly profitability**:

**Formula:**
```
Quarterly Profit = (Cash Change) + (Portfolio Value Change)
ROQ = Quarterly Profit / Portfolio Value
Reputation Change = ROQ × 0.5
```

**Capped at ±5% per quarter**

### Examples

**Profitable Quarter:**
```
Portfolio Value: $10M
Quarterly Profit: $2M
ROQ: 20%
Reputation Change: +10% → capped to +5%

Result: 20% → 25% reputation
```

**Break-Even Quarter:**
```
Portfolio Value: $10M
Quarterly Profit: $0
ROQ: 0%
Reputation Change: 0%

Result: Reputation unchanged
```

**Losing Quarter:**
```
Portfolio Value: $10M
Quarterly Loss: -$1M
ROQ: -10%
Reputation Change: -5%

Result: 25% → 20% reputation
```

### Impact on Debt Capacity

Low reputation **severely limits** debt capacity:

```
At 20% reputation:
- Base: $10M
- Net Worth Bonus: Heavily reduced by low reputation
- Total: ~$7M capacity

At 50% reputation:
- Base: $10M
- Net Worth Bonus: Moderate
- Total: ~$15M capacity

At 100% reputation:
- Base: $10M
- Net Worth Bonus: Full multiplier
- Total: ~$30M+ capacity
```

### Strategic Implications

**Early Game:**
- Limited debt capacity due to low reputation
- Must generate profits quickly to unlock more borrowing
- Can't over-leverage without reputation

**Mid Game:**
- Build reputation through consistent profitability
- Debt capacity grows as reputation improves
- Enables larger acquisitions

**Late Game:**
- High reputation = maximum debt capacity
- Can execute large deals
- One bad quarter won't destroy reputation

---

## 2. Quote Display System

### Inspirational Quotes

During quarter transitions, a **random motivational quote** displays for 2.5 seconds:

```
╔══════════════════════════════════════════════╗
║       💎 Words of Wisdom 💎                  ║
║                                              ║
║   "All my losses was lessons."               ║
║                                              ║
╚══════════════════════════════════════════════╝
```

### Quote Examples

**Classic Dumb Ones:**
- "All my losses was lessons."
- "Ever wonder why a Bugatti only has two seats? It's lonely at the top."
- "Started from the bottom now we're here. (Still at the bottom financially.)"
- "Dream big, fail bigger, capitalize the interest."

**PE-Specific:**
- "Rome wasn't built in a day, but it was leveraged to the hilt."
- "Behind every successful person is a substantial amount of debt."
- "If at first you don't succeed, use more leverage."
- "Live, laugh, leverage."

**Self-Aware:**
- "I followed my heart and it led me to debt."
- "I'm not broke, I'm pre-rich."
- "Why fall in love when you can fall into debt?"
- "I'm not underwater, I'm just investing in future swimming skills."

### Quote Database

100+ quotes stored in `/data/quotes.json`:

```json
{
  "inspirational_quotes": [
    "All my losses was lessons.",
    "Ever wonder why a Bugatti only has two seats? It's lonely at the top.",
    ...
  ]
}
```

### Implementation

**Loading:**
```python
def load_quotes():
    """Load inspirational quotes from JSON file."""
    quotes_path = Path(__file__).parent.parent / 'data' / 'quotes.json'
    with open(quotes_path, 'r') as f:
        data = json.load(f)
        return data.get('inspirational_quotes', [])
```

**Display:**
```python
def show_quote_screen():
    """Display a random inspirational quote."""
    quotes = load_quotes()
    quote = random.choice(quotes)
    
    # Styled display with rich library
    panel = Panel(
        Align.center(quote_text, vertical="middle"),
        title="💎 Words of Wisdom 💎",
        border_style="bright_yellow",
        padding=(2, 4)
    )
    
    console.print(panel)
    time.sleep(2.5)  # Pause for effect
```

**Integration:**
```python
def advance_quarter(self):
    """Advance to next quarter."""
    print("\nAdvancing to next quarter...")
    
    # Show quote screen
    screens.show_quote_screen()
    
    # Continue with quarter simulation...
```

---

## Combined System Effects

### The Grind

**Q1: Start**
- Reputation: 20%
- Debt Capacity: $7M
- Quote: "Started from the bottom now we're here."

**Q2: First Profit**
- Made $500K profit
- Reputation: 21% (+1%)
- Debt Capacity: $7.5M
- Quote: "Hustle until your haters ask if you're hiring."

**Q4: Building**
- Made $1M profit
- Reputation: 26% (+5%)
- Debt Capacity: $10M
- Quote: "Diamonds are made under pressure."

**Q8: Success**
- Consistent profits
- Reputation: 45%
- Debt Capacity: $20M
- Quote: "The best view comes after the hardest climb."

**Q12: Peak**
- Major exit
- Reputation: 75%
- Debt Capacity: $40M
- Quote: "I'm not saying I'm Batman, but have you ever seen me and massive debt in the same room?"

### The Spiral

**Q1: Overleverage**
- Reputation: 20%
- Take $6M debt (near max)
- Quote: "Risk is my middle name."

**Q2: Losses**
- Lost $500K
- Reputation: 19% (-1%)
- Debt Capacity shrinking
- Quote: "Fall seven times, stand up eight."

**Q3: More Losses**
- Lost $300K
- Reputation: 17% (-2%)
- Quote: "Adversity introduces a man to himself."

**Q5: Crisis**
- Lost $1M
- Reputation: 12% (-5%)
- Debt Capacity crashed
- Quote: "I followed my heart and it led me to debt."

**Q7: Rock Bottom**
- Reputation: 8%
- Can barely borrow
- Quote: "I'm not underwater, I'm just investing in future swimming skills."

---

## Game Balance

### Reputation as Progression Gate

**Early Game Lock:**
- Low reputation prevents over-leveraging
- Forces focus on profitability first
- Can't buy way to victory immediately

**Mid Game Unlock:**
- Building reputation unlocks debt capacity
- Rewards consistent performance
- Enables portfolio scaling

**Late Game Power:**
- High reputation = full borrowing power
- Can execute large strategies
- Reward for good management

### Quote System Impact

**Psychological:**
- Humor relieves tension
- Memorable moments
- Personality to the game

**Pacing:**
- 2.5 second pause creates anticipation
- Break between quarters
- Time to process previous results

---

## Configuration

### Reputation Settings

```python
# config.py
STARTING_REPUTATION = 0.20  # Start low
```

### Quote Settings

```python
# screens.py
time.sleep(2.5)  # Quote display duration
```

### Adding New Quotes

Edit `/data/quotes.json`:

```json
{
  "inspirational_quotes": [
    "Your new quote here.",
    ...
  ]
}
```

---

## Summary

These systems add **character and challenge**:

**Reputation:**
✅ Start from bottom, earn your way up  
✅ Profits matter, losses hurt  
✅ Organic difficulty progression  
✅ Rewards consistent performance  
✅ Natural leverage limits  

**Quotes:**
✅ Personality and humor  
✅ Memorable moments  
✅ Pacing between quarters  
✅ Dumb fun  
✅ Expandable quote database  

You must **prove yourself** before the game lets you take big swings!

---

**Version**: 2.5  
**Added**: November 29, 2025  
**Features**: Low Starting Reputation + Quote System  
**Impact**: Progression gate + personality

