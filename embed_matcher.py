import json
from sentence_transformers import SentenceTransformer, util

# Load pretrained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load QA pairs from file (convert data.js manually if needed)
qa_pairs = {
    "hello": "नमस्ते! भवतः स्वागतं हार्दं कुर्मः।",
    "hi": "नमस्कारणम्! अहं संस्कृतसहायकः अस्मि।",
    "good morning": "सुप्रभातम्! नूतनदिनस्य आरम्भः सदा आशया पूर्णः भवतु।",
    "how are you": "अहं अत्यन्तं कुशलः अस्मि। भवतः कुशलं किम्?",
    "who are you": "अहं कृत्रिमबुद्ध्या युक्तः एकः संवादसहायकः अस्मि।",
}

# Encode questions
questions = list(qa_pairs.keys())
question_embeddings = model.encode(questions, convert_to_tensor=True)

# Input loop
print("Sanskrit Chatbot (Semantic Matching)
Type 'exit' to quit.
")
while True:
    query = input("You: ").strip()
    if query.lower() == "exit":
        break

    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, question_embeddings)[0]
    best_match_idx = scores.argmax().item()
    best_score = scores[best_match_idx].item()

    if best_score > 0.6:
        matched_question = questions[best_match_idx]
        print("Bot:", qa_pairs[matched_question])
    else:
        print("Bot: क्षम्यताम्। मम कृते उत्तरं नास्ति।")