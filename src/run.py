import input_pdf
import process
import flashcard_generation
import postprocess
def main():
    input_pdf.perform_extraction()
    process.main()
    flashcard_generation.main()
    postprocess.main()

if __name__=="__main__":
    main()

