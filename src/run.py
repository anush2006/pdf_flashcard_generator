import input_pdf
import process
import flashcard_generation
import postprocess
def main(pdf_path,start,end):
    input_pdf.main(pdf_path,start,end)
    process.main()
    flashcard_generation.main()
    postprocess.main()

if __name__=="__main__":
    main()

