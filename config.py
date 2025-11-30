"""
Global configuration settings for the PE Simulator game.
"""

# Game Settings
STARTING_CAPITAL = 2_000_000  # $2M (must use debt to acquire)
STARTING_REPUTATION = 0.20  # Start with low reputation (20%)
BASE_DEBT_CAPACITY = 10_000_000  # $10M (base capacity)
GAME_DURATION_QUARTERS = 56  # 14 years

# Debt Capacity Dynamics
DEBT_TO_NET_WORTH_RATIO = 3.0  # Max debt = 3x net worth
REPUTATION_DEBT_MULTIPLIER = 2.0  # Reputation doubles the effect (at max rep)
MIN_DEBT_CAPACITY = 5_000_000  # Always have at least $5M capacity

# Random Seed (None for random, or set a number for reproducibility)
RANDOM_SEED = None

# Market Settings
BASE_INTEREST_RATE = 0.05  # 5%
INTEREST_RATE_VOLATILITY = 0.01  # 1% quarterly volatility
MARKET_GROWTH_RATE = 0.02  # 2% quarterly growth
MARKET_VOLATILITY = 0.05  # 5% volatility

# Company Generation
MIN_COMPANY_REVENUE = 500_000  # $500K (small local businesses)
MAX_COMPANY_REVENUE = 1_000_000_000_000  # $1T (mega-cap maximum revenue)
MIN_EBITDA_MARGIN = 0.10  # 10%
MAX_EBITDA_MARGIN = 0.35  # 35%
MIN_GROWTH_RATE = -0.02  # -2% quarterly
MAX_GROWTH_RATE = 0.08  # 8% quarterly
REVENUE_VOLATILITY = 0.10  # 10% standard deviation

# Multiple Distribution (standard deviation around sector mean)
MULTIPLE_STD_DEV = 1.5  # Standard deviation for multiple distribution

# Valuation
MIN_EBITDA_MULTIPLE = 6.0
MAX_EBITDA_MULTIPLE = 25.0
DCF_PROJECTION_YEARS = 8
TERMINAL_GROWTH_RATE = 0.02  # 2% perpetual growth

# Deal Generation
NUM_AVAILABLE_DEALS = 5  # Companies available for acquisition each quarter
NEGOTIATION_ROUNDS = 3  # Max counter-offers

# Manager Attributes (0-1 scale)
MIN_MANAGER_COMPETENCE = 0.3
MAX_MANAGER_COMPETENCE = 1.0
MIN_MANAGER_RISK_PROFILE = 0.0  # Conservative
MAX_MANAGER_RISK_PROFILE = 1.0  # Aggressive
MIN_MANAGER_COOPERATIVENESS = 0.3
MAX_MANAGER_COOPERATIVENESS = 1.0

# Events
EVENT_PROBABILITY = 0.25  # 25% chance of event each quarter (medium difficulty)
CRISIS_PROBABILITY = 0.1  # 10% of events are crises (medium difficulty)

# Difficulty Settings (applied at game start)
DIFFICULTY_SETTINGS = {
    'easy': {
        'name': 'Obama Era',
        'description': 'Fish in a barrel. Easy credit, stable multiples, rare crises',
        'market_volatility_multiplier': 0.7,
        'multiple_trend_volatility': 0.02,  # ±2% instead of ±3%
        'event_probability_multiplier': 0.7,
        'crisis_probability_multiplier': 0.5,
        'starting_reputation_bonus': 0.10,  # Start at 30% instead of 20%
        'capital_gains_tax_rate': 0.15,  # 15% tax on profits
        'base_interest_rate': 0.03,  # 3% - easy credit!
    },
    'medium': {
        'name': 'Reagan Era',
        'description': 'Balanced challenge, realistic market dynamics',
        'market_volatility_multiplier': 1.0,
        'multiple_trend_volatility': 0.03,  # Standard ±3%
        'event_probability_multiplier': 1.0,
        'crisis_probability_multiplier': 1.0,
        'starting_reputation_bonus': 0.0,
        'capital_gains_tax_rate': 0.20,  # 20% tax on profits
        'base_interest_rate': 0.05,  # 5% - standard rate
    },
    'hard': {
        'name': 'Newsom Era',
        'description': 'Volatile markets, frequent crises, tough conditions',
        'market_volatility_multiplier': 1.4,
        'multiple_trend_volatility': 0.045,  # ±4.5% volatility
        'event_probability_multiplier': 1.5,
        'crisis_probability_multiplier': 2.0,
        'starting_reputation_bonus': -0.05,  # Start at 15% instead of 20%
        'capital_gains_tax_rate': 0.30,  # 30% tax on profits (brutal!)
        'base_interest_rate': 0.08,  # 8% - tight credit!
    }
}

# Portfolio Operations
COST_CUTTING_MAX_IMPACT = 0.15  # Up to 15% margin improvement
CAPEX_BOOST_MAX_IMPACT = 0.10  # Up to 10% revenue growth boost
MANAGER_REPLACEMENT_COST = 2_000_000  # $2M

# Leverage
MAX_DEBT_TO_EBITDA = 5.0
DEBT_INTEREST_RATE_SPREAD = 0.02  # 2% over base rate

# Display Settings
CURRENCY_DECIMALS = 0
PERCENTAGE_DECIMALS = 1

