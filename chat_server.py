from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

qa_pairs = {
    "hello": "नमस्ते! भवतः स्वागतं हार्दं कुर्मः।",
    "hi": "नमस्कारणम्! अहं संस्कृतसहायकः अस्मि।",
    "good morning": "सुप्रभातम्! नूतनदिनस्य आरम्भः सदा आशया पूर्णः भवतु।",
    "how are you": "अहं अत्यन्तं कुशलः अस्मि। भवतः कुशलं किम्?",
    "who are you": "अहं कृत्रिमबुद्ध्या युक्तः एकः संवादसहायकः अस्मि।",
}
questions = list(qa_pairs.keys())
question_embeddings = model.encode(questions, convert_to_tensor=True)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, question_embeddings)[0]
    best_match_idx = scores.argmax().item()
    best_score = scores[best_match_idx].item()

    if best_score > 0.6:
        matched_question = questions[best_match_idx]
        return jsonify({"response": qa_pairs[matched_question]})
    else:
        return jsonify({"response": "क्षम्यताम्। मम कृते उत्तरं नास्ति।"})

if __name__ == "__main__":
    app.run(port=5000)
