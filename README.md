This code uses a combination of Llava and Llama3 to generate flashcards based on the content provided from a pdf within a page range,
The code consists of 5 main modules:-
    1.input_pdf- Converts the pdf to images using PyMuPdf
    2.process- Parses the pdf into text and queries Llava about the image description.
    3.flashcard_generation-generates the flashcards using Llama3 
    4.postprocess-clean up the raw response from Llama3 to json format [{"front":..,"back":...}]
    5.Flashcard- A simple css+streamlit script to view the flashcards

The require python packages are attached as requirements.txt
Install required Python packages with: pip install -r requirements.txt

Additionally these programs require Ollama to run the llm's locally,
  Download ollama at: https://ollama.com/download/windows 
  Download Llava and Llama using "ollama pull llava/llama"

Make sure Ollama is running at: http://localhost:11434

To run whole project execute : run.py
Project structure:
```
.
├── src/
│   ├── input_pdf.py
│   ├── process.py
│   ├── flashcard_generation.py
│   ├── postprocess.py
│   ├── Flashcard.py
│   ├── run.py
│   └── flashcards.json         # raw output (auto generated)
├── train_ocr/              # (auto-generated)
├── uploads/                # (input PDFs)
├── cleaned_flashcards.json
├── requirements.txt
└── README.md
```
