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
                 growth_rate: float = None, volatility: float = None, manager: Manager = None,
                 valuation_multiple: float = None):
        self.name = name
        self.sector = sector
        self.revenue = revenue
        self.ebitda_margin = ebitda_margin
        self.growth_rate = growth_rate if growth_rate is not None else random.uniform(
            config.MIN_GROWTH_RATE, config.MAX_GROWTH_RATE
        )
        self.volatility = volatility if volatility is not None else config.REVENUE_VOLATILITY
        self.manager = manager or Manager()
        
        # Company-specific valuation multiple (initialized from sector mean + noise)
        self.valuation_multiple = valuation_multiple
        
        # Valuation tracking
        self.acquisition_price: Optional[float] = None
        self.acquisition_quarter: Optional[int] = None
        self.current_valuation = 0.0
        
        # Operation tracking
        self.last_operation_quarter: Optional[int] = None
        self.operations_this_quarter = 0
        
        # Historical tracking
        self.revenue_history = [revenue]
        self.ebitda_history = [revenue * ebitda_margin]
        
        # Operational health (0-1 scale, affects long-term viability)
        # Initialize AFTER all other attributes are set
        self.operational_health = self._calculate_initial_health()
    
    def _calculate_initial_health(self) -> float:
        """
        Calculate initial operational health based on company fundamentals.
        
        Returns:
            Float between 0 and 1 representing health
        """
        import random
        
        # Base health from management quality (60-90% of final)
        mgmt_contribution = 0.5 + (self.manager.competence * 0.4)  # 50-90%
        
        # Bonus from good fundamentals
        margin_bonus = (self.ebitda_margin - 0.10) * 0.5  # Good margins = health
        growth_bonus = max(0, self.growth_rate) * 2.0  # Positive growth = health
        
        # Small random factor
        random_factor = random.uniform(-0.05, 0.05)
        
        # Calculate total
        health = mgmt_contribution + margin_bonus + growth_bonus + random_factor
        
        # Clamp between 0.5 and 1.0 (companies start reasonably healthy)
        return max(0.5, min(1.0, health))
        
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
        Uses company-specific multiple if available, otherwise uses sector multiple from market.
        """
        if self.valuation_multiple is not None:
            # Use company-specific multiple (already incorporates sector characteristics + noise)
            multiple = self.valuation_multiple
        elif market:
            # Fall back to sector average from market
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
        
    def mark_operated(self, current_quarter: int) -> None:
        """Mark that an operation was performed on this company this quarter."""
        if self.last_operation_quarter != current_quarter:
            self.operations_this_quarter = 0
        self.last_operation_quarter = current_quarter
        self.operations_this_quarter += 1
        
    def can_operate(self, current_quarter: int) -> bool:
        """Check if company can be operated on this quarter."""
        return self.last_operation_quarter != current_quarter
        
    def reset_quarterly_operations(self) -> None:
        """Reset operation tracking for new quarter."""
        self.operations_this_quarter = 0
    
    def __repr__(self) -> str:
        return f"Company(name='{self.name}', sector='{self.sector}', revenue={self.revenue:.0f})"

