import json

INPUT_FILE = "flashcards.json"
OUTPUT_FILE = "D:/autogen/cleaned_flashcards.json"

def parse_json_block(text):
    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        return json.loads(text[start:end])
    except Exception:
        return []


def clean_flashcards(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    skipped = 0

    for batch in data:
        raw = batch.get("raw_output", "").strip()

        if "[" in raw and "]" in raw:
            parsed = parse_json_block(raw)
            for card in parsed:
                if "front" in card and "back" in card:
                    cleaned.append({
                        "front": card["front"].strip(),
                        "back": card["back"].strip()
                    })
                else:
                    skipped += 1
        
    return cleaned, skipped

def main():
    flashcards, skipped_count = clean_flashcards(INPUT_FILE)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(flashcards, out, indent=2, ensure_ascii=False)

    print(f" Extracted {len(flashcards)} flashcards")
    print(f" Skipped {skipped_count} incomplete or malformed entries")
    print(f" Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()