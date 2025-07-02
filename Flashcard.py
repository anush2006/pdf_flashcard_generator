import streamlit as st
import os
from streamlit import session_state as ss
import json
import streamlit.components.v1 as components
import sys
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from run import main

st.set_page_config(page_title="Flashcard Viewer", layout="wide")
st.title("Flashcard Viewer")


SAVE_DIR = "src/uploads"

def has_pdf(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            return True
    return False


os.makedirs(SAVE_DIR, exist_ok=True)
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file is not None:
    save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.uploaded_pdf = uploaded_file.name
    st.success(f"File saved successfully to: {save_path}")
start =int(st.number_input("Enter start page"))
end = int(st.number_input("Enter end page"))
if st.button("Generate"):
    if os.path.exists(SAVE_DIR) and has_pdf(SAVE_DIR):
        uploaded_pdf = st.session_state.get("uploaded_pdf", None)
        if uploaded_pdf:
            st.success("Executing module...This may take a while...")
            main(uploaded_pdf,start,end) 
            
        else:
            st.error("No uploaded PDF filename found in session state.If u want a new set of questions add the pdf again.")
    else:
        st.error("PDF not uploaded")
if st.button("End"):
        os._exit(0)

if os.path.exists("cleaned_flashcards.json"):
    with open("cleaned_flashcards.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if "card_index" not in st.session_state:
        st.session_state.card_index = 1

    i = st.session_state.card_index
    if i >= len(data):
        st.success("You've reached the end of the flashcards!")
        st.stop()

    question = data[i]["front"]
    answer = data[i]["back"]

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            overflow: visible;
        }}
        .scene {{
            width: 500px;
            height: 300px;
            perspective: 1200px;
            margin: 50px auto;
            overflow: visible;
        }}
        .card {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.8s;
            cursor: pointer;
        }}
        .card.flipped {{
            transform: rotateY(180deg);
        }}
        .face {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: Arial, sans-serif;
            font-size: 28px;
            padding: 30px;
            text-align: center;
            border: 2px solid #ccc;
            border-radius: 16px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }}
        .front {{
            background-color: #f0f0f0;
        }}
        .back {{
            background-color: #2e8b57;
            color: white;
            transform: rotateY(180deg);
        }}
    </style>
    </head>
    <body>
    <div class="scene" onclick="this.querySelector('.card').classList.toggle('flipped')">
        <div class="card">
            <div class="face front">{question}</div>
            <div class="face back">{answer}</div>
        </div>
    </div>
    </body>
    </html>
    """

    components.html(html_code, height=550)
    current = st.session_state.card_index + 1
    total = len(data)
    st.progress(current / total)
    if st.button("Next"):
        st.session_state.card_index += 1
    if st.button("Previous"):
        if(st.session_state.card_index==1):
            st.error("First page")
        else:
            st.session_state.card_index -= 1 
if st.button("Clear stored Data"):
        try:
            shutil.rmtree("src/uploads")
            os.remove("cleaned_flashcards.json")

        except :
            st.warning("Data does not exist\n")

