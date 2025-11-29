"""
Market model - global economic conditions affecting all companies.
"""

from typing import Dict
import random
import config


class Market:
    """Represents global market conditions and sector-specific factors."""
    
    def __init__(self):
        self.interest_rate = config.BASE_INTEREST_RATE
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
        
        # Historical tracking
        self.interest_rate_history = [self.interest_rate]
        self.growth_rate_history = [self.growth_rate]
        
    def update_quarter(self) -> None:
        """Update market conditions for the new quarter."""
        # Interest rate random walk
        rate_change = random.gauss(0, config.INTEREST_RATE_VOLATILITY)
        self.interest_rate += rate_change
        self.interest_rate = max(0.01, min(0.15, self.interest_rate))  # Keep between 1% and 15%
        
        # Market growth rate
        growth_change = random.gauss(0, config.MARKET_VOLATILITY)
        self.growth_rate += growth_change
        self.growth_rate = max(-0.10, min(0.10, self.growth_rate))  # Keep between -10% and +10%
        
        # Credit conditions random walk
        credit_change = random.gauss(0, 0.05)
        self.credit_conditions += credit_change
        self.credit_conditions = max(0.0, min(1.0, self.credit_conditions))
        
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
            'debt_rate': self.get_debt_rate()
        }
        
    def is_recession(self) -> bool:
        """Check if market is in recession (negative growth)."""
        return self.growth_rate < 0
        
    def is_boom(self) -> bool:
        """Check if market is booming (high growth)."""
        return self.growth_rate > 0.05

