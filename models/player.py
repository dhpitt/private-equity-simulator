"""
Player model - represents the player's state in the game.
"""

from typing import List, Dict, Any
import config


class Player:
    """Represents the player managing the PE fund."""
    
    def __init__(self, starting_cash: float = None, fund_name: str = None, difficulty: str = 'medium'):
        self.cash = starting_cash if starting_cash is not None else config.STARTING_CAPITAL
        self.current_debt = 0.0
        self.portfolio: List['Company'] = []
        self.fund_name = fund_name or "Unnamed Fund"
        self.difficulty = difficulty
        
        # Apply difficulty-based reputation adjustment
        difficulty_settings = config.DIFFICULTY_SETTINGS.get(difficulty, config.DIFFICULTY_SETTINGS['medium'])
        base_reputation = config.STARTING_REPUTATION
        self.reputation = base_reputation + difficulty_settings['starting_reputation_bonus']
        
        self.deal_history: List[Dict[str, Any]] = []
        
        # Tax tracking
        self.total_taxes_paid = 0.0
        
        # Base debt capacity (grows with reputation and net worth)
        self.base_debt_capacity = config.BASE_DEBT_CAPACITY
        
    def adjust_cash(self, amount: float) -> None:
        """Add or remove cash from player's balance."""
        self.cash += amount
        
    def get_debt_capacity(self) -> float:
        """
        Calculate current debt capacity based on net worth and reputation.
        
        Formula: base_capacity + (net_worth * debt_to_nw_ratio * reputation_factor)
        
        Higher reputation increases debt capacity significantly.
        Higher net worth allows more leverage.
        """
        net_worth = self.compute_net_worth()
        
        # Reputation factor: ranges from 0.5 (low rep) to 2.0 (high rep)
        # This means low reputation severely limits debt access
        reputation_factor = 0.5 + (self.reputation * config.REPUTATION_DEBT_MULTIPLIER - 0.5)
        
        # Calculate capacity from net worth
        net_worth_capacity = max(0, net_worth) * config.DEBT_TO_NET_WORTH_RATIO * reputation_factor
        
        # Total capacity is base plus net-worth-driven capacity
        total_capacity = self.base_debt_capacity + net_worth_capacity
        
        # Ensure minimum capacity
        total_capacity = max(config.MIN_DEBT_CAPACITY, total_capacity)
        
        return total_capacity
    
    def take_debt(self, amount: float) -> bool:
        """Attempt to take on debt. Returns True if successful."""
        current_capacity = self.get_debt_capacity()
        if self.current_debt + amount <= current_capacity:
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
    
    def update_reputation_from_profits(self, quarterly_profit: float) -> float:
        """
        Update reputation based on quarterly profits.
        Profits increase reputation, losses decrease it.
        
        Args:
            quarterly_profit: Total profit/loss for the quarter
            
        Returns:
            The reputation change
        """
        # Calculate reputation change based on profit relative to portfolio value
        portfolio_value = self.compute_portfolio_value()
        
        if portfolio_value > 0:
            # ROQ (Return on Quarter) = Quarterly Profit / Portfolio Value
            roq = quarterly_profit / portfolio_value
            
            # Scale reputation change: 10% quarterly return = +5% reputation
            reputation_change = roq * 0.5
            
            # Cap the change at ±5% per quarter
            reputation_change = max(-0.05, min(0.05, reputation_change))
        else:
            # No portfolio, small gain/loss based on profit sign
            if quarterly_profit > 0:
                reputation_change = 0.01
            elif quarterly_profit < 0:
                reputation_change = -0.01
            else:
                reputation_change = 0.0
        
        self.adjust_reputation(reputation_change)
        return reputation_change

        
    def available_capital(self) -> float:
        """Calculate available capital for investments (cash + unused debt capacity)."""
        current_capacity = self.get_debt_capacity()
        return self.cash + (current_capacity - self.current_debt)
    
    def get_debt_utilization(self) -> float:
        """Calculate debt utilization as percentage of capacity."""
        capacity = self.get_debt_capacity()
        if capacity <= 0:
            return 0.0
        return self.current_debt / capacity
    
    def calculate_capital_gains_tax(self, sale_price: float, cost_basis: float) -> float:
        """
        Calculate capital gains tax on an investment exit.
        
        Args:
            sale_price: The price the company was sold for
            cost_basis: The original purchase price
            
        Returns:
            Tax amount owed (0 if loss)
        """
        capital_gain = sale_price - cost_basis
        
        # Only tax gains, not losses
        if capital_gain <= 0:
            return 0.0
        
        # Get tax rate from difficulty settings
        difficulty_settings = config.DIFFICULTY_SETTINGS.get(self.difficulty, config.DIFFICULTY_SETTINGS['medium'])
        tax_rate = difficulty_settings['capital_gains_tax_rate']
        
        tax_owed = capital_gain * tax_rate
        return tax_owed
    
    def pay_taxes(self, tax_amount: float) -> None:
        """
        Pay taxes and track total paid.
        
        Args:
            tax_amount: Amount of tax to pay
        """
        self.adjust_cash(-tax_amount)
        self.total_taxes_paid += tax_amount

