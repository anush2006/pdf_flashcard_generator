import os
import json
import ollama
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

BASE_DIR = "train_ocr"
IMAGE_DESC_FILE = "image_dissection.txt"
TEXT_FILE = "page_text.txt"
OUTPUT_FILE = "flashcards.json"
BATCH_SIZE = 3

def load_index():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_vectorstore", embeddings, allow_dangerous_deserialization=True)
    return vectorstore

def retrieve(query_text, k=3):
    vectorstore = load_index()
    docs = vectorstore.similarity_search(query_text, k=k)

    chunks = []
    for d in docs:
        if hasattr(d, "page_content"):
            chunks.append(str(d.page_content))
        else:
            chunks.append(str(d))

    return chunks


def summarize(text):
    prompt = f"""
    Summarize the following text into 3–5 clear bullet points focusing ONLY on the
    concepts and ideas that are important for question/flashcard generation.

    Text:
    {text}

    Summary:
    """
    result = ollama.generate(model="llama3", prompt=prompt)
    return result["response"]

def main():
    all_flashcards = []

    all_items = os.listdir(BASE_DIR)
    folders = []
    for item in all_items:
        item_path = os.path.join(BASE_DIR, item)
        if os.path.isdir(item_path):
            folders.append(item)

    for batch_start in range(1, len(folders), BATCH_SIZE):
        batch_folders = folders[batch_start:batch_start + BATCH_SIZE]
        combined_text = ""

        for folder in batch_folders:
            folder_path = os.path.join(BASE_DIR, folder)
            text_path = os.path.join(folder_path, TEXT_FILE)
            image_path = os.path.join(folder_path, IMAGE_DESC_FILE)

            if os.path.isfile(text_path) and os.path.isfile(image_path):
                with open(text_path, "r", encoding="utf-8") as f:
                    pagetext = f.read().strip()

                with open(image_path, "r", encoding="utf-8") as f:
                    imagedescription = f.read().strip()

                combined_text += f"Page: {folder}\n\nText:\n{pagetext}\n\nDiagram:\n{imagedescription}\n\n---\n\n"

        retrieved_chunks = retrieve(combined_text, k=3)

        if retrieved_chunks:
            combined_retrieved = "\n\n".join(retrieved_chunks)
            retrieved_summary = summarize(combined_retrieved)
        else:
            retrieved_summary = "No relevant retrieved knowledge found."

        if combined_text:
            prompt = f"""

You are an expert educator. Use the provided academic content and retrieved knowledge
to generate high-quality flashcards.

Retrieved Knowledge (Summarized):
{retrieved_summary}

Guidelines:
- Classify each question into one of Bloom’s Taxonomy levels: Remember, Understand, Apply, Analyze, Evaluate, Create.
- Generate 25 questions and answers in this JSON format:
  {{ "front": "question", "back": "answer" }}
- Ensure factual accuracy.
- No vague answers.
- Include higher-order thinking where possible.
- Avoid repetition.
- Do NOT refer to any images directly.
- Base questions strictly on the content above.

**Output (JSON only):**
"""

            print(f"Querying llama3 for page set {batch_start} to {batch_start + BATCH_SIZE}...")
            res = ollama.generate(
                model=MODEL_NAME,
                prompt=prompt,
                stream=False
            )

            output = res.get("response", "").strip()

            if output.startswith("```json"):
                output = output.removeprefix("```json").strip()
            if output.endswith("```"):
                output = output.removesuffix("```").strip()

            all_flashcards.append({
                "batch_start_page": batch_folders[0],
                "raw_output": output
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_flashcards, f, indent=2, ensure_ascii=False)

    print(f"Saved to {OUTPUT_FILE}")
if __name__=="__main__":
    main()
