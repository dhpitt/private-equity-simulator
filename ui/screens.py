"""
Screens - high-level UI screens for intro, endgame, etc.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from models.player import Player
from models.market import Market
from game.time_manager import TimeManager
from ui.table_views import display_player_summary, display_deal_history
import config

console = Console()


def show_intro() -> None:
    """Show game introduction screen."""
    console.clear()
    
    title = Text("PRIVATE EQUITY SIMULATOR", style="bold cyan", justify="center")
    
    intro_text = f"""
Welcome to the Private Equity Simulator!

You are the managing partner of a new private equity fund with:
  • ${config.STARTING_CAPITAL:,.0f} in capital
  • ${config.STARTING_DEBT_CAPACITY:,.0f} in debt capacity
  • {config.GAME_DURATION_QUARTERS} quarters ({config.GAME_DURATION_QUARTERS // 4} years) to build your portfolio

Your goal is to maximize your fund's value by:
  • Acquiring promising companies
  • Improving their operations
  • Managing through market cycles
  • Exiting at the right time

Good luck!
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
  
REPUTATION:           {player.reputation:>15.1%}
    """
    
    # Determine grade
    if return_multiple >= 3.0:
        grade = "S - Legendary"
        grade_style = "bold bright_green"
    elif return_multiple >= 2.5:
        grade = "A - Excellent"
        grade_style = "bold green"
    elif return_multiple >= 2.0:
        grade = "B - Very Good"
        grade_style = "green"
    elif return_multiple >= 1.5:
        grade = "C - Good"
        grade_style = "yellow"
    elif return_multiple >= 1.0:
        grade = "D - Modest Success"
        grade_style = "yellow"
    else:
        grade = "F - Loss"
        grade_style = "red"
        
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
    
    # Commentary
    if return_multiple >= 3.0:
        comment = "Outstanding performance! You're a PE superstar!"
    elif return_multiple >= 2.0:
        comment = "Excellent work! Your investors are very happy."
    elif return_multiple >= 1.5:
        comment = "Good job! You've delivered solid returns."
    elif return_multiple >= 1.0:
        comment = "Modest returns. Room for improvement."
    else:
        comment = "Tough market. Better luck next time."
        
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

