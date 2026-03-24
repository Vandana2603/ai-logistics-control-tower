from sklearn.ensemble import RandomForestClassifier

def train_model(df):
    X = df[["orders", "workers", "safety", "productivity"]]
    y = df["delay"]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    return model