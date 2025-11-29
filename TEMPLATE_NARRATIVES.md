# Template-Based Narrative System

## Overview

The narrative system now supports **template-based random generation** in addition to static narratives, creating infinite variety in cost-cutting descriptions!

---

## How It Works

### Dual System

**50% chance**: Use template-based generation (new!)  
**50% chance**: Use static narratives (original)

This creates variety while maintaining quality hand-written narratives.

### Template Format

Templates use `{placeholder}` markers that get replaced with random sector-specific options:

```
"You switch to using {production_input} made of {inferior_material}"
```

Becomes:
- "You switch to using **yoga mats** made of **eco-friendly paper**"
- "You switch to using **napkins** made of **compressed sawdust**"
- "You switch to using **patient gowns** made of **tissue paper**"

---

## Template Examples

### Low Intensity Templates
```
"You switch to using {production_input} made of {inferior_material}"
"You require staff to {cost_cutting_action} to save money"
"You replace {premium_item} with {cheap_alternative}"
"You eliminate {luxury_item} to cut costs"
```

### Medium Intensity Templates
```
"You mandate that all {equipment} be {degrading_action}"
"You switch to {substandard_practice} despite {obvious_problem}"
"You require {staff_type} to {unreasonable_demand}"
```

### High Intensity Templates
```
"You direct management to use {essential_item} made of {absurd_material}"
"You replace all {important_equipment} with {ridiculous_substitute}"
"You require {workers} to {extreme_measure} or face termination"
```

---

## Sector-Specific Variables

Each sector has custom variables that make sense for that industry:

### Food & Beverage Example

**production_input**: plates, cups, utensils, napkins, tablecloths, menus  
**inferior_material**: cardboard, recycled newspaper, paper mache, biodegradable seaweed, compressed sawdust, eco-friendly paper  
**absurd_material**: origami paper, wax-coated cardboard, compressed tofu, recyclable foam  

**Results:**
- "You switch to using **menus** made of **biodegradable seaweed**"
- "You direct management to use **serving dishes** made of **origami paper**"
- "You require **servers** to **work for food instead of wages** or face termination"

### Healthcare Example

**production_input**: patient gowns, exam table paper, bandages, surgical masks, gloves  
**inferior_material**: tissue paper, newspaper, cheese cloth, coffee filters, paper towels, sandwich bags  
**ridiculous_substitute**: smartphone flashlights, a Magic 8-Ball, equipment borrowed from veterinarians  

**Results:**
- "You switch to using **surgical masks** made of **coffee filters**"
- "You replace all **X-ray machines** with **a Magic 8-Ball**"
- "You replace all **ultrasounds** with **equipment borrowed from veterinarians**"

### Personal Services Example

**production_input**: towels, robes, yoga mats, massage tables, styling capes  
**inferior_material**: paper towels, garbage bags, eco-friendly paper, pool floaties, plastic tarps  
**absurd_material**: plastic, cardboard, pool noodles, duct tape  

**Results:**
- "You switch to using **yoga mats** made of **eco-friendly paper**"  ← Perfect example!
- "You direct management to use **dumbbells** made of **pool noodles**"
- "You require **trainers** to **train clients in groups of 50** or face termination"

### Auto Services Example

**essential_item**: jack stands, torque wrenches, brake fluid, engine oil  
**absurd_material**: wooden blocks, eyeball measurements, water, cooking oil  
**extreme_measure**: work on cars in the parking lot, eyeball all measurements, hammer it until it fits  

**Results:**
- "You direct management to use **engine oil** made of **cooking oil**"
- "You direct management to use **jack stands** made of **wooden blocks**"
- "You require **mechanics** to **hammer it until it fits** or face termination"

---

## Real Generated Examples

From actual test runs:

### Food & Beverage (High Intensity)
1. "You require kitchen staff to share tips with management or face termination"
2. "You direct management to use cooking pots made of compressed tofu"
3. "You replace all stoves with hot plates from Goodwill"

### Healthcare (High Intensity)
1. "You replace all ultrasounds with equipment borrowed from veterinarians"
2. "You require doctors to diagnose without examining patients or face termination"
3. "You direct management to use syringes made of recycled plastic"

### Personal Services (High Intensity)
1. "You direct management to use combs made of pool noodles"
2. "You replace all styling chairs with yoga mats on the floor"
3. "You direct management to use dumbbells made of plastic"

### Auto Services (High Intensity)
1. "You direct management to use engine oil made of water"
2. "You require mechanics to hammer it until it fits or face termination"
3. "You replace all hydraulic lifts with floor jacks and prayers"

---

## Variable Categories

Each sector defines these variable types:

**Equipment/Materials:**
- `production_input` - Basic items used daily
- `premium_item` - High-quality options
- `equipment` - Major equipment
- `essential_item` - Critical items
- `important_equipment` - Key machinery

**Substitutes:**
- `inferior_material` - Cheap alternatives
- `absurd_material` - Ridiculous substitutes
- `cheap_alternative` - Lower-quality options
- `ridiculous_substitute` - Absurd replacements

**Actions:**
- `cost_cutting_action` - Minor cuts
- `degrading_action` - Equipment misuse
- `unreasonable_demand` - Staff requirements
- `extreme_measure` - Desperate actions

**Context:**
- `luxury_item` - Nice-to-haves
- `staff_type` - Employee categories
- `workers` - Labor categories
- `obvious_problem` - Negative consequences
- `substandard_practice` - Poor practices

---

## Adding New Templates

### 1. Add Template to JSON

Edit `/data/narratives.json`:

```json
{
  "narrative_templates": {
    "low_intensity": [
      "Your new template with {placeholder}"
    ]
  }
}
```

### 2. Add Variables for Each Sector

```json
{
  "template_variables": {
    "Your Sector": {
      "placeholder": ["option1", "option2", "option3"]
    }
  }
}
```

### 3. Test It

Run the game and check for variety!

---

## Technical Implementation

### Template Substitution

```python
def substitute_template(template: str, variables: Dict[str, List[str]]) -> str:
    """Replace {placeholders} with random choices from variables."""
    result = template
    placeholders = re.findall(r'\{(\w+)\}', template)
    
    for placeholder in placeholders:
        if placeholder in variables:
            replacement = random.choice(variables[placeholder])
            result = result.replace(f'{{{placeholder}}}', replacement, 1)
    
    return result
```

### Selection Logic

```python
# 50% chance to use template, 50% chance to use static
use_template = random.random() < 0.5

if use_template and sector in template_variables:
    template = random.choice(templates[intensity_level])
    return substitute_template(template, variables[sector])
else:
    return random.choice(static_narratives[intensity_level])
```

---

## Advantages

### Infinite Variety
- Static: 4-6 options per sector/intensity = ~200 total narratives
- Templates: 3-4 templates × 6-8 variables × 10 sectors = **thousands** of combinations!

### Sector-Appropriate
- Each substitution makes sense for that industry
- "Yoga mats made of eco-friendly paper" only appears for Personal Services
- "Equipment borrowed from veterinarians" only for Healthcare

### Maintains Quality
- Templates ensure grammatical correctness
- Variables curated for humor and appropriateness
- 50/50 mix preserves hand-crafted narratives

### Easy Expansion
- Add variables without writing full narratives
- One template works across all sectors
- Community can contribute variables easily

---

## Future Enhancements

### More Template Types

**Capex Investment:**
```
"You invest in {new_equipment} to improve {business_aspect}"
→ "You invest in state-of-the-art ovens to improve food quality"
```

**Management Replacement:**
```
"You fire {old_manager_type} and hire {new_manager_type}"
→ "You fire the incompetent CEO and hire a turnaround specialist"
```

**Growth Strategies:**
```
"You acquire {number} {business_type} to create {strategy_result}"
→ "You acquire 3 competing pizza shops to create economies of scale"
```

### Dynamic Consequences

Match consequences to specific actions:
```
Action: "using yoga mats made of eco-friendly paper"
Consequence: "Clients slip and slide during downward dog poses"
```

---

## Summary

The template system adds **massive variety** to the narrative experience:

✅ **Thousands of combinations** instead of hundreds  
✅ **Sector-specific humor** (yoga mats of eco-friendly paper!)  
✅ **Maintains quality** with 50/50 static/template mix  
✅ **Easy to expand** - just add variables  
✅ **Grammatically correct** - templates ensure structure  
✅ **Hilarious results** - unexpected combinations are comedy gold  

Every playthrough will have unique, memorable stories!

---

**Version**: 2.2  
**Added**: November 29, 2025  
**File**: `/data/narratives.json`  
**Code**: `/simulation/narratives.py`

