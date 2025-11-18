# Step 1: Import libraries
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Step 2: Create a small sample dataset
texts = [
    "I love this product, it's amazing",
    "This is the best experience ever",
    "I am very happy with the service",
    "The product is terrible and bad",
    "I hate this, worst purchase",
    "Very disappointing quality"
]

labels = ["positive", "positive", "positive", "negative", "negative", "negative"]

# Step 3: Convert text to TF-IDF features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Step 4: Train–test split
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=42)

# Step 5: Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 6: Test the model
predictions = model.predict(X_test)

# Step 7: Accuracy
print("Accuracy:", accuracy_score(y_test, predictions))

# Step 8: Test with your own text
sample = ["I love this product, it's amazing"]
sample_vector = vectorizer.transform(sample)
print("Sentiment Prediction:", model.predict(sample_vector)[0])
