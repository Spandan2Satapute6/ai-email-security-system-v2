from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
import pickle
import os
import numpy as np

# -------------------- BALANCED DATASET --------------------

spam_emails = [
    # Financial scams
    "Win money now",
    "Free lottery prize", 
    "Claim your reward now",
    "Limited time offer click here",
    "Get rich quick offer",
    "Congratulations you won free cash",
    "Exclusive deal just for you",
    "Act now to win big prizes",
    "Limited offer buy now",
    
    # Account security threats
    "Urgent account verification required",
    "Click this link to reset password",
    "Your account is at risk click here",
    "Your account will be suspended",
    "Verify your account immediately",
    "Security alert action required",
    
    # Urgency tactics
    "Urgent response needed",
    "You have won a prize",
    "Click here to claim your reward",
    
    # More spam examples
    "Free iPhone giveaway",
    "You've been selected for cash prize",
    "Click here for instant money",
    "Claim your inheritance now",
    "Win big prizes today",
    "Free money transfer waiting",
    "Lottery winner notification",
    "Cash prize delivery today"
]

normal_emails = [
    # Work-related
    "Project meeting tomorrow",
    "Submit your report by evening", 
    "Deadline for assignment",
    "Team meeting at 5pm",
    "Please review the document",
    "Let's schedule a call",
    "Lunch meeting tomorrow",
    "Update project status",
    "Can we reschedule meeting",
    "Please find attached document",
    "Reminder for tomorrow's meeting",
    "Discussion on project requirements",
    "Client call scheduled today",
    "Prepare presentation slides",
    "Submit assignment before deadline",
    
    # Personal/General
    "Let's connect today",
    "Call me when free",
    "Report is attached",
    "How are you doing today",
    "Following up on our conversation",
    "Can you review this document",
    "Thanks for your help",
    "Looking forward to our meeting",
    "Please confirm your attendance",
    "Schedule for next week",
    "Team building event Friday",
    "Quarterly review next week"
]

# Combine and create balanced dataset
emails = spam_emails + normal_emails
labels = ["spam"] * len(spam_emails) + ["not_spam"] * len(normal_emails)

print(f"Dataset: {len(spam_emails)} spam + {len(normal_emails)} normal = {len(emails)} total")
print(f"Balance: {len(spam_emails)}/{len(normal_emails)} = {len(spam_emails)/len(normal_emails):.1f}")

# -------------------- VECTORIZE --------------------

vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2),   # unigram + bigram (better detection)
    max_features=1000,       # limit features for better generalization
    lowercase=True,          # normalize case
    sublinear_tf=True        # reduce impact of very frequent terms
)

X = vectorizer.fit_transform(emails)

# -------------------- TRAIN MODEL --------------------

model = MultinomialNB(alpha=1.0)  # Laplace smoothing for better generalization
model.fit(X, labels)

# -------------------- EVALUATE MODEL --------------------

# Cross-validation for better accuracy estimate
cv_scores = cross_val_score(model, X, labels, cv=5, scoring='accuracy')
print(f"Cross-validation accuracy: {np.mean(cv_scores):.3f} (+/- {np.std(cv_scores):.3f})")

# -------------------- SAVE MODEL --------------------

os.makedirs("server", exist_ok=True)

with open("server/model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("✅ Model trained and saved as server/model.pkl")
print(f"Dataset size: {len(emails)} samples")
print(f"Feature count: {X.shape[1]} features")

# -------------------- BASELINE TEST --------------------

test_emails = [
    "Win a free iPhone now",
    "Meeting scheduled at 3pm",
    "Click here to claim your prize",
    "URGENT!!! verify your account now http://fake.com"
]

print("\n🔍 Testing Model:\n")

for email in test_emails:
    X_test = vectorizer.transform([email])
    pred = model.predict(X_test)[0]
    prob = max(model.predict_proba(X_test)[0])

    print(f"Email: {email}")
    print(f"Prediction: {pred}, Confidence: {round(prob,2)}\n")