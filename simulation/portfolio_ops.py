"""
Portfolio operations - actions that can be taken on portfolio companies.
"""

from typing import Dict, Any
import random
import config
from simulation.narratives import get_cost_cutting_consequence


def apply_cost_cutting(company: 'Company', intensity: float = 0.5) -> Dict[str, Any]:
    """
    Apply cost-cutting measures to improve margins.
    Now with narrative consequences!
    
    Args:
        company: Company to apply cost-cutting to
        intensity: Intensity of cost-cutting (0-1 scale)
        
    Returns:
        Dictionary with results including narrative
    """
    # Get sector-specific narrative
    narrative_result = get_cost_cutting_consequence(company.sector, intensity)
    
    # Cost cutting improves margins but may hurt growth
    max_margin_improvement = config.COST_CUTTING_MAX_IMPACT * intensity
    margin_improvement = random.uniform(0, max_margin_improvement)
    
    # Growth penalty (aggressive cost cutting hurts growth)
    growth_penalty = intensity * 0.02  # Up to -2% growth
    
    # Higher intensity = higher risk of additional negative effects
    morale_impact = False
    reputation_hit = 0.0
    
    if intensity > 0.7:
        # High intensity - significant risks
        if random.random() < 0.5:
            additional_growth_penalty = random.uniform(0.01, 0.03)
            growth_penalty += additional_growth_penalty
            morale_impact = True
        
        # Might hurt reputation
        if random.random() < 0.3:
            reputation_hit = random.uniform(0.01, 0.03)
    
    elif intensity > 0.4:
        # Medium intensity - moderate risks
        if random.random() < 0.3:
            additional_growth_penalty = 0.01
            growth_penalty += additional_growth_penalty
            morale_impact = True
    
    # OPERATIONAL HEALTH DAMAGE (long-term viability risk)
    # Cost-cutting damages operational health, making company fragile
    health_damage = intensity * 0.15  # Up to 15% health loss per cut
    
    # Aggressive cutting causes exponentially more damage
    if intensity > 0.7:
        health_damage = intensity * 0.25  # Up to 25% health loss
    
    company.operational_health = max(0.0, company.operational_health - health_damage)
    
    # Apply changes
    old_margin = company.ebitda_margin
    company.ebitda_margin = min(0.50, company.ebitda_margin + margin_improvement)
    company.growth_rate -= growth_penalty
        
    return {
        'success': True,
        'margin_improvement': company.ebitda_margin - old_margin,
        'growth_penalty': growth_penalty,
        'health_damage': health_damage,
        'morale_impact': morale_impact,
        'reputation_hit': reputation_hit,
        'narrative_action': narrative_result['action'],
        'narrative_consequence': narrative_result['consequence'],
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
    
    # HEALTH IMPROVEMENT - investing in the business improves operational health
    # Larger investments relative to revenue = more health improvement
    health_improvement = min(0.15, revenue_ratio * 0.10)  # Up to 15% improvement
    company.operational_health = min(1.0, company.operational_health + health_improvement)
    
    return {
        'success': True,
        'growth_boost': actual_growth_boost,
        'health_improvement': health_improvement,
        'effectiveness': effectiveness,
        'message': f"Growth rate increased by {actual_growth_boost:.1%}. "
                  f"Operational health improved by {health_improvement:.1%}."
    }


def replace_management(company: 'Company', player: 'Player', selected_manager: 'Manager' = None) -> Dict[str, Any]:
    """
    Replace company management team with a selected candidate.
    
    Args:
        company: Company to replace management
        player: Player (for cost and reputation effects)
        selected_manager: The chosen manager (if None, generates random)
        
    Returns:
        Dictionary with results including narratives
    """
    from models.manager import Manager
    from simulation import manager_system
    
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
    
    # Use selected manager or generate random
    new_manager = selected_manager if selected_manager else Manager()
    company.manager = new_manager
    
    # Calculate transition impact
    impact = manager_system.calculate_transition_impact(old_manager, new_manager)
    
    # Apply transition effects
    company.growth_rate -= impact['transition_penalty']
    company.volatility += impact['volatility_change']
    
    # HEALTH IMPROVEMENT - better management can improve operational health
    health_improvement = max(0, impact['competence_delta'] * 0.20)  # Up to 20% if much better
    company.operational_health = min(1.0, company.operational_health + health_improvement)
    
    # Generate narratives
    firing_narrative = manager_system.get_firing_narrative(old_manager)
    hiring_narrative = manager_system.get_hiring_narrative(new_manager)
    
    return {
        'success': True,
        'cost': cost,
        'old_manager': old_manager,
        'new_manager': new_manager,
        'transition_penalty': impact['transition_penalty'],
        'long_term_improvement': impact['long_term_improvement'],
        'volatility_change': impact['volatility_change'],
        'difficult': difficult,
        'health_improvement': health_improvement,
        'firing_narrative': firing_narrative,
        'hiring_narrative': hiring_narrative,
        'message': f"Management transition complete. Growth penalty: -{impact['transition_penalty']:.1%}. "
                  f"{'⚠️ Additional cost due to difficult termination. ' if difficult else ''}"
                  f"Health: {'+' if health_improvement > 0 else ''}{health_improvement:.1%}"
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
        # Buy competitors to consolidate market - EXPENSIVE and RISKY
        num_acquisitions = random.randint(2, 5)
        
        # COST: Acquiring competitors is expensive
        # Cost = 150-200% of current revenue to buy smaller competitors
        cost_multiplier = random.uniform(1.5, 2.0)
        cost = company.revenue * cost_multiplier
        
        # BENEFITS: Revenue and margin improvements
        revenue_boost = random.uniform(0.10, 0.20)  # Reduced from 0.25
        margin_boost = random.uniform(0.01, 0.03)  # Reduced from 0.05
        
        company.revenue *= (1 + revenue_boost)
        company.ebitda_margin += margin_boost
        company.ebitda_margin = min(0.50, company.ebitda_margin)
        
        # RISKS: Integration challenges
        # Increased volatility during integration period
        volatility_increase = random.uniform(0.03, 0.08)
        company.volatility += volatility_increase
        
        # Integration period creates temporary growth drag
        integration_drag = random.uniform(0.01, 0.03)
        company.growth_rate -= integration_drag
        
        # HEALTH: Mixed impact - scale improves some things, integration damages others
        # Net effect is usually slightly positive but not guaranteed
        integration_success = random.random()
        
        if integration_success > 0.7:
            # Smooth integration
            health_improvement = random.uniform(0.03, 0.08)
            company.operational_health = min(1.0, company.operational_health + health_improvement)
            integration_message = "Integration went smoothly."
        elif integration_success > 0.4:
            # Neutral integration
            health_improvement = 0
            integration_message = "Integration proceeded normally."
        else:
            # Rough integration
            health_damage = random.uniform(0.05, 0.10)
            company.operational_health = max(0.0, company.operational_health - health_damage)
            health_improvement = -health_damage
            integration_message = "Integration challenges encountered!"
        
        return {
            'success': True,
            'cost': cost,
            'num_acquisitions': num_acquisitions,
            'revenue_boost': revenue_boost,
            'margin_boost': margin_boost,
            'volatility_increase': volatility_increase,
            'integration_drag': integration_drag,
            'health_improvement': health_improvement,
            'integration_success': integration_success,
            'message': f"Roll-up strategy: Acquired {num_acquisitions} competitors for ${cost:,.0f}. "
                      f"Revenue +{revenue_boost:.1%}, Margin +{margin_boost:.1%}. "
                      f"Volatility +{volatility_increase:.1%} (integration risk). "
                      f"Temporary growth drag -{integration_drag:.1%}. "
                      f"{integration_message}"
        }
        
    elif strategy_type == 'expand':
        # Geographic or market expansion
        growth_boost = random.uniform(0.02, 0.05)
        upfront_cost_ratio = 0.10  # Costs 10% of revenue upfront
        
        company.growth_rate += growth_boost
        cost = company.revenue * upfront_cost_ratio
        
        # HEALTH IMPROVEMENT - expansion strengthens business
        health_improvement = random.uniform(0.03, 0.08)
        company.operational_health = min(1.0, company.operational_health + health_improvement)
        
        return {
            'success': True,
            'growth_boost': growth_boost,
            'health_improvement': health_improvement,
            'cost': cost,
            'message': f"Expansion strategy: Growth +{growth_boost:.1%}, Cost ${cost:,.0f}. "
                      f"Operational health improved by {health_improvement:.1%}."
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

