import streamlit as st
import os
import pandas as pd

def parse_choices(choices):
    labels = choices["label"]
    texts = choices["text"]
    return [f"{label}: {text}" for label, text in zip(labels, texts)]

data_folder = 'data/'

st.set_page_config(page_title="ARC", page_icon="1️⃣")

st.title("AI2 Reasoning Challenge (ARC)")

gameState = "preStart" if "1_gameState" not in st.session_state else st.session_state["1_gameState"]

# Choose Subset
subset = st.sidebar.selectbox("Choose Split", ("Train", "Validation", "Test"), disabled=gameState != "preStart")

# Choose Difficulty
difficulty = st.sidebar.selectbox("Choose Difficulty", ("Easy", "Challenge"), disabled=gameState != "preStart")

data = pd.read_parquet(os.path.join(data_folder, f'ARC-{difficulty}-{subset.lower()}.parquet')) if '1_data' not in st.session_state else st.session_state['1_data']

total_questions = len(pd.read_parquet(os.path.join(data_folder, f'ARC-{difficulty}-{subset.lower()}.parquet')))

num_questions = st.sidebar.text_input("Number of Questions (Total Questions: {})".format(total_questions), 10, disabled=gameState != "preStart")
num_questions = int(num_questions) if num_questions.isdigit() else 10


currQuestion = 0 if "1_currQuestion" not in st.session_state else st.session_state["1_currQuestion"]
currScore = 0 if "1_currScore" not in st.session_state else st.session_state["1_currScore"]

st.session_state["1_currScore"] = currScore
st.session_state["1_currQuestion"] = currQuestion
st.session_state["1_gameState"] = gameState

data = data.sample(n=num_questions) if len(data) > num_questions else data
questions = data["question"].tolist() if "1_questions" not in st.session_state else st.session_state["1_questions"]
choices = data["choices"].tolist() if "1_choices" not in st.session_state else st.session_state["1_choices"]
answerKey = data["answerKey"].tolist() if "1_answerKey" not in st.session_state else st.session_state["1_answerKey"]

st.session_state["1_data"] = data
st.session_state["1_questions"] = questions
st.session_state["1_choices"] = choices
st.session_state["1_answerKey"] = answerKey

if gameState == "preStart":
    st.write("You will be presented with 10 randomly questions from the AI2 Reasoning Challenge (ARC).")
    st.write("Your task is to answer the questions correctly.")
    st.write("You will be scored based on your accuracy")
    st.write("Good luck!")
    st.button("Start Game", on_click=lambda: st.session_state.update({"1_gameState": "gameOn"}))

st.session_state["1_isCorrect"] = False if "isCorrect" not in st.session_state else st.session_state["1_isCorrect"]

def onNextClick():
    st.session_state.update({"1_currQuestion": st.session_state["1_currQuestion"] + 1})
    if st.session_state["1_isCorrect"]:
        st.session_state.update({"1_currScore": st.session_state["1_currScore"] + 1})

def restartGame():
    st.session_state = {}

if gameState == "gameOn":
    # show 2 buttons, prev and next
    col1, col2 = st.columns([8, 1])
    if st.session_state["1_currQuestion"] != num_questions-1:
        col2.button("Next", disabled=st.session_state["1_currQuestion"] == num_questions-1, on_click=lambda: onNextClick())
    else:
        col2.button("Finish", on_click=lambda: st.session_state.update({"1_gameState": "gameOver"}))

    question = questions[currQuestion]
    choices = parse_choices(choices[currQuestion])
    correctAnswer = answerKey[currQuestion]

    st.write(f"Question {currQuestion+1}: {question}")
    # create radio buttons
    chosenAnswer = st.radio("Choose Answer", choices)
    st.write(f"Your Answer: {chosenAnswer}")

    if chosenAnswer[0] == correctAnswer:
        st.session_state["1_isCorrect"] = True
    else:
        st.session_state["1_isCorrect"] = False

if gameState == "gameOver":
    st.write(f"Your score is {currScore}/{num_questions}")
    st.write("Thank you for playing!")
    st.button("Play Again", on_click=lambda: restartGame())




