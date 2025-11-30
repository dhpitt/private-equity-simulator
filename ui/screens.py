"""
Screens - high-level UI screens for intro, endgame, etc.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import time
import random
import json
from pathlib import Path
from models.player import Player
from models.market import Market
from game.time_manager import TimeManager
from ui.table_views import display_player_summary, display_deal_history
import config

console = Console()


def get_funny_fund_name_message() -> str:
    """Get a random funny message for fund name selection."""
    messages = [
        "Choose wisely, this is going on all the Patagonias and embroidery ain't cheap.",
        "This name better be good - we're printing 100,000 business cards.",
        "Your LPs are gonna see this on every quarterly report. No pressure.",
        "This will be on your yacht. Make it yacht-worthy.",
        "Fun fact: 'Synergy Capital' is already taken. Try harder.",
        "The SEC is watching. Choose accordingly.",
        "How good would this look on a plaque in Epstein's temple?",
        "Would this look good on your LinkedIn page?",
        "WWJD? (What would Jeffrey do?)",
    ]
    return random.choice(messages)


def select_difficulty() -> str:
    """Let player select difficulty level."""
    console.clear()
    
    title = Text("SELECT DIFFICULTY", style="bold cyan", justify="center")
    console.print(title)
    console.print()
    
    difficulty_text = """
[bold green]1. Obama Era[/bold green] (Easy)
   • Fish in a barrel. Money is free!
   • Stable markets (low volatility)
   • [green]3% interest rate[/green] - easy credit!
   • Rare crises
   • Start with 30% reputation
   • [cyan]15% capital gains tax[/cyan]
   • Good for learning the game
   
[bold yellow]2. Reagan Era[/bold yellow] (Medium)
   • Balanced market dynamics
   • [yellow]5% interest rate[/yellow] - standard
   • Realistic challenges
   • Standard reputation (20%)
   • [yellow]20% capital gains tax[/yellow]
   • Recommended for most players
   
[bold red]3. Newsom Era[/bold red] (Hard)
   • In the People's Republic of California, money is scarce.
   • Volatile, unpredictable markets
   • [red]8% interest rate[/red] - tight credit!
   • Frequent crises
   • Start with only 15% reputation
   • [red]30% capital gains tax![/red]
   • For masochists and legends only
"""
    
    panel = Panel(
        difficulty_text.strip(),
        title="Choose Your Difficulty",
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'medium'
        elif choice == '3':
            return 'hard'
        else:
            console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")


def select_fund_name() -> str:
    """Let player name their fund with a funny message."""
    console.clear()
    
    title = Text("NAME YOUR FUND", style="bold cyan", justify="center")
    console.print(title)
    console.print()
    
    funny_message = get_funny_fund_name_message()
    console.print(Panel(funny_message, style="italic yellow", border_style="yellow"))
    console.print()
    
    while True:
        fund_name = input("Enter your fund name: ").strip()
        if fund_name:
            # Show confirmation
            console.print()
            console.print(f"[bold cyan]{fund_name}[/bold cyan]")
            console.print()
            confirm = input("Is this correct? (y/n): ").strip().lower()
            if confirm == 'y':
                return fund_name
            else:
                console.print("\nLet's try again...\n")
        else:
            console.print("[red]Fund name cannot be empty. Try again.[/red]")


def load_quotes():
    """Load inspirational quotes from JSON file."""
    quotes_path = Path(__file__).parent.parent / 'data' / 'quotes.json'
    try:
        with open(quotes_path, 'r') as f:
            data = json.load(f)
            return data.get('inspirational_quotes', [])
    except FileNotFoundError:
        # Fallback quotes if file not found
        return [
            "All my losses was lessons.",
            "It's lonely at the top.",
            "Hustle harder."
        ]


def show_quote_screen():
    """Display a random inspirational quote during quarter transitions."""
    quotes = load_quotes()
    quote = random.choice(quotes)
    
    console.clear()
    
    # Create styled quote
    quote_text = Text(quote, style="bold cyan", justify="center")
    
    # Display in a panel
    panel = Panel(
        Align.center(quote_text, vertical="middle"),
        title="[bold yellow]💎 Words of Wisdom 💎[/bold yellow]",
        border_style="bright_yellow",
        padding=(2, 4)
    )
    
    console.print("\n" * 5)
    console.print(panel)
    console.print("\n" * 5)
    
    # Pause for effect
    time.sleep(2.5)


def show_intro(player: Player, market: Market) -> None:
    """Show game introduction screen."""
    console.clear()
    
    title = Text("PRIVATE EQUITY SIMULATOR", style="bold cyan", justify="center")
    
    # Get difficulty info
    difficulty_name = config.DIFFICULTY_SETTINGS[player.difficulty]['name']
    difficulty_desc = config.DIFFICULTY_SETTINGS[player.difficulty]['description']
    
    # Calculate starting debt capacity for intro
    starting_capacity = player.get_debt_capacity()
    
    intro_text = f"""
Welcome to the Private Equity Simulator!

[bold cyan]{player.fund_name}[/bold cyan]
Difficulty: [bold]{difficulty_name}[/bold] - {difficulty_desc}

You are the managing partner of this fund with:
  • ${config.STARTING_CAPITAL:,.0f} in starting capital
  • ${starting_capacity:,.0f} initial debt capacity
  • {player.reputation:.0%} starting reputation (build this through profits!)
  • {config.GAME_DURATION_QUARTERS} quarters ({config.GAME_DURATION_QUARTERS // 4} years) to build your portfolio

Your goal is to maximize your fund's value by:
  • Acquiring promising companies (debt financing required!)
  • Improving their operations
  • Generating profits to build reputation and net worth
  • Managing through market cycles
  • Exiting at the right time

Key Mechanics:
  • Start with LOW reputation - prove yourself through profits
  • Debt capacity grows with net worth and reputation
  • One operation per company per quarter (choose wisely!)
  • Success breeds more opportunity!

Good luck, and may the markets be ever in your favor!
"""
    
    panel = Panel(
        intro_text.strip(),
        title="Welcome",
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(title)
    console.print()
    console.print(panel)
    console.print()
    input("Press Enter to begin...")


def show_endgame_summary(player: Player, time_manager: TimeManager) -> None:
    """Show endgame summary and final score."""
    console.clear()
    
    title = Text("GAME OVER", style="bold cyan", justify="center")
    console.print(title)
    console.print()
    
    # Calculate final metrics
    final_net_worth = player.compute_net_worth()
    starting_capital = config.STARTING_CAPITAL
    total_return = final_net_worth - starting_capital
    return_multiple = final_net_worth / starting_capital
    
    # Annualized return
    years = time_manager.current_quarter / 4
    if years > 0:
        annualized_return = ((final_net_worth / starting_capital) ** (1 / years)) - 1
    else:
        annualized_return = 0
        
    # Results panel
    difficulty_settings = config.DIFFICULTY_SETTINGS.get(player.difficulty, config.DIFFICULTY_SETTINGS['medium'])
    tax_rate = difficulty_settings['capital_gains_tax_rate']
    
    results_text = f"""
Final Results after {time_manager.current_quarter} quarters ({years:.1f} years):

FINANCIAL PERFORMANCE:
  Starting Capital:     ${starting_capital:>15,.0f}
  Final Net Worth:      ${final_net_worth:>15,.0f}
  Total Return:         ${total_return:>15,.0f}
  
  Return Multiple:      {return_multiple:>15.2f}x
  Annualized Return:    {annualized_return:>15.1%}

PORTFOLIO:
  Companies Owned:      {len(player.portfolio):>15}
  Portfolio Value:      ${player.compute_portfolio_value():>15,.0f}
  Total Deals:          {len(player.deal_history):>15}
  
TAXES:
  Capital Gains Tax Rate: {tax_rate:>13.0%}
  Total Taxes Paid:     ${player.total_taxes_paid:>15,.0f}
  
REPUTATION:           {player.reputation:>15.1%}
    """
    
    # Determine grade based on ABSOLUTE NET WORTH (not multiples)
    # The grade tiers now match the commentary gates below
    if final_net_worth >= 100_000_000_000:  # $100B+
        grade = "S+ - ULTIMATE PE LEGEND"
        grade_style = "bold bright_magenta"
    elif final_net_worth >= 10_000_000_000:  # $10B+
        grade = "S - LEGENDARY PE TITAN"
        grade_style = "bold bright_magenta"
    elif final_net_worth >= 1_000_000_000:  # $1B+
        grade = "A - PE SUPERSTAR"
        grade_style = "bold bright_green"
    elif final_net_worth >= 100_000_000:  # $100M+
        grade = "B - Excellent Performance"
        grade_style = "bold green"
    elif final_net_worth >= 10_000_000:  # $10M+
        grade = "C - Solid Performance"
        grade_style = "yellow"
    elif final_net_worth >= 1_000_000:  # $1M+
        grade = "D - Mediocre Performance"
        grade_style = "red"
    else:  # < $1M (less than starting capital)
        grade = "F - LOSS"
        grade_style = "bold red"
        
    console.print(Panel(results_text.strip(), title="Final Score", border_style="cyan"))
    console.print()
    console.print(Panel(f"Grade: {grade}", style=grade_style, border_style=grade_style))
    console.print()
    
    # Show final player summary
    display_player_summary(player)
    console.print()
    
    # Show deal history
    display_deal_history(player)
    console.print()
    
    # Commentary based on absolute wealth achieved
    if final_net_worth >= 100_000_000_000:  # $100B+
        comment = "Legendary. Leon Black core. Epstein's calling you back."
    elif final_net_worth >= 10_000_000_000:  # $10B+
        comment = "Nicely done. You're in the billionaire's club."
    elif final_net_worth >= 1_000_000_000:  # $1B+
        comment = "Decent work. Technically a billionaire, but they all make fun of you at Davos."
    elif final_net_worth >= 100_000_000:  # $100M+
        comment = "Solid work. You're making real money. Keep scaling."
    elif final_net_worth >= 10_000_000:  # $10M+
        comment = "You barely beat the market. ."
    else:
        comment = "You lost to SPY. Time to find a new career."
        
    console.print(Panel(comment, style="italic", border_style="dim"))
    console.print()
    
    input("Press Enter to exit...")


def show_deal_screen(company: 'Company', deal_type: str = 'acquisition') -> None:
    """Show deal negotiation screen."""
    from ui.table_views import display_company_detail
    
    console.clear()
    
    title_text = f"{deal_type.upper()}: {company.name}"
    console.print(Panel(title_text, style="bold cyan"))
    console.print()
    
    display_company_detail(company)


def show_event_screen(event_title: str, event_description: str, effects: dict = None) -> None:
    """Show event notification screen."""
    console.clear()
    
    event_text = Text(event_title, style="bold yellow", justify="center")
    console.print()
    console.print(Panel(event_text, border_style="yellow"))
    console.print()
    
    console.print(event_description)
    console.print()
    
    if effects:
        console.print("[bold]Effects:[/bold]")
        for effect, value in effects.items():
            if isinstance(value, float):
                console.print(f"  • {effect}: [bold]{value:+.1%}[/bold]")
            else:
                console.print(f"  • {effect}: [bold]{value}[/bold]")
        console.print()


def show_quarter_summary(quarter: str, player: Player, market: Market) -> None:
    """Show quarterly summary screen."""
    console.clear()
    
    title = Text(f"QUARTER SUMMARY - {quarter}", style="bold cyan", justify="center")
    console.print(title)
    console.print()
    
    display_player_summary(player)
    console.print()
    
    from ui.table_views import display_market_conditions
    display_market_conditions(market)

