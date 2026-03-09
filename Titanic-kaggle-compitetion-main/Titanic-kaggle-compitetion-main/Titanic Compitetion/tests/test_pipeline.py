import pytest
import pandas as pd
from src.data.data_validation import DataValidator
from src.features.feature_engineering import FeatureEngineer

def test_data_validator():
    """Test standard data validator"""
    expected_cols = ["Age", "HomePlanet"]
    validator = DataValidator(expected_cols, "Transported")
    
    # Valid dataframe
    df_valid = pd.DataFrame({
        "Age": [25, 30],
        "HomePlanet": ["Earth", "Europa"],
        "Transported": [True, False]
    })
    
    assert validator.validate(df_valid) == True
    
    # Missing column
    df_invalid = pd.DataFrame({"Age": [25]})
    assert validator.validate(df_invalid) == False

def test_feature_engineering():
    """Test cabin decomposition and spending grouping"""
    fe = FeatureEngineer()
    
    df = pd.DataFrame({
        "PassengerId": ["0001_01", "0002_01"],
        "Cabin": ["B/0/P", "F/1/S"],
        "Age": [20, 25],
        "RoomService": [100, 0],
        "FoodCourt": [50, 0],
        "ShoppingMall": [0, 0],
        "Spa": [0, 0],
        "VRDeck": [0, 0]
    })
    
    transformed = fe.transform(df)
    
    # Check if new features were added
    assert "CabinSide" in transformed.columns
    assert "CabinDeck" in transformed.columns
    assert "TotalSpend" in transformed.columns
    assert "Group" in transformed.columns
    
    assert transformed["TotalSpend"].iloc[0] == 150
    assert transformed["CabinSide"].iloc[0] == "P"
    assert transformed["CabinDeck"].iloc[1] == "F"
