"""
Narrative generator for business operations.
Creates sector-specific stories for cost-cutting and other actions.
Supports both static narratives and template-based random generation.
"""

import random
import json
import os
from pathlib import Path
from typing import Dict, List, Optional


def load_narratives() -> Dict:
    """Load narrative data from JSON file."""
    data_path = Path(__file__).parent.parent / 'data' / 'narratives.json'
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'cost_cutting_narratives': {}, 'narrative_templates': {}, 'template_variables': {}}


def substitute_template(template: str, variables: Dict[str, List[str]]) -> str:
    """
    Substitute placeholders in a template with random choices from variables.
    
    Args:
        template: Template string with {placeholder} markers
        variables: Dictionary mapping placeholder names to lists of options
        
    Returns:
        String with all placeholders replaced
    """
    result = template
    
    # Find all placeholders in the template
    import re
    placeholders = re.findall(r'\{(\w+)\}', template)
    
    # Replace each placeholder with a random choice
    for placeholder in placeholders:
        if placeholder in variables:
            replacement = random.choice(variables[placeholder])
            result = result.replace(f'{{{placeholder}}}', replacement, 1)
    
    return result


def get_cost_cutting_narrative(sector: str, intensity: float) -> str:
    """
    Get a sector-specific cost-cutting narrative based on intensity.
    Now with template-based random generation!
    
    Args:
        sector: Company sector
        intensity: Cost-cutting intensity (0-1 scale)
        
    Returns:
        Narrative string describing the cost-cutting measure
    """
    narratives_data = load_narratives()
    sector_narratives = narratives_data.get('cost_cutting_narratives', {}).get(sector, {})
    
    # Determine intensity level
    if intensity < 0.33:
        level = 'low_intensity'
    elif intensity < 0.67:
        level = 'medium_intensity'
    else:
        level = 'high_intensity'
    
    # 50% chance to use template, 50% chance to use static narrative
    use_template = random.random() < 0.5
    
    if use_template and sector in narratives_data.get('template_variables', {}):
        # Use template-based generation
        templates = narratives_data.get('narrative_templates', {}).get(level, [])
        if templates:
            template = random.choice(templates)
            variables = narratives_data['template_variables'][sector]
            return substitute_template(template, variables)
    
    # Fall back to static narratives
    static_options = sector_narratives.get(level, [])
    
    if static_options:
        return random.choice(static_options)
    
    # Ultimate fallback to generic
    return get_generic_cost_cutting_narrative(intensity)


def get_generic_cost_cutting_narrative(intensity: float) -> str:
    """Fallback generic cost-cutting narratives."""
    if intensity < 0.33:
        options = [
            "You negotiate better rates with suppliers",
            "You implement energy-saving measures",
            "You reduce discretionary spending",
            "You renegotiate service contracts"
        ]
    elif intensity < 0.67:
        options = [
            "You reduce staff through attrition",
            "You eliminate non-essential positions",
            "You cut employee benefits",
            "You reduce operational hours"
        ]
    else:
        options = [
            "You implement aggressive layoffs",
            "You cut wages across the board",
            "You eliminate most employee benefits",
            "You drastically reduce quality standards"
        ]
    
    return random.choice(options)


def get_cost_cutting_consequence(sector: str, intensity: float) -> Dict[str, str]:
    """
    Get the narrative and consequence message for cost-cutting.
    
    Args:
        sector: Company sector
        intensity: Cost-cutting intensity (0-1 scale)
        
    Returns:
        Dictionary with 'action' and 'consequence' keys
    """
    narrative = get_cost_cutting_narrative(sector, intensity)
    
    # Generate consequence based on intensity
    if intensity < 0.33:
        consequences = [
            "Employees grumble but accept the changes",
            "Minor efficiency losses but margins improve",
            "Some customers notice but don't complain",
            "Short-term pain for long-term gain"
        ]
    elif intensity < 0.67:
        consequences = [
            "Employee morale drops noticeably",
            "Some customers start complaining",
            "Quality metrics show slight decline",
            "Turnover increases among skilled workers",
            "Operations become noticeably more strained"
        ]
    else:
        consequences = [
            "Mass employee exodus begins",
            "Customer complaints surge dramatically",
            "Quality plummets - reviews turn negative",
            "Risk of regulatory violations increases",
            "Long-term damage to brand reputation",
            "Several key employees quit immediately"
        ]
    
    consequence = random.choice(consequences)
    
    return {
        'action': narrative,
        'consequence': consequence
    }


def format_cost_cutting_message(company_name: str, sector: str, intensity: float, 
                                margin_improvement: float) -> str:
    """
    Format a complete cost-cutting message with narrative.
    
    Args:
        company_name: Name of the company
        sector: Company sector
        intensity: Cost-cutting intensity (0-1 scale)
        margin_improvement: Actual margin improvement percentage
        
    Returns:
        Formatted multi-line message
    """
    result = get_cost_cutting_consequence(sector, intensity)
    
    message = f"\n{'='*70}\n"
    message += f"COST-CUTTING INITIATIVE: {company_name}\n"
    message += f"{'='*70}\n\n"
    message += f"ACTION TAKEN:\n"
    message += f"  {result['action']}\n\n"
    message += f"IMMEDIATE CONSEQUENCE:\n"
    message += f"  {result['consequence']}\n\n"
    message += f"FINANCIAL IMPACT:\n"
    message += f"  EBITDA Margin improved by {margin_improvement:+.1%}\n"
    
    # Add risk warning for high intensity
    if intensity > 0.7:
        message += f"\n⚠️  WARNING: Aggressive cost-cutting may have long-term consequences!\n"
    
    message += f"\n{'='*70}\n"
    
    return message

