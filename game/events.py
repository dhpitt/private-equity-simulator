"""
Events - random events that affect companies, players, or markets.
"""

import random
from typing import Dict, Any, List, Optional
from models.company import Company
from models.player import Player
from models.market import Market
from simulation.procedural_gen import generate_event_description
import config


def generate_event(player: Player, portfolio: List[Company], market: Market) -> Optional[Dict[str, Any]]:
    """
    Generate a random event.
    
    Args:
        player: Player object
        portfolio: List of portfolio companies
        market: Market object
        
    Returns:
        Event dictionary or None if no event
    """
    # Check if event occurs
    if random.random() > config.EVENT_PROBABILITY:
        return None
        
    # Determine event type
    event_types = [
        'market_shift',
        'company_operational',
        'company_crisis',
        'company_breakthrough',
        'management_issue',
        'regulatory',
        'market_crash',
        'market_boom'
    ]
    
    # Crisis events are rarer
    if random.random() < config.CRISIS_PROBABILITY:
        event_type = random.choice(['company_crisis', 'market_crash', 'management_issue'])
    else:
        event_type = random.choice(event_types)
        
    # Generate event based on type
    if event_type == 'market_shift':
        return _generate_market_shift_event(market)
    elif event_type == 'market_crash':
        return _generate_market_crash_event(market)
    elif event_type == 'market_boom':
        return _generate_market_boom_event(market)
    elif event_type in ['company_operational', 'company_crisis', 'company_breakthrough']:
        if portfolio:
            company = random.choice(portfolio)
            if event_type == 'company_operational':
                return _generate_operational_event(company)
            elif event_type == 'company_crisis':
                return _generate_crisis_event(company)
            else:
                return _generate_breakthrough_event(company)
    elif event_type == 'management_issue':
        if portfolio:
            company = random.choice(portfolio)
            return _generate_management_event(company, player)
    elif event_type == 'regulatory':
        if portfolio:
            company = random.choice(portfolio)
            return _generate_regulatory_event(company)
            
    return None


def apply_event(event: Dict[str, Any]) -> None:
    """
    Apply an event's effects.
    
    Args:
        event: Event dictionary with effects
    """
    if event is None:
        return
        
    # Event application is handled by the objects themselves
    # This function is mainly for logging/tracking
    pass


def _generate_market_shift_event(market: Market) -> Dict[str, Any]:
    """Generate a market shift event."""
    shift_size = random.uniform(-0.03, 0.03)
    
    return {
        'type': 'market_shift',
        'title': 'Market Conditions Shift',
        'description': generate_event_description('market_crash' if shift_size < 0 else 'market_boom'),
        'effects': {
            'market_growth_change': shift_size,
            'interest_rate_change': random.uniform(-0.01, 0.01)
        },
        'target': market
    }


def _generate_market_crash_event(market: Market) -> Dict[str, Any]:
    """Generate a market crash event."""
    severity = random.uniform(0.10, 0.30)
    
    return {
        'type': 'market_crash',
        'title': 'Market Crash!',
        'description': generate_event_description('market_crash'),
        'effects': {
            'market_growth_change': -severity,
            'multiple_compression': random.uniform(0.10, 0.20),
            'credit_tightening': random.uniform(0.10, 0.30)
        },
        'target': market,
        'severity': severity
    }


def _generate_market_boom_event(market: Market) -> Dict[str, Any]:
    """Generate a market boom event."""
    strength = random.uniform(0.05, 0.15)
    
    return {
        'type': 'market_boom',
        'title': 'Market Boom!',
        'description': generate_event_description('market_boom'),
        'effects': {
            'market_growth_change': strength,
            'multiple_expansion': random.uniform(0.05, 0.15),
            'credit_easing': random.uniform(0.05, 0.15)
        },
        'target': market,
        'strength': strength
    }


def _generate_operational_event(company: Company) -> Dict[str, Any]:
    """Generate an operational event for a company."""
    impact = random.uniform(-0.10, 0.10)
    
    if impact < 0:
        title = "Operational Challenges"
        description = generate_event_description('operational_crisis', company.name)
    else:
        title = "Operational Improvements"
        description = f"{company.name} implements successful operational initiatives."
        
    return {
        'type': 'operational',
        'title': title,
        'description': description,
        'effects': {
            'revenue_impact': impact,
            'margin_impact': impact * 0.5
        },
        'target': company
    }


def _generate_crisis_event(company: Company) -> Dict[str, Any]:
    """Generate a crisis event for a company."""
    severity = random.uniform(0.15, 0.40)
    
    crisis_types = [
        "Product recall forces major operational changes.",
        "Cyber attack disrupts operations and damages reputation.",
        "Key customer bankruptcy impacts revenue.",
        "Natural disaster affects production facilities.",
        "Major lawsuit threatens financial stability."
    ]
    
    description = f"{company.name}: {random.choice(crisis_types)}"
    
    return {
        'type': 'crisis',
        'title': f'CRISIS: {company.name}',
        'description': description,
        'effects': {
            'revenue_impact': -severity,
            'margin_impact': -severity * 0.3,
            'growth_impact': -0.03
        },
        'target': company,
        'severity': severity
    }


def _generate_breakthrough_event(company: Company) -> Dict[str, Any]:
    """Generate a breakthrough event for a company."""
    magnitude = random.uniform(0.10, 0.30)
    
    breakthrough_types = [
        "Wins major contract with Fortune 500 company.",
        "Launches innovative product that captures market attention.",
        "Secures strategic partnership with industry leader.",
        "Achieves technological breakthrough.",
        "Successfully enters high-growth market segment."
    ]
    
    description = f"{company.name}: {random.choice(breakthrough_types)}"
    
    return {
        'type': 'breakthrough',
        'title': f'Breakthrough: {company.name}',
        'description': description,
        'effects': {
            'revenue_impact': magnitude * 0.5,
            'growth_impact': 0.02,
            'margin_impact': magnitude * 0.2
        },
        'target': company,
        'magnitude': magnitude
    }


def _generate_management_event(company: Company, player: Player) -> Dict[str, Any]:
    """Generate a management-related event."""
    event_severity = random.uniform(0.0, 1.0)
    
    if event_severity < 0.3:
        # Minor dispute
        description = generate_event_description('management_dispute', company.name)
        growth_impact = -0.01
    elif event_severity < 0.7:
        # Moderate issue
        description = f"{company.name}: Management team demands higher compensation and more autonomy."
        growth_impact = -0.02
    else:
        # Major crisis
        description = f"{company.name}: CEO threatens to leave unless given equity stake."
        growth_impact = -0.03
        
    return {
        'type': 'management',
        'title': f'Management Issue: {company.name}',
        'description': description,
        'effects': {
            'growth_impact': growth_impact,
            'requires_action': event_severity > 0.5
        },
        'target': company,
        'severity': event_severity
    }


def _generate_regulatory_event(company: Company) -> Dict[str, Any]:
    """Generate a regulatory event."""
    impact = random.uniform(-0.15, 0.05)  # Usually negative
    
    if impact < 0:
        description = generate_event_description('regulatory', company.name)
    else:
        description = f"{company.name}: Regulatory changes create new opportunities."
        
    return {
        'type': 'regulatory',
        'title': f'Regulatory Change: {company.name}',
        'description': description,
        'effects': {
            'margin_impact': impact,
            'one_time_cost': abs(impact) * company.revenue * 0.1 if impact < 0 else 0
        },
        'target': company,
        'impact': impact
    }


def resolve_event_with_player_choice(event: Dict[str, Any], player_choice: str) -> Dict[str, Any]:
    """
    Resolve an event based on player's choice.
    
    Args:
        event: Event dictionary
        player_choice: Player's chosen response
        
    Returns:
        Updated event with resolution results
    """
    # Placeholder for event resolution logic
    # This would be expanded with specific choices for each event type
    
    results = {
        'choice_made': player_choice,
        'outcome': 'Event resolved.'
    }
    
    event['resolution'] = results
    return event

