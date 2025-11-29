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
        'Technology', 'Healthcare', 'Food & Beverage', 'Retail & Consumer',
        'Home Services', 'Auto Services', 'Personal Services', 
        'Professional Services', 'Real Estate', 'Manufacturing'
    ])


def get_sector_business_types(sector: str) -> List[str]:
    """Get business types for a specific sector."""
    data = load_data_file('sectors.json')
    sector_types = data.get('sector_local_business_types', {})
    return sector_types.get(sector, [])


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


def get_local_business_names() -> Dict[str, Any]:
    """Get local business name components."""
    data = load_data_file('names.json')
    return data.get('local_business_names', {
        'prefixes': ['Main Street', 'Downtown', 'City', 'Corner', 'Family', 'Joe\'s',
                    'Mom\'s', 'Bob\'s', 'Quick', 'Best', 'Quality', 'Hometown'],
        'descriptors': ['& Sons', '& Daughters', 'Shop', 'Store', 'Market', 'Emporium',
                       'Company', 'Express', 'Plus', 'Depot', 'Center', 'Outlet']
    })


def get_sector_business_types() -> Dict[str, List[str]]:
    """Get business types organized by sector."""
    data = load_data_file('names.json')
    return data.get('sector_business_types', {
        'Consumer': ['Pizza', 'Deli', 'Bakery', 'Cafe', 'Liquor Store', 'Grocery'],
        'Retail': ['Boutique', 'Electronics', 'Furniture', 'Pet Store'],
        'Healthcare': ['Pharmacy', 'Dental Office', 'Medical Clinic'],
        'Consumer Services': ['Barbershop', 'Hair Salon', 'Dry Cleaners', 'Gym'],
        'Industrial': ['Auto Repair', 'Plumbing', 'HVAC', 'Landscaping'],
        'Real Estate': ['Property Management', 'Real Estate Office'],
        'Technology': ['Computer Repair', 'IT Services', 'Web Design'],
        'Financial Services': ['Insurance Agency', 'Tax Preparation', 'Accounting Services']
    })


def generate_company_name(sector: str = None, style: str = 'corporate') -> str:
    """
    Generate a random company name.
    
    Args:
        sector: Company sector (optional, used for local business names)
        style: 'corporate' for traditional names, 'local' for local business names
    
    Returns:
        Generated company name
    """
    if style == 'local':
        return generate_local_business_name(sector)
    
    # Corporate style names
    names = get_company_names()
    
    prefix = random.choice(names.get('prefixes', ['Global']))
    root = random.choice(names.get('roots', ['Industries']))
    
    # Sometimes add suffix
    if random.random() > 0.5:
        suffix = random.choice(names.get('suffixes', ['Inc']))
        return f"{prefix} {root} {suffix}"
    else:
        return f"{prefix} {root}"


def generate_local_business_name(sector: str = None) -> str:
    """
    Generate a local business style name appropriate for the sector.
    
    Args:
        sector: Business sector to generate name for
    """
    local_names = get_local_business_names()
    sector_types = get_sector_business_types()
    
    # Get business types for this sector, or use generic if sector not found
    if sector and sector in sector_types:
        business_types = sector_types[sector]
    else:
        # Fallback to all business types
        all_types = []
        for types_list in sector_types.values():
            all_types.extend(types_list)
        business_types = all_types
    
    # Multiple styles of local business names
    style_choice = random.choice(['prefix_type', 'type_descriptor', 'possessive_type', 'simple'])
    
    business_type = random.choice(business_types)
    
    if style_choice == 'prefix_type':
        # e.g., "Main Street Pizza"
        prefix = random.choice(local_names.get('prefixes', ['Main Street']))
        return f"{prefix} {business_type}"
    
    elif style_choice == 'type_descriptor':
        # e.g., "Pizza Express", "Hardware Depot"
        descriptor = random.choice(local_names.get('descriptors', ['Store']))
        return f"{business_type} {descriptor}"
    
    elif style_choice == 'possessive_type':
        # e.g., "Joe's Hardware", "Bob's Auto Repair"
        possessive_prefixes = [p for p in local_names.get('prefixes', []) 
                              if '\'' in p or 'Family' in p]
        if not possessive_prefixes:
            possessive_prefixes = ["Joe's", "Mom's", "Tony's", "Family"]
        prefix = random.choice(possessive_prefixes)
        return f"{prefix} {business_type}"
    
    else:  # simple
        # e.g., "Quality Bakery", "Best Cafe"
        simple_prefixes = [p for p in local_names.get('prefixes', []) 
                          if p in ['Quick', 'Best', 'Quality', 'Hometown', 'Premium', 'Elite']]
        if not simple_prefixes:
            simple_prefixes = ["Quality", "Best", "Premium"]
        prefix = random.choice(simple_prefixes)
        return f"{prefix} {business_type}"


def generate_company(sector: str = None, revenue_range: tuple = None, 
                    name_style: str = None) -> Company:
    """
    Generate a random company with realistic attributes.
    
    Args:
        sector: Specific sector (or None for random)
        revenue_range: Tuple of (min_revenue, max_revenue) or None for default
        name_style: 'corporate', 'local', or None for automatic based on size
        
    Returns:
        Generated Company object
    """
    # Choose sector
    if sector is None:
        sector = random.choice(get_sectors())
        
    # Generate financials
    if revenue_range:
        min_rev, max_rev = revenue_range
    else:
        min_rev = config.MIN_COMPANY_REVENUE
        max_rev = config.MAX_COMPANY_REVENUE
    
    revenue = random.uniform(min_rev, max_rev)
    ebitda_margin = random.uniform(config.MIN_EBITDA_MARGIN, config.MAX_EBITDA_MARGIN)
    growth_rate = random.uniform(config.MIN_GROWTH_RATE, config.MAX_GROWTH_RATE)
    
    # Determine name style based on company size if not specified
    if name_style is None:
        # Smaller companies (< $5M revenue) are more likely to have local names
        if revenue < 5_000_000:
            name_style = 'local' if random.random() < 0.7 else 'corporate'
        else:
            name_style = 'corporate' if random.random() < 0.8 else 'local'
    
    # Generate name
    name = generate_company_name(sector, style=name_style)
    
    # Sector-specific adjustments
    sector_adjustments = {
        'Technology': {'margin_boost': 0.05, 'growth_boost': 0.02, 'base_multiple': 12.0},
        'Healthcare': {'margin_boost': 0.03, 'growth_boost': 0.01, 'base_multiple': 11.0},
        'Food & Beverage': {'margin_boost': -0.03, 'growth_boost': 0.0, 'base_multiple': 7.5},
        'Retail & Consumer': {'margin_boost': -0.02, 'growth_boost': 0.01, 'base_multiple': 8.0},
        'Home Services': {'margin_boost': 0.02, 'growth_boost': 0.01, 'base_multiple': 8.5},
        'Auto Services': {'margin_boost': 0.0, 'growth_boost': 0.0, 'base_multiple': 8.0},
        'Personal Services': {'margin_boost': 0.03, 'growth_boost': 0.01, 'base_multiple': 9.0},
        'Professional Services': {'margin_boost': 0.08, 'growth_boost': 0.01, 'base_multiple': 10.0},
        'Real Estate': {'margin_boost': 0.02, 'growth_boost': 0.0, 'base_multiple': 8.5},
        'Manufacturing': {'margin_boost': -0.02, 'growth_boost': 0.0, 'base_multiple': 8.0},
    }
    
    adjustments = sector_adjustments.get(sector, {
        'margin_boost': 0.0, 
        'growth_boost': 0.0, 
        'base_multiple': 9.0
    })
    
    ebitda_margin = max(0.05, min(0.50, ebitda_margin + adjustments['margin_boost']))
    growth_rate += adjustments['growth_boost']
    
    # Generate company-specific valuation multiple from normal distribution
    # around sector mean
    base_multiple = adjustments['base_multiple']
    multiple_std = config.MULTIPLE_STD_DEV
    
    
    # Draw from normal distribution, then clamp to reasonable bounds
    valuation_multiple = random.gauss(base_multiple, multiple_std)
    valuation_multiple = max(config.MIN_EBITDA_MULTIPLE, 
                            min(config.MAX_EBITDA_MULTIPLE, valuation_multiple))
    
    # Generate manager
    manager = Manager()
    
    # Create company
    company = Company(
        name=name,
        sector=sector,
        revenue=revenue,
        ebitda_margin=ebitda_margin,
        growth_rate=growth_rate,
        manager=manager,
        valuation_multiple=valuation_multiple
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

