# PE Simulator - Recent Enhancements

## Overview of New Features

This document describes the three major enhancements added to make the game more realistic and better suited for small-scale local business investing.

---

## 1. Per-Company Valuation Multiples (Normal Distribution)

### What Changed
Previously, all companies in a sector used the same valuation multiple from the market. Now each company has its own unique valuation multiple drawn from a normal distribution around the sector mean.

### Implementation Details

**Company Model (`models/company.py`):**
- Added `valuation_multiple` attribute to Company class
- Companies now store their own multiple, calculated at generation time
- Multiple is used in `calculate_valuation()` if available

**Config (`config.py`):**
```python
MULTIPLE_STD_DEV = 1.5  # Standard deviation for multiple distribution
```

**Generation (`simulation/procedural_gen.py`):**
```python
# Generate company-specific valuation multiple from normal distribution
base_multiple = adjustments['base_multiple']  # Sector mean
multiple_std = config.MULTIPLE_STD_DEV
valuation_multiple = random.gauss(base_multiple, multiple_std)
# Clamped to MIN_EBITDA_MULTIPLE (6.0x) and MAX_EBITDA_MULTIPLE (25.0x)
```

### Sector Base Multiples
- Technology: 12.0x
- Healthcare: 11.0x
- Financial Services: 10.0x
- Consumer: 9.0x
- Industrial: 8.5x
- Real Estate: 8.0x
- Energy: 7.5x
- Retail: 7.0x

### Example Results
With standard deviation of 1.5x, a Technology company (mean 12.0x) could have multiples ranging from ~9x to ~15x (68% of the time), creating realistic valuation dispersion within sectors.

### UI Display
The company detail view now shows the valuation multiple:
```
Valuation Multiple:  10.5x
```

---

## 2. Smaller Starting Capital & Local Business Focus

### What Changed
Game now starts with much less capital ($10M instead of $100M) and generates much smaller businesses suitable for this scale.

### Configuration Changes

**Starting Capital (`config.py`):**
```python
STARTING_CAPITAL = 10_000_000  # $10M (down from $100M)
STARTING_DEBT_CAPACITY = 200_000_000  # $200M (unchanged)
```

**Company Size Range (`config.py`):**
```python
MIN_COMPANY_REVENUE = 500_000  # $500K (down from $10M)
MAX_COMPANY_REVENUE = 20_000_000  # $20M (down from $100M)
```

### Why This Improves Gameplay
1. **More Realistic Starting Point**: Most PE funds don't start with $100M
2. **Gradual Progression**: Players build up from small local businesses
3. **More Deals Available**: With smaller valuations, more deals are affordable
4. **Local Business Focus**: Matches the new local business naming system

### Typical Deal Sizes
- **Small Local Businesses**: $1-5M valuation
- **Mid-Size Businesses**: $5-15M valuation  
- **Larger Opportunities**: $15-50M valuation (requiring debt)

### Available Capital
- **Starting Cash**: $10M
- **Total Available** (with max debt): $210M
- This allows for 2-4 initial acquisitions without debt

---

## 3. Local Business Name Generation

### What Changed
Added a new naming style for generating authentic-sounding local business names, automatically applied based on company size.

### Implementation

**New Name Generation Function (`simulation/procedural_gen.py`):**
```python
def generate_company_name(sector: str = None, style: str = 'corporate') -> str
def generate_local_business_name() -> str
```

**Automatic Style Selection:**
- Companies < $5M revenue: 70% local, 30% corporate names
- Companies ≥ $5M revenue: 80% corporate, 20% local names

### Local Business Name Patterns

**Pattern 1: Prefix + Type**
- Main Street Pizza
- Downtown Hardware
- Corner Cafe

**Pattern 2: Type + Descriptor**
- Pizza Express
- Hardware Depot
- Diner & Grill

**Pattern 3: Possessive + Type**
- Joe's Hardware
- Mom's Bakery
- Bob's Auto Repair

**Pattern 4: Simple**
- Quality Bakery
- Best Cafe
- Hometown Grocery

### Name Components (`data/names.json`)

**Prefixes:**
- Main Street, Downtown, City, Corner
- Family, Joe's, Mom's, Bob's, Mike's, Tony's
- Quick, Best, Quality, Hometown

**Business Types (28 types):**
- Pizza, Hardware, Auto Repair, Bakery, Cafe
- Dry Cleaners, Pharmacy, Grocery, Bar & Grill
- Barbershop, Pet Store, Plumbing, HVAC
- Nail Salon, Hair Salon, Car Wash
- And more...

**Descriptors:**
- & Sons, & Daughters, & Co
- Shop, Store, Market, Emporium
- Express, Plus, Depot, Center

### Example Generated Names
- "Mom's Roofing"
- "Village Hair Salon"
- "Landscaping Works"
- "Family Nail Salon"
- "Pizza Express"
- "Joe's Hardware"
- "Main Street Bakery"

### Corporate Names (Still Available)
For larger businesses, traditional corporate names are still generated:
- "Prime Products Partners"
- "Dynamic Technologies LLC"
- "Elite Corp"
- "Advanced Systems International"

---

## Impact on Gameplay

### Early Game (Quarters 1-5)
- **Focus**: Acquire 2-4 small local businesses
- **Strategy**: Build cash flow through operations
- **Capital**: Use mostly equity, minimal debt

### Mid Game (Quarters 6-12)  
- **Focus**: Improve operations, consider larger deals
- **Strategy**: Use leverage for bigger acquisitions
- **Capital**: Mix of cash from exits and new debt

### Late Game (Quarters 13-20)
- **Focus**: Optimize portfolio, strategic exits
- **Strategy**: Exit improved businesses at premium valuations
- **Capital**: Recycled proceeds from exits

### Valuation Strategy
With per-company multiples, players can now:
1. **Hunt for Value**: Find low-multiple companies in good sectors
2. **Quality Focus**: Target high-quality businesses with premium multiples
3. **Multiple Arbitrage**: Buy low-multiple, sell after multiple expansion
4. **Sector Timing**: Exploit sector multiple trends

---

## Technical Notes

### Backward Compatibility
- Existing save files will work (if implemented)
- Companies without `valuation_multiple` fall back to sector average
- Old-style names still generated for larger companies

### Testing
All features have been tested:
- ✓ Multiple generation within bounds (6.0x - 25.0x)
- ✓ Normal distribution around sector means
- ✓ Local business names generate correctly
- ✓ Company size appropriate for starting capital
- ✓ No linting errors

### Configuration Flexibility
All settings can be adjusted in `config.py`:
- `STARTING_CAPITAL` - adjust starting cash
- `MIN_COMPANY_REVENUE` / `MAX_COMPANY_REVENUE` - business size range
- `MULTIPLE_STD_DEV` - valuation dispersion
- `MIN_EBITDA_MULTIPLE` / `MAX_EBITDA_MULTIPLE` - multiple bounds

---

## Future Enhancement Ideas

1. **Geography System**: Add city names to local businesses
2. **Franchise Opportunities**: Roll up multiple local businesses
3. **Sector-Specific Local Names**: Pizza shops mostly in Consumer sector, etc.
4. **Owner Personalities**: Add owner attributes like "family business" flag
5. **Multiple Drivers**: Make multiple relate to company quality metrics

---

## Summary

These three enhancements transform the game from a large-cap PE simulator into a realistic small-business acquisition game:

✅ **Realistic Valuation Variation** - Companies have unique multiples  
✅ **Appropriate Scale** - Start small, build up gradually  
✅ **Authentic Names** - Local businesses feel like real businesses  

The game now provides a much more engaging and realistic experience for players interested in small business investing and roll-up strategies!

