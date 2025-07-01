import streamlit as st
import os
from streamlit import session_state as ss
import json
import streamlit.components.v1 as components


st.set_page_config(page_title="Flashcard Viewer", layout="wide")

with open("cleaned_flashcards.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if "card_index" not in st.session_state:
    st.session_state.card_index = 0

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

components.html(html_code, height=600)

if st.button("Next"):
    st.session_state.card_index += 1
if st.button("End"):
    os._exit(0)