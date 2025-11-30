# Fund Name & Difficulty Selection System

## Overview

Players now customize their experience by:
1. **Selecting a difficulty mode** (Easy/Medium/Hard) with clever era-based names
2. **Naming their fund** with funny validation messages
3. **Seeing their fund name prominently displayed** throughout the game

## Features

### 1. Difficulty Selection

Three difficulty modes with distinct characteristics:

#### Easy Mode: "Obama Era"
**Description:** "Fish in a barrel. Easy credit, stable multiples, rare crises"

**Settings:**
- Market Volatility: 0.7x (30% less volatile)
- Multiple Trend Volatility: ±2.0% (vs. ±3.0% normal)
- Event Probability: 0.7x (30% fewer events)
- Crisis Probability: 0.5x (50% fewer crises)
- Starting Reputation: 30% (vs. 20% normal)
- Interest Rate: 3% (vs. 5% normal)
- Capital Gains Tax: 15%

**Best For:**
- New players learning the game
- Casual playthroughs
- Testing strategies without harsh penalties

#### Medium Mode: "Reagan Era"
**Description:** "Balanced challenge, realistic market dynamics"

**Settings:**
- Market Volatility: 1.0x (standard)
- Multiple Trend Volatility: ±3.0% (standard)
- Event Probability: 1.0x (standard)
- Crisis Probability: 1.0x (standard)
- Starting Reputation: 20% (standard)
- Interest Rate: 5% (standard)
- Capital Gains Tax: 20%

**Best For:**
- Regular gameplay
- Recommended difficulty
- Balanced challenge

#### Hard Mode: "Newsom Era"
**Description:** "In the People's Republic of California, money is scarce. Volatile markets, frequent crises, tough conditions"

**Settings:**
- Market Volatility: 1.4x (40% more volatile)
- Multiple Trend Volatility: ±4.5% (vs. ±3.0% normal)
- Event Probability: 1.5x (50% more events)
- Crisis Probability: 2.0x (2x more crises!)
- Starting Reputation: 15% (vs. 20% normal)
- Interest Rate: 8% (vs. 5% normal)
- Capital Gains Tax: 30%

**Best For:**
- Experienced players
- Maximum challenge
- "Impossible mode" enthusiasts

### 2. Fund Name Selection

**Process:**
1. Player enters their fund name
2. Funny message displayed
3. Confirmation required
4. Name displayed prominently throughout game

**Funny Messages** (randomly selected):
- "Choose wisely, this is going on all the Patagonias and embroidery ain't cheap."
- "This name better be good - we're printing 10,000 business cards."
- "Your LPs are gonna see this on every quarterly report. No pressure."
- "Remember: A bad name is forever. Well, for 20 quarters anyway."
- "Make it count - this is going on the trophy in your corner office."
- "Choose something your mother would be proud of. Or not. I'm not judging."
- "This will be on your yacht. Make it yacht-worthy."
- "Fun fact: 'Synergy Capital' is already taken. Try harder."
- "Your competitors will see this name and weep. Or laugh. Probably laugh."
- "The SEC is watching. Choose accordingly."

### 3. UI Integration

**Fund Name Appears:**

**Main Menu:**
```
======================================================================
SYNERGY CAPITAL PARTNERS - QUARTER 5 (Year 2)
======================================================================

Cash: $5,234,123
Debt: $2,000,000 / $15,000,000 (13% utilized)
...
```

**Player Summary:**
```
Synergy Capital Partners | Reagan Era Mode
======================================================================
Metric                  Value
----------------------------------------------------------------------
Cash                    $5,234,123
Debt                    $2,000,000
...
```

**Intro Screen:**
```
PRIVATE EQUITY SIMULATOR

Synergy Capital Partners
Difficulty: Reagan Era - Balanced challenge, realistic market dynamics

You are the managing partner of this fund with:
  • $2,000,000 in starting capital
  • $16,500,000 initial debt capacity
  • 20% starting reputation
  ...
```

## Difficulty Impact Details

### Market Dynamics

**Multiple Trend Volatility:**
- Easy: ±2.0% → Bull/bear cycles are gentler
- Medium: ±3.0% → Standard volatility
- Hard: ±4.5% → Extreme market swings

**Example Quarter:**
- Easy: Multiple trend changes from 1.00 → 0.98 (mild)
- Medium: Multiple trend changes from 1.00 → 0.95 (moderate)
- Hard: Multiple trend changes from 1.00 → 0.91 (severe)

### Events & Crises

**Event Frequency:**
- Easy: ~17.5% chance per quarter (vs. 25% base)
- Medium: 25% chance per quarter
- Hard: 37.5% chance per quarter

**Crisis Frequency:**
- Easy: ~1.25% chance per quarter (very rare)
- Medium: 2.5% chance per quarter
- Hard: 5.0% chance per quarter (1 per year!)

### Starting Reputation

**Impact on Debt Capacity:**

Initial net worth: $2M

**Easy (30% reputation):**
```
Debt Capacity = $10M + ($2M × 3.0 × 1.1) = $16.6M
```

**Medium (20% reputation):**
```
Debt Capacity = $10M + ($2M × 3.0 × 0.9) = $15.4M
```

**Hard (15% reputation):**
```
Debt Capacity = $10M + ($2M × 3.0 × 0.8) = $14.8M
```

**Difference:** Easy mode starts with $1.8M more debt capacity!

## Strategic Implications

### Easy Mode Strategy

**Advantages:**
- More stable valuations (easier to predict exits)
- Fewer crisis events to manage
- Higher starting debt capacity
- More forgiving of mistakes

**Optimal Play:**
- Aggressive expansion early
- Use full debt capacity
- Exit timing less critical
- Can survive poor decisions

### Medium Mode Strategy

**Characteristics:**
- Balanced risk/reward
- Market timing matters
- Must manage health carefully
- Standard PE dynamics

**Optimal Play:**
- Balanced approach
- Time exits with bull markets
- Active health management
- Diversified portfolio

### Hard Mode Strategy

**Challenges:**
- Extreme volatility (±4.5% swings!)
- Frequent crises (expect 3-5 per game)
- Lower starting debt capacity
- One mistake can be fatal

**Optimal Play:**
- Conservative early game
- Heavy diversification essential
- Always maintain cash reserves
- Defensive portfolio operations
- Perfect timing critical

## Difficulty Comparison Example

### Scenario: 4-Quarter Performance

**Same Company, Different Difficulties:**

**Easy Mode:**
- Q1: +3% growth, +1.5% market → +4.5% val → Profit ✅
- Q2: +4% growth, -1.0% market → +3.0% val → Profit ✅
- Q3: +2% growth, +2.0% market → +4.0% val → Profit ✅
- Q4: +3% growth, -0.5% market → +2.5% val → Profit ✅
- **Result: 4/4 profitable, +14% total**

**Medium Mode:**
- Q1: +3% growth, -3.0% market → -0% val → Break even ~
- Q2: +4% growth, +1.0% market → +5.0% val → Profit ✅
- Q3: +2% growth, -4.0% market → -2.0% val → Loss ❌
- Q4: +3% growth, +2.0% market → +5.0% val → Profit ✅
- **Result: 2/4 profitable, +8% total**

**Hard Mode:**
- Q1: +3% growth, -5.0% market → -2.0% val → Loss ❌
- Q2: +4% growth, -2.0% market → +2.0% val → Profit ✅
- Q3: +2% growth, -6.0% market, CRISIS! → -10% val → Big Loss ❌❌
- Q4: +3% growth, +4.0% market → +7.0% val → Profit ✅
- **Result: 2/4 profitable, -3% total (NET LOSS!)**

## Implementation Details

### Files Modified

**1. `config.py`**
- Added `DIFFICULTY_SETTINGS` dictionary
- Three difficulty levels with multipliers

**2. `models/player.py`**
- Added `fund_name` and `difficulty` parameters
- Apply reputation bonus based on difficulty
- Constructor: `Player(fund_name, difficulty)`

**3. `models/market.py`**
- Added `difficulty` and `difficulty_settings`
- Market volatility uses difficulty multipliers
- Multiple trend volatility scales with difficulty
- Constructor: `Market(difficulty)`

**4. `ui/screens.py`**
- Added `select_difficulty()` - difficulty selection screen
- Added `select_fund_name()` - fund name entry with funny messages
- Added `get_funny_fund_name_message()` - random funny messages
- Updated `show_intro()` to display fund name and difficulty

**5. `ui/table_views.py`**
- Updated `display_player_summary()` to show fund name in title

**6. `game/menus.py`**
- Updated `main_menu()` to show fund name in header

**7. `game/engine.py`**
- Updated `__init__()` to accept difficulty and fund_name
- Updated `start_game()` to call selection screens
- Re-initializes player and market with selections

**8. `game/events.py`**
- Event probability scaled by difficulty
- Crisis probability scaled by difficulty

### Configuration Schema

```python
DIFFICULTY_SETTINGS = {
    'easy': {
        'name': str,  # Display name
        'description': str,  # Description text
        'market_volatility_multiplier': float,  # Market volatility scaling
        'multiple_trend_volatility': float,  # Multiple trend ±% range
        'event_probability_multiplier': float,  # Event frequency scaling
        'crisis_probability_multiplier': float,  # Crisis frequency scaling
        'starting_reputation_bonus': float,  # Reputation adjustment
    },
    # ... medium, hard
}
```

## Testing Results

### Fund Name System
```
✅ Random funny messages displayed
✅ Empty names rejected
✅ Confirmation required
✅ Displayed in all UI screens
```

### Difficulty System
```
✅ Three difficulty modes
✅ Market volatility scales correctly
✅ Event frequency scales correctly
✅ Starting reputation varies
✅ Mode shown in UI
```

### Integration
```
✅ Difficulty selection → Fund name → Intro → Game
✅ Fund name in main menu header
✅ Fund name in player summary
✅ Difficulty name shown with fund name
✅ All systems functional
```

## Player Experience

### Game Start Flow

1. **Main Menu** (if saves exist)
   - "Start New Game" or "Load Saved Game"

2. **Difficulty Selection**
   ```
   SELECT DIFFICULTY
   
   1. Obama Era (Easy)
      • Stable markets (low volatility)
      • Easy credit conditions
      • Rare crises
      ...
   
   2. Reagan Era (Medium)
      ...
   
   3. Brandon Era (Hard)
      ...
   ```

3. **Fund Name Entry**
   ```
   NAME YOUR FUND
   
   Choose wisely, this is going on all the Patagonias 
   and embroidery ain't cheap.
   
   Enter your fund name: _
   ```

4. **Confirmation**
   ```
   Synergy Capital Partners
   
   Is this correct? (y/n): _
   ```

5. **Intro Screen**
   ```
   PRIVATE EQUITY SIMULATOR
   
   Synergy Capital Partners
   Difficulty: Reagan Era - Balanced challenge
   
   You are the managing partner of this fund with:
   ...
   ```

6. **Game Begins**
   ```
   SYNERGY CAPITAL PARTNERS - QUARTER 1 (Year 1)
   ======================================================================
   Cash: $2,000,000
   ...
   ```

## Conclusion

The Fund Name & Difficulty system adds:

✅ **Personalization** - Your fund, your name  
✅ **Humor** - Funny messages during setup  
✅ **Replayability** - Three distinct difficulty modes  
✅ **Accessibility** - Easy mode for learning  
✅ **Challenge** - Hard mode for masochists  
✅ **Visibility** - Fund name everywhere  

**Players can now have their own unique PE adventure!** 🏢💼🎯

From building "Synergy Capital Partners" in the Obama Era to surviving as "YOLO Investments" in the Brandon Era - the choice is yours!

