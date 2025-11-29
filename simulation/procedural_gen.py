"""
Procedural generation for companies, managers, and content.
"""

import random
import json
import os
from typing import Dict, List
from models.company import Company
from models.manager import Manager
import config


def load_data_file(filename: str) -> Dict:
    """Load a JSON data file from the data directory."""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return defaults if file doesn't exist yet
        return {}


def get_sectors() -> List[str]:
    """Get list of available sectors."""
    data = load_data_file('sectors.json')
    return data.get('sectors', [
        'Technology', 'Healthcare', 'Consumer', 'Industrial',
        'Financial Services', 'Energy', 'Real Estate', 'Retail'
    ])


def get_company_names() -> Dict[str, List[str]]:
    """Get company name components."""
    data = load_data_file('names.json')
    return data.get('company_names', {
        'prefixes': ['Advanced', 'Global', 'Premier', 'United', 'National', 'Metro',
                    'Apex', 'Prime', 'Elite', 'Summit', 'Vertex', 'Optimal'],
        'roots': ['Tech', 'Systems', 'Solutions', 'Industries', 'Services', 'Group',
                 'Dynamics', 'Innovations', 'Ventures', 'Partners', 'Holdings', 'Corp'],
        'suffixes': ['Inc', 'LLC', 'Co', 'Ltd', 'International', 'Enterprises']
    })


def generate_company_name(sector: str = None) -> str:
    """Generate a random company name."""
    names = get_company_names()
    
    prefix = random.choice(names.get('prefixes', ['Global']))
    root = random.choice(names.get('roots', ['Industries']))
    
    # Sometimes add suffix
    if random.random() > 0.5:
        suffix = random.choice(names.get('suffixes', ['Inc']))
        return f"{prefix} {root} {suffix}"
    else:
        return f"{prefix} {root}"


def generate_company(sector: str = None) -> Company:
    """
    Generate a random company with realistic attributes.
    
    Args:
        sector: Specific sector (or None for random)
        
    Returns:
        Generated Company object
    """
    # Choose sector
    if sector is None:
        sector = random.choice(get_sectors())
        
    # Generate name
    name = generate_company_name(sector)
    
    # Generate financials
    revenue = random.uniform(config.MIN_COMPANY_REVENUE, config.MAX_COMPANY_REVENUE)
    ebitda_margin = random.uniform(config.MIN_EBITDA_MARGIN, config.MAX_EBITDA_MARGIN)
    growth_rate = random.uniform(config.MIN_GROWTH_RATE, config.MAX_GROWTH_RATE)
    
    # Sector-specific adjustments
    sector_adjustments = {
        'Technology': {'margin_boost': 0.05, 'growth_boost': 0.02},
        'Healthcare': {'margin_boost': 0.03, 'growth_boost': 0.01},
        'Consumer': {'margin_boost': 0.0, 'growth_boost': 0.0},
        'Industrial': {'margin_boost': -0.02, 'growth_boost': 0.0},
        'Financial Services': {'margin_boost': 0.08, 'growth_boost': 0.01},
        'Energy': {'margin_boost': -0.03, 'growth_boost': -0.01},
        'Real Estate': {'margin_boost': 0.02, 'growth_boost': 0.0},
        'Retail': {'margin_boost': -0.05, 'growth_boost': 0.01},
    }
    
    adjustments = sector_adjustments.get(sector, {'margin_boost': 0.0, 'growth_boost': 0.0})
    ebitda_margin = max(0.05, min(0.50, ebitda_margin + adjustments['margin_boost']))
    growth_rate += adjustments['growth_boost']
    
    # Generate manager
    manager = Manager()
    
    # Create company
    company = Company(
        name=name,
        sector=sector,
        revenue=revenue,
        ebitda_margin=ebitda_margin,
        growth_rate=growth_rate,
        manager=manager
    )
    
    return company


def generate_deal_portfolio(num_companies: int, market: 'Market' = None) -> List[Company]:
    """
    Generate a portfolio of companies available for acquisition.
    
    Args:
        num_companies: Number of companies to generate
        market: Market object for valuation
        
    Returns:
        List of Company objects
    """
    companies = []
    sectors = get_sectors()
    
    for _ in range(num_companies):
        sector = random.choice(sectors)
        company = generate_company(sector)
        
        # Calculate valuation
        if market:
            company.calculate_valuation(market)
        else:
            # Use default multiple
            default_multiple = (config.MIN_EBITDA_MULTIPLE + config.MAX_EBITDA_MULTIPLE) / 2
            company.current_valuation = company.ebitda * default_multiple
            
        companies.append(company)
        
    return companies


def generate_manager() -> Manager:
    """Generate a random manager."""
    return Manager()


def generate_event_description(event_type: str, company_name: str = None) -> str:
    """
    Generate a narrative description for an event.
    
    Args:
        event_type: Type of event
        company_name: Company affected (if applicable)
        
    Returns:
        Event description string
    """
    descriptions = {
        'market_crash': [
            "Global markets tumble as recession fears mount.",
            "Economic downturn spreads across sectors.",
            "Market volatility spikes amid uncertainty."
        ],
        'market_boom': [
            "Markets rally on strong economic data.",
            "Bull market continues with broad gains.",
            "Investor confidence reaches new highs."
        ],
        'operational_crisis': [
            f"{company_name} faces major operational disruption.",
            f"Supply chain issues plague {company_name}.",
            f"{company_name} experiences significant quality problems."
        ],
        'breakthrough': [
            f"{company_name} announces major innovation.",
            f"{company_name} secures game-changing contract.",
            f"{company_name} expands into lucrative new market."
        ],
        'management_dispute': [
            f"Leadership turmoil at {company_name}.",
            f"{company_name}'s management team clashes over strategy.",
            f"Key executives threaten to leave {company_name}."
        ],
        'regulatory': [
            f"New regulations impact {company_name}'s operations.",
            f"{company_name} faces regulatory investigation.",
            f"Compliance costs surge for {company_name}."
        ]
    }
    
    options = descriptions.get(event_type, [f"Event occurred at {company_name}"])
    return random.choice(options)


def generate_market_sector_shock(sectors: List[str]) -> Dict[str, float]:
    """
    Generate a random shock affecting specific sectors.
    
    Args:
        sectors: List of all sectors
        
    Returns:
        Dictionary mapping sector to impact multiplier
    """
    # Pick 1-3 sectors to be affected
    affected_sectors = random.sample(sectors, k=random.randint(1, 3))
    
    shock_map = {sector: 1.0 for sector in sectors}  # Default: no impact
    
    for sector in affected_sectors:
        # Impact can be positive or negative
        impact = random.uniform(-0.30, 0.30)
        shock_map[sector] = 1.0 + impact
        
    return shock_map

