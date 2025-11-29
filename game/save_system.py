"""
Save/Load system for PE Simulator.
Handles serialization and deserialization of game state.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


SAVES_DIR = Path("saves")


def ensure_saves_directory():
    """Ensure the saves directory exists."""
    SAVES_DIR.mkdir(exist_ok=True)


def serialize_game_state(engine: 'GameEngine') -> Dict[str, Any]:
    """
    Serialize game state to a dictionary.
    
    Args:
        engine: GameEngine instance
        
    Returns:
        Dictionary containing all game state
    """
    from models.company import Company
    
    # Serialize player
    player_data = {
        'cash': engine.player.cash,
        'current_debt': engine.player.current_debt,
        'base_debt_capacity': engine.player.base_debt_capacity,
        'reputation': engine.player.reputation,
        'deal_history': engine.player.deal_history,
        'portfolio': []
    }
    
    # Serialize portfolio companies
    for company in engine.player.portfolio:
        company_data = {
            'name': company.name,
            'sector': company.sector,
            'revenue': company.revenue,
            'ebitda_margin': company.ebitda_margin,
            'growth_rate': company.growth_rate,
            'volatility': company.volatility,
            'valuation_multiple': company.valuation_multiple,
            'acquisition_price': company.acquisition_price,
            'acquisition_quarter': company.acquisition_quarter,
            'current_valuation': company.current_valuation,
            'revenue_history': company.revenue_history,
            'ebitda_history': company.ebitda_history,
            'manager': {
                'name': company.manager.name,
                'competence': company.manager.competence,
                'risk_profile': company.manager.risk_profile,
                'cooperativeness': company.manager.cooperativeness
            }
        }
        player_data['portfolio'].append(company_data)
    
    # Serialize market
    market_data = {
        'interest_rate': engine.market.interest_rate,
        'growth_rate': engine.market.growth_rate,
        'sector_multiples': engine.market.sector_multiples,
        'credit_conditions': engine.market.credit_conditions,
        'interest_rate_history': engine.market.interest_rate_history,
        'growth_rate_history': engine.market.growth_rate_history
    }
    
    # Serialize time manager
    time_data = {
        'current_quarter': engine.time_manager.current_quarter,
        'current_year': engine.time_manager.current_year,
        'total_quarters': engine.time_manager.total_quarters
    }
    
    # Serialize available deals
    deals_data = []
    for company in engine.available_deals:
        deal_data = {
            'name': company.name,
            'sector': company.sector,
            'revenue': company.revenue,
            'ebitda_margin': company.ebitda_margin,
            'growth_rate': company.growth_rate,
            'volatility': company.volatility,
            'valuation_multiple': company.valuation_multiple,
            'current_valuation': company.current_valuation,
            'manager': {
                'name': company.manager.name,
                'competence': company.manager.competence,
                'risk_profile': company.manager.risk_profile,
                'cooperativeness': company.manager.cooperativeness
            }
        }
        deals_data.append(deal_data)
    
    return {
        'version': '2.0',
        'timestamp': datetime.now().isoformat(),
        'player': player_data,
        'market': market_data,
        'time': time_data,
        'available_deals': deals_data
    }


def deserialize_game_state(data: Dict[str, Any], engine: 'GameEngine') -> None:
    """
    Deserialize game state from a dictionary and apply to engine.
    
    Args:
        data: Dictionary containing game state
        engine: GameEngine instance to populate
    """
    from models.company import Company
    from models.manager import Manager
    
    # Restore player
    player_data = data['player']
    engine.player.cash = player_data['cash']
    engine.player.current_debt = player_data['current_debt']
    engine.player.base_debt_capacity = player_data['base_debt_capacity']
    engine.player.reputation = player_data['reputation']
    engine.player.deal_history = player_data['deal_history']
    engine.player.portfolio = []
    
    # Restore portfolio companies
    for company_data in player_data['portfolio']:
        mgr_data = company_data['manager']
        manager = Manager(
            name=mgr_data['name'],
            competence=mgr_data['competence'],
            risk_profile=mgr_data['risk_profile'],
            cooperativeness=mgr_data['cooperativeness']
        )
        
        company = Company(
            name=company_data['name'],
            sector=company_data['sector'],
            revenue=company_data['revenue'],
            ebitda_margin=company_data['ebitda_margin'],
            growth_rate=company_data['growth_rate'],
            volatility=company_data['volatility'],
            manager=manager,
            valuation_multiple=company_data['valuation_multiple']
        )
        
        company.acquisition_price = company_data['acquisition_price']
        company.acquisition_quarter = company_data['acquisition_quarter']
        company.current_valuation = company_data['current_valuation']
        company.revenue_history = company_data['revenue_history']
        company.ebitda_history = company_data['ebitda_history']
        
        engine.player.portfolio.append(company)
    
    # Restore market
    market_data = data['market']
    engine.market.interest_rate = market_data['interest_rate']
    engine.market.growth_rate = market_data['growth_rate']
    engine.market.sector_multiples = market_data['sector_multiples']
    engine.market.credit_conditions = market_data['credit_conditions']
    engine.market.interest_rate_history = market_data['interest_rate_history']
    engine.market.growth_rate_history = market_data['growth_rate_history']
    
    # Restore time manager
    time_data = data['time']
    engine.time_manager.current_quarter = time_data['current_quarter']
    engine.time_manager.current_year = time_data['current_year']
    engine.time_manager.total_quarters = time_data['total_quarters']
    
    # Restore available deals
    engine.available_deals = []
    for deal_data in data['available_deals']:
        mgr_data = deal_data['manager']
        manager = Manager(
            name=mgr_data['name'],
            competence=mgr_data['competence'],
            risk_profile=mgr_data['risk_profile'],
            cooperativeness=mgr_data['cooperativeness']
        )
        
        company = Company(
            name=deal_data['name'],
            sector=deal_data['sector'],
            revenue=deal_data['revenue'],
            ebitda_margin=deal_data['ebitda_margin'],
            growth_rate=deal_data['growth_rate'],
            volatility=deal_data['volatility'],
            manager=manager,
            valuation_multiple=deal_data['valuation_multiple']
        )
        
        company.current_valuation = deal_data['current_valuation']
        engine.available_deals.append(company)


def save_game(engine: 'GameEngine', save_name: str) -> bool:
    """
    Save game state to a file.
    
    Args:
        engine: GameEngine instance
        save_name: Name for the save file (without extension)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_saves_directory()
        
        game_state = serialize_game_state(engine)
        save_path = SAVES_DIR / f"{save_name}.json"
        
        with open(save_path, 'w') as f:
            json.dump(game_state, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False


def load_game(save_name: str, engine: 'GameEngine') -> bool:
    """
    Load game state from a file.
    
    Args:
        save_name: Name of the save file (without extension)
        engine: GameEngine instance to populate
        
    Returns:
        True if successful, False otherwise
    """
    try:
        save_path = SAVES_DIR / f"{save_name}.json"
        
        if not save_path.exists():
            print(f"Save file not found: {save_name}")
            return False
        
        with open(save_path, 'r') as f:
            game_state = json.load(f)
        
        deserialize_game_state(game_state, engine)
        
        return True
    except Exception as e:
        print(f"Error loading game: {e}")
        return False


def list_save_files() -> list:
    """
    List all available save files.
    
    Returns:
        List of tuples: (save_name, timestamp, quarter)
    """
    ensure_saves_directory()
    
    saves = []
    for save_file in SAVES_DIR.glob("*.json"):
        try:
            with open(save_file, 'r') as f:
                data = json.load(f)
            
            save_name = save_file.stem
            timestamp = data.get('timestamp', 'Unknown')
            quarter = data['time']['current_quarter']
            year = data['time']['current_year']
            
            saves.append((save_name, timestamp, f"Year {year}, Q{quarter % 4 + 1}"))
        except Exception:
            continue
    
    return sorted(saves, key=lambda x: x[1], reverse=True)


def delete_save(save_name: str) -> bool:
    """
    Delete a save file.
    
    Args:
        save_name: Name of the save file (without extension)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        save_path = SAVES_DIR / f"{save_name}.json"
        if save_path.exists():
            save_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting save: {e}")
        return False
