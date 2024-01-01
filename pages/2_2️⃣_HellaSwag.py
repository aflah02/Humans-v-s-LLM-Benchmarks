import streamlit as st
import os
import pandas as pd
import string

def parse_choices(choices):
    uppercases = list(string.ascii_uppercase)
    return [f"{label}: {text}" for label, text in zip(uppercases, choices)]

data_folder = 'data/'

st.set_page_config(page_title="HellaSwag", page_icon="2️⃣")

st.title("HellaSwag")

gameState = "preStart" if "2_gameState" not in st.session_state else st.session_state["2_gameState"]

# Choose Subset
subset = st.sidebar.selectbox("Choose Split", ("Train", "Validation", "Test"), disabled=gameState != "preStart")

data = pd.read_parquet(os.path.join(data_folder, f'hellaswag-{subset.lower()}.parquet')) if '2_data' not in st.session_state else st.session_state['2_data']

total_questions = len(pd.read_parquet(os.path.join(data_folder, f'hellaswag-{subset.lower()}.parquet')))

num_questions = st.sidebar.text_input("Number of Questions (Total Questions: {})".format(total_questions), 10, disabled=gameState != "preStart")
num_questions = int(num_questions) if num_questions.isdigit() else 10


currQuestion = 0 if "2_currQuestion" not in st.session_state else st.session_state["2_currQuestion"]
currScore = 0 if "2_currScore" not in st.session_state else st.session_state["2_currScore"]

st.session_state["2_currScore"] = currScore
st.session_state["2_currQuestion"] = currQuestion
st.session_state["2_gameState"] = gameState

data = data.sample(n=num_questions) if len(data) > num_questions else data
ctxs = data["ctx"].tolist() if "2_ctxs" not in st.session_state else st.session_state["2_ctxs"]
endings = data["endings"].tolist() if "2_endings" not in st.session_state else st.session_state["2_endings"]
labels = data["label"].tolist() if "2_labels" not in st.session_state else st.session_state["2_labels"]

uppercases = list(string.ascii_uppercase)
labels = [uppercases[label] for label in labels]

st.session_state["2_data"] = data
st.session_state["2_ctxs"] = ctxs
st.session_state["2_endings"] = endings

if gameState == "preStart":
    st.write("You will be presented with 10 randomly questions from the Hellaswag dataset.")
    st.write("Your task is to answer the questions correctly.")
    st.write("You will be scored based on your accuracy")
    st.write("Good luck!")
    st.button("Start Game", on_click=lambda: st.session_state.update({"2_gameState": "gameOn"}))

st.session_state["2_isCorrect"] = False if "2_isCorrect" not in st.session_state else st.session_state["2_isCorrect"]

def onNextClick():
    st.session_state.update({"2_currQuestion": st.session_state["2_currQuestion"] + 1})
    if st.session_state["2_isCorrect"]:
        st.session_state.update({"2_currScore": st.session_state["2_currScore"] + 1})

def restartGame():
    st.session_state = {}

if gameState == "gameOn":
    # show 2 buttons, prev and next
    col1, col2 = st.columns([8, 1])
    if st.session_state["2_currQuestion"] != num_questions-1:
        col2.button("Next", disabled=st.session_state["2_currQuestion"] == num_questions-1, on_click=lambda: onNextClick())
    else:
        col2.button("Finish", on_click=lambda: st.session_state.update({"2_gameState": "gameOver"}))

    question = ctxs[currQuestion]
    choices = parse_choices(endings[currQuestion])
    correctAnswer = labels[currQuestion]

    st.write(f"Question {currQuestion+1}: {question}")
    # create radio buttons
    chosenAnswer = st.radio("Choose Answer", choices)
    st.write(f"Your Answer: {chosenAnswer}")

    if chosenAnswer[0] == correctAnswer:
        st.session_state["2_isCorrect"] = True
    else:
        st.session_state["2_isCorrect"] = False

if gameState == "gameOver":
    st.write(f"Your score is {currScore}/{num_questions}")
    st.write("Thank you for playing!")
    st.button("Play Again", on_click=lambda: restartGame())




