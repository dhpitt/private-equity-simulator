"""
Market model - global economic conditions affecting all companies.
"""

from typing import Dict
import random
import config


class Market:
    """Represents global market conditions and sector-specific factors."""
    
    def __init__(self, difficulty: str = 'medium'):
        self.difficulty = difficulty
        self.difficulty_settings = config.DIFFICULTY_SETTINGS.get(difficulty, config.DIFFICULTY_SETTINGS['medium'])
        
        # Use difficulty-based interest rate
        self.interest_rate = self.difficulty_settings['base_interest_rate']
        self.growth_rate = config.MARKET_GROWTH_RATE
        
        # Sector-specific EBITDA multiples
        self.sector_multiples: Dict[str, float] = {
            'Technology': 12.0,
            'Healthcare': 11.0,
            'Consumer': 9.0,
            'Industrial': 8.5,
            'Financial Services': 10.0,
            'Energy': 7.5,
            'Real Estate': 8.0,
            'Retail': 7.0,
        }
        
        # Credit conditions (0-1 scale, higher = easier credit)
        self.credit_conditions = 0.7
        
        # PHASE 1: Market multiple trend (affects ALL company valuations)
        # 1.0 = neutral, >1.0 = multiple expansion, <1.0 = multiple compression
        self.multiple_trend = 1.0
        
        # Historical tracking
        self.interest_rate_history = [self.interest_rate]
        self.growth_rate_history = [self.growth_rate]
        self.multiple_trend_history = [self.multiple_trend]
        
    def update_quarter(self) -> None:
        """Update market conditions for the new quarter."""
        # Interest rate random walk
        rate_change = random.gauss(0, config.INTEREST_RATE_VOLATILITY * self.difficulty_settings['market_volatility_multiplier'])
        self.interest_rate += rate_change
        self.interest_rate = max(0.01, min(0.15, self.interest_rate))  # Keep between 1% and 15%
        
        # Market growth rate (adjusted by difficulty)
        growth_change = random.gauss(0, config.MARKET_VOLATILITY * self.difficulty_settings['market_volatility_multiplier'])
        self.growth_rate += growth_change
        self.growth_rate = max(-0.10, min(0.10, self.growth_rate))  # Keep between -10% and +10%
        
        # Credit conditions random walk
        credit_change = random.gauss(0, 0.05)
        self.credit_conditions += credit_change
        self.credit_conditions = max(0.0, min(1.0, self.credit_conditions))
        
        # PHASE 1: Update market multiple trend (mean-reverting random walk)
        # This creates bull/bear market cycles for valuations
        # Volatility adjusted by difficulty
        cycle_change = random.gauss(0, self.difficulty_settings['multiple_trend_volatility'])
        reversion = (1.0 - self.multiple_trend) * 0.1  # Pull back to neutral (1.0)
        
        self.multiple_trend += cycle_change + reversion
        self.multiple_trend = max(0.80, min(1.20, self.multiple_trend))  # ±20% range
        
        # Sector multiples drift based on market conditions
        for sector in self.sector_multiples:
            multiple_change = random.gauss(0, 0.3)
            self.sector_multiples[sector] += multiple_change
            # Keep multiples within reasonable bounds
            self.sector_multiples[sector] = max(
                config.MIN_EBITDA_MULTIPLE,
                min(config.MAX_EBITDA_MULTIPLE, self.sector_multiples[sector])
            )
            
        # Record history
        self.interest_rate_history.append(self.interest_rate)
        self.growth_rate_history.append(self.growth_rate)
        self.multiple_trend_history.append(self.multiple_trend)
        
    def get_sector_multiple(self, sector: str) -> float:
        """Get the EBITDA multiple for a specific sector."""
        return self.sector_multiples.get(sector, 9.0)  # Default to 9x if sector unknown
        
    def get_discount_rate(self) -> float:
        """Calculate discount rate for DCF (interest rate + risk premium)."""
        risk_premium = 0.05  # 5% equity risk premium
        return self.interest_rate + risk_premium
        
    def get_debt_rate(self) -> float:
        """Calculate cost of debt."""
        return self.interest_rate + config.DEBT_INTEREST_RATE_SPREAD
        
    def get_conditions_summary(self) -> Dict[str, float]:
        """Return current market conditions."""
        return {
            'interest_rate': self.interest_rate,
            'growth_rate': self.growth_rate,
            'credit_conditions': self.credit_conditions,
            'discount_rate': self.get_discount_rate(),
            'debt_rate': self.get_debt_rate(),
            'multiple_trend': self.multiple_trend
        }
        
    def is_recession(self) -> bool:
        """Check if market is in recession (negative growth)."""
        return self.growth_rate < 0
        
    def is_boom(self) -> bool:
        """Check if market is booming (high growth)."""
        return self.growth_rate > 0.05

