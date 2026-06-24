import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

def generate_churn_data(samples=1500):
    np.random.seed(101)
    login_frequency = np.random.randint(0, 30, samples)  # logins per month
    days_since_last_purchase = np.random.randint(0, 180, samples)
    cart_abandonment_rate = np.random.uniform(0.0, 1.0, samples)
    
    # Hidden probability logic for churning
    linear_comb = (
        (days_since_last_purchase * 0.03) + 
        (cart_abandonment_rate * 3.5) - 
        (login_frequency * 0.15) - 1.0
    )
    prob = 1 / (1 + np.exp(-linear_comb))
    churn = np.where(prob > 0.5, 1, 0)
    
    df = pd.DataFrame({
        "login_frequency": login_frequency,
        "days_since_last_purchase": days_since_last_purchase,
        "cart_abandonment_rate": cart_abandonment_rate,
        "churn": churn
    })
    return df

def train_and_export():
    print("Generating synthetic data for Churn Model...")
    df = generate_churn_data()
    
    X = df[["login_frequency", "days_since_last_purchase", "cart_abandonment_rate"]]
    y = df["churn"]
    
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=50, random_state=42))
    ])
    
    print("Training Churn Shield Random Forest Pipeline...")
    pipeline.fit(X, y)
    
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/ml_artifacts"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "churn_v1.joblib")
    
    joblib.dump(pipeline, output_path)
    print(f"Churn model exported successfully to: {output_path}")

if __name__ == "__main__":
    train_and_export()