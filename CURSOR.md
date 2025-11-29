Always use the provided root-level UV environment to run code and install dependencies.

location:
.venv/bin/activate

Command: 
`source .venv/bin/activate`

or `uv run <command>`

Overall desired project structure:

Project Structure
pe_simulator/
    ├── main.py
    ├── config.py
    ├── game/
    │     ├── __init__.py
    │     ├── engine.py
    │     ├── menus.py
    │     ├── events.py
    │     ├── time_manager.py
    │     └── input_handlers.py
    │
    ├── models/
    │     ├── __init__.py
    │     ├── player.py
    │     ├── company.py
    │     ├── manager.py
    │     ├── market.py
    │     ├── deal.py
    │     └── finance.py
    │
    ├── simulation/
    │     ├── __init__.py
    │     ├── dcf.py
    │     ├── stochastic.py
    │     ├── procedural_gen.py
    │     └── portfolio_ops.py
    │
    ├── ui/
    │     ├── __init__.py
    │     ├── table_views.py
    │     └── screens.py
    │
    ├── data/
    │     ├── names.json      (procedural generation materials)
    │     └── sectors.json
    │
    └── tests/
          ├── test_company.py
          ├── test_market.py
          ├── test_dcf.py
          └── test_game_flow.py

Module Responsibilities
main.py

Entry point of the game.

Creates Player, Market, and GameEngine objects.

Starts the main menu loop.

Responsible only for bootstrapping; no logic.

config.py

Contains global default settings:

Starting capital

Number of quarters

Random seed

Default interest rate, growth volatility

Procedural generation knobs (min/max company sizes)

All modules import configuration from here.

game/
engine.py

The central orchestrator of the simulation.

Controls the turn loop:

Update market variables

Update portfolio companies

Trigger random events

Advance the time manager

Call UI menus

Provides entry points such as:

run_quarter()

handle_acquisition()

operate_portfolio()

exit_investments()

Interacts with:

models.* for state

simulation.* for calculations

ui.* for rendering

menus.py

Houses all user-facing menus:

Main menu

Acquisition menu

Portfolio overview menu

Event decision screens

Each menu:

Prints UI via ui.table_views or simple text

Requests user input via input_handlers

Returns selected actions to the engine

events.py

Handles game events such as:

Market crashes

Manager disputes

Operational crises

Lawsuits, supply shocks, talent departures

Exposes:

generate_event(player, portfolio, market) → Event

apply_event(event)

Event resolution modifies company or market state.

time_manager.py

Central clock for the game.

Maintains:

Current quarter

Fiscal years

Notifies engine when the game ending condition has been met.

input_handlers.py

Standardized user input methods (numeric, multiple choice).

Ensures robust input parsing.

Functions like:

prompt_choice(options_list)

prompt_number(min, max)

prompt_yes_no()

Used by menus.py.

models/
player.py

Defines the Player object:

Cash, debt capacity

Portfolio (list of Company)

Reputation

Deal history

Implements:

Adjust cash

Add/remove company

Compute net worth

company.py

Core Company simulation object:

Name, sector, initial revenue and EBITDA

Growth rate, volatility

Management team

Current valuation

Methods:

simulate_quarter(market_conditions)

value(dcf_parameters)

apply_event(event)

Heavily uses simulation.dcf and stochastic.

manager.py

Procedurally generated NPCs with attributes:

Risk profile

Competence

Cooperativeness

Behavioral model affecting:

Performance variance

Negotiation difficulty

Operational stability

market.py

Global market model:

Interest rates

Sector valuation multiples

Credit conditions

Updated each quarter via stochastic model.

Affects DCF discount rates and leverage.

deal.py

Represents acquisition or exit negotiations.

Contains:

Asking price

Offer price

Counter-offer logic

Hidden quality parameters

Interacts with:

Company

Player cash/debt

Market for valuation reference

finance.py

Finance helpers:

Leverage modeling

Debt service calculations

Interest rate adjustments

IRR computations on exits

simulation/
dcf.py

Discounted cash flow functions:

project_free_cash_flows(company)

discount_cash_flows(fcf_list, discount_rate)

enterprise_value(...)

Used by Company.value() and Market.

stochastic.py

Stochastic processes used everywhere:

Revenue random walk

Growth drift

Market volatility

Manager behavioral noise

Centralized randomness (seeded in config.py).

procedural_gen.py

Procedural content generators:

Random company profiles

Management teams

Sectors

Name generators

Loads data from /data.

portfolio_ops.py

Operations performed after an acquisition:

Cost-cutting effects

Capex decisions

Manager replacement

Expansion or roll-up strategies

Returns numeric impact to Company state.

ui/
table_views.py

Terminal UI using rich for:

Portfolio overview table

Company detail view

Market conditions dashboard

Purely formatting; no business logic.

screens.py

High-level UI screens:

Intro screen

Endgame summary

Deal negotiation screen

Composes table_views and plain text.

tests/
Unit Tests

test_company.py: revenue updates, valuation logic

test_market.py: interest-rate drift, sector multiples

test_dcf.py: cash flow and discounting correctness

test_game_flow.py: advancing quarters, buying/selling flow

Ensure each module is independently testable.

Interactions Between Modules

engine.py orchestrates everything.

menus.py gathers user intent, returning standardized action objects.

models.company.Company delegates heavy math to simulation.*.

ui. modules* only render; they do not compute.

input_handlers.py always handles parsing and validation.

procedural_gen.py is used when the engine spawns new companies.

time_manager.py signals game progression and end state.

deal.py handles negotiation; results modify Player and Company.

events.py injects randomness affecting Company, Player, or Market.
