"""
Manager system - narratives and hiring mechanics.
"""

import json
import random
from typing import Dict, List, Tuple, Any
from pathlib import Path
from models.manager import Manager


def load_manager_narratives() -> Dict[str, Any]:
    """Load manager narrative templates from JSON."""
    narratives_path = Path(__file__).parent.parent / 'data' / 'manager_narratives.json'
    
    try:
        with open(narratives_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find manager_narratives.json at {narratives_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse manager_narratives.json: {e}")
        return {}


def get_quarterly_performance_narrative(company: 'Company', manager_impact: float, growth: float) -> str:
    """
    Generate narrative explaining how the manager's attributes affected quarterly performance.
    
    Args:
        company: The company
        manager_impact: The manager's performance modifier this quarter
        growth: The total growth this quarter
        
    Returns:
        Narrative string explaining manager impact
    """
    narratives = load_manager_narratives()
    manager = company.manager
    
    # Determine manager's performance category
    if manager.competence >= 0.75 and manager_impact > 0.03:
        category = "high_competence_positive"
    elif manager.competence >= 0.65 and abs(manager_impact) < 0.02:
        category = "high_competence_neutral"
    elif manager.competence < 0.45 and manager_impact < -0.02:
        category = "low_competence_negative"
    elif manager.risk_profile > 0.7 and manager_impact > 0.04:
        category = "high_risk_success"
    elif manager.risk_profile > 0.7 and manager_impact < -0.04:
        category = "high_risk_failure"
    elif manager.cooperativeness < 0.4 and random.random() < 0.3:
        category = "low_cooperativeness_issue"
    else:
        return None  # No notable narrative this quarter
    
    templates = narratives.get('quarterly_performance', {}).get(category, [])
    if not templates:
        return None
    
    template = random.choice(templates)
    return template.format(manager=manager.name)


def get_firing_narrative(old_manager: Manager) -> str:
    """
    Generate narrative for firing a manager.
    
    Args:
        old_manager: The manager being fired
        
    Returns:
        Narrative string
    """
    narratives = load_manager_narratives()
    
    # Base narrative on cooperativeness
    if old_manager.cooperativeness > 0.7:
        category = "cooperative"
    else:
        category = "uncooperative"
    
    templates = narratives.get('firing', {}).get(category, [])
    base_narrative = random.choice(templates).format(old_manager=old_manager.name)
    
    # Add secondary narrative based on competence
    if old_manager.competence >= 0.7:
        secondary_templates = narratives.get('firing', {}).get('competent_loss', [])
    else:
        secondary_templates = narratives.get('firing', {}).get('incompetent_relief', [])
    
    if secondary_templates and random.random() < 0.6:
        secondary = random.choice(secondary_templates).format(old_manager=old_manager.name)
        return f"{base_narrative}\n\n{secondary}"
    
    return base_narrative


def get_hiring_narrative(new_manager: Manager) -> str:
    """
    Generate narrative for hiring a new manager.
    
    Args:
        new_manager: The newly hired manager
        
    Returns:
        Narrative string
    """
    narratives = load_manager_narratives()
    
    # Determine primary characteristic to highlight
    if new_manager.competence >= 0.75:
        category = "high_competence"
    elif new_manager.competence < 0.5:
        category = "low_competence"
    elif new_manager.risk_profile >= 0.7:
        category = "high_risk"
    elif new_manager.cooperativeness >= 0.75:
        category = "high_cooperativeness"
    elif new_manager.cooperativeness < 0.4:
        category = "low_cooperativeness"
    else:
        # Default to competence-based
        category = "high_competence" if new_manager.competence > 0.6 else "low_competence"
    
    templates = narratives.get('hiring', {}).get(category, [])
    if not templates:
        return f"You've hired {new_manager.name} as the new manager."
    
    template = random.choice(templates)
    return template.format(new_manager=new_manager.name)


def generate_manager_candidates(current_manager: Manager, num_candidates: int = 3) -> List[Tuple[str, Manager, str]]:
    """
    Generate multiple manager candidates with different strengths and tradeoffs.
    
    Args:
        current_manager: The current manager (to ensure improvements)
        num_candidates: Number of candidates to generate
        
    Returns:
        List of (archetype_name, Manager, pitch) tuples
    """
    narratives = load_manager_narratives()
    archetypes = narratives.get('candidate_archetypes', {})
    
    if not archetypes:
        # Fallback if no data
        return [(
            "Candidate",
            Manager(),
            "A potential replacement."
        ) for _ in range(num_candidates)]
    
    # Select random archetypes (without replacement)
    archetype_keys = list(archetypes.keys())
    selected = random.sample(archetype_keys, min(num_candidates, len(archetype_keys)))
    
    candidates = []
    for archetype_key in selected:
        archetype = archetypes[archetype_key]
        
        # Generate manager with archetype's attribute ranges
        competence = random.uniform(*archetype['competence_range'])
        risk = random.uniform(*archetype['risk_range'])
        coop = random.uniform(*archetype['coop_range'])
        
        # Ensure at least one attribute is better than current manager
        improvements = []
        if competence > current_manager.competence + 0.1:
            improvements.append(f"Competence +{(competence - current_manager.competence):.0%}")
        if coop > current_manager.cooperativeness + 0.1:
            improvements.append(f"Cooperativeness +{(coop - current_manager.cooperativeness):.0%}")
        
        # If no clear improvement, boost competence to guarantee one
        if not improvements:
            competence = min(0.95, current_manager.competence + random.uniform(0.15, 0.30))
            improvements.append(f"Competence +{(competence - current_manager.competence):.0%}")
        
        manager = Manager(competence=competence, risk_profile=risk, cooperativeness=coop)
        
        # Build pitch with improvements
        pitch = archetype['pitch']
        if improvements:
            pitch += f" ({', '.join(improvements)})"
        
        candidates.append((
            archetype['title'],
            manager,
            pitch
        ))
    
    return candidates


def calculate_transition_impact(old_manager: Manager, new_manager: Manager) -> Dict[str, float]:
    """
    Calculate the impact of management transition.
    
    Args:
        old_manager: The outgoing manager
        new_manager: The incoming manager
        
    Returns:
        Dictionary with impact metrics
    """
    # Base transition penalty
    transition_penalty = random.uniform(0.01, 0.03)
    
    # Cooperativeness affects transition difficulty
    if old_manager.cooperativeness < 0.4:
        # Difficult manager makes transition harder
        transition_penalty += random.uniform(0.01, 0.02)
    
    if new_manager.cooperativeness > 0.7:
        # Cooperative new manager eases transition
        transition_penalty *= 0.7
    
    # Competence delta affects long-term improvement
    competence_delta = new_manager.competence - old_manager.competence
    long_term_improvement = competence_delta * random.uniform(0.015, 0.025)  # 1.5-2.5% per competence point
    
    # Risk profile change affects volatility
    risk_delta = new_manager.risk_profile - old_manager.risk_profile
    volatility_change = risk_delta * 0.05  # ±5% volatility
    
    return {
        'transition_penalty': transition_penalty,
        'long_term_improvement': long_term_improvement,
        'volatility_change': volatility_change,
        'competence_delta': competence_delta
    }

