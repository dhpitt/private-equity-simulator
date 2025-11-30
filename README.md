# Private Equity Simulator

A terminal-based business simulation game where you manage a private equity fund, acquire companies, improve operations, and build portfolio value.

## Overview

You are the managing partner of a private equity fund with limited time and capital to build a successful portfolio. Navigate market cycles, negotiate deals, manage companies, and maximize returns over 5 years (20 quarters).

## Features

- **Dynamic Market Simulation**: Interest rates, sector multiples, and economic conditions that evolve each quarter
- **Procedural Company Generation**: Unique companies with realistic financials across 8 different sectors
- **Deal Negotiation**: Multi-round negotiations with counter-offers and hidden information
- **Portfolio Operations**: 
  - Cost-cutting initiatives
  - Capital investment programs  
  - Management replacement
  - Growth strategies (roll-ups, expansion, diversification)
- **Random Events**: Market crashes, operational crises, breakthroughs, and management disputes
- **DCF Valuation**: Proper discounted cash flow analysis and financial modeling
- **Beautiful Terminal UI**: Rich formatting with tables, panels, and colored output

## Installation

PE Simulator is a pip-installable Python package!

### Prerequisites
- Python 3.8+ (tested on 3.8-3.13)
- pip package manager

### Quick Install

```bash
# Install in editable/development mode (recommended)
pip install -e .

# Or standard install
pip install .
```

### Running the Game

After installation, run from anywhere:
```bash
pe-sim
```

Or using Python:
```bash
python -m main
```

### Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

## How to Play

### Starting the Game

Run the game using:
```bash
uv run python main.py
```

Or if installed:
```bash
pe-sim
```

### Game Flow

1. **Main Menu**: Each quarter, choose from:
   - View your portfolio
   - Check market conditions
   - Acquire new companies
   - Operate on portfolio companies
   - Exit investments
   - Advance to next quarter

2. **Acquisitions**: 
   - Browse available companies
   - Review financials and management
   - Negotiate purchase price
   - Use cash and/or debt to finance

3. **Operations**:
   - Implement cost-cutting (improves margins, may hurt growth)
   - Invest in growth initiatives
   - Replace underperforming management
   - Pursue strategic growth strategies

4. **Exits**:
   - Sell companies when valuations are favorable
   - Lock in returns and recycle capital

5. **Market Events**:
   - Respond to unexpected events
   - Mitigate crises through quick action

### Winning

The game ends after 20 quarters. Your final score is based on:
- **Net Worth**: Cash + Portfolio Value - Debt
- **Return Multiple**: Final Net Worth / Starting Capital
- **Annualized Return**: IRR over the game period


## Project Structure

```
pe_simulator/
├── main.py              # Entry point
├── config.py            # Game configuration
├── game/                # Game logic
│   ├── engine.py        # Main game loop
│   ├── menus.py         # User menus
│   ├── events.py        # Random events
│   ├── time_manager.py  # Time tracking
│   └── input_handlers.py# Input utilities
├── models/              # Data models
│   ├── player.py        # Player state
│   ├── company.py       # Company model
│   ├── manager.py       # Management teams
│   ├── market.py        # Market conditions
│   ├── deal.py          # Deal negotiations
│   └── finance.py       # Financial calculations
├── simulation/          # Simulation logic
│   ├── dcf.py           # DCF valuation
│   ├── stochastic.py    # Random processes
│   ├── procedural_gen.py# Content generation
│   └── portfolio_ops.py # Portfolio operations
├── ui/                  # User interface
│   ├── table_views.py   # Table displays
│   └── screens.py       # Game screens
├── data/                # Game data
│   ├── names.json       # Company names
│   └── sectors.json     # Sector definitions
└── tests/               # Unit tests
```

## Configuration

Edit `config.py` to customize:
- Starting capital and debt capacity
- Game duration
- Company generation parameters
- Market volatility
- Event probabilities
- Random seed (for reproducibility)

## Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

## Tips for Success

1. **Diversify**: Don't put all eggs in one basket
2. **Mind the Market**: Buy in recessions, sell in booms
3. **Leverage Wisely**: Debt amplifies returns but adds risk
4. **Active Management**: Don't just buy and hold - improve operations
5. **Know When to Exit**: Taking profits matters as much as making acquisitions
6. **Watch Cash Flow**: Debt interest adds up each quarter
7. **Management Matters**: Competent managers make a real difference

## License

This is a personal project created for educational and entertainment purposes.

## Credits

Created as a comprehensive business simulation game demonstrating:
- Object-oriented design
- Financial modeling (DCF, IRR, leverage)
- Stochastic processes
- Procedural content generation
- Terminal UI design with Rich library

