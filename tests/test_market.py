"""
Tests for Market model.
"""

import pytest
from models.market import Market


def test_market_creation():
    """Test market initialization."""
    market = Market()
    
    assert market.interest_rate > 0
    assert market.growth_rate >= -0.10
    assert market.growth_rate <= 0.10
    assert 0.0 <= market.credit_conditions <= 1.0
    assert len(market.sector_multiples) > 0


def test_market_quarterly_update():
    """Test market conditions update."""
    market = Market()
    
    initial_rate = market.interest_rate
    initial_growth = market.growth_rate
    
    # Update market for several quarters
    market.update_quarter()
    
    # Values should have changed (though exact values depend on randomness)
    assert len(market.interest_rate_history) == 2
    assert len(market.growth_rate_history) == 2


def test_market_sector_multiples():
    """Test sector multiple retrieval."""
    market = Market()
    
    # Test known sector
    tech_multiple = market.get_sector_multiple("Technology")
    assert tech_multiple > 0
    
    # Test unknown sector (should return default)
    unknown_multiple = market.get_sector_multiple("Unknown Sector")
    assert unknown_multiple == 9.0  # Default


def test_market_rates():
    """Test market rate calculations."""
    market = Market()
    
    discount_rate = market.get_discount_rate()
    debt_rate = market.get_debt_rate()
    
    # Discount rate should be higher than interest rate (includes risk premium)
    assert discount_rate > market.interest_rate
    
    # Debt rate should be higher than base interest rate
    assert debt_rate > market.interest_rate


def test_market_conditions():
    """Test market condition detection."""
    market = Market()
    
    # Test recession detection
    market.growth_rate = -0.05
    assert market.is_recession() == True
    assert market.is_boom() == False
    
    # Test boom detection
    market.growth_rate = 0.08
    assert market.is_recession() == False
    assert market.is_boom() == True
    
    # Test normal conditions
    market.growth_rate = 0.02
    assert market.is_recession() == False
    assert market.is_boom() == False


def test_market_conditions_summary():
    """Test market conditions summary."""
    market = Market()
    
    summary = market.get_conditions_summary()
    
    assert 'interest_rate' in summary
    assert 'growth_rate' in summary
    assert 'credit_conditions' in summary
    assert 'discount_rate' in summary
    assert 'debt_rate' in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

