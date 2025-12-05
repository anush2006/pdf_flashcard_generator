def main():
    from langchain.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print("Script is running from:", BASE_DIR)
    src = os.path.join(BASE_DIR, "..", "train_ocr")
    src = os.path.abspath(src)  
    print("train_ocr path:", src)
    contents = os.listdir(src)
    all_texts = []
    metadata = []

    for folder in contents:
        folder_path = os.path.join(src, folder)
        text_path = os.path.join(folder_path, "page_text.txt")
        image_path = os.path.join(folder_path, "image_dissection.txt")
        if os.path.isfile(text_path):
            with open(text_path, "r", encoding="utf-8") as f:
                pagetext = f.read().strip()
            with open(image_path, "r", encoding="utf-8") as f:
                imagedescription = f.read().strip()
            combined_text = pagetext + "\n" + imagedescription
            all_texts.append(combined_text)
            metadata.append({"folder": folder, "folder_path": folder_path})
    print(f"Loaded {len(all_texts)} documents from {src}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(all_texts, embeddings, metadatas=metadata)
    vectorstore.save_local("faiss_vectorstore")
    print("FAISS vector store created and saved as 'faiss_vectorstore' directory.")
if __name__ == "__main__":
    main()