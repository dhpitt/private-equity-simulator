"""
Tests for DCF calculations.
"""

import pytest
from simulation.dcf import (
    project_free_cash_flows,
    discount_cash_flows,
    calculate_terminal_value,
    calculate_enterprise_value
)


def test_project_free_cash_flows():
    """Test FCF projection."""
    fcf_list = project_free_cash_flows(
        current_ebitda=10_000_000,
        growth_rate=0.02,  # Quarterly
        ebitda_margin=0.25,
        years=5
    )
    
    assert len(fcf_list) == 5
    assert all(fcf > 0 for fcf in fcf_list)
    # FCFs should generally grow over time
    assert fcf_list[-1] > fcf_list[0]


def test_discount_cash_flows():
    """Test cash flow discounting."""
    cash_flows = [1000, 1100, 1200, 1300, 1400]
    discount_rate = 0.10
    
    pv = discount_cash_flows(cash_flows, discount_rate)
    
    # PV should be less than sum of cash flows
    assert pv < sum(cash_flows)
    assert pv > 0
    
    # Manually calculate first year to verify
    expected_first_year_pv = 1000 / (1 + discount_rate)
    actual_first_year_component = 1000 / (1 + discount_rate)
    
    assert pv > expected_first_year_pv  # Should include all years


def test_calculate_terminal_value():
    """Test terminal value calculation."""
    final_cf = 1000
    terminal_growth = 0.02
    discount_rate = 0.10
    
    tv = calculate_terminal_value(final_cf, terminal_growth, discount_rate)
    
    assert tv > 0
    assert tv > final_cf  # Terminal value should be multiple of final CF


def test_calculate_enterprise_value():
    """Test enterprise value calculation."""
    ev = calculate_enterprise_value(
        current_ebitda=10_000_000,
        growth_rate=0.02,
        ebitda_margin=0.25,
        discount_rate=0.10
    )
    
    assert ev > 0
    # EV should be a reasonable multiple of EBITDA
    multiple = ev / 10_000_000
    assert 5.0 < multiple < 20.0


def test_zero_cash_flows():
    """Test handling of edge cases."""
    # Zero cash flows
    pv = discount_cash_flows([0, 0, 0], 0.10)
    assert pv == 0
    
    # Empty cash flows
    pv = discount_cash_flows([], 0.10)
    assert pv == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

