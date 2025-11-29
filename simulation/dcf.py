"""
Discounted Cash Flow (DCF) analysis functions.
"""

from typing import List
import config


def project_free_cash_flows(
    current_ebitda: float,
    growth_rate: float,
    ebitda_margin: float,
    capex_rate: float = 0.05,
    nwc_rate: float = 0.10,
    years: int = None
) -> List[float]:
    """
    Project future free cash flows for a company.
    
    Args:
        current_ebitda: Current EBITDA
        growth_rate: Annual growth rate
        ebitda_margin: EBITDA margin
        capex_rate: Capex as % of revenue
        nwc_rate: Net working capital as % of revenue
        years: Number of years to project (defaults to config)
        
    Returns:
        List of projected free cash flows
    """
    years = years if years else config.DCF_PROJECTION_YEARS
    
    # Convert quarterly growth to annual
    annual_growth = (1 + growth_rate) ** 4 - 1
    
    fcf_list = []
    ebitda = current_ebitda
    
    for _ in range(years):
        # Project next year's EBITDA
        ebitda *= (1 + annual_growth)
        
        # Calculate revenue from EBITDA
        revenue = ebitda / ebitda_margin if ebitda_margin > 0 else 0
        
        # Calculate free cash flow
        # FCF = EBITDA - Capex - NWC increase - Taxes (simplified)
        tax_rate = 0.25  # 25% tax rate
        capex = revenue * capex_rate
        nwc_increase = revenue * annual_growth * nwc_rate
        
        fcf = ebitda * (1 - tax_rate) - capex - nwc_increase
        fcf_list.append(fcf)
        
    return fcf_list


def discount_cash_flows(cash_flows: List[float], discount_rate: float) -> float:
    """
    Discount a list of cash flows to present value.
    
    Args:
        cash_flows: List of future cash flows
        discount_rate: Annual discount rate
        
    Returns:
        Present value of cash flows
    """
    pv = 0.0
    for year, cf in enumerate(cash_flows, start=1):
        pv += cf / (1 + discount_rate) ** year
    return pv


def calculate_terminal_value(
    final_cash_flow: float,
    terminal_growth_rate: float,
    discount_rate: float
) -> float:
    """
    Calculate terminal value using perpetuity growth method.
    
    Args:
        final_cash_flow: Last projected cash flow
        terminal_growth_rate: Perpetual growth rate
        discount_rate: Discount rate
        
    Returns:
        Terminal value
    """
    if discount_rate <= terminal_growth_rate:
        # Avoid division by zero or negative denominator
        terminal_growth_rate = discount_rate - 0.01
        
    terminal_fcf = final_cash_flow * (1 + terminal_growth_rate)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth_rate)
    
    return terminal_value


def calculate_enterprise_value(
    current_ebitda: float,
    growth_rate: float,
    ebitda_margin: float,
    discount_rate: float,
    terminal_growth_rate: float = None,
    years: int = None
) -> float:
    """
    Calculate enterprise value using DCF method.
    
    Args:
        current_ebitda: Current EBITDA
        growth_rate: Quarterly growth rate
        ebitda_margin: EBITDA margin
        discount_rate: Annual discount rate
        terminal_growth_rate: Terminal growth rate (defaults to config)
        years: Projection years (defaults to config)
        
    Returns:
        Enterprise value
    """
    terminal_growth_rate = terminal_growth_rate if terminal_growth_rate else config.TERMINAL_GROWTH_RATE
    
    # Project cash flows
    fcf_list = project_free_cash_flows(current_ebitda, growth_rate, ebitda_margin, years=years)
    
    if not fcf_list:
        return 0.0
        
    # Discount projected cash flows
    pv_fcf = discount_cash_flows(fcf_list, discount_rate)
    
    # Calculate terminal value
    terminal_value = calculate_terminal_value(fcf_list[-1], terminal_growth_rate, discount_rate)
    
    # Discount terminal value back to present
    years = len(fcf_list)
    pv_terminal = terminal_value / (1 + discount_rate) ** years
    
    # Enterprise value = PV of FCFs + PV of terminal value
    enterprise_value = pv_fcf + pv_terminal
    
    return max(0, enterprise_value)


def calculate_dcf_valuation(company: 'Company', market: 'Market') -> float:
    """
    Calculate DCF-based valuation for a company.
    
    Args:
        company: Company object
        market: Market object for discount rate
        
    Returns:
        DCF valuation
    """
    discount_rate = market.get_discount_rate()
    
    ev = calculate_enterprise_value(
        current_ebitda=company.ebitda,
        growth_rate=company.growth_rate,
        ebitda_margin=company.ebitda_margin,
        discount_rate=discount_rate
    )
    
    return ev

