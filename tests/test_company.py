"""
Tests for Company model.
"""

import pytest
from models.company import Company
from models.manager import Manager
from models.market import Market


def test_company_creation():
    """Test basic company creation."""
    manager = Manager(name="Test Manager", competence=0.8, risk_profile=0.5, cooperativeness=0.7)
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25,
        growth_rate=0.05,
        manager=manager
    )
    
    assert company.name == "Test Corp"
    assert company.sector == "Technology"
    assert company.revenue == 50_000_000
    assert company.ebitda_margin == 0.25
    assert company.growth_rate == 0.05
    assert company.ebitda == 12_500_000


def test_company_quarterly_simulation():
    """Test quarterly performance simulation."""
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25,
        growth_rate=0.02
    )
    
    initial_revenue = company.revenue
    market = Market()
    market_conditions = market.get_conditions_summary()
    market_conditions['sector_multipliers'] = {'Technology': 1.0}
    
    # Simulate a quarter
    company.simulate_quarter(market_conditions)
    
    # Revenue should have changed (though exact amount depends on randomness)
    assert company.revenue != initial_revenue
    assert len(company.revenue_history) == 2
    assert len(company.ebitda_history) == 2


def test_company_valuation():
    """Test company valuation calculation."""
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25
    )
    
    market = Market()
    valuation = company.calculate_valuation(market)
    
    # Valuation should be EBITDA * sector multiple
    expected_multiple = market.get_sector_multiple("Technology")
    expected_valuation = company.ebitda * expected_multiple
    
    assert abs(valuation - expected_valuation) < 1.0  # Allow for rounding


def test_company_event_application():
    """Test applying events to companies."""
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25,
        growth_rate=0.02
    )
    
    initial_revenue = company.revenue
    initial_margin = company.ebitda_margin
    initial_growth = company.growth_rate
    
    # Apply negative event
    event = {
        'revenue_impact': -0.10,  # -10% revenue
        'margin_impact': -0.02,   # -2% margin
        'growth_impact': -0.01    # -1% growth
    }
    
    company.apply_event(event)
    
    assert company.revenue < initial_revenue
    assert company.ebitda_margin < initial_margin
    assert company.growth_rate < initial_growth


def test_company_metrics():
    """Test company metrics calculation."""
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25
    )
    
    metrics = company.get_metrics()
    
    assert 'revenue' in metrics
    assert 'ebitda' in metrics
    assert 'ebitda_margin' in metrics
    assert 'growth_rate' in metrics
    assert 'valuation' in metrics
    assert metrics['revenue'] == 50_000_000
    assert metrics['ebitda'] == 12_500_000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

