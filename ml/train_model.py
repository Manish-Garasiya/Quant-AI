from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd


FEATURES = [
    "macd",
    "adx",
    "di_plus",
    "di_minus",
    "ret_5",
    "volatility_20",
    "volume_ratio",
    "distance_sma20"
]


def train_model(feature_df):

    train = feature_df[
        feature_df.index < "2024-01-01"
    ]

    test = feature_df[
        feature_df.index >= "2024-01-01"
    ]

    X_train = train[FEATURES]
    y_train = train["target"]

    X_test = test[FEATURES]
    y_test = test["target"]

    model = XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    probs = model.predict_proba(X_test)[:, 1]

    print("Accuracy :", accuracy_score(y_test, preds))
    print("Precision:", precision_score(y_test, preds))
    print("Recall   :", recall_score(y_test, preds))

    prediction_df = pd.DataFrame(
        {
            "probability_up": probs,
            "prediction": preds
        },
        index=X_test.index
    )

    return model, prediction_df