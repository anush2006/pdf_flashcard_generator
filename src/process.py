import os
import requests
import base64
import FAISS_store

def image_to_base64(path):
    with open(path, "rb") as img_file:
        img_bytes = img_file.read()                    
        img_base64 = base64.b64encode(img_bytes)      
        img_str = img_base64.decode("utf-8")         
        return img_str

def query_llava(image_list_base64, context):
    prompt_text  =""" This image is a page from a technical book. Examine the visual layout and focus on any diagram, chart, or structured information it contains.In case you find any diagrams give an indepth explanation of what you see in the diagram and any logical relationships that you can identify. Make it as detailed as possible.

"""


    payload = {
        "model": "llava",
        "prompt": prompt_text,
        "images": image_list_base64,
        "stream": False
    }

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        if res.ok:
            return res.json().get("response", "")
        else:
            return f"Error: Check details: {res.text} "
        
    except Exception as err:
        return f"{err}"

def handle_batch(batch_path):
    img_dir = os.path.join(batch_path, "images")
    text_path = os.path.join(batch_path, "page_text.txt")

    if (not os.path.isdir(img_dir)) or (not os.path.isfile(text_path)):#handling if process is run without batch details
        print(f"Skipping {batch_path} (missing images or text)")
        return

    with open(text_path, "r", encoding="utf-8") as f:
        context = f.read().strip()

    image_b64_list = []
    for img_file in sorted(os.listdir(img_dir)):
        if img_file.lower().endswith((".png", ".jpg", ".jpeg")):
            full_img_path = os.path.join(img_dir, img_file)
            print(f"Including image: {img_file}")
            image_b64_list.append(image_to_base64(full_img_path))

    if not image_b64_list:
        print(f"No images found in {img_dir}")
        return

    print("Querying LLaVA...")
    response_text = query_llava(image_b64_list, context)

    output_path = os.path.join(batch_path, "image_dissection.txt")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response_text)
        print(f" Dissection saved to: {output_path}")

def main():
    base_dir = "train_ocr"
    print(f" Processing all batches in: {base_dir}")

    for folder in sorted(os.listdir(base_dir)):
        batch_path = os.path.join(base_dir, folder)
        if os.path.isdir(batch_path):
            print(f"\n Handling batch: {folder}")
            handle_batch(batch_path)

if __name__ == "__main__":
    main()
