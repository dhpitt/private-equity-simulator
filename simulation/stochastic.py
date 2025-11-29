"""
Stochastic processes for modeling randomness and volatility.
"""

import random
from typing import List
import config


def random_walk(
    initial_value: float,
    drift: float,
    volatility: float,
    steps: int
) -> List[float]:
    """
    Generate a random walk time series.
    
    Args:
        initial_value: Starting value
        drift: Mean change per step
        volatility: Standard deviation of changes
        steps: Number of steps to generate
        
    Returns:
        List of values following random walk
    """
    values = [initial_value]
    current = initial_value
    
    for _ in range(steps):
        change = random.gauss(drift, volatility)
        current += change
        values.append(current)
        
    return values


def geometric_brownian_motion(
    initial_value: float,
    drift: float,
    volatility: float,
    steps: int,
    dt: float = 1.0
) -> List[float]:
    """
    Generate a geometric Brownian motion time series.
    Commonly used for modeling stock prices and revenue growth.
    
    Args:
        initial_value: Starting value
        drift: Expected return per period
        volatility: Volatility (standard deviation)
        steps: Number of steps
        dt: Time increment (default 1.0)
        
    Returns:
        List of values following GBM
    """
    values = [initial_value]
    current = initial_value
    
    for _ in range(steps):
        # GBM formula: S(t+dt) = S(t) * exp((drift - 0.5*vol^2)*dt + vol*sqrt(dt)*Z)
        # where Z ~ N(0,1)
        z = random.gauss(0, 1)
        exponent = (drift - 0.5 * volatility**2) * dt + volatility * (dt**0.5) * z
        current *= (1 + exponent)  # Simplified multiplicative form
        current = max(0, current)  # Can't go negative
        values.append(current)
        
    return values


def mean_reverting_process(
    initial_value: float,
    long_term_mean: float,
    reversion_speed: float,
    volatility: float,
    steps: int,
    dt: float = 1.0
) -> List[float]:
    """
    Generate a mean-reverting (Ornstein-Uhlenbeck) process.
    Useful for modeling interest rates and cyclical variables.
    
    Args:
        initial_value: Starting value
        long_term_mean: Long-run equilibrium value
        reversion_speed: Speed of reversion to mean (higher = faster)
        volatility: Random volatility
        steps: Number of steps
        dt: Time increment
        
    Returns:
        List of values following mean-reverting process
    """
    values = [initial_value]
    current = initial_value
    
    for _ in range(steps):
        # OU process: dx = reversion_speed * (mean - x) * dt + volatility * dW
        z = random.gauss(0, 1)
        drift_term = reversion_speed * (long_term_mean - current) * dt
        diffusion_term = volatility * (dt**0.5) * z
        
        current += drift_term + diffusion_term
        values.append(current)
        
    return values


def add_noise(value: float, volatility: float) -> float:
    """
    Add random noise to a value.
    
    Args:
        value: Base value
        volatility: Standard deviation of noise
        
    Returns:
        Value with noise added
    """
    noise = random.gauss(0, volatility)
    return value * (1 + noise)


def simulate_growth_shock(base_growth: float, shock_probability: float = 0.1) -> float:
    """
    Simulate occasional growth shocks (positive or negative).
    
    Args:
        base_growth: Normal growth rate
        shock_probability: Probability of a shock occurring
        
    Returns:
        Growth rate (possibly with shock)
    """
    if random.random() < shock_probability:
        # Shock occurs - can be ±20% impact
        shock = random.uniform(-0.20, 0.20)
        return base_growth + shock
    return base_growth


def simulate_market_cycle(
    quarters: int,
    base_growth: float = 0.02,
    cycle_length: int = 16  # 4 years
) -> List[float]:
    """
    Simulate a cyclical market with boom and bust periods.
    
    Args:
        quarters: Number of quarters to simulate
        base_growth: Base growth rate
        cycle_length: Length of full cycle in quarters
        
    Returns:
        List of quarterly growth rates
    """
    import math
    
    growth_rates = []
    for q in range(quarters):
        # Sinusoidal cycle + random noise
        cycle_position = (2 * math.pi * q) / cycle_length
        cyclical_component = 0.03 * math.sin(cycle_position)  # ±3% cyclical swing
        
        noise = random.gauss(0, 0.02)
        
        growth = base_growth + cyclical_component + noise
        growth_rates.append(growth)
        
    return growth_rates


def correlated_random_walk(
    initial_values: List[float],
    correlation: float,
    drift: float,
    volatility: float,
    steps: int
) -> List[List[float]]:
    """
    Generate multiple correlated random walks.
    Useful for modeling related companies or sectors.
    
    Args:
        initial_values: Starting values for each series
        correlation: Correlation coefficient (-1 to 1)
        drift: Mean drift per step
        volatility: Volatility
        steps: Number of steps
        
    Returns:
        List of time series (one per initial value)
    """
    n_series = len(initial_values)
    series = [[iv] for iv in initial_values]
    
    for _ in range(steps):
        # Common shock (drives correlation)
        common_shock = random.gauss(0, 1)
        
        for i in range(n_series):
            # Idiosyncratic shock
            idio_shock = random.gauss(0, 1)
            
            # Combine shocks with correlation
            combined_shock = (correlation * common_shock + 
                            (1 - correlation) * idio_shock)
            
            change = drift + volatility * combined_shock
            new_value = series[i][-1] + change
            series[i].append(new_value)
            
    return series

