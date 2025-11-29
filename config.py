"""
Global configuration settings for the PE Simulator game.
"""

# Game Settings
STARTING_CAPITAL = 10_000_000  # $10M
STARTING_DEBT_CAPACITY = 200_000_000  # $200M
GAME_DURATION_QUARTERS = 20  # 5 years

# Random Seed (None for random, or set a number for reproducibility)
RANDOM_SEED = None

# Market Settings
BASE_INTEREST_RATE = 0.05  # 5%
INTEREST_RATE_VOLATILITY = 0.01  # 1% quarterly volatility
MARKET_GROWTH_RATE = 0.02  # 2% quarterly growth
MARKET_VOLATILITY = 0.05  # 5% volatility

# Company Generation
MIN_COMPANY_REVENUE = 10_000_000  # $10M
MAX_COMPANY_REVENUE = 100_000_000  # $100M
MIN_EBITDA_MARGIN = 0.10  # 10%
MAX_EBITDA_MARGIN = 0.35  # 35%
MIN_GROWTH_RATE = -0.02  # -2% quarterly
MAX_GROWTH_RATE = 0.08  # 8% quarterly
REVENUE_VOLATILITY = 0.10  # 10% standard deviation

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
EVENT_PROBABILITY = 0.25  # 25% chance of event each quarter
CRISIS_PROBABILITY = 0.1  # 10% of events are crises

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

