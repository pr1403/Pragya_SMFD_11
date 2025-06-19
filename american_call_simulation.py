import numpy as np
from datetime import datetime, time
import pandas as pd

def simulate_stock_price(S0, mu, sigma, dt, n_steps):
    """
    Simulate stock price using Geometric Brownian Motion
    
    Parameters:
    S0: Initial stock price
    mu: Expected return (drift)
    sigma: Volatility
    dt: Time step
    n_steps: Number of time steps
    
    Returns:
    Array of simulated stock prices
    """
    # Generate random walk
    Z = np.random.normal(0, 1, n_steps)
    # Calculate drift and diffusion terms
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    # Calculate price path
    price_path = S0 * np.exp(np.cumsum(drift + diffusion))
    return price_path

def run_simulation(n_simulations=10000):
    # Parameters
    S0 = 125  # Initial stock price (equal to strike price)
    K = 125   # Strike price
    mu = 0.05  # Expected annual return (5%)
    sigma = 0.2  # Annual volatility (20%)
    
    # Time parameters
    market_open = time(9, 15)  # Market opens at 9:15 AM
    target_time = time(13, 0)  # Target time is 1:00 PM
    trading_minutes = (datetime.combine(datetime.today(), target_time) - 
                      datetime.combine(datetime.today(), market_open)).seconds // 60
    
    # Simulation parameters
    dt = 1/252/390  # Time step (1 minute in trading days)
    n_steps = trading_minutes
    
    # Track successful exercises
    successful_exercises = 0
    
    for _ in range(n_simulations):
        # Simulate price path
        price_path = simulate_stock_price(S0, mu, sigma, dt, n_steps)
        
        # Check if price reaches 130 at any point
        if np.max(price_path) >= 130:
            successful_exercises += 1
    
    probability = successful_exercises / n_simulations
    return probability

if __name__ == "__main__":
    # Run simulation
    prob = run_simulation()
    print(f"Probability of earning Rs. 5 before 1:00 PM: {prob:.2%}")
    print(f"This means there is a {prob:.2%} chance that the stock price will reach Rs. 130")
    print(f"before 1:00 PM, allowing you to exercise the option and earn Rs. 5 (130 - 125)") 