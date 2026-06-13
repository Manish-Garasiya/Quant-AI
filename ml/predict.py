import joblib
import pandas as pd


def load_model(model_path="ml/models/xgb_trend_model.pkl"):
    obj = joblib.load(model_path)
    return obj["model"], obj["feature_cols"]

def predict_latest(raw_df, model_path="ml/models/xgb_trend_model.pkl"):
    from features.feature_engineering import build_feature_frame

    model, feature_cols = load_model(model_path)
    df = build_feature_frame(raw_df, horizon=5)

    X = df[feature_cols].tail(1)
    prob_up = float(model.predict_proba(X)[0, 1])
    pred = int(prob_up >= 0.5)

    return prob_up, pred, df.tail(1)