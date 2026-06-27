#!/usr/bin/env python
"""
Machine Learning Model Training Script
Trains a Random Forest classifier on Telco Customer Churn data
"""

import argparse
import os
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix


def load_data(csv_path):
    """Load and preprocess customer data"""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    return df


def preprocess_data(df):
    """Preprocess the dataset"""
    print("Preprocessing data...")
    
    # Expected features for the model
    feature_columns = [
        'tenure_months', 'monthly_charges', 'total_charges', 'partner',
        'dependents', 'contract', 'internet_service', 'paperless_billing'
    ]
    
    # Ensure all required columns exist
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns {missing_cols}, will use available columns")
        feature_columns = [col for col in feature_columns if col in df.columns]
    
    X = df[feature_columns].copy()
    
    # Determine target column (churn_label or Churn)
    if 'churn_label' in df.columns:
        y = (df['churn_label'] == 'Yes').astype(int)
    elif 'Churn' in df.columns:
        y = (df['Churn'] == 'Yes').astype(int)
    else:
        raise ValueError("Dataset must contain 'churn_label' or 'Churn' column")
    
    print(f"Features: {list(X.columns)}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    # Encode categorical features
    for col in ['partner', 'dependents', 'contract', 'internet_service', 'paperless_billing']:
        if col in X.columns:
            X[col] = (X[col] == 'Yes').astype(int)
    
    # Handle missing values
    X = X.fillna(0)
    
    # Convert to numeric
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    print(f"Processed features shape: {X.shape}")
    print(f"Features: {X.dtypes}")
    
    return X, y


def train_model(X, y, test_size=0.2, random_state=42, n_estimators=100):
    """Train Random Forest model"""
    print(f"Training Random Forest with {n_estimators} estimators...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=15,
        min_samples_split=10,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\nModel Performance:")
    print(f"Training Accuracy: {train_score:.4f}")
    print(f"Testing Accuracy: {test_score:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 5 Important Features:")
    print(feature_importance.head())
    
    # Classification report
    y_pred = model.predict(X_test)
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return model


def save_model(model, model_path):
    """Save trained model to pickle file"""
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="Train ML model for Telco Customer Churn prediction"
    )
    parser.add_argument(
        '--data',
        type=str,
        required=True,
        help='Path to CSV file with customer data'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='ml_models/random_forest_churn.pkl',
        help='Output path for trained model'
    )
    parser.add_argument(
        '--estimators',
        type=int,
        default=100,
        help='Number of trees in Random Forest'
    )
    parser.add_argument(
        '--test-size',
        type=float,
        default=0.2,
        help='Test set size (0.0-1.0)'
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not os.path.exists(args.data):
        print(f"Error: Data file not found: {args.data}")
        return 1
    
    try:
        # Load and process data
        df = load_data(args.data)
        X, y = preprocess_data(df)
        
        # Train model
        model = train_model(X, y, test_size=args.test_size, n_estimators=args.estimators)
        
        # Save model
        save_model(model, args.output)
        
        print("\n✓ Training completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
