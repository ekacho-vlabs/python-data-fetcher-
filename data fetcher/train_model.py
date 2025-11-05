import pandas as pd
import mysql.connector
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

conn = mysql.connector.connect(
    host="localhost",
    user="vlabsmwc_mobile_agency_tracker",
    password="1234@@##mobile",
    database="vlabsmwc_mobile_agency_tracker"
)

df = pd.read_sql("SELECT * FROM price_log ORDER BY id DESC LIMIT 5000", conn)
conn.close()

df["price"] = df["price"].astype(float)
df["ret"] = df["price"].pct_change()
df["target"] = (df["price"].shift(-1) > df["price"]).astype(int)
df = df.dropna()

X = df[["price", "ret"]]
y = df["target"]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=200))
])
model.fit(X, y)
joblib.dump(model, "usdt_rwf_model.pkl")

print("✅ Model retrained and saved.")
