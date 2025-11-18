# Step 1: Import required libraries
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

#Converts text to numbers using CountVectorizer
#Trains a Naive Bayes classifier (MultinomialNB)
#Predicts whether a message is spam or not spam (ham)
#Prints accuracy
#Tests new messages

# Step 2: Sample dataset (You can replace it with your own)
texts = [
    "Congratulations! You won a free lottery",
    "Get a free mobile now",
    "Call me when you reach home",
    "Let's meet tomorrow for lunch",
    "You have won a prize! Claim now",
    "Please send me the assignment"
]

labels = ["spam", "spam", "ham", "ham", "spam", "ham"]   # ham = not spam

# Step 3: Convert text into numerical form
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Step 4: Split data into train/test
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=42)

# Step 5: Train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 6: Test the model
predictions = model.predict(X_test)

# Step 7: See accuracy
print("Accuracy:", accuracy_score(y_test, predictions))

# Step 8: Test with your own message
sample = ["Call me when you reach home"]
sample_vector = vectorizer.transform(sample)
print("Prediction:", model.predict(sample_vector)[0])
