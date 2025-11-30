"""
Menus - user-facing menu system for the game.
"""

from typing import List, Optional, Dict, Any
from models.player import Player
from models.company import Company
from models.market import Market
from models.deal import Deal
from game import input_handlers as ih
from ui import table_views as tv


def main_menu(player: Player, market: Market, time_manager: 'TimeManager') -> str:
    """
    Display main menu and get player's action choice.
    
    Returns:
        Action string: 'acquire', 'operate', 'exit', 'portfolio', 'market', 'advance', 'save', 'quit'
    """
    ih.clear_screen()
    
    print("=" * 70)
    print(f"PRIVATE EQUITY SIMULATOR - {time_manager.get_time_display()}")
    print("=" * 70)
    print(f"\nCash: ${player.cash:,.0f}")
    print(f"Debt: ${player.current_debt:,.0f} / ${player.get_debt_capacity():,.0f} ({player.get_debt_utilization():.0%} utilized)")
    print(f"Available Capital: ${player.available_capital():,.0f}")
    print(f"Portfolio Value: ${player.compute_portfolio_value():,.0f}")
    print(f"Net Worth: ${player.compute_net_worth():,.0f}")
    print(f"Reputation: {player.reputation:.0%}")
    print(f"Portfolio Companies: {len(player.portfolio)}")
    
    options = [
        "View Portfolio",
        "View Market Conditions",
        "Acquire Company",
        "Operate Portfolio Companies",
        "Exit Investment",
        "Advance to Next Quarter",
        "Save & Continue",
        "Save & Exit",
        "Quit Game (without saving)"
    ]
    
    actions = ['portfolio', 'market', 'acquire', 'operate', 'exit', 'advance', 'save_continue', 'save_exit', 'quit']
    
    choice = ih.prompt_choice(options, "What would you like to do?")
    
    if choice < 0 or choice >= len(actions):
        return 'quit'
        
    return actions[choice]


def acquisition_menu(available_companies: List[Company], player: Player, market: Market) -> Optional[Company]:
    """
    Display available companies for acquisition.
    
    Returns:
        Selected company or None
    """
    if not available_companies:
        print("\nNo companies available for acquisition this quarter.")
        ih.press_enter_to_continue()
        return None
        
    ih.clear_screen()
    print("=" * 70)
    print("AVAILABLE ACQUISITION TARGETS")
    print("=" * 70)
    
    tv.display_company_list(available_companies)
    
    print(f"\nYour available capital: ${player.available_capital():,.0f}")
    
    options = [f"{c.name} - ${c.current_valuation:,.0f}" for c in available_companies]
    options.append("Cancel")
    
    choice = ih.prompt_choice(options, "Select a company to review")
    
    if choice < 0 or choice >= len(available_companies):
        return None
        
    return available_companies[choice]


def deal_negotiation_menu(deal: Deal, player: Player) -> str:
    """
    Handle deal negotiation.
    
    Returns:
        Action: 'offer', 'accept', 'walk'
    """
    ih.clear_screen()
    print("=" * 70)
    print(f"DEAL NEGOTIATION: {deal.company.name}")
    print("=" * 70)
    
    tv.display_company_detail(deal.company)
    
    print(f"\n{'Asking Price:':<30} ${deal.asking_price:,.0f}")
    print(f"{'Fair Value (estimate):':<30} ${deal.fair_value:,.0f}")
    print(f"{'Your Cash:':<30} ${player.cash:,.0f}")
    print(f"{'Available Capital:':<30} ${player.available_capital():,.0f}")
    
    if deal.current_offer:
        print(f"{'Your Last Offer:':<30} ${deal.current_offer:,.0f}")
        
    print(f"\nNegotiation Rounds Remaining: {deal.max_counter_offers - deal.counter_offers}")
    
    options = [
        f"Accept asking price (${deal.asking_price:,.0f})",
        "Make an offer",
        "Walk away"
    ]
    
    actions = ['accept', 'offer', 'walk']
    
    choice = ih.prompt_choice(options, "What would you like to do?")
    
    if choice < 0 or choice >= len(actions):
        return 'walk'
        
    return actions[choice]


def portfolio_menu(player: Player) -> Optional[Company]:
    """
    Display portfolio and allow selection of a company for viewing (read-only).
    
    Returns:
        Selected company or None
    """
    if not player.portfolio:
        print("\nYour portfolio is empty.")
        ih.press_enter_to_continue()
        return None
        
    ih.clear_screen()
    print("=" * 70)
    print("YOUR PORTFOLIO")
    print("=" * 70)
    
    tv.display_portfolio(player.portfolio)
    
    print(f"\nTotal Portfolio Value: ${player.compute_portfolio_value():,.0f}")
    
    options = [f"{c.name}" for c in player.portfolio]
    options.append("Back to Main Menu")
    
    choice = ih.prompt_choice(options, "Select a company to view details")
    
    if choice < 0 or choice >= len(player.portfolio):
        return None
        
    return player.portfolio[choice]


def portfolio_operations_menu(player: Player, current_quarter: int) -> Optional[Company]:
    """
    Display portfolio for operations and allow selection of a company.
    Shows which companies have already been operated on this quarter.
    
    Returns:
        Selected company or None
    """
    if not player.portfolio:
        print("\nYour portfolio is empty.")
        ih.press_enter_to_continue()
        return None
        
    ih.clear_screen()
    print("=" * 70)
    print("PORTFOLIO OPERATIONS")
    print("=" * 70)
    print("\nNote: You can only perform ONE operation per company per quarter.")
    print("Companies already operated on this quarter are marked with ✗\n")
    
    tv.display_portfolio(player.portfolio)
    
    # Build options list with availability indicators
    options = []
    available_companies = []
    
    for i, company in enumerate(player.portfolio):
        can_operate = company.can_operate(current_quarter)
        status = "✓" if can_operate else "✗"
        options.append(f"{status} {company.name} {'[OPERATED]' if not can_operate else ''}")
        if can_operate:
            available_companies.append((i, company))
    
    options.append("Back to Main Menu")
    
    if not available_companies:
        print("\n⚠️  All companies have been operated on this quarter!")
        print("Advance to the next quarter to operate on them again.")
        ih.press_enter_to_continue()
        return None
    
    choice = ih.prompt_choice(options, "Select a company to operate on")
    
    if choice < 0 or choice >= len(player.portfolio):
        return None
    
    # Check if selected company can be operated on
    selected_company = player.portfolio[choice]
    if not selected_company.can_operate(current_quarter):
        print(f"\n⚠️  {selected_company.name} has already been operated on this quarter!")
        ih.press_enter_to_continue()
        return None
        
    return selected_company


def company_operations_menu(company: Company, player: Player) -> str:
    """
    Menu for operating on a portfolio company.
    
    Returns:
        Action: 'cost_cutting', 'capex', 'replace_mgmt', 'strategy', 'back'
    """
    ih.clear_screen()
    print("=" * 70)
    print(f"OPERATIONS: {company.name}")
    print("=" * 70)
    
    tv.display_company_detail(company)
    
    options = [
        "Implement Cost Cutting",
        "Invest in Capex/Growth",
        "Replace Management",
        "Pursue Growth Strategy",
        "Back"
    ]
    
    actions = ['cost_cutting', 'capex', 'replace_mgmt', 'strategy', 'back']
    
    choice = ih.prompt_choice(options, "What operation would you like to perform?")
    
    if choice < 0 or choice >= len(actions):
        return 'back'
        
    return actions[choice]


def exit_menu(player: Player, market: Market) -> Optional[Company]:
    """
    Menu for exiting an investment.
    
    Returns:
        Selected company or None
    """
    if not player.portfolio:
        print("\nYour portfolio is empty.")
        ih.press_enter_to_continue()
        return None
        
    ih.clear_screen()
    print("=" * 70)
    print("EXIT INVESTMENT")
    print("=" * 70)
    
    tv.display_portfolio(player.portfolio)
    
    options = [f"{c.name} - Current Value: ${c.current_valuation:,.0f}" for c in player.portfolio]
    options.append("Cancel")
    
    choice = ih.prompt_choice(options, "Select a company to exit")
    
    if choice < 0 or choice >= len(player.portfolio):
        return None
        
    return player.portfolio[choice]


def market_overview_menu(market: Market) -> None:
    """Display market conditions overview."""
    ih.clear_screen()
    print("=" * 70)
    print("MARKET CONDITIONS")
    print("=" * 70)
    
    tv.display_market_conditions(market)
    
    ih.press_enter_to_continue()


def event_menu(event: Dict[str, Any]) -> Optional[str]:
    """
    Display an event and get player response.
    
    Returns:
        Player's choice or None
    """
    ih.clear_screen()
    print("=" * 70)
    print(f"EVENT: {event['title']}")
    print("=" * 70)
    
    print(f"\n{event['description']}\n")
    
    if event.get('effects'):
        print("Effects:")
        for effect, value in event['effects'].items():
            if isinstance(value, float):
                print(f"  • {effect}: {value:+.1%}")
            else:
                print(f"  • {effect}: {value}")
                
    # If event requires action, present choices
    if event.get('effects', {}).get('requires_action'):
        options = [
            "Address the issue immediately",
            "Monitor the situation",
            "Ignore for now"
        ]
        choice = ih.prompt_choice(options, "How would you like to respond?")
        choices = ['immediate', 'monitor', 'ignore']
        return choices[choice] if 0 <= choice < len(choices) else 'ignore'
    else:
        ih.press_enter_to_continue()
        return None


def save_game_menu() -> Optional[str]:
    """
    Menu for saving the game.
    
    Returns:
        Save name or None if cancelled
    """
    from game.save_system import list_save_files
    
    ih.clear_screen()
    print("=" * 70)
    print("SAVE GAME")
    print("=" * 70)
    
    # Show existing saves
    saves = list_save_files()
    if saves:
        print("\nExisting saves:")
        for i, (name, timestamp, quarter) in enumerate(saves, 1):
            print(f"  {i}. {name} - {quarter} (saved: {timestamp[:19]})")
    else:
        print("\nNo existing saves.")
    
    print("\nEnter a name for your save (or press Enter to cancel):")
    save_name = ih.prompt_text("Save name", allow_empty=True)
    
    if not save_name:
        return None
    
    # Sanitize filename
    save_name = "".join(c for c in save_name if c.isalnum() or c in (' ', '-', '_')).strip()
    
    if not save_name:
        print("Invalid save name!")
        ih.press_enter_to_continue()
        return None
    
    return save_name


def load_game_menu() -> Optional[str]:
    """
    Menu for loading a saved game.
    
    Returns:
        Save name or None if cancelled
    """
    from game.save_system import list_save_files
    
    ih.clear_screen()
    print("=" * 70)
    print("LOAD GAME")
    print("=" * 70)
    
    saves = list_save_files()
    
    if not saves:
        print("\nNo save files found!")
        ih.press_enter_to_continue()
        return None
    
    print("\nAvailable saves:")
    options = [f"{name} - {quarter} (saved: {timestamp[:19]})" 
               for name, timestamp, quarter in saves]
    options.append("Cancel")
    
    choice = ih.prompt_choice(options, "Select a save to load")
    
    if choice < 0 or choice >= len(saves):
        return None
    
    return saves[choice][0]  # Return save name



def sector_selection_menu() -> str:
    """
    Display menu for selecting a sector to browse companies.
    
    Returns:
        Selected sector name or None if back
    """
    from simulation.procedural_gen import get_sectors
    
    ih.clear_screen()
    print("=" * 70)
    print("SELECT SECTOR TO BROWSE")
    print("=" * 70)
    print("\nChoose a sector to view available companies:\n")
    
    sectors = get_sectors()
    options = sectors + ["Back to Main Menu"]
    
    choice = ih.prompt_choice(options, "Select a sector")
    
    if choice < 0 or choice >= len(sectors):
        return None
        
    return sectors[choice]


def valuation_tier_menu(sector: str) -> str:
    """
    Display menu for selecting a valuation tier within a sector.
    
    Args:
        sector: The selected sector
        
    Returns:
        Selected tier name or None if back
    """
    ih.clear_screen()
    print("=" * 70)
    print(f"SELECT VALUATION TIER - {sector.upper()}")
    print("=" * 70)
    print("\nChoose a price range:\n")
    
    tiers = {
        'micro': ('Micro', '$500K - $2M', 'Small local businesses'),
        'small': ('Small', '$2M - $5M', 'Established local/regional companies'),
        'medium': ('Medium', '$5M - $15M', 'Regional leaders'),
        'large': ('Large', '$15M - $50M', 'Large regional/national players')
    }
    
    tier_keys = list(tiers.keys())
    options = []
    
    for tier_key in tier_keys:
        name, range_str, desc = tiers[tier_key]
        options.append(f"{name:8} {range_str:15} - {desc}")
    
    options.append("Back to Sector Selection")
    
    choice = ih.prompt_choice(options, "Select a tier")
    
    if choice < 0 or choice >= len(tier_keys):
        return None
        
    return tier_keys[choice]


def tiered_company_selection_menu(sector: str, tier: str, companies: List) -> Optional[Any]:
    """
    Display companies in a specific sector and tier for selection.
    
    Args:
        sector: The selected sector
        tier: The selected valuation tier
        companies: List of companies in this tier
        
    Returns:
        Selected company or None if back
    """
    from ui import table_views as tv
    
    ih.clear_screen()
    
    tier_names = {
        'micro': 'Micro ($500K - $2M)',
        'small': 'Small ($2M - $5M)',
        'medium': 'Medium ($5M - $15M)',
        'large': 'Large ($15M - $50M)'
    }
    
    print("=" * 70)
    print(f"{sector.upper()} - {tier_names.get(tier, tier.upper())}")
    print("=" * 70)
    print(f"\n{len(companies)} companies available:\n")
    
    # Display companies in a simple table format
    print(f"{'Company':<30} {'Revenue':<15} {'Valuation':<15}")
    print("-" * 70)
    for company in companies:
        print(f"{company.name:<30} ${company.revenue:>12,.0f}  ${company.current_valuation:>12,.0f}")
    print()
    
    options = [f"{c.name} - ${c.current_valuation:,.0f}" for c in companies]
    options.append("Back to Tier Selection")
    
    choice = ih.prompt_choice(options, "Select a company to view details")
    
    if choice < 0 or choice >= len(companies):
        return None
        
    return companies[choice]
