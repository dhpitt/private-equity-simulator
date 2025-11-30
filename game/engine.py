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
    
    def __init__(self, difficulty: str = 'medium', fund_name: str = None):
        # Initialize random seed
        if config.RANDOM_SEED is not None:
            random.seed(config.RANDOM_SEED)
            
        # Initialize game components with difficulty
        self.player = Player(fund_name=fund_name, difficulty=difficulty)
        self.market = Market(difficulty=difficulty)
        self.time_manager = TimeManager()
        
        # Available companies for acquisition (organized by sector/tier)
        self.available_deals: Dict[str, Dict[str, List[Company]]] = {}
        
        # Game state
        self.running = True
        
    def start_game(self) -> None:
        """Start the game and show intro or load menu."""
        # Check if user wants to load a game
        from game.save_system import GameSaver
        
        saves = GameSaver.list_saves()
        
        if saves:
            print("\n" + "=" * 70)
            print("WELCOME TO PE SIMULATOR")
            print("=" * 70)
            options = ["Start New Game", "Load Saved Game"]
            choice = ih.prompt_choice(options, "What would you like to do?")
            
            if choice == 1:  # Load game
                self.load_game_menu()
                self.main_loop()
                return
        
        # New game - select difficulty and fund name
        # Note: __init__ was already called with defaults, so we need to reinitialize
        # with the player's choices
        difficulty = screens.select_difficulty()
        fund_name = screens.select_fund_name()
        
        # Reinitialize with player choices
        self.player = Player(fund_name=fund_name, difficulty=difficulty)
        self.market = Market(difficulty=difficulty)
        
        screens.show_intro(self.player, self.market)
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
            elif action == 'save_continue':
                self.save_game()
            elif action == 'save_exit':
                self.save_game()
                self.running = False
                
        # Game over
        self.end_game()
        
    def advance_quarter(self) -> None:
        """Advance to the next quarter."""
        print("\nAdvancing to next quarter...")
        
        # Show inspirational quote screen
        from ui import screens
        screens.show_quote_screen()
        
        # Calculate profit before quarter simulation
        starting_cash = self.player.cash
        starting_portfolio_value = self.player.compute_portfolio_value()
        
        # Update market
        self.market.update_quarter()
        
        # Update all portfolio companies
        market_conditions = self.market.get_conditions_summary()
        market_conditions['sector_multipliers'] = {
            sector: 1.0 for sector in self.market.sector_multiples.keys()
        }
        
        # Track manager narratives
        manager_narratives = []
        
        for company in self.player.portfolio:
            performance = company.simulate_quarter(market_conditions)
            company.calculate_valuation(self.market)
            # Reset operation tracking for new quarter
            company.reset_quarterly_operations()
            
            # Generate manager narrative if noteworthy
            from simulation import manager_system
            narrative = manager_system.get_quarterly_performance_narrative(
                company, 
                performance['manager_impact'], 
                performance['growth']
            )
            
            if narrative:
                manager_narratives.append((company.name, narrative))
            
        # Generate random event
        event = events.generate_event(self.player, self.player.portfolio, self.market)
        if event:
            self.handle_event(event)
        
        # Display manager performance narratives
        if manager_narratives:
            print("\n" + "=" * 70)
            print("MANAGEMENT REPORTS")
            print("=" * 70)
            for company_name, narrative in manager_narratives:
                print(f"\n📊 {company_name}:")
                print(f"   {narrative}")
            
        # Pay interest on debt
        if self.player.current_debt > 0:
            interest = self.player.current_debt * (self.market.get_debt_rate() / 4)
            
            if self.player.cash >= interest:
                # Can afford to pay interest
                self.player.adjust_cash(-interest)
                print(f"\nPaid ${interest:,.0f} in debt interest.")
            else:
                # Cannot afford interest - capitalize it into debt
                unpaid_interest = interest - self.player.cash
                
                if self.player.cash > 0:
                    # Pay what we can
                    paid_amount = self.player.cash
                    self.player.adjust_cash(-paid_amount)
                    print(f"\nPaid ${paid_amount:,.0f} in debt interest from cash.")
                
                # Add unpaid interest to debt
                self.player.current_debt += unpaid_interest
                print(f"⚠️  Insufficient cash! ${unpaid_interest:,.0f} in unpaid interest added to debt.")
                print(f"Total debt is now ${self.player.current_debt:,.0f}")
                
                # This hurts reputation
                self.player.adjust_reputation(-0.02)
                print(f"📉 Reputation decreased by 2% for missing interest payment (now {self.player.reputation:.0%})")
        
        # Calculate quarterly profit and update reputation
        ending_cash = self.player.cash
        ending_portfolio_value = self.player.compute_portfolio_value()
        
        quarterly_profit = (ending_cash - starting_cash) + (ending_portfolio_value - starting_portfolio_value)
        reputation_change = self.player.update_reputation_from_profits(quarterly_profit)
        
        if reputation_change > 0:
            print(f"\n📈 Reputation increased by {reputation_change:.1%} from profitable quarter (now {self.player.reputation:.0%})")
        elif reputation_change < 0:
            print(f"\n📉 Reputation decreased by {abs(reputation_change):.1%} from unprofitable quarter (now {self.player.reputation:.0%})")
            
        # Generate new acquisition opportunities
        self.generate_new_deals()
        
        # Advance time
        self.time_manager.advance_quarter()
        
        print(f"\nNow in {self.time_manager.get_time_display()}")
        print(f"Net Worth: ${self.player.compute_net_worth():,.0f}")
        
        ih.press_enter_to_continue()
        
    def generate_new_deals(self) -> None:
        """Generate new companies available for acquisition organized by sector and tier."""
        self.available_deals = procedural_gen.generate_tiered_deal_portfolio(self.market)
        
    def handle_acquisition(self) -> None:
        """Handle company acquisition flow with hierarchical navigation."""
        while True:
            # Step 1: Select sector
            sector = menus.sector_selection_menu()
            if sector is None:
                return
            
            # Step 2: Select valuation tier
            while True:
                tier = menus.valuation_tier_menu(sector)
                if tier is None:
                    break  # Back to sector selection
                
                # Step 3: Select company
                companies = self.available_deals.get(sector, {}).get(tier, [])
                
                if not companies:
                    print(f"\nNo companies available in this tier right now.")
                    ih.press_enter_to_continue()
                    continue
                
                while True:
                    company = menus.tiered_company_selection_menu(sector, tier, companies)
                    
                    if company is None:
                        break  # Back to tier selection
                    
                    # Show company details
                    ih.clear_screen()
                    print("=" * 70)
                    print(f"COMPANY DETAILS: {company.name}")
                    print("=" * 70)
                    from ui import table_views
                    table_views.display_company_detail(company)
                    
                    # Check if player can afford
                    max_affordable = self.player.cash + (self.player.get_debt_capacity() - self.player.current_debt)
                    
                    if company.current_valuation > max_affordable:
                        print(f"\n⚠️  This company costs ${company.current_valuation:,.0f}")
                        print(f"Your maximum capital (cash + available debt): ${max_affordable:,.0f}")
                        print("\nYou cannot afford this acquisition. Build your reputation and net worth!")
                        ih.press_enter_to_continue()
                        continue
                    
                    # Negotiate
                    if ih.prompt_yes_no("Proceed with acquisition?"):
                        deal = Deal(company, deal_type='acquisition')
                        
                        # Simple negotiation
                        while not deal.deal_closed:
                            action = menus.deal_negotiation_menu(deal, self.player)
                            
                            if action == 'accept':
                                result = deal.accept_asking_price()
                                print(f"\n{result['message']}")
                                
                                if result['accepted']:
                                    self.complete_acquisition(company, result['final_price'])
                                    
                                    # Remove from available deals
                                    if company in companies:
                                        companies.remove(company)
                                    
                                    ih.press_enter_to_continue()
                                    return  # Exit acquisition flow
                                
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
                                    self.complete_acquisition(company, result['final_price'])
                                    
                                    # Remove from available deals
                                    if company in companies:
                                        companies.remove(company)
                                    
                                    ih.press_enter_to_continue()
                                    return
                                elif 'counter_offer' in result:
                                    deal.asking_price = result['counter_offer']
                                ih.press_enter_to_continue()
                                
                            else:  # walk away
                                result = deal.walk_away()
                                print(f"\n{result['message']}")
                                ih.press_enter_to_continue()
                                break
                    
                    break  # Back to company selection
                    
    def complete_acquisition(self, company: Company, price: float) -> None:
        """Complete an acquisition transaction with player-chosen financing."""
        # Calculate available resources
        available_cash = self.player.cash
        available_debt = self.player.get_debt_capacity() - self.player.current_debt
        max_affordable = available_cash + available_debt
        
        if price > max_affordable:
            print("\nInsufficient capital to complete acquisition!")
            return
        
        # Let player choose financing structure
        print("\n" + "=" * 70)
        print("FINANCING STRUCTURE")
        print("=" * 70)
        print(f"\nPurchase Price: ${price:,.0f}")
        print(f"\nAvailable Resources:")
        print(f"  Cash Available:        ${available_cash:,.0f}")
        print(f"  Debt Capacity:         ${available_debt:,.0f}")
        print(f"  Total Available:       ${max_affordable:,.0f}")
        print()
        
        # Determine min/max debt needed
        min_debt_needed = max(0, price - available_cash)
        max_debt_allowed = min(available_debt, price)
        
        if min_debt_needed > 0:
            print(f"⚠️  You must use at least ${min_debt_needed:,.0f} in debt (insufficient cash)")
        
        print("\nHow much DEBT would you like to use for this acquisition?")
        print(f"  • Minimum: ${min_debt_needed:,.0f}")
        print(f"  • Maximum: ${max_debt_allowed:,.0f}")
        print(f"  • Recommended: ${min(price * 0.7, max_debt_allowed):,.0f} (70% leverage)")
        
        debt_to_use = ih.prompt_number(
            "\nEnter debt amount",
            min_value=min_debt_needed,
            max_value=max_debt_allowed,
            allow_float=False
        )
        
        if debt_to_use is None:
            print("\nAcquisition cancelled.")
            return
        
        cash_to_use = price - debt_to_use
        
        # Confirm the structure
        print("\n" + "=" * 70)
        print("CONFIRM FINANCING")
        print("=" * 70)
        print(f"\nPurchase Price:  ${price:,.0f}")
        print(f"  Cash:          ${cash_to_use:,.0f} ({cash_to_use/price:.1%})")
        print(f"  Debt:          ${debt_to_use:,.0f} ({debt_to_use/price:.1%})")
        print(f"\nAfter Transaction:")
        print(f"  Remaining Cash:     ${available_cash - cash_to_use:,.0f}")
        print(f"  Total Debt:         ${self.player.current_debt + debt_to_use:,.0f}")
        print(f"  Debt Utilization:   {(self.player.current_debt + debt_to_use) / self.player.get_debt_capacity():.1%}")
        print()
        
        if not ih.prompt_yes_no("Proceed with this financing structure?"):
            print("\nAcquisition cancelled.")
            return
        
        # Execute the transaction
        if debt_to_use > 0:
            if not self.player.take_debt(debt_to_use):
                print("\nFailed to secure debt financing!")
                return
        
        self.player.adjust_cash(-price)
        debt_used = debt_to_use
                
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
        company = menus.portfolio_operations_menu(self.player, self.time_manager.current_quarter)
        
        if company is None:
            return
            
        while True:
            action = menus.company_operations_menu(company, self.player)
            
            if action == 'back':
                break
            elif action == 'cost_cutting':
                self.handle_cost_cutting(company)
                # Mark company as operated
                company.mark_operated(self.time_manager.current_quarter)
                break  # Exit after one operation
            elif action == 'capex':
                self.handle_capex_investment(company)
                company.mark_operated(self.time_manager.current_quarter)
                break
            elif action == 'replace_mgmt':
                self.handle_management_replacement(company)
                company.mark_operated(self.time_manager.current_quarter)
                break
            elif action == 'strategy':
                self.handle_growth_strategy(company)
                company.mark_operated(self.time_manager.current_quarter)
                break
                
    def handle_cost_cutting(self, company: Company) -> None:
        """Handle cost cutting operation with narrative."""
        print("\n" + "=" * 70)
        print(f"COST CUTTING INITIATIVE: {company.name}")
        print("=" * 70)
        print(f"\nSector: {company.sector}")
        print(f"Current EBITDA Margin: {company.ebitda_margin:.1%}")
        print(f"Current Growth Rate: {company.growth_rate:+.1%}")
        print(f"Current Operational Health: {company.operational_health:.0%}")
        print("\nCost Cutting Initiative Impact:")
        print("  • Higher intensity = Better margins BUT worse growth")
        print("  • Aggressive cuts risk employee morale and reputation")
        print("  • Each sector has different cost-cutting approaches")
        
        intensity = ih.prompt_number("Enter intensity (0-100)", min_value=0, max_value=100)
        if intensity is None:
            return
            
        intensity_normalized = intensity / 100
        
        # PREVIEW IMPACT before executing
        print("\n" + "=" * 70)
        print("PROJECTED IMPACT")
        print("=" * 70)
        
        # Estimate the impact
        estimated_margin_improvement = intensity_normalized * 0.10  # Up to 10%
        estimated_growth_penalty = intensity_normalized * 0.08  # Up to 8%
        estimated_health_damage = intensity_normalized * 0.25  # Up to 25%
        
        print(f"\nExpected Results for {intensity}% intensity:")
        print(f"  • EBITDA Margin:  {company.ebitda_margin:.1%} → {company.ebitda_margin + estimated_margin_improvement:.1%} (+{estimated_margin_improvement:.1%})")
        print(f"  • Growth Rate:    {company.growth_rate:+.1%} → {company.growth_rate - estimated_growth_penalty:+.1%} (-{estimated_growth_penalty:.1%})")
        print(f"  • Health:         {company.operational_health:.0%} → {max(0, company.operational_health - estimated_health_damage):.0%} (-{estimated_health_damage:.0%})")
        
        if intensity_normalized > 0.7:
            print(f"\n⚠️  WARNING: High intensity cost-cutting!")
            print(f"  • Significant operational health damage")
            print(f"  • Potential reputation hit")
            print(f"  • Long recovery period")
        
        print("\n" + "=" * 70)
        
        if not ih.prompt_yes_no("Proceed with this cost-cutting initiative?"):
            print("\n❌ Cost-cutting cancelled.")
            ih.press_enter_to_continue()
            return
        
        result = portfolio_ops.apply_cost_cutting(company, intensity_normalized)
        
        # Display narrative
        print("\n" + "=" * 70)
        print("COST-CUTTING ACTION")
        print("=" * 70)
        print(f"\n📋 ACTION TAKEN:")
        print(f"   {result['narrative_action']}")
        print(f"\n⚠️  IMMEDIATE CONSEQUENCE:")
        print(f"   {result['narrative_consequence']}")
        print(f"\n💰 FINANCIAL IMPACT:")
        print(f"   • EBITDA Margin: {result['margin_improvement']:+.1%}")
        print(f"   • Growth Rate: {-result['growth_penalty']:.1%}")
        
        # Show operational health damage
        if result.get('health_damage', 0) > 0:
            print(f"\n🏥 OPERATIONAL HEALTH:")
            print(f"   • Health Decreased: -{result['health_damage']:.1%}")
            print(f"   • Current Health: {company.operational_health:.0%}")
            
            if company.operational_health < 0.5:
                print(f"   ⚠️  CRITICAL: Company health below 50%!")
                print(f"   • Increased volatility and downside risk")
                print(f"   • Reduced growth potential")
                print(f"   • Risk of operational failure")
            elif company.operational_health < 0.7:
                print(f"   ⚠️  WARNING: Company health degraded")
                print(f"   • Higher volatility in performance")
                print(f"   • Reduced growth potential")
        
        if result.get('morale_impact'):
            print(f"\n😞 MORALE IMPACT:")
            print(f"   Additional growth penalty from poor employee morale")
            
        if result.get('reputation_hit', 0) > 0:
            self.player.adjust_reputation(-result['reputation_hit'])
            print(f"\n📉 REPUTATION IMPACT:")
            print(f"   Your reputation decreased by {result['reputation_hit']:.1%}")
            print(f"   (Now at {self.player.reputation:.0%})")
        
        if intensity_normalized > 0.7:
            print(f"\n⚠️  WARNING: Aggressive cost-cutting causes lasting operational damage!")
            print(f"   Health recovers slowly (1% per quarter) - plan accordingly.")
        
        print("=" * 70)
            
        ih.press_enter_to_continue()
        
    def choose_financing(self, amount: float, operation_name: str) -> tuple[bool, float]:
        """
        Let player choose financing for an operation.
        
        Args:
            amount: Total amount needed
            operation_name: Name of operation (for display)
            
        Returns:
            (success, debt_used) tuple
        """
        available_cash = self.player.cash
        available_debt = self.player.get_debt_capacity() - self.player.current_debt
        max_affordable = available_cash + available_debt
        
        if amount > max_affordable:
            print(f"\n⚠️  Insufficient capital for this operation!")
            print(f"Amount needed: ${amount:,.0f}")
            print(f"Available: ${max_affordable:,.0f}")
            return (False, 0)
        
        # If can pay all cash, ask if they want to
        if amount <= available_cash:
            print(f"\nYou have sufficient cash (${available_cash:,.0f}) to pay all ${amount:,.0f}")
            if ih.prompt_yes_no("Use all cash (no debt)?"):
                return (True, 0)
        
        # Show financing dialog
        print("\n" + "=" * 70)
        print(f"FINANCING: {operation_name.upper()}")
        print("=" * 70)
        print(f"\nAmount Required: ${amount:,.0f}")
        print(f"\nAvailable Resources:")
        print(f"  Cash Available:    ${available_cash:,.0f}")
        print(f"  Debt Capacity:     ${available_debt:,.0f}")
        print(f"  Total Available:   ${max_affordable:,.0f}")
        
        min_debt_needed = max(0, amount - available_cash)
        max_debt_allowed = min(available_debt, amount)
        
        if min_debt_needed > 0:
            print(f"\n⚠️  Must use at least ${min_debt_needed:,.0f} in debt")
        
        print(f"\nHow much DEBT to use?")
        print(f"  Range: ${min_debt_needed:,.0f} - ${max_debt_allowed:,.0f}")
        
        debt_to_use = ih.prompt_number(
            "Enter debt amount",
            min_value=min_debt_needed,
            max_value=max_debt_allowed,
            allow_float=False
        )
        
        if debt_to_use is None:
            return (False, 0)
        
        cash_to_use = amount - debt_to_use
        
        # Confirm
        print(f"\nFinancing breakdown:")
        print(f"  Cash: ${cash_to_use:,.0f}")
        print(f"  Debt: ${debt_to_use:,.0f}")
        
        if not ih.prompt_yes_no("Proceed?"):
            return (False, 0)
        
        # Execute financing
        if debt_to_use > 0:
            if not self.player.take_debt(debt_to_use):
                print("\nFailed to secure debt!")
                return (False, 0)
        
        self.player.adjust_cash(-amount)
        return (True, debt_to_use)
    
    def handle_capex_investment(self, company: Company) -> None:
        """Handle capex investment with debt financing option."""
        print("\n" + "=" * 70)
        print(f"CAPITAL INVESTMENT: {company.name}")
        print("=" * 70)
        print(f"\nCompany revenue: ${company.revenue:,.0f}")
        print(f"Current growth rate: {company.growth_rate:+.1%}")
        print(f"Current operational health: {company.operational_health:.0%}")
        
        max_affordable = self.player.cash + (self.player.get_debt_capacity() - self.player.current_debt)
        print(f"\nAvailable capital (cash + debt): ${max_affordable:,.0f}")
        
        amount = ih.prompt_number(
            "Enter investment amount",
            min_value=0,
            max_value=max_affordable,
            allow_float=False
        )
        
        if amount is None or amount == 0:
            return
        
        # PREVIEW IMPACT before financing
        print("\n" + "=" * 70)
        print("PROJECTED IMPACT")
        print("=" * 70)
        
        # Estimate impact
        investment_ratio = amount / company.revenue
        estimated_growth_boost = investment_ratio * 0.05  # ~5% per revenue-dollar invested
        estimated_health_improvement = min(0.15, investment_ratio * 0.10)  # Up to 15%
        
        print(f"\nExpected Results for ${amount:,.0f} investment:")
        print(f"  • Investment/Revenue ratio: {investment_ratio:.1%}")
        print(f"  • Growth Rate:   {company.growth_rate:+.1%} → {company.growth_rate + estimated_growth_boost:+.1%} (+{estimated_growth_boost:.1%})")
        print(f"  • Health:        {company.operational_health:.0%} → {min(1.0, company.operational_health + estimated_health_improvement):.0%} (+{estimated_health_improvement:.0%})")
        print(f"  • Cost:          ${amount:,.0f}")
        
        print("\n" + "=" * 70)
        
        if not ih.prompt_yes_no("Proceed with this capital investment?"):
            print("\n❌ Investment cancelled.")
            ih.press_enter_to_continue()
            return
        
        # Choose financing
        success, debt_used = self.choose_financing(amount, "CapEx Investment")
        
        if not success:
            print("\nInvestment cancelled.")
            ih.press_enter_to_continue()
            return
            
        result = portfolio_ops.apply_capex_investment(company, amount)
        
        print(f"\n{result['message']}")
        if debt_used > 0:
            print(f"Financed with ${debt_used:,.0f} debt")
        ih.press_enter_to_continue()
        
    def handle_management_replacement(self, company: Company) -> None:
        """Handle management replacement with candidate selection and narratives."""
        from simulation import manager_system
        
        print("\n" + "=" * 70)
        print(f"MANAGEMENT REPLACEMENT: {company.name}")
        print("=" * 70)
        print(f"\nCurrent Manager: {company.manager}")
        print(f"Replacement cost: ${config.MANAGER_REPLACEMENT_COST:,.0f}")
        print()
        
        # Generate candidate options
        candidates = manager_system.generate_manager_candidates(company.manager, num_candidates=3)
        
        print("SELECT NEW MANAGER:")
        print("=" * 70)
        
        for i, (archetype, manager, pitch) in enumerate(candidates, 1):
            print(f"\n{i}. {archetype} - {manager.name}")
            print(f"   {pitch}")
            print(f"   Stats: Competence {manager.competence:.0%} | Risk {manager.risk_profile:.0%} | Coop {manager.cooperativeness:.0%}")
        
        print(f"\n{len(candidates) + 1}. Cancel")
        
        choice = ih.prompt_choice(
            list(range(len(candidates) + 2)),
            "Select candidate"
        )
        
        if choice < 0 or choice >= len(candidates):
            print("\nReplacement cancelled.")
            ih.press_enter_to_continue()
            return
        
        selected_archetype, selected_manager, selected_pitch = candidates[choice]
        
        print(f"\n✓ Selected: {selected_archetype} - {selected_manager.name}")
        
        # PREVIEW TRANSITION IMPACT
        from simulation import manager_system
        impact = manager_system.calculate_transition_impact(company.manager, selected_manager)
        
        print("\n" + "=" * 70)
        print("PROJECTED TRANSITION IMPACT")
        print("=" * 70)
        print(f"\nOld Manager: {company.manager.name}")
        print(f"  Competence: {company.manager.competence:.0%} | Risk: {company.manager.risk_profile:.0%} | Coop: {company.manager.cooperativeness:.0%}")
        print(f"\nNew Manager: {selected_manager.name}")
        print(f"  Competence: {selected_manager.competence:.0%} | Risk: {selected_manager.risk_profile:.0%} | Coop: {selected_manager.cooperativeness:.0%}")
        print(f"\nExpected Impact:")
        print(f"  • Transition Penalty:     -{impact['transition_penalty']:.1%} growth (temporary)")
        print(f"  • Long-term Improvement:  +{impact['long_term_improvement']:.1%} growth")
        print(f"  • Volatility Change:       {impact['volatility_change']:+.1%}")
        print(f"  • Health Impact:           {'+' if impact['competence_delta'] > 0 else ''}{impact['competence_delta'] * 0.20:.1%}")
        print(f"  • Cost:                    ${config.MANAGER_REPLACEMENT_COST:,.0f}")
        
        if company.manager.cooperativeness < 0.4:
            print(f"\n⚠️  WARNING: Current manager may resist termination")
            print(f"  • Potential additional costs")
            print(f"  • Possible reputation damage")
        
        print("\n" + "=" * 70)
        
        if not ih.prompt_yes_no(f"Proceed with hiring {selected_manager.name}?"):
            print("\n❌ Management replacement cancelled.")
            ih.press_enter_to_continue()
            return
        
        # Choose financing
        success, debt_used = self.choose_financing(
            config.MANAGER_REPLACEMENT_COST, 
            "Management Replacement"
        )
        
        if not success:
            print("\nReplacement cancelled.")
            ih.press_enter_to_continue()
            return
            
        result = portfolio_ops.replace_management(company, self.player, selected_manager)
        
        if result['success']:
            # Display firing narrative
            print("\n" + "=" * 70)
            print("💼 TERMINATION")
            print("=" * 70)
            print(f"\n{result['firing_narrative']}")
            
            print("\n" + "=" * 70)
            print("🤝 NEW HIRE")
            print("=" * 70)
            print(f"\n{result['hiring_narrative']}")
            
            # Display transition impact
            print("\n" + "=" * 70)
            print("TRANSITION IMPACT")
            print("=" * 70)
            print(f"\n  Growth Penalty:       -{result['transition_penalty']:.1%} (temporary)")
            print(f"  Volatility Change:     {result['volatility_change']:+.1%}")
            print(f"  Health Impact:         {result['health_improvement']:+.1%}")
            print(f"  Cost:                  ${result['cost']:,.0f}")
            
            if result['difficult']:
                print(f"\n⚠️  Difficult termination incurred additional costs and reputation damage.")
            
            if debt_used > 0:
                print(f"\n💳 Financed with ${debt_used:,.0f} debt")
        else:
            print(f"\n{result['message']}")
            
        ih.press_enter_to_continue()
        
    def handle_growth_strategy(self, company: Company) -> None:
        """Handle growth strategy selection with debt financing option."""
        print("\n" + "=" * 70)
        print(f"GROWTH STRATEGY: {company.name}")
        print("=" * 70)
        print(f"\nCurrent revenue: ${company.revenue:,.0f}")
        print(f"Current growth rate: {company.growth_rate:+.1%}")
        print(f"Current operational health: {company.operational_health:.0%}")
        
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
        
        # PREVIEW IMPACT before executing
        print("\n" + "=" * 70)
        print("PROJECTED IMPACT")
        print("=" * 70)
        
        # Show estimated ranges for selected strategy
        if strategy == 'roll_up':
            print(f"\nRoll-up Strategy - Acquire competitors to consolidate market")
            print(f"\nExpected Impact:")
            print(f"  • Cost:              ${company.revenue * 1.5:,.0f} - ${company.revenue * 2.0:,.0f} (150-200% of revenue)")
            print(f"  • Revenue Growth:    +10% to +20%")
            print(f"  • Margin Improvement: +1% to +3%")
            print(f"  • Volatility:        +3% to +8% (integration risk)")
            print(f"  • Growth Drag:       -1% to -3% (temporary integration period)")
            print(f"  • Health Impact:     -10% to +8% (integration success varies)")
            print(f"\n⚠️  HIGH RISK, HIGH COST, HIGH REWARD")
            
        elif strategy == 'expand':
            print(f"\nExpansion Strategy - Enter new markets or geographies")
            print(f"\nExpected Impact:")
            print(f"  • Revenue Growth:    +5% to +15%")
            print(f"  • Volatility:        +2% to +5% (new market risk)")
            print(f"  • Health Impact:     +3% to +8%")
            print(f"\n💰 MODERATE RISK, ORGANIC GROWTH")
            
        elif strategy == 'diversify':
            print(f"\nDiversification Strategy - New products or services")
            print(f"\nExpected Impact:")
            print(f"  • Revenue Growth:    +3% to +10%")
            print(f"  • Volatility:        -1% to -3% (risk reduction)")
            print(f"  • Health Impact:     +2% to +6%")
            print(f"\n🛡️  DEFENSIVE, REDUCES VOLATILITY")
        
        print("\n" + "=" * 70)
        
        if not ih.prompt_yes_no("Proceed with this growth strategy?"):
            print("\n❌ Growth strategy cancelled.")
            ih.press_enter_to_continue()
            return
        
        result = portfolio_ops.pursue_acquisition_strategy(company, strategy)
        
        if result.get('cost'):
            strategy_names = {
                'roll_up': 'Roll-up Strategy',
                'expand': 'Expansion Strategy',
                'diversify': 'Diversification Strategy'
            }
            
            # Choose financing
            success, debt_used = self.choose_financing(
                result['cost'], 
                strategy_names.get(strategy, 'Growth Strategy')
            )
            
            if not success:
                print("\nStrategy cancelled.")
                ih.press_enter_to_continue()
                return
                
        print(f"\n{result['message']}")
        if result.get('cost') and debt_used > 0:
            print(f"Financed with ${debt_used:,.0f} debt")
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
        
        # Calculate taxes if profitable
        tax_owed = self.player.calculate_capital_gains_tax(deal.asking_price, company.acquisition_price)
        
        if tax_owed > 0:
            difficulty_settings = config.DIFFICULTY_SETTINGS.get(self.player.difficulty, config.DIFFICULTY_SETTINGS['medium'])
            tax_rate = difficulty_settings['capital_gains_tax_rate']
            print(f"\n💸 Capital Gains Tax ({tax_rate:.0%}): ${tax_owed:,.0f}")
            proceeds_after_tax = deal.asking_price - tax_owed
            print(f"Net Proceeds (after tax): ${proceeds_after_tax:,.0f}")
        
        if ih.prompt_yes_no("Accept this offer?"):
            # Complete exit
            self.player.adjust_cash(deal.asking_price)
            
            # Pay taxes on gains
            if tax_owed > 0:
                self.player.pay_taxes(tax_owed)
            
            self.player.remove_company(company)
            self.player.record_deal('exit', company.name, deal.asking_price, 
                                  self.time_manager.current_quarter)
            
            print(f"\nInvestment exited successfully!")
            print(f"Gross Proceeds: ${deal.asking_price:,.0f}")
            if tax_owed > 0:
                print(f"Taxes Paid: ${tax_owed:,.0f}")
                print(f"Net Proceeds: ${deal.asking_price - tax_owed:,.0f}")
            else:
                print(f"Net Proceeds: ${deal.asking_price:,.0f} (no tax on loss)")
            
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
        
    def save_game_flow(self) -> bool:
        """Handle save game flow."""
        save_name = menus.save_game_menu()
        
        if not save_name:
            return False
        
        from game.save_system import save_game
        
        if save_game(self, save_name):
            print(f"\nGame saved as '{save_name}'!")
            ih.press_enter_to_continue()
            return True
        else:
            print("\nFailed to save game!")
            ih.press_enter_to_continue()
            return False
    
    def load_game_flow(self) -> bool:
        """Handle load game flow."""
        save_name = menus.load_game_menu()
        
        if not save_name:
            return False
        
        from game.save_system import load_game
        
        if load_game(save_name, self):
            return True
        else:
            print(f"\nFailed to load game '{save_name}'!")
            ih.press_enter_to_continue()
            return False
    
    def save_game(self) -> None:
        """Save the current game state."""
        from game.save_system import GameSaver
        
        print("\n" + "=" * 70)
        print("SAVE GAME")
        print("=" * 70)
        
        save_name = ih.prompt_text("Enter save name (or press Enter for auto-name)", allow_empty=True)
        
        try:
            save_path = GameSaver.save_game(self, save_name)
            print(f"\n✓ Game saved successfully to: {save_path}")
        except Exception as e:
            print(f"\n✗ Error saving game: {e}")
            
        ih.press_enter_to_continue()
    
    def load_game_menu(self) -> None:
        """Show load game menu and restore selected save."""
        from game.save_system import GameSaver
        
        saves = GameSaver.list_saves()
        
        if not saves:
            print("\nNo saved games found.")
            ih.press_enter_to_continue()
            return
        
        print("\n" + "=" * 70)
        print("LOAD GAME")
        print("=" * 70)
        print("\nAvailable Saves:")
        
        for i, save in enumerate(saves, 1):
            print(f"  {i}. {save['name']} (Last modified: {save['modified'].strftime('%Y-%m-%d %H:%M:%S')})")
        
        options = [s['name'] for s in saves] + ["Cancel"]
        choice = ih.prompt_choice(options, "Select a save to load")
        
        if choice < 0 or choice >= len(saves):
            return
        
        try:
            save_name = saves[choice]['name']
            game_state = GameSaver.load_game(save_name)
            GameSaver.restore_game(game_state, self)
            print(f"\n✓ Game loaded successfully from: {save_name}")
            print(f"   Quarter: {self.time_manager.get_time_display()}")
            print(f"   Net Worth: ${self.player.compute_net_worth():,.0f}")
            ih.press_enter_to_continue()
        except Exception as e:
            print(f"\n✗ Error loading game: {e}")
            ih.press_enter_to_continue()

