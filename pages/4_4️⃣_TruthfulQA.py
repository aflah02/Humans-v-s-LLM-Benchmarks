import streamlit as st
import os
import pandas as pd
import string

def parse_choices(choices):
    uppercases = list(string.ascii_uppercase)
    return [f"{label}: {text}" for label, text in zip(uppercases, choices)]

data_folder = 'data/'

st.set_page_config(page_title="TruthfulQA", page_icon="4️⃣")

st.title("TruthfulQA")

gameState = "preStart" if "4_gameState" not in st.session_state else st.session_state["4_gameState"]

# Choose Subset
subset = st.sidebar.selectbox("Choose Split", ["Validation"], disabled=gameState != "preStart")

data = pd.read_parquet(os.path.join(data_folder, f'truthful_qa_mc-{subset.lower()}.parquet')) if '4_data' not in st.session_state else st.session_state['4_data']

total_questions = len(pd.read_parquet(os.path.join(data_folder, f'truthful_qa_mc-{subset.lower()}.parquet')))

num_questions = st.sidebar.text_input("Number of Questions (Total Questions: {})".format(total_questions), 10, disabled=gameState != "preStart")
num_questions = int(num_questions) if num_questions.isdigit() else 10


currQuestion = 0 if "4_currQuestion" not in st.session_state else st.session_state["4_currQuestion"]
currScore = 0 if "4_currScore" not in st.session_state else st.session_state["4_currScore"]

st.session_state["4_currScore"] = currScore
st.session_state["4_currQuestion"] = currQuestion
st.session_state["4_gameState"] = gameState

data = data.sample(n=num_questions) if len(data) > num_questions else data
questions = data["question"].tolist() if "4_questions" not in st.session_state else st.session_state["4_questions"]
choices = data["choices"].tolist() if "4_choices" not in st.session_state else st.session_state["4_choices"]
answerKey = data["label"].tolist() if "4_answerKey" not in st.session_state else st.session_state["4_answerKey"]

if type(answerKey[0]) == int:
    uppercases = list(string.ascii_uppercase)
    answerKey = [uppercases[label] for label in answerKey]

st.session_state["4_data"] = data
st.session_state["4_questions"] = questions
st.session_state["4_choices"] = choices
st.session_state["4_answerKey"] = answerKey

if gameState == "preStart":
    st.write(f"You will be presented with {num_questions} randomly chosen questions from the TruthfulQA dataset.")
    st.write("Your task is to answer the questions correctly.")
    st.write("You will be scored based on your accuracy")
    st.write("Good luck!")
    st.button("Start Game", on_click=lambda: st.session_state.update({"4_gameState": "gameOn"}))

st.session_state["4_isCorrect"] = False if "isCorrect" not in st.session_state else st.session_state["4_isCorrect"]

def onNextClick():
    st.session_state.update({"4_currQuestion": st.session_state["4_currQuestion"] + 1})
    if st.session_state["4_isCorrect"]:
        st.session_state.update({"4_currScore": st.session_state["4_currScore"] + 1})

def restartGame():
    st.session_state = {}

if gameState == "gameOn":
    # show 2 buttons, prev and next
    col1, col2 = st.columns([8, 1])
    if st.session_state["4_currQuestion"] != num_questions-1:
        col2.button("Next", disabled=st.session_state["4_currQuestion"] == num_questions-1, on_click=lambda: onNextClick())
    else:
        col2.button("Finish", on_click=lambda: st.session_state.update({"4_gameState": "gameOver"}))

    question = questions[currQuestion]
    choices = parse_choices(choices[currQuestion])
    correctAnswer = answerKey[currQuestion]

    st.write(f"Question {currQuestion+1}: {question}")
    # create radio buttons
    chosenAnswer = st.radio("Choose Answer", choices)
    st.write(f"Your Answer: {chosenAnswer}")

    if chosenAnswer[0] == correctAnswer:
        st.session_state["4_isCorrect"] = True
    else:
        st.session_state["4_isCorrect"] = False

if gameState == "gameOver":
    st.write(f"Your score is {currScore}/{num_questions}")
    st.write("Thank you for playing!")
    st.button("Play Again", on_click=lambda: restartGame())




