import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

def generate_pricing_data(samples=1200):
    np.random.seed(42)
    base_price = np.random.uniform(10.0, 500.0, samples)
    # Competitor price generally tracks base price with variance
    competitor_price = base_price * np.random.uniform(0.85, 1.15, samples)
    stock_level = np.random.randint(0, 200, samples)
    days_to_restock = np.random.randint(1, 30, samples)
    search_velocity_multiplier = np.random.uniform(0.5, 2.5, samples)
    
    # Target pricing logic: High search velocity and low stock spikes the recommendation
    recommended_price = (
        (base_price * 0.4) + 
        (competitor_price * 0.5) + 
        (search_velocity_multiplier * 15.0) - 
        (stock_level * 0.05) + 
        (days_to_restock * 0.2)
    )
    # Clamp recommended price to not drop below 70% of base price
    recommended_price = np.maximum(recommended_price, base_price * 0.7)
    
    df = pd.DataFrame({
        "base_price": base_price,
        "competitor_price": competitor_price,
        "stock_level": stock_level,
        "days_to_restock": days_to_restock,
        "search_velocity_multiplier": search_velocity_multiplier,
        "recommended_price": recommended_price
    })
    return df

def train_and_export():
    print("Generating synthetic data for Pricing Model...")
    df = generate_pricing_data()
    
    X = df[["base_price", "competitor_price", "stock_level", "days_to_restock", "search_velocity_multiplier"]]
    y = df["recommended_price"]
    
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", LinearRegression())
    ])
    
    print("Training Dynamic Pricing Linear Regression Pipeline...")
    pipeline.fit(X, y)
    
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/ml_artifacts"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "pricer_v1.joblib")
    
    joblib.dump(pipeline, output_path)
    print(f"Pricing model exported successfully to: {output_path}")

if __name__ == "__main__":
    train_and_export()