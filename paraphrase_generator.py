from transformers import pipeline

# Load paraphrasing model
paraphraser = pipeline("text2text-generation", model="ramsrigouthamg/t5_paraphraser")

print("Paraphrase Generator (T5)
Type 'exit' to quit.
")
while True:
    sentence = input("Enter sentence: ").strip()
    if sentence.lower() == "exit":
        break
    input_text = f"paraphrase: {sentence}"
    result = paraphraser(input_text, max_length=60, num_return_sequences=3, num_beams=5)
    print("Paraphrases:")
    for res in result:
        print("-", res["generated_text"])