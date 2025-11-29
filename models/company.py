"""
Company model - core business entity with financial and operational attributes.
"""

from typing import Optional, Dict, Any
import random
from .manager import Manager
import config


class Company:
    """Represents a portfolio company with financial and operational characteristics."""
    
    def __init__(self, name: str, sector: str, revenue: float, ebitda_margin: float,
                 growth_rate: float = None, volatility: float = None, manager: Manager = None):
        self.name = name
        self.sector = sector
        self.revenue = revenue
        self.ebitda_margin = ebitda_margin
        self.growth_rate = growth_rate if growth_rate is not None else random.uniform(
            config.MIN_GROWTH_RATE, config.MAX_GROWTH_RATE
        )
        self.volatility = volatility if volatility is not None else config.REVENUE_VOLATILITY
        self.manager = manager or Manager()
        
        # Valuation tracking
        self.acquisition_price: Optional[float] = None
        self.acquisition_quarter: Optional[int] = None
        self.current_valuation = 0.0
        
        # Historical tracking
        self.revenue_history = [revenue]
        self.ebitda_history = [revenue * ebitda_margin]
        
    @property
    def ebitda(self) -> float:
        """Current EBITDA."""
        return self.revenue * self.ebitda_margin
        
    def simulate_quarter(self, market_conditions: Dict[str, Any]) -> None:
        """
        Simulate one quarter of company performance.
        Updates revenue based on growth rate, volatility, manager performance, and market.
        """
        # Base growth from company's inherent rate
        growth = self.growth_rate
        
        # Add manager performance impact
        manager_impact = self.manager.get_performance_modifier()
        growth += manager_impact
        
        # Add market impact
        market_growth = market_conditions.get('growth_rate', 0.0)
        sector_multiplier = market_conditions.get('sector_multipliers', {}).get(self.sector, 1.0)
        growth += market_growth * sector_multiplier
        
        # Add stochastic noise
        noise = random.gauss(0, self.volatility)
        growth += noise
        
        # Apply growth to revenue
        self.revenue *= (1 + growth)
        self.revenue = max(0, self.revenue)  # Can't go negative
        
        # EBITDA margin can drift slightly
        margin_drift = random.gauss(0, 0.01)  # ±1% margin drift
        self.ebitda_margin = max(0.0, min(1.0, self.ebitda_margin + margin_drift))
        
        # Record history
        self.revenue_history.append(self.revenue)
        self.ebitda_history.append(self.ebitda)
        
    def calculate_valuation(self, market: 'Market' = None) -> float:
        """
        Calculate company valuation using EBITDA multiple.
        If market is provided, use sector-specific multiple.
        """
        if market:
            multiple = market.get_sector_multiple(self.sector)
        else:
            # Default multiple
            multiple = (config.MIN_EBITDA_MULTIPLE + config.MAX_EBITDA_MULTIPLE) / 2
            
        valuation = self.ebitda * multiple
        self.current_valuation = valuation
        return valuation
        
    def apply_event(self, event: Dict[str, Any]) -> None:
        """Apply an event's effects to the company."""
        if 'revenue_impact' in event:
            self.revenue *= (1 + event['revenue_impact'])
            self.revenue = max(0, self.revenue)
            
        if 'margin_impact' in event:
            self.ebitda_margin += event['margin_impact']
            self.ebitda_margin = max(0.0, min(1.0, self.ebitda_margin))
            
        if 'growth_impact' in event:
            self.growth_rate += event['growth_impact']
            
    def get_quarterly_growth(self) -> float:
        """Calculate most recent quarterly revenue growth rate."""
        if len(self.revenue_history) < 2:
            return 0.0
        return (self.revenue_history[-1] / self.revenue_history[-2]) - 1
        
    def get_metrics(self) -> Dict[str, float]:
        """Return key company metrics."""
        return {
            'revenue': self.revenue,
            'ebitda': self.ebitda,
            'ebitda_margin': self.ebitda_margin,
            'growth_rate': self.growth_rate,
            'valuation': self.current_valuation,
            'quarterly_growth': self.get_quarterly_growth()
        }
        
    def __str__(self) -> str:
        return (f"{self.name} ({self.sector}): "
                f"Rev ${self.revenue:,.0f}, "
                f"EBITDA ${self.ebitda:,.0f} ({self.ebitda_margin:.1%})")
        
    def __repr__(self) -> str:
        return f"Company(name='{self.name}', sector='{self.sector}', revenue={self.revenue:.0f})"

