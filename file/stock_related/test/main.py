import time
import numpy as np
import pandas as pd

# ==========================================
# APPROACH 1: Bulk Calculation (From Scratch)
# ==========================================
def approach_1_bulk(data_100):
    """
    Takes 100 data points, creates a DataFrame, 
    calculates all indicators, and returns the latest row.
    """
    df = pd.DataFrame({'value': data_100})
    
    # Calculate indicators using pandas built-ins
    df['ema11'] = df['value'].ewm(span=11, adjust=False).mean()
    df['ema25'] = df['value'].ewm(span=25, adjust=False).mean()
    df['sma20'] = df['value'].rolling(window=20).mean()
    
    return df.iloc[-1].to_dict()

# ==========================================
# APPROACH 2: Optimized / Iterative Update
# ==========================================
def approach_2_optimized(data_20, prev_ema11, prev_ema25):
    """
    Takes only 20 data points and the previous step's EMAs.
    Calculates SMA20 via numpy and steps the EMAs forward by 1 tick.
    """
    # SMA20 only requires the last 20 data points
    sma20 = np.mean(data_20)
    
    # Extract the newest data point (the 20th item)
    new_val = data_20[-1]
    
    # Standard EMA formula multipliers: 2 / (span + 1)
    mult_11 = 2 / (11 + 1)
    mult_25 = 2 / (25 + 1)
    
    # Step the EMAs forward mathematically
    ema11 = (new_val * mult_11) + (prev_ema11 * (1 - mult_11))
    ema25 = (new_val * mult_25) + (prev_ema25 * (1 - mult_25))
    
    return {'value': new_val, 'ema11': ema11, 'ema25': ema25, 'sma20': sma20}


# ==========================================
# BENCHMARK AND VALIDATION SETUP
# ==========================================
if __name__ == "__main__":
    # 1. Generate a mock history of 110 data points
    np.random.seed(42)
    mock_stream = np.random.uniform(100, 150, 110)
    
    # Inputs for Approach 1 (The last 100 points)
    data_100 = mock_stream[-100:]
    
    # Inputs for Approach 2 (The last 20 points)
    data_20 = mock_stream[-20:]
    
    # Mocking the 'past data': Calculate the EMAs right BEFORE the final tick lands
    df_history = pd.DataFrame({'value': mock_stream[:-1]})
    past_ema11 = df_history['value'].ewm(span=11, adjust=False).mean().iloc[-1]
    past_ema25 = df_history['value'].ewm(span=25, adjust=False).mean().iloc[-1]

    # 2. Execute and verify they yield identical numbers
    res_1 = approach_1_bulk(data_100)
    res_2 = approach_2_optimized(data_20, past_ema11, past_ema25)
    
    print("--- MATHEMATICAL VALIDATION ---")
    print(f"Approach 1 Result -> EMA11: {res_1['ema11']:.4f} | EMA25: {res_1['ema25']:.4f} | SMA20: {res_1['sma20']:.4f}")
    print(f"Approach 2 Result -> EMA11: {res_2['ema11']:.4f} | EMA25: {res_2['ema25']:.4f} | SMA20: {res_2['sma20']:.4f}")
    print(f"Outputs Match Perfectly: {np.isclose(res_1['ema11'], res_2['ema11']) and np.isclose(res_1['sma20'], res_2['sma20'])}\n")

    # 3. Benchmark execution speeds over 1,000 iterations
    iterations = 1000
    
    # Warm-up cycles to eliminate CPU/Memory allocation noise
    approach_1_bulk(data_100)
    approach_2_optimized(data_20, past_ema11, past_ema25)
    
    # Time Approach 1
    start_time = time.perf_counter()
    for _ in range(iterations):
        approach_1_bulk(data_100)
    time_1 = ((time.perf_counter() - start_time) / iterations) * 1000

    # Time Approach 2
    start_time = time.perf_counter()
    for _ in range(iterations):
        approach_2_optimized(data_20, past_ema11, past_ema25)
    time_2 = ((time.perf_counter() - start_time) / iterations) * 1000

    print("--- SPEED PERFORMANCE ---")
    print(f"Approach 1 (Bulk Pandas): {time_1:.4f} ms per run")
    print(f"Approach 2 (Stream Numpy): {time_2:.4f} ms per run")
    print(f"Speed multiplier: Approach 2 is {time_1 / time_2:.1f}x faster.")
