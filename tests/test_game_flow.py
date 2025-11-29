"""
Tests for game flow and integration.
"""

import pytest
from game.engine import GameEngine
from game.time_manager import TimeManager
from models.player import Player
from models.company import Company
from models.market import Market
import config


def test_time_manager():
    """Test time management."""
    tm = TimeManager(total_quarters=20)
    
    assert tm.current_quarter == 0
    assert tm.current_year == 1
    assert tm.get_quarter_in_year() == 1
    assert tm.quarters_remaining() == 20
    assert not tm.is_game_over()
    
    # Advance several quarters
    for _ in range(4):
        tm.advance_quarter()
        
    assert tm.current_quarter == 4
    assert tm.current_year == 2
    assert tm.get_quarter_in_year() == 1


def test_player_cash_operations():
    """Test player cash management."""
    player = Player(starting_cash=100_000_000)
    
    assert player.cash == 100_000_000
    
    # Add cash
    player.adjust_cash(10_000_000)
    assert player.cash == 110_000_000
    
    # Remove cash
    player.adjust_cash(-5_000_000)
    assert player.cash == 105_000_000


def test_player_debt_operations():
    """Test player debt management."""
    player = Player(starting_cash=100_000_000)
    
    # Take debt
    success = player.take_debt(50_000_000)
    assert success == True
    assert player.current_debt == 50_000_000
    assert player.cash == 150_000_000
    
    # Debt capacity should be sufficient for initial player
    initial_capacity = player.get_debt_capacity()
    assert initial_capacity > 50_000_000
    
    # Try to exceed capacity (exact limit depends on net worth, so test with large amount)
    original_debt = player.current_debt
    success = player.take_debt(10_000_000_000)  # $10B - definitely too much
    assert success == False
    assert player.current_debt == original_debt  # Debt unchanged
    
    # Repay debt
    success = player.repay_debt(20_000_000)
    assert success == True
    assert player.current_debt == 30_000_000


def test_player_portfolio_management():
    """Test player portfolio operations."""
    player = Player()
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25
    )
    
    assert len(player.portfolio) == 0
    
    # Add company
    player.add_company(company)
    assert len(player.portfolio) == 1
    assert company in player.portfolio
    
    # Remove company
    player.remove_company(company)
    assert len(player.portfolio) == 0


def test_player_net_worth():
    """Test net worth calculation."""
    player = Player(starting_cash=100_000_000)
    
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25
    )
    company.current_valuation = 100_000_000
    
    player.add_company(company)
    player.take_debt(50_000_000)
    
    net_worth = player.compute_net_worth()
    
    # Net worth = cash + portfolio value - debt
    # = 150M + 100M - 50M = 200M
    assert net_worth == 200_000_000


def test_acquisition_flow():
    """Test basic acquisition flow."""
    player = Player(starting_cash=100_000_000)
    market = Market()
    
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25
    )
    company.calculate_valuation(market)
    
    purchase_price = company.current_valuation
    
    # Acquire company
    if purchase_price <= player.cash:
        player.adjust_cash(-purchase_price)
        company.acquisition_price = purchase_price
        player.add_company(company)
        
        assert company in player.portfolio
        assert player.cash == 100_000_000 - purchase_price


def test_quarter_advancement():
    """Test quarter advancement logic."""
    player = Player()
    market = Market()
    tm = TimeManager(total_quarters=20)
    
    # Add a company
    company = Company(
        name="Test Corp",
        sector="Technology",
        revenue=50_000_000,
        ebitda_margin=0.25
    )
    player.add_company(company)
    
    initial_quarter = tm.current_quarter
    initial_revenue = company.revenue
    
    # Advance quarter
    market.update_quarter()
    market_conditions = market.get_conditions_summary()
    market_conditions['sector_multipliers'] = {s: 1.0 for s in market.sector_multiples.keys()}
    company.simulate_quarter(market_conditions)
    tm.advance_quarter()
    
    assert tm.current_quarter == initial_quarter + 1
    assert len(company.revenue_history) == 2


def test_game_engine_initialization():
    """Test game engine initialization."""
    engine = GameEngine()
    
    assert engine.player is not None
    assert engine.market is not None
    assert engine.time_manager is not None
    assert engine.running == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

