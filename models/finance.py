"""
Finance utilities - leverage, debt service, IRR calculations.
"""

from typing import List, Tuple
import config


def calculate_max_leverage(company_ebitda: float, debt_to_ebitda_ratio: float = None) -> float:
    """
    Calculate maximum debt for a company based on EBITDA.
    
    Args:
        company_ebitda: Company's EBITDA
        debt_to_ebitda_ratio: Maximum debt/EBITDA ratio (defaults to config)
        
    Returns:
        Maximum debt amount
    """
    ratio = debt_to_ebitda_ratio if debt_to_ebitda_ratio else config.MAX_DEBT_TO_EBITDA
    return company_ebitda * ratio


def calculate_debt_service(debt_amount: float, interest_rate: float, years: int = 5) -> float:
    """
    Calculate annual debt service payment (principal + interest).
    Assumes amortizing loan.
    
    Args:
        debt_amount: Total debt
        interest_rate: Annual interest rate
        years: Loan term in years
        
    Returns:
        Quarterly debt service payment
    """
    if debt_amount <= 0 or interest_rate <= 0:
        return 0.0
        
    # Convert to quarterly
    quarterly_rate = interest_rate / 4
    num_payments = years * 4
    
    # Amortizing loan formula
    if quarterly_rate == 0:
        payment = debt_amount / num_payments
    else:
        payment = debt_amount * (quarterly_rate * (1 + quarterly_rate)**num_payments) / \
                  ((1 + quarterly_rate)**num_payments - 1)
    
    return payment


def calculate_interest_payment(debt_amount: float, interest_rate: float) -> float:
    """
    Calculate quarterly interest payment on debt.
    
    Args:
        debt_amount: Outstanding debt
        interest_rate: Annual interest rate
        
    Returns:
        Quarterly interest payment
    """
    return debt_amount * (interest_rate / 4)


def calculate_irr(cash_flows: List[float], quarters: List[int] = None) -> float:
    """
    Calculate Internal Rate of Return using Newton's method.
    
    Args:
        cash_flows: List of cash flows (negative for investments, positive for returns)
        quarters: List of quarter numbers (optional, defaults to 0, 1, 2, ...)
        
    Returns:
        Quarterly IRR (multiply by 4 for annual IRR)
    """
    if not cash_flows:
        return 0.0
        
    if quarters is None:
        quarters = list(range(len(cash_flows)))
        
    # Newton's method to find IRR
    rate = 0.1  # Initial guess: 10% quarterly
    tolerance = 0.0001
    max_iterations = 100
    
    for _ in range(max_iterations):
        npv = sum(cf / (1 + rate)**q for cf, q in zip(cash_flows, quarters))
        
        if abs(npv) < tolerance:
            return rate
            
        # Derivative of NPV with respect to rate
        dnpv = sum(-q * cf / (1 + rate)**(q + 1) for cf, q in zip(cash_flows, quarters))
        
        if abs(dnpv) < 1e-10:
            break
            
        rate = rate - npv / dnpv
        
    return rate


def calculate_moic(initial_investment: float, exit_value: float) -> float:
    """
    Calculate Multiple on Invested Capital.
    
    Args:
        initial_investment: Initial investment amount
        exit_value: Exit value
        
    Returns:
        MOIC (exit_value / initial_investment)
    """
    if initial_investment <= 0:
        return 0.0
    return exit_value / initial_investment


def calculate_equity_value(enterprise_value: float, debt: float, cash: float = 0) -> float:
    """
    Calculate equity value from enterprise value.
    
    Args:
        enterprise_value: Enterprise value
        debt: Total debt
        cash: Cash on hand
        
    Returns:
        Equity value (EV - debt + cash)
    """
    return enterprise_value - debt + cash


def calculate_leveraged_returns(
    purchase_price: float,
    exit_price: float,
    debt_amount: float,
    equity_amount: float,
    quarters_held: int,
    interest_rate: float
) -> Tuple[float, float, float]:
    """
    Calculate returns on a leveraged buyout.
    
    Args:
        purchase_price: Total purchase price
        exit_price: Exit sale price
        debt_amount: Debt used in purchase
        equity_amount: Equity invested
        quarters_held: Number of quarters held
        interest_rate: Annual interest rate on debt
        
    Returns:
        Tuple of (equity_return, equity_irr, moic)
    """
    # Calculate total interest paid over holding period
    total_interest = debt_amount * (interest_rate / 4) * quarters_held
    
    # Exit proceeds after repaying debt
    exit_proceeds = exit_price - debt_amount
    
    # Net equity return
    equity_return = exit_proceeds - equity_amount - total_interest
    
    # Cash flows for IRR calculation
    cash_flows = [-equity_amount]  # Initial investment
    cash_flows.extend([0] * (quarters_held - 1))  # Holding periods
    cash_flows.append(exit_proceeds)  # Exit
    
    equity_irr = calculate_irr(cash_flows)
    moic = calculate_moic(equity_amount, exit_proceeds)
    
    return equity_return, equity_irr * 4, moic  # Convert quarterly IRR to annual

