import joblib

# Dummy intent model (replace with trained one)
intent_keywords = {
    "greeting": ["hello", "hi", "good morning", "good night"],
    "farewell": ["bye", "goodbye"],
    "info": ["who", "what", "how"],
}

def predict_intent(text):
    text = text.lower()
    for intent, keywords in intent_keywords.items():
        if any(kw in text for kw in keywords):
            return intent
    return "unknown"

print("Intent Classifier Demo — type 'exit' to quit")
while True:
    msg = input("You: ").strip()
    if msg == "exit":
        break
    intent = predict_intent(msg)
    print("Intent:", intent)