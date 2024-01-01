import streamlit as st
import os
import pandas as pd
import string

data_folder = 'data/'

st.set_page_config(page_title="GSM8k", page_icon="6️⃣")

st.title("GSM8k")

gameState = "preStart" if "6_gameState" not in st.session_state else st.session_state["6_gameState"]

# Choose Subset
split = st.sidebar.selectbox("Choose Split", ("Train", "Test"), disabled=gameState != "preStart")

# Choose subset
winogrande_subsets = ['main', 'socratic']
subset = st.sidebar.selectbox("Choose Subset", winogrande_subsets, disabled=gameState != "preStart")

data = pd.read_parquet(os.path.join(data_folder, f'gsm8k-{subset}-{split.lower()}.parquet')) if '6_data' not in st.session_state else st.session_state['6_data']
total_questions = len(pd.read_parquet(os.path.join(data_folder, f'gsm8k-{subset}-{split.lower()}.parquet')))

num_questions = st.sidebar.text_input("Number of Questions (Total Questions: {})".format(total_questions), 10, disabled=gameState != "preStart")
num_questions = int(num_questions) if num_questions.isdigit() else 10


currQuestion = 0 if "6_currQuestion" not in st.session_state else st.session_state["6_currQuestion"]
currScore = 0 if "6_currScore" not in st.session_state else st.session_state["6_currScore"]

st.session_state["6_currScore"] = currScore
st.session_state["6_currQuestion"] = currQuestion
st.session_state["6_gameState"] = gameState

data = data.sample(n=num_questions) if len(data) > num_questions else data
answers = data["answer"].tolist()
final_values = [ans.split("#### ")[1] for ans in answers]
data['answer_proc'] = final_values
questions = data["question"].tolist() if "6_questions" not in st.session_state else st.session_state["6_questions"]
answerKey = data["answer_proc"].tolist() if "6_answerKey" not in st.session_state else st.session_state["6_answerKey"]

st.session_state["6_data"] = data
st.session_state["6_questions"] = questions
st.session_state["6_answerKey"] = answerKey

if gameState == "preStart":
    st.write(f"You will be presented with {num_questions} randomly chosen questions from the GSM8k dataset.")
    st.write("Your task is to answer the questions correctly.")
    st.write("You will be scored based on your accuracy")
    st.write("Good luck!")
    st.button("Start Game", on_click=lambda: st.session_state.update({"6_gameState": "gameOn"}))

st.session_state["6_isCorrect"] = False if "isCorrect" not in st.session_state else st.session_state["6_isCorrect"]

def onNextClick():
    st.session_state.update({"6_currQuestion": st.session_state["6_currQuestion"] + 1})
    if st.session_state["6_isCorrect"]:
        st.session_state.update({"6_currScore": st.session_state["6_currScore"] + 1})

def restartGame():
    st.session_state = {}

if gameState == "gameOn":
    # show 2 buttons, prev and next
    col1, col2 = st.columns([8, 1])
    if st.session_state["6_currQuestion"] != num_questions-1:
        col2.button("Next", disabled=st.session_state["6_currQuestion"] == num_questions-1, on_click=lambda: onNextClick())
    else:
        col2.button("Finish", on_click=lambda: st.session_state.update({"6_gameState": "gameOver"}))

    question = questions[currQuestion]
    correctAnswer = answerKey[currQuestion]

    st.write(f"Question {currQuestion+1}: {question}")
    # create radio buttons
    chosenAnswer = st.text_input("Answer", "0")
    st.write(f"Your Answer: {chosenAnswer}")

    st.write(correctAnswer)

    try:
        if float(chosenAnswer) == float(correctAnswer):
            st.session_state["6_isCorrect"] = True
        else:
            st.session_state["6_isCorrect"] = False
    except:
        st.error("Please enter a number")
        st.session_state["6_isCorrect"] = False

if gameState == "gameOver":
    st.write(f"Your score is {currScore}/{num_questions}")
    st.write("Thank you for playing!")
    st.button("Play Again", on_click=lambda: restartGame())




