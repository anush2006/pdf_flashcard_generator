import fitz
import shutil
import os


OUTPUT_DIR = "train_ocr"
PAGES_PER_BATCH = 1
DPI = 200

def main(name_pdf,start_page,end_page,output_dir=OUTPUT_DIR, batch_size=PAGES_PER_BATCH, dpi=DPI):
    pdf_path = os.path.join("src/uploads",name_pdf)
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Could not open PDF: {e}")
        return

    page_count = doc.page_count
    print(f"PDF loaded: {page_count} pages")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    loop_end_page = end_page
    batch_num = 1

    print(f"Start page: {start_page}\nEnd page: {end_page}")

    for start in range(start_page-1, loop_end_page, batch_size):
        end = min(start + batch_size, page_count)
        batch_dir = os.path.join(output_dir, f"batch_{batch_num:03d}")
        img_dir = os.path.join(batch_dir, "images")

        os.makedirs(img_dir, exist_ok=True)

        text_path = os.path.join(batch_dir, "page_text.txt")
        with open(text_path, "w", encoding="utf-8") as tf:
            for i in range(start, end):
                page = doc.load_page(i)
                pix = page.get_pixmap(dpi=dpi)
                img_path = os.path.join(img_dir, f"page_{i+1}.png")
                pix.save(img_path)
                text = page.get_text()
                tf.write(f"\n\n--- Page {i+1} ---\n{text.strip()}")

        print(f"Batch {batch_num:03d} saved (pages {start + 1}-{end})")
        batch_num += 1

    print("All pages processed successfully.")

if __name__ == "__main__":
   main()
