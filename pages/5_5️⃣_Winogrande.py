import streamlit as st
import os
import pandas as pd
import string

def parse_choices(choices):
    uppercases = list(string.ascii_uppercase)
    return [f"{label}: {text}" for label, text in zip(uppercases, choices)]

data_folder = 'data/'

st.set_page_config(page_title="Winogrande", page_icon="5️⃣")

st.title("Winogrande")

gameState = "preStart" if "5_gameState" not in st.session_state else st.session_state["5_gameState"]

# Choose Subset
split = st.sidebar.selectbox("Choose Split", ("Train", "Validation", "Test"), disabled=gameState != "preStart")

# Choose Difficulty
winogrande_subsets = ['winogrande_xs', 'winogrande_s', 'winogrande_m', 'winogrande_l', 'winogrande_xl', 'winogrande_debiased']
subset = st.sidebar.selectbox("Choose Subset", winogrande_subsets, disabled=gameState != "preStart")

data = pd.read_parquet(os.path.join(data_folder, f'Winogrande-{subset}-{split}.parquet')) if '5_data' not in st.session_state else st.session_state['5_data']

total_questions = len(pd.read_parquet(os.path.join(data_folder, f'Winogrande-{subset}-{split}.parquet')))

num_questions = st.sidebar.text_input("Number of Questions (Total Questions: {})".format(total_questions), 10, disabled=gameState != "preStart")
num_questions = int(num_questions) if num_questions.isdigit() else 10


currQuestion = 0 if "5_currQuestion" not in st.session_state else st.session_state["5_currQuestion"]
currScore = 0 if "5_currScore" not in st.session_state else st.session_state["5_currScore"]

st.session_state["5_currScore"] = currScore
st.session_state["5_currQuestion"] = currQuestion
st.session_state["5_gameState"] = gameState

data = data.sample(n=num_questions) if len(data) > num_questions else data
option1 = data["option1"].tolist()
option2 = data["option2"].tolist()
data['choices'] = list(zip(option1, option2))
questions = data["sentence"].tolist() if "5_questions" not in st.session_state else st.session_state["5_questions"]
choices = data["choices"].tolist() if "5_choices" not in st.session_state else st.session_state["5_choices"]
answerKey = data["answer"].tolist() if "5_answerKey" not in st.session_state else st.session_state["5_answerKey"]

uppercases = list(string.ascii_uppercase)
if answerKey[0] in ['1', '2']:
    answerKey = [uppercases[int(label)-1] for label in answerKey]

st.session_state["5_data"] = data
st.session_state["5_questions"] = questions
st.session_state["5_choices"] = choices
st.session_state["5_answerKey"] = answerKey

if gameState == "preStart":
    st.write("You will be presented with 10 randomly questions from the Winogrande dataset.")
    st.write("Your task is to answer the questions correctly.")
    st.write("You will be scored based on your accuracy")
    st.write("Good luck!")
    st.button("Start Game", on_click=lambda: st.session_state.update({"5_gameState": "gameOn"}))

st.session_state["5_isCorrect"] = False if "isCorrect" not in st.session_state else st.session_state["5_isCorrect"]

def onNextClick():
    st.session_state.update({"5_currQuestion": st.session_state["5_currQuestion"] + 1})
    if st.session_state["5_isCorrect"]:
        st.session_state.update({"5_currScore": st.session_state["5_currScore"] + 1})

def restartGame():
    st.session_state = {}

if gameState == "gameOn":
    # show 2 buttons, prev and next
    col1, col2 = st.columns([8, 1])
    if st.session_state["5_currQuestion"] != num_questions-1:
        col2.button("Next", disabled=st.session_state["5_currQuestion"] == num_questions-1, on_click=lambda: onNextClick())
    else:
        col2.button("Finish", on_click=lambda: st.session_state.update({"5_gameState": "gameOver"}))

    question = questions[currQuestion]
    choices = parse_choices(choices[currQuestion])
    correctAnswer = answerKey[currQuestion]

    st.write(f"Question {currQuestion+1}: {question}")
    # create radio buttons
    chosenAnswer = st.radio("Choose Answer", choices)
    st.write(f"Your Answer: {chosenAnswer}")

    st.write(correctAnswer)

    if chosenAnswer[0] == correctAnswer:
        st.session_state["5_isCorrect"] = True
    else:
        st.session_state["5_isCorrect"] = False

if gameState == "gameOver":
    st.write(f"Your score is {currScore}/{num_questions}")
    st.write("Thank you for playing!")
    st.button("Play Again", on_click=lambda: restartGame())




