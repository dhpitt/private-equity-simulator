"""
Game Engine - central orchestrator for the PE Simulator.
"""

from typing import List, Optional, Dict, Any
import random

from models.player import Player
from models.company import Company
from models.market import Market
from models.deal import Deal
from game.time_manager import TimeManager
from game import menus
from game import events
from game import input_handlers as ih
from simulation import procedural_gen
from simulation import portfolio_ops
from ui import screens
import config


class GameEngine:
    """Central game engine that orchestrates all game systems."""
    
    def __init__(self):
        # Initialize random seed
        if config.RANDOM_SEED is not None:
            random.seed(config.RANDOM_SEED)
            
        # Initialize game components
        self.player = Player()
        self.market = Market()
        self.time_manager = TimeManager()
        
        # Available companies for acquisition
        self.available_deals: List[Company] = []
        
        # Game state
        self.running = True
        
    def start_game(self) -> None:
        """Start the game and show intro."""
        screens.show_intro()
        self.generate_new_deals()
        self.main_loop()
        
    def main_loop(self) -> None:
        """Main game loop."""
        while self.running and not self.time_manager.is_game_over():
            action = menus.main_menu(self.player, self.market, self.time_manager)
            
            if action == 'quit':
                if ih.prompt_yes_no("Are you sure you want to quit?"):
                    self.running = False
            elif action == 'portfolio':
                self.view_portfolio()
            elif action == 'market':
                self.view_market()
            elif action == 'acquire':
                self.handle_acquisition()
            elif action == 'operate':
                self.operate_portfolio()
            elif action == 'exit':
                self.exit_investment()
            elif action == 'advance':
                self.advance_quarter()
                
        # Game over
        self.end_game()
        
    def advance_quarter(self) -> None:
        """Advance to the next quarter."""
        print("\nAdvancing to next quarter...")
        
        # Update market
        self.market.update_quarter()
        
        # Update all portfolio companies
        market_conditions = self.market.get_conditions_summary()
        market_conditions['sector_multipliers'] = {
            sector: 1.0 for sector in self.market.sector_multiples.keys()
        }
        
        for company in self.player.portfolio:
            company.simulate_quarter(market_conditions)
            company.calculate_valuation(self.market)
            
        # Generate random event
        event = events.generate_event(self.player, self.player.portfolio, self.market)
        if event:
            self.handle_event(event)
            
        # Pay interest on debt
        if self.player.current_debt > 0:
            interest = self.player.current_debt * (self.market.get_debt_rate() / 4)
            self.player.adjust_cash(-interest)
            print(f"\nPaid ${interest:,.0f} in debt interest.")
            
        # Generate new acquisition opportunities
        self.generate_new_deals()
        
        # Advance time
        self.time_manager.advance_quarter()
        
        print(f"\nNow in {self.time_manager.get_time_display()}")
        print(f"Net Worth: ${self.player.compute_net_worth():,.0f}")
        
        ih.press_enter_to_continue()
        
    def generate_new_deals(self) -> None:
        """Generate new companies available for acquisition."""
        self.available_deals = procedural_gen.generate_deal_portfolio(
            config.NUM_AVAILABLE_DEALS,
            self.market
        )
        
    def handle_acquisition(self) -> None:
        """Handle company acquisition flow."""
        selected_company = menus.acquisition_menu(self.available_deals, self.player, self.market)
        
        if selected_company is None:
            return
            
        # Show company details
        ih.clear_screen()
        print("=" * 70)
        print(f"COMPANY DETAILS: {selected_company.name}")
        print("=" * 70)
        from ui import table_views
        table_views.display_company_detail(selected_company)
        
        if not ih.prompt_yes_no("Would you like to proceed with negotiation?"):
            return
            
        # Create deal
        deal = Deal(selected_company, deal_type='acquisition')
        
        # Negotiation loop
        while not deal.deal_closed:
            action = menus.deal_negotiation_menu(deal, self.player)
            
            if action == 'accept':
                result = deal.accept_asking_price()
                print(f"\n{result['message']}")
                
                if result['accepted']:
                    self.complete_acquisition(selected_company, result['final_price'])
                    
                ih.press_enter_to_continue()
                break
                
            elif action == 'offer':
                max_offer = self.player.available_capital()
                offer = ih.prompt_number(
                    "Enter your offer",
                    min_value=0,
                    max_value=max_offer,
                    allow_float=False
                )
                
                if offer is None:
                    continue
                    
                result = deal.make_offer(offer)
                print(f"\n{result['message']}")
                
                if result['accepted']:
                    self.complete_acquisition(selected_company, result['final_price'])
                    ih.press_enter_to_continue()
                    break
                elif 'counter_offer' in result:
                    deal.asking_price = result['counter_offer']
                    ih.press_enter_to_continue()
                else:
                    ih.press_enter_to_continue()
                    break
                    
            else:  # walk away
                result = deal.walk_away()
                print(f"\n{result['message']}")
                ih.press_enter_to_continue()
                break
                
    def complete_acquisition(self, company: Company, price: float) -> None:
        """Complete an acquisition transaction."""
        # Check if player has enough cash
        if price <= self.player.cash:
            # All cash deal
            self.player.adjust_cash(-price)
            debt_used = 0
        else:
            # Need to use debt
            cash_available = self.player.cash
            debt_needed = price - cash_available
            
            if self.player.take_debt(debt_needed):
                debt_used = debt_needed
                self.player.adjust_cash(-cash_available)
            else:
                print("\nInsufficient capital to complete acquisition!")
                return
                
        # Add company to portfolio
        company.acquisition_price = price
        company.acquisition_quarter = self.time_manager.current_quarter
        self.player.add_company(company)
        
        # Remove from available deals
        if company in self.available_deals:
            self.available_deals.remove(company)
            
        # Record deal
        self.player.record_deal('acquisition', company.name, price, self.time_manager.current_quarter)
        
        print(f"\nAcquisition completed!")
        print(f"Purchase price: ${price:,.0f}")
        if debt_used > 0:
            print(f"Debt used: ${debt_used:,.0f}")
        print(f"Cash remaining: ${self.player.cash:,.0f}")
        
    def operate_portfolio(self) -> None:
        """Operate on portfolio companies."""
        company = menus.portfolio_menu(self.player)
        
        if company is None:
            return
            
        while True:
            action = menus.company_operations_menu(company, self.player)
            
            if action == 'back':
                break
            elif action == 'cost_cutting':
                self.handle_cost_cutting(company)
            elif action == 'capex':
                self.handle_capex_investment(company)
            elif action == 'replace_mgmt':
                self.handle_management_replacement(company)
            elif action == 'strategy':
                self.handle_growth_strategy(company)
                
    def handle_cost_cutting(self, company: Company) -> None:
        """Handle cost cutting operation."""
        print("\nCost Cutting Initiative")
        print("Higher intensity improves margins but may hurt growth.")
        
        intensity = ih.prompt_number("Enter intensity (0-100)", min_value=0, max_value=100)
        if intensity is None:
            return
            
        intensity_normalized = intensity / 100
        
        result = portfolio_ops.apply_cost_cutting(company, intensity_normalized)
        
        print(f"\n{result['message']}")
        if result.get('morale_impact'):
            print("Warning: Aggressive cost cutting hurt employee morale.")
            
        ih.press_enter_to_continue()
        
    def handle_capex_investment(self, company: Company) -> None:
        """Handle capex investment."""
        print("\nCapital Investment")
        print(f"Company revenue: ${company.revenue:,.0f}")
        print(f"Your available cash: ${self.player.cash:,.0f}")
        
        amount = ih.prompt_number(
            "Enter investment amount",
            min_value=0,
            max_value=self.player.cash,
            allow_float=False
        )
        
        if amount is None or amount == 0:
            return
            
        result = portfolio_ops.apply_capex_investment(company, amount)
        self.player.adjust_cash(-amount)
        
        print(f"\n{result['message']}")
        ih.press_enter_to_continue()
        
    def handle_management_replacement(self, company: Company) -> None:
        """Handle management replacement."""
        print(f"\nCurrent Manager: {company.manager}")
        print(f"Replacement cost: ${config.MANAGER_REPLACEMENT_COST:,.0f}")
        
        if not ih.prompt_yes_no("Proceed with management replacement?"):
            return
            
        result = portfolio_ops.replace_management(company, self.player)
        
        print(f"\n{result['message']}")
        if result['success']:
            print(f"New Manager: {result['new_manager']}")
            
        ih.press_enter_to_continue()
        
    def handle_growth_strategy(self, company: Company) -> None:
        """Handle growth strategy selection."""
        print("\nGrowth Strategies:")
        
        options = [
            "Roll-up Strategy (acquire competitors)",
            "Expansion Strategy (new markets/geographies)",
            "Diversification Strategy (new products/services)",
            "Cancel"
        ]
        
        choice = ih.prompt_choice(options, "Select a strategy")
        
        strategies = ['roll_up', 'expand', 'diversify']
        
        if choice < 0 or choice >= len(strategies):
            return
            
        strategy = strategies[choice]
        
        result = portfolio_ops.pursue_acquisition_strategy(company, strategy)
        
        if result.get('cost'):
            if self.player.cash >= result['cost']:
                self.player.adjust_cash(-result['cost'])
            else:
                print("\nInsufficient cash for this strategy!")
                ih.press_enter_to_continue()
                return
                
        print(f"\n{result['message']}")
        ih.press_enter_to_continue()
        
    def exit_investment(self) -> None:
        """Handle investment exit."""
        company = menus.exit_menu(self.player, self.market)
        
        if company is None:
            return
            
        # Create exit deal
        deal = Deal(company, deal_type='exit')
        
        print(f"\nBuyer offers: ${deal.asking_price:,.0f}")
        print(f"Your acquisition price: ${company.acquisition_price:,.0f}")
        
        profit = deal.asking_price - company.acquisition_price
        print(f"Profit/Loss: ${profit:,.0f} ({profit/company.acquisition_price:+.1%})")
        
        if ih.prompt_yes_no("Accept this offer?"):
            # Complete exit
            self.player.adjust_cash(deal.asking_price)
            self.player.remove_company(company)
            self.player.record_deal('exit', company.name, deal.asking_price, 
                                  self.time_manager.current_quarter)
            
            print(f"\nInvestment exited successfully!")
            print(f"Proceeds: ${deal.asking_price:,.0f}")
            
        ih.press_enter_to_continue()
        
    def view_portfolio(self) -> None:
        """View portfolio in detail."""
        company = menus.portfolio_menu(self.player)
        
        if company:
            ih.clear_screen()
            from ui import table_views
            table_views.display_company_detail(company)
            ih.press_enter_to_continue()
            
    def view_market(self) -> None:
        """View market conditions."""
        menus.market_overview_menu(self.market)
        
    def handle_event(self, event: Dict[str, Any]) -> None:
        """Handle a random event."""
        player_choice = menus.event_menu(event)
        
        # Apply event effects
        target = event.get('target')
        effects = event.get('effects', {})
        
        if isinstance(target, Market):
            # Market event
            if 'market_growth_change' in effects:
                self.market.growth_rate += effects['market_growth_change']
            if 'interest_rate_change' in effects:
                self.market.interest_rate += effects['interest_rate_change']
            if 'multiple_compression' in effects:
                for sector in self.market.sector_multiples:
                    self.market.sector_multiples[sector] *= (1 - effects['multiple_compression'])
            if 'multiple_expansion' in effects:
                for sector in self.market.sector_multiples:
                    self.market.sector_multiples[sector] *= (1 + effects['multiple_expansion'])
                    
        elif isinstance(target, Company):
            # Company event
            target.apply_event(effects)
            
            # If player chose to address issue, provide some mitigation
            if player_choice == 'immediate':
                # Reduce negative impact by 50%
                for key in ['revenue_impact', 'margin_impact', 'growth_impact']:
                    if key in effects and effects[key] < 0:
                        mitigation = effects[key] * 0.5
                        # Reverse some damage
                        if key == 'revenue_impact':
                            target.revenue *= (1 - mitigation / (1 + effects[key]))
                        elif key == 'margin_impact':
                            target.ebitda_margin -= mitigation
                        elif key == 'growth_impact':
                            target.growth_rate -= mitigation
                            
    def end_game(self) -> None:
        """End the game and show summary."""
        screens.show_endgame_summary(self.player, self.time_manager)

