"""
Table views - formatted displays using rich library.
"""

from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from models.company import Company
from models.market import Market
from config import DIFFICULTY_SETTINGS
from models.player import Player

console = Console()


def display_company_list(companies: List[Company]) -> None:
    """Display a list of companies in a table."""
    table = Table(title="Companies")
    
    table.add_column("Name", style="cyan")
    table.add_column("Sector", style="magenta")
    table.add_column("Revenue", justify="right", style="green")
    table.add_column("EBITDA", justify="right", style="green")
    table.add_column("Margin", justify="right", style="yellow")
    table.add_column("Growth", justify="right", style="blue")
    table.add_column("Valuation", justify="right", style="bold green")
    
    for company in companies:
        table.add_row(
            company.name,
            company.sector,
            f"${company.revenue:,.0f}",
            f"${company.ebitda:,.0f}",
            f"{company.ebitda_margin:.1%}",
            f"{company.growth_rate:+.1%}",
            f"${company.current_valuation:,.0f}"
        )
        
    console.print(table)


def display_portfolio(companies: List[Company]) -> None:
    """Display portfolio companies with P&L tracking."""
    table = Table(title="Portfolio Companies")
    
    table.add_column("#", style="dim")
    table.add_column("Name", style="cyan")
    table.add_column("Sector", style="magenta")
    table.add_column("Purchase", justify="right", style="blue")
    table.add_column("Current Val", justify="right", style="yellow")
    table.add_column("P&L", justify="right")
    table.add_column("Return", justify="right")
    table.add_column("Health", justify="right")
    
    total_invested = 0
    total_current_value = 0
    
    for i, company in enumerate(companies, 1):
        # Calculate returns
        purchase_price = company.acquisition_price if company.acquisition_price else company.current_valuation
        current_value = company.current_valuation
        pnl = current_value - purchase_price
        return_pct = (pnl / purchase_price) if purchase_price > 0 else 0
        
        # Track totals
        total_invested += purchase_price
        total_current_value += current_value
        
        # Color code P&L and returns
        if pnl > 0:
            pnl_str = f"[green]+${abs(pnl):,.0f}[/green]"
            return_str = f"[green]{return_pct:+.1%}[/green]"
        elif pnl < 0:
            pnl_str = f"[red]-${abs(pnl):,.0f}[/red]"
            return_str = f"[red]{return_pct:.1%}[/red]"
        else:
            pnl_str = "$0"
            return_str = "0.0%"
        
        # Color code operational health
        health = company.operational_health
        if health >= 0.8:
            health_str = f"[green]{health:.0%}[/green]"
        elif health >= 0.6:
            health_str = f"[yellow]{health:.0%}[/yellow]"
        elif health >= 0.4:
            health_str = f"[orange]{health:.0%}[/orange]"
        else:
            health_str = f"[red]{health:.0%} ⚠️[/red]"
        
        table.add_row(
            str(i),
            company.name,
            company.sector,
            f"${purchase_price:,.0f}",
            f"${current_value:,.0f}",
            pnl_str,
            return_str,
            health_str
        )
        
    console.print(table)
    
    # Display portfolio summary
    if companies:
        portfolio_pnl = total_current_value - total_invested
        portfolio_return = (portfolio_pnl / total_invested) if total_invested > 0 else 0
        
        pnl_color = "green" if portfolio_pnl >= 0 else "red"
        
        print("\n" + "=" * 70)
        print("PORTFOLIO SUMMARY")
        print("=" * 70)
        print(f"Total Invested:      ${total_invested:>15,.0f}")
        print(f"Current Value:       ${total_current_value:>15,.0f}")
        
        from rich.console import Console as RichConsole
        rc = RichConsole()
        
        pnl_sign = "+" if portfolio_pnl >= 0 else ""
        return_sign = "+" if portfolio_return >= 0 else ""
        
        rc.print(f"Total P&L:           [{pnl_color}]{pnl_sign}${portfolio_pnl:>14,.0f}[/{pnl_color}]")
        rc.print(f"Portfolio Return:    [{pnl_color}]{return_sign}{portfolio_return:>14.1%}[/{pnl_color}]")
        print("=" * 70)


def display_company_detail(company: Company) -> None:
    """Display detailed information about a company."""
    # Financial metrics
    financial_table = Table(title=f"{company.name} - Financial Metrics", show_header=False)
    financial_table.add_column("Metric", style="cyan")
    financial_table.add_column("Value", style="bold")
    
    financial_table.add_row("Sector", company.sector)
    financial_table.add_row("Revenue", f"${company.revenue:,.0f}")
    financial_table.add_row("EBITDA", f"${company.ebitda:,.0f}")
    financial_table.add_row("EBITDA Margin", f"{company.ebitda_margin:.1%}")
    
    # Show company-specific multiple if available
    if company.valuation_multiple:
        financial_table.add_row("Valuation Multiple", f"{company.valuation_multiple:.1f}x")
    
    financial_table.add_row("Growth Rate", f"{company.growth_rate:+.1%} quarterly")
    financial_table.add_row("Quarterly Growth", f"{company.get_quarterly_growth():+.1%}")
    financial_table.add_row("Current Valuation", f"${company.current_valuation:,.0f}")
    
    if company.acquisition_price:
        financial_table.add_row("Acquisition Price", f"${company.acquisition_price:,.0f}")
        value_change = company.current_valuation - company.acquisition_price
        value_change_pct = value_change / company.acquisition_price
        financial_table.add_row("Value Change", f"${value_change:+,.0f} ({value_change_pct:+.1%})")
        
    console.print(financial_table)
    
    # Management info
    mgmt_table = Table(title="Management Team", show_header=False)
    mgmt_table.add_column("Attribute", style="cyan")
    mgmt_table.add_column("Value", style="bold")
    
    mgmt_table.add_row("Manager", company.manager.name)
    mgmt_table.add_row("Competence", f"{company.manager.competence:.1%}")
    mgmt_table.add_row("Risk Profile", f"{company.manager.risk_profile:.1%}")
    mgmt_table.add_row("Cooperativeness", f"{company.manager.cooperativeness:.1%}")
    
    console.print(mgmt_table)


def display_market_conditions(market: Market) -> None:
    """Display market conditions dashboard."""
    conditions_table = Table(title="Market Conditions")
    
    conditions_table.add_column("Metric", style="cyan")
    conditions_table.add_column("Value", style="bold")
    
    # Highlight multiple trend with color coding
    multiple_trend_pct = (market.multiple_trend - 1.0) * 100
    if market.multiple_trend > 1.05:
        trend_str = f"[bold green]{market.multiple_trend:.3f} ({multiple_trend_pct:+.1f}%) 📈 BULL[/bold green]"
    elif market.multiple_trend < 0.95:
        trend_str = f"[bold red]{market.multiple_trend:.3f} ({multiple_trend_pct:+.1f}%) 📉 BEAR[/bold red]"
    else:
        trend_str = f"[yellow]{market.multiple_trend:.3f} ({multiple_trend_pct:+.1f}%) → NEUTRAL[/yellow]"
    
    conditions_table.add_row("Valuation Multiple Trend", trend_str)
    conditions_table.add_row("Interest Rate", f"{market.interest_rate:.2%}")
    conditions_table.add_row("Market Growth Rate", f"{market.growth_rate:+.2%} quarterly")
    conditions_table.add_row("Credit Conditions", f"{market.credit_conditions:.1%}")
    conditions_table.add_row("Discount Rate (DCF)", f"{market.get_discount_rate():.2%}")
    conditions_table.add_row("Debt Rate", f"{market.get_debt_rate():.2%}")
    
    console.print(conditions_table)
    
    # Sector multiples
    multiples_table = Table(title="Sector EBITDA Multiples")
    
    multiples_table.add_column("Sector", style="cyan")
    multiples_table.add_column("Multiple", justify="right", style="bold")
    
    for sector, multiple in sorted(market.sector_multiples.items()):
        multiples_table.add_row(sector, f"{multiple:.1f}x")
        
    console.print(multiples_table)
    
    # Market status
    if market.is_recession():
        console.print(Panel("[bold red]⚠ Market is in RECESSION[/bold red]"))
    elif market.is_boom():
        console.print(Panel("[bold green]📈 Market is BOOMING[/bold green]"))
    else:
        console.print(Panel("[bold yellow]📊 Market conditions are STABLE[/bold yellow]"))


def display_player_summary(player: Player) -> None:
    """Display player financial summary."""
    # Get difficulty name
    difficulty_name = DIFFICULTY_SETTINGS.get(player.difficulty, DIFFICULTY_SETTINGS['medium'])['name']
    
    title = f"[bold cyan]{player.fund_name}[/bold cyan] | {difficulty_name} Mode"
    summary_table = Table(title=title)
    
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="bold green")
    
    debt_capacity = player.get_debt_capacity()
    debt_utilization = player.get_debt_utilization()
    
    summary_table.add_row("Cash", f"${player.cash:,.0f}")
    summary_table.add_row("Debt", f"${player.current_debt:,.0f}")
    summary_table.add_row("Debt Capacity", f"${debt_capacity:,.0f}")
    summary_table.add_row("Debt Utilization", f"{debt_utilization:.1%}")
    summary_table.add_row("Available Capital", f"${player.available_capital():,.0f}")
    summary_table.add_row("Portfolio Value", f"${player.compute_portfolio_value():,.0f}")
    summary_table.add_row("Net Worth", f"${player.compute_net_worth():,.0f}")
    summary_table.add_row("Portfolio Companies", str(len(player.portfolio)))
    summary_table.add_row("Reputation", f"{player.reputation:.1%}")
    
    console.print(summary_table)


def display_deal_history(player: Player) -> None:
    """Display player's deal history."""
    if not player.deal_history:
        console.print("[dim]No deals completed yet.[/dim]")
        return
        
    history_table = Table(title="Deal History")
    
    history_table.add_column("Quarter", style="cyan")
    history_table.add_column("Type", style="magenta")
    history_table.add_column("Company", style="yellow")
    history_table.add_column("Price", justify="right", style="green")
    
    for deal in player.deal_history:
        history_table.add_row(
            f"Q{deal['quarter']}",
            deal['type'].title(),
            deal['company'],
            f"${deal['price']:,.0f}"
        )
        
    console.print(history_table)

