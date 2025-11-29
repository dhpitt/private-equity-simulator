"""
Portfolio operations - actions that can be taken on portfolio companies.
"""

from typing import Dict, Any
import random
import config


def apply_cost_cutting(company: 'Company', intensity: float = 0.5) -> Dict[str, Any]:
    """
    Apply cost-cutting measures to improve margins.
    
    Args:
        company: Company to apply cost-cutting to
        intensity: Intensity of cost-cutting (0-1 scale)
        
    Returns:
        Dictionary with results
    """
    # Cost cutting improves margins but may hurt growth
    max_margin_improvement = config.COST_CUTTING_MAX_IMPACT * intensity
    margin_improvement = random.uniform(0, max_margin_improvement)
    
    # Growth penalty (aggressive cost cutting hurts growth)
    growth_penalty = intensity * 0.02  # Up to -2% growth
    
    # Apply changes
    old_margin = company.ebitda_margin
    company.ebitda_margin = min(0.50, company.ebitda_margin + margin_improvement)
    company.growth_rate -= growth_penalty
    
    # Chance of negative morale impact
    if intensity > 0.7 and random.random() < 0.3:
        additional_growth_penalty = 0.01
        company.growth_rate -= additional_growth_penalty
        morale_impact = True
    else:
        morale_impact = False
        
    return {
        'success': True,
        'margin_improvement': company.ebitda_margin - old_margin,
        'growth_penalty': growth_penalty,
        'morale_impact': morale_impact,
        'message': f"Margins improved by {(company.ebitda_margin - old_margin):.1%}"
    }


def apply_capex_investment(company: 'Company', amount: float) -> Dict[str, Any]:
    """
    Invest in capex to boost growth.
    
    Args:
        company: Company to invest in
        amount: Investment amount
        
    Returns:
        Dictionary with results
    """
    # Convert investment amount to growth boost
    # Rough heuristic: $1M investment per $10M revenue = 0.5% growth boost
    revenue_ratio = amount / company.revenue
    growth_boost = revenue_ratio * 0.05
    growth_boost = min(growth_boost, config.CAPEX_BOOST_MAX_IMPACT)
    
    # Add some randomness to effectiveness
    effectiveness = random.uniform(0.7, 1.3)
    actual_growth_boost = growth_boost * effectiveness
    
    old_growth = company.growth_rate
    company.growth_rate += actual_growth_boost
    
    return {
        'success': True,
        'growth_boost': actual_growth_boost,
        'effectiveness': effectiveness,
        'message': f"Growth rate increased by {actual_growth_boost:.1%}"
    }


def replace_management(company: 'Company', player: 'Player') -> Dict[str, Any]:
    """
    Replace company management team.
    
    Args:
        company: Company to replace management
        player: Player (for cost and reputation effects)
        
    Returns:
        Dictionary with results
    """
    from models.manager import Manager
    
    cost = config.MANAGER_REPLACEMENT_COST
    
    # Check if player can afford it
    if player.cash < cost:
        return {
            'success': False,
            'message': "Insufficient cash for management replacement."
        }
        
    # Factor in current manager's cooperativeness
    old_manager = company.manager
    difficulty = old_manager.get_negotiation_difficulty()
    
    # Difficult managers may cost more or hurt reputation
    if difficulty > 0.7 and random.random() < 0.5:
        additional_cost = cost * 0.5
        cost += additional_cost
        player.adjust_reputation(-0.05)
        difficult = True
    else:
        difficult = False
        
    # Deduct cost
    player.adjust_cash(-cost)
    
    # Generate new manager
    new_manager = Manager()
    company.manager = new_manager
    
    # Transition period: temporary growth penalty
    transition_penalty = random.uniform(0.01, 0.03)
    company.growth_rate -= transition_penalty
    
    return {
        'success': True,
        'cost': cost,
        'old_manager': old_manager,
        'new_manager': new_manager,
        'transition_penalty': transition_penalty,
        'difficult': difficult,
        'message': f"Management replaced. Cost: ${cost:,.0f}"
    }


def pursue_acquisition_strategy(company: 'Company', strategy_type: str) -> Dict[str, Any]:
    """
    Pursue a specific growth strategy (roll-up, expansion, etc).
    
    Args:
        company: Company to apply strategy to
        strategy_type: Type of strategy ('roll_up', 'expand', 'diversify')
        
    Returns:
        Dictionary with results
    """
    if strategy_type == 'roll_up':
        # Buy competitors to consolidate market
        revenue_boost = random.uniform(0.10, 0.25)
        margin_boost = random.uniform(0.02, 0.05)  # Synergies
        
        company.revenue *= (1 + revenue_boost)
        company.ebitda_margin += margin_boost
        company.ebitda_margin = min(0.50, company.ebitda_margin)
        
        return {
            'success': True,
            'revenue_boost': revenue_boost,
            'margin_boost': margin_boost,
            'message': f"Roll-up strategy: Revenue +{revenue_boost:.1%}, Margin +{margin_boost:.1%}"
        }
        
    elif strategy_type == 'expand':
        # Geographic or market expansion
        growth_boost = random.uniform(0.02, 0.05)
        upfront_cost_ratio = 0.10  # Costs 10% of revenue upfront
        
        company.growth_rate += growth_boost
        cost = company.revenue * upfront_cost_ratio
        
        return {
            'success': True,
            'growth_boost': growth_boost,
            'cost': cost,
            'message': f"Expansion strategy: Growth +{growth_boost:.1%}, Cost ${cost:,.0f}"
        }
        
    elif strategy_type == 'diversify':
        # Diversify revenue streams (reduces volatility)
        volatility_reduction = random.uniform(0.02, 0.05)
        
        old_volatility = company.volatility
        company.volatility = max(0.02, company.volatility - volatility_reduction)
        
        # Slight margin improvement from diversification
        margin_boost = random.uniform(0.0, 0.02)
        company.ebitda_margin += margin_boost
        company.ebitda_margin = min(0.50, company.ebitda_margin)
        
        return {
            'success': True,
            'volatility_reduction': old_volatility - company.volatility,
            'margin_boost': margin_boost,
            'message': f"Diversification: Reduced risk, Margin +{margin_boost:.1%}"
        }
        
    return {
        'success': False,
        'message': "Unknown strategy type"
    }


def implement_value_creation_plan(
    company: 'Company',
    player: 'Player',
    plan: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Implement a comprehensive value creation plan.
    
    Args:
        company: Company to improve
        player: Player
        plan: Dictionary specifying plan details
        
    Returns:
        Dictionary with cumulative results
    """
    results = []
    total_cost = 0
    
    if plan.get('cost_cutting'):
        result = apply_cost_cutting(company, plan['cost_cutting'])
        results.append(result)
        
    if plan.get('capex_amount'):
        if player.cash >= plan['capex_amount']:
            player.adjust_cash(-plan['capex_amount'])
            total_cost += plan['capex_amount']
            result = apply_capex_investment(company, plan['capex_amount'])
            results.append(result)
            
    if plan.get('replace_management'):
        result = replace_management(company, player)
        if result['success']:
            total_cost += result['cost']
        results.append(result)
        
    if plan.get('strategy'):
        result = pursue_acquisition_strategy(company, plan['strategy'])
        if result.get('cost'):
            if player.cash >= result['cost']:
                player.adjust_cash(-result['cost'])
                total_cost += result['cost']
        results.append(result)
        
    return {
        'success': True,
        'total_cost': total_cost,
        'results': results,
        'message': f"Value creation plan implemented. Total cost: ${total_cost:,.0f}"
    }

