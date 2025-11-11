

import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px
import os

# -----------------------------------
# 1  Data Ingestion (Create + Read)
# -----------------------------------
print(" Step 1: Data Ingestion")

# Create a sample CSV if not exists
csv_file = "sales_data.csv"

if not os.path.exists(csv_file):
    print("Creating sample dataset...")
    data_dict = {
        "TV": [230.1, 44.5, 17.2, 151.5, 180.8, 8.7, 57.5, 120.2, 199.8, 66.1,
               214.7, 23.8, 97.5, 204.1, 195.4, 67.8, 281.4, 69.2, 147.3, 218.4],
        "Radio": [37.8, 39.3, 45.9, 41.3, 10.8, 48.9, 32.8, 19.6, 2.6, 5.8,
                  24.0, 35.1, 7.6, 32.9, 47.7, 36.6, 39.6, 20.5, 23.9, 27.7],
        "Newspaper": [69.2, 45.1, 69.3, 58.5, 58.4, 75.0, 23.5, 11.6, 21.2, 24.2,
                      4.0, 65.9, 7.2, 46.0, 52.9, 114.0, 55.8, 18.3, 19.1, 53.4],
        "Sales": [22.1, 10.4, 9.3, 18.5, 12.9, 7.2, 11.8, 13.2, 14.6, 8.6,
                  17.4, 9.2, 9.7, 19.0, 22.4, 12.5, 24.4, 11.3, 13.2, 14.8]
    }
    df = pd.DataFrame(data_dict)
    df.to_csv(csv_file, index=False)
    print(f" Sample CSV '{csv_file}' created successfully.")
else:
    print(f" Found existing dataset: {csv_file}")

# Read data
data = pd.read_csv(csv_file)
print("\n First 5 rows of data:")
print(data.head())

# -----------------------------------
# 2 Data Storage (SQLite)
# -----------------------------------
print("\n Step 2: Data Storage")

# Connect to SQLite DB
conn = sqlite3.connect("sales_db.sqlite")

# Store data in SQLite
data.to_sql("sales_table", conn, if_exists="replace", index=False)
print("Data successfully stored in 'sales_db.sqlite' database.")

# Verify by reading back
df = pd.read_sql("SELECT * FROM sales_table", conn)
print("\n Retrieved data from database:")
print(df.head())

# -----------------------------------
# 3️ Machine Learning
# -----------------------------------
print("\n Step 3: Machine Learning")

# Feature and target
X = df[["TV", "Radio", "Newspaper"]]
y = df["Sales"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, predictions)
print(f" Model trained successfully. Mean Squared Error: {mse:.2f}")

# Combine results for visualization
results_df = X_test.copy()
results_df["Actual Sales"] = y_test.values
results_df["Predicted Sales"] = predictions

# -----------------------------------
# 4️ Visualization
# -----------------------------------
print("\n Step 4: Visualization")

fig = px.scatter(
    results_df,
    x="Actual Sales",
    y="Predicted Sales",
    title="Actual vs Predicted Sales (Linear Regression)",
    size_max=10,
    color_discrete_sequence=["#2b8cbe"]
)

fig.update_layout(
    title_font=dict(size=20, color="darkblue"),
    xaxis_title="Actual Sales",
    yaxis_title="Predicted Sales",
    template="plotly_white"
)

fig.show()

print("\n End-to-End Data Pipeline Executed Successfully!")
