# Stub — full model would require large download or API access
# Use external tool like IndicTrans or HuggingFace

def mock_translate(text):
    # Just a demo map
    sample = {
        "hello": "नमस्ते",
        "how are you": "कथमस्ति भवान्?",
        "thank you": "धन्यवादः"
    }
    return sample.get(text.lower(), "क्षम्यताम्। अनुवादं कर्तुं न शक्यते।")

print("English → Sanskrit Translator (Mock)
")
while True:
    en = input("Enter English: ").strip()
    if en == "exit":
        break
    print("Sanskrit:", mock_translate(en))