import os
import json
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

BASE_DIR = "train_ocr"
IMAGE_DESC_FILE = "image_dissection.txt"
TEXT_FILE = "page_text.txt"
OUTPUT_FILE = "flashcards.json"
BATCH_SIZE = 3
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

        if combined_text:
            prompt = f"""

    You are an expert educator generating high-quality flashcards for students based on academic content.

    DEEPLY ANALYZE THE TEXT AND DESCRIPTION GIVEN TO DO THE FOLLOWING
    -GENERATE FLASHCARDS WITH: 

    - Each item should be of the form: [{{ "front": "<question>", "back": "<answer summarized in normal english>" }}]
    - Do not say refer to this/that give the full answer
    - make sure the questions satisfy the following: Remember , analyze , evaluate and create
    **Input:**

    {combined_text}


    **Output (JSON only):**



    """

            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            }
            print(f"Querying page set {batch_start} to {batch_start + BATCH_SIZE}")
            res = requests.post(OLLAMA_API_URL, json=payload)
            output = res.json().get("response", "").strip()

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