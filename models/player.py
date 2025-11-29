"""
Player model - represents the player's state in the game.
"""

from typing import List, Dict, Any
import config


class Player:
    """Represents the player managing the PE fund."""
    
    def __init__(self, starting_cash: float = None, debt_capacity: float = None):
        self.cash = starting_cash if starting_cash is not None else config.STARTING_CAPITAL
        self.debt_capacity = debt_capacity if debt_capacity is not None else config.STARTING_DEBT_CAPACITY
        self.current_debt = 0.0
        self.portfolio: List['Company'] = []
        self.reputation = 1.0  # 0-1 scale, affects deal terms
        self.deal_history: List[Dict[str, Any]] = []
        
    def adjust_cash(self, amount: float) -> None:
        """Add or remove cash from player's balance."""
        self.cash += amount
        
    def take_debt(self, amount: float) -> bool:
        """Attempt to take on debt. Returns True if successful."""
        if self.current_debt + amount <= self.debt_capacity:
            self.current_debt += amount
            self.cash += amount
            return True
        return False
        
    def repay_debt(self, amount: float) -> bool:
        """Repay debt. Returns True if successful."""
        if amount <= self.cash and amount <= self.current_debt:
            self.cash -= amount
            self.current_debt -= amount
            return True
        return False
        
    def add_company(self, company: 'Company') -> None:
        """Add a company to the portfolio."""
        self.portfolio.append(company)
        
    def remove_company(self, company: 'Company') -> None:
        """Remove a company from the portfolio."""
        if company in self.portfolio:
            self.portfolio.remove(company)
            
    def compute_net_worth(self) -> float:
        """Calculate total net worth: cash + portfolio value - debt."""
        portfolio_value = sum(company.current_valuation for company in self.portfolio)
        return self.cash + portfolio_value - self.current_debt
        
    def compute_portfolio_value(self) -> float:
        """Calculate total portfolio value."""
        return sum(company.current_valuation for company in self.portfolio)
        
    def record_deal(self, deal_type: str, company_name: str, price: float, quarter: int) -> None:
        """Record a deal in history."""
        self.deal_history.append({
            'type': deal_type,
            'company': company_name,
            'price': price,
            'quarter': quarter
        })
        
    def adjust_reputation(self, delta: float) -> None:
        """Adjust reputation, keeping it between 0 and 1."""
        self.reputation = max(0.0, min(1.0, self.reputation + delta))
        
    def available_capital(self) -> float:
        """Calculate available capital for investments (cash + unused debt capacity)."""
        return self.cash + (self.debt_capacity - self.current_debt)

