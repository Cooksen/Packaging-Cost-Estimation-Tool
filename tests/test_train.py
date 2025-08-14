import os
import json
import joblib
from sklearn.linear_model import LinearRegression
from src.core.train_multi_input import train_model_for_component

def test_train_script_runs_and_creates_model(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    data_dir = tmp_path / "parsed_data"
    data_dir.mkdir()
    mock_data_path = data_dir / "price_weight_corrugate.json"
    mock_data = [
        {"weight": 10, "price": 50, "qty": 1, "label": "test1"},
        {"weight": 20, "price": 100, "qty": 1, "label": "test2"}
    ]
    with open(mock_data_path, 'w') as f:
        json.dump(mock_data, f)

    if not os.path.exists("trained_models"):
        os.mkdir("trained_models")

    component, mse, r2 = train_model_for_component(
        component="corrugate",
        model_type="linear"
    )

    expected_model_path = tmp_path / "trained_models" / "corrugate_linear_model.pkl"
    assert os.path.exists(expected_model_path), "Model file was not created."

    assert isinstance(mse, float)
    assert isinstance(r2, float)
    assert component == "corrugate"

    loaded_model = joblib.load(expected_model_path)
    assert isinstance(loaded_model, LinearRegression)