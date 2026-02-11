# -------------------------------
# 1. Import Required Libraries
# -------------------------------
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# 2. Load Dataset
# -------------------------------
url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
data = pd.read_csv(url)

print("Dataset Shape:", data.shape)
print(data.head())

# -------------------------------
# 3. Data Info & Summary
# -------------------------------
print("\nInfo:")
print(data.info())

print("\nStatistical Summary:")
print(data.describe())

# -------------------------------
# 4. Correlation Heatmap
# -------------------------------
plt.figure(figsize=(10,8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.show()

# -------------------------------
# 5. Features & Target
# -------------------------------
X = data.drop("medv", axis=1)  # medv = house price
y = data["medv"]

# -------------------------------
# 6. Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# 7. Train Model
# -------------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -------------------------------
# 8. Predict & Evaluate
# -------------------------------
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation:")
print("RMSE:", rmse)
print("R2 Score:", r2)

# -------------------------------
# 9. Actual vs Predicted Plot
# -------------------------------
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted House Price")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.tight_layout()
plt.show()

# -------------------------------
# 10. Predict New House Price
# -------------------------------
# Example: new house with 13 features
new_house = np.array([[0.03, 0, 7.07, 0, 0.469, 6.421, 78.9, 4.9671, 2, 242, 17.8, 396.9, 9.14]])
pred_price = model.predict(new_house)
print("\nPredicted House Price for new sample:", pred_price[0])
