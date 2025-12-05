import input_pdf
import process
import FAISS_store
import flashcard_generation
import postprocess


def main(pdf_path, start_page, end_page, batch_size):
    input_pdf.main(pdf_path, start_page, end_page, batch_size=batch_size)
    process.main()
    FAISS_store.main()
    flashcard_generation.main()
    postprocess.main()
