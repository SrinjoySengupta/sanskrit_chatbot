Sanskrit Chatbot — Interactive Web-Based Q&A System

The Sanskrit Chatbot is an interactive, browser-based application designed to answer basic queries in Sanskrit. It combines natural language processing (NLP) techniques with a clean, minimalistic Gradio interface to create an engaging and educational experience for users interested in learning or exploring Sanskrit.

At its core, the chatbot uses Python and the NLTK library for text preprocessing, tokenization, stemming, and keyword matching. The underlying architecture is built on a text-matching algorithm that compares user input against a structured dataset of question-answer pairs. This ensures accurate and context-relevant responses while keeping the implementation lightweight and efficient.

One of the main goals of the project was accessibility. By leveraging Gradio, the chatbot runs directly in a web browser without requiring any complex setup from the user. The interface provides a real-time conversational flow, allowing instant interaction and immediate feedback. This makes the chatbot suitable for educational purposes, demonstrations, or as a base for more advanced NLP integration.

The dataset used for intent recognition is stored in JSON format, allowing developers and educators to easily expand the chatbot’s capabilities by adding new intents and responses. The modular structure ensures that both the NLP logic and the dataset can evolve independently, making future upgrades seamless.

From a deployment standpoint, the chatbot is lightweight and can be hosted locally or on cloud platforms like Hugging Face Spaces, Heroku, or PythonAnywhere.

Key Features

Real-time interaction via browser using Gradio UI

Preprocessing pipeline for Sanskrit text normalization and intent recognition

Lightweight architecture without heavy ML dependencies

Easily extensible dataset stored in JSON for quick updates

Cross-platform deployment capability on local or cloud environments

Tech Stack

Languages & Libraries: Python, NLTK, Pandas, Regex

Frontend: Gradio Web Interface

Data Storage: JSON

This project demonstrates skills in full-stack development, NLP preprocessing, frontend-backend integration, and educational technology design. It reflects a practical approach to merging linguistic preservation with modern web-based application development.
