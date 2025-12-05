import streamlit as st
import os
from streamlit import session_state
import json
import sys
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from run import main

st.set_page_config(page_title="Flashcard Generator and Viewer", layout="wide")
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

start = int(st.number_input("Enter start page", min_value=1, value=1))
end = int(st.number_input("Enter end page", min_value=1, value=1))
batch_size = int(st.number_input("Enter batch size", min_value=1))
st.session_state.batch_size = batch_size
if st.button("Generate"):
    if os.path.exists(SAVE_DIR) and has_pdf(SAVE_DIR):
        uploaded_pdf = st.session_state.get("uploaded_pdf", None)
        if uploaded_pdf:
            st.success("Executing module... This may take a while...")
            main(uploaded_pdf, start, end,st.session_state.get("batch_size"))
            st.rerun()
        else:
            st.error("No uploaded PDF filename found in session state. If you want a new set of questions, add the PDF again.")
    else:
        st.error("PDF not uploaded")

if st.button("End"):
    os._exit(0)

if st.button("Clear stored Data"):
    try:
        shutil.rmtree("src/uploads")
        shutil.rmtree("./train_ocr")
        os.remove("cleaned_flashcards.json")
        st.success("Data cleared")
        st.rerun()
    except:
        st.warning("Data does not exist")
        st.rerun()

if os.path.exists("./train_ocr") and os.path.isfile("cleaned_flashcards.json"):
    with open("cleaned_flashcards.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if "card_index" not in st.session_state:
        st.session_state.card_index = 1
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    i = st.session_state.card_index
    if i >= len(data):
        st.success("You've reached the end of the flashcards!")
        st.stop()

    question = data[i]["front"]
    answer = data[i]["back"]

    st.write(f"**Card {i} of {len(data)-1}**")

    if not st.session_state.show_answer:
        st.info(question)
        if st.button("Show Answer"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.success(answer)
        if st.button("Hide Answer"):
            st.session_state.show_answer = False
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            if st.session_state.card_index == 1:
                st.error("First page")
            else:
                st.session_state.card_index -= 1
                st.session_state.show_answer = False
                st.rerun()
    with col2:
        if st.button("Next"):
            if st.session_state.card_index < len(data) - 1:
                st.session_state.card_index += 1
                st.session_state.show_answer = False
                st.rerun()


