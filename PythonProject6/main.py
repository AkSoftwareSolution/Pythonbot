# ------------------------------------
# 1. Import Required Libraries
# ------------------------------------
import pandas as pd
import imaplib
import email
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# ------------------------------------
# 2. Load Dataset
# ------------------------------------
data = pd.read_csv(
    "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv",
    sep="\t",
    names=["label", "message"]
)

data["label"] = data["label"].map({"ham": 0, "spam": 1})


# ------------------------------------
# 3. Train-Test Split
# ------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    data["message"],
    data["label"],
    test_size=0.2,
    random_state=42
)


# ------------------------------------
# 4. Text Vectorization
# ------------------------------------
vectorizer = TfidfVectorizer(stop_words="english")

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# ------------------------------------
# 5. Train Model
# ------------------------------------
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)


# ------------------------------------
# 6. Model Evaluation
# ------------------------------------
y_pred = model.predict(X_test_tfidf)

print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# ------------------------------------
# 7. Spam Check Function
# ------------------------------------
def check_spam(text):
    text_tfidf = vectorizer.transform([text])
    result = model.predict(text_tfidf)
    return "Spam 🚫" if result[0] == 1 else "Not Spam ✅"


# ------------------------------------
# 8. Gmail Inbox Email Fetch
# ------------------------------------
EMAIL = "abulkhair77912@gmail.com"          # আপনার Gmail
PASSWORD = "tnboolydoiiykggc"     # Gmail App Password

def read_latest_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    latest_email_id = email_ids[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    email_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        email_body = msg.get_payload(decode=True).decode(errors="ignore")

    return email_body


# ------------------------------------
# 9. Run Spam Check on Email
# ------------------------------------
email_text = read_latest_email()

print("\nLatest Email Content:\n")
print(email_text[:500])   # শুধু প্রথম 500 character দেখাবে

print("\nSpam Check Result:")
print(check_spam(email_text))


# ------------------------------------
# 10. Manual Test
# ------------------------------------
print("\nManual Test:")
print(check_spam("Congratulations! You won a free iPhone"))
print(check_spam("Hey, are we meeting today?"))
print(check_spam("Win cash prize now, click this link"))
