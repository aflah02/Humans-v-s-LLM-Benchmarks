import streamlit as st
import os
import pandas as pd
import string

def parse_choices(choices):
    uppercases = list(string.ascii_uppercase)
    return [f"{label}: {text}" for label, text in zip(uppercases, choices)]

data_folder = 'data/'

st.set_page_config(page_title="MMLU", page_icon="3️⃣")

st.title("Massive Multitask Language Understanding (MMLU)")

gameState = "preStart" if "3_gameState" not in st.session_state else st.session_state["3_gameState"]

mmlu_subsets = ['high_school_european_history', 'business_ethics', 'clinical_knowledge', 'medical_genetics', 'high_school_us_history', 'high_school_physics', 
                'high_school_world_history', 'virology', 'high_school_microeconomics', 'econometrics', 'college_computer_science', 'high_school_biology', 
                'abstract_algebra', 'professional_accounting', 'philosophy', 'professional_medicine', 'nutrition', 'global_facts', 'machine_learning', 
                'security_studies', 'public_relations', 'professional_psychology', 'prehistory', 'anatomy', 'human_sexuality', 'college_medicine', 
                'high_school_government_and_politics', 'college_chemistry', 'logical_fallacies', 'high_school_geography', 'elementary_mathematics', 'human_aging', 
                'college_mathematics', 'high_school_psychology', 'formal_logic', 'high_school_statistics', 'international_law', 'high_school_mathematics', 
                'high_school_computer_science', 'conceptual_physics', 'miscellaneous', 'high_school_chemistry', 'marketing', 'professional_law', 'management', 
                'college_physics', 'jurisprudence', 'world_religions', 'sociology', 'us_foreign_policy', 'high_school_macroeconomics', 'computer_security', 
                'moral_scenarios', 'moral_disputes', 'electrical_engineering', 'astronomy', 'college_biology']
# Choose Subset
subset = st.sidebar.selectbox("Choose Split", ("Train", "Validation", "Test"), disabled=gameState != "preStart")

# Choose Difficulty
subject = st.sidebar.selectbox("Choose Subject", mmlu_subsets, disabled=gameState != "preStart")

data = pd.read_parquet(os.path.join(data_folder, f'MMLU-{subject}-{subset.lower()}.parquet'))

total_questions = len(pd.read_parquet(os.path.join(data_folder, f'MMLU-{subject}-{subset.lower()}.parquet')))

num_questions = st.sidebar.text_input("Number of Questions (Total Questions: {})".format(total_questions), min(10, total_questions), disabled=gameState != "preStart")
num_questions = int(num_questions) if num_questions.isdigit() else min(10, total_questions)


currQuestion = 0 if "3_currQuestion" not in st.session_state else st.session_state["3_currQuestion"]
currScore = 0 if "3_currScore" not in st.session_state else st.session_state["3_currScore"]

st.session_state["3_currScore"] = currScore
st.session_state["3_currQuestion"] = currQuestion
st.session_state["3_gameState"] = gameState

data = data.sample(n=num_questions) if len(data) > num_questions else data
# create new column mering columns A,B,C and D as list
data['choices'] = data[['A', 'B', 'C', 'D']].values.tolist()
questions = data["input"].tolist() if "3_questions" not in st.session_state else st.session_state["3_questions"]
choices = data["choices"].tolist() if "3_choices" not in st.session_state else st.session_state["3_choices"]
answerKey = data["target"].tolist() if "3_answerKey" not in st.session_state else st.session_state["3_answerKey"]

st.session_state["3_data"] = data
st.session_state["3_questions"] = questions
st.session_state["3_choices"] = choices
st.session_state["3_answerKey"] = answerKey

if gameState == "preStart":
    st.write(f"You will be presented with {num_questions} randomly chosen questions from the MMLU dataset.")
    st.write("Your task is to answer the questions correctly.")
    st.write("You will be scored based on your accuracy")
    st.write("Good luck!")
    st.button("Start Game", on_click=lambda: st.session_state.update({"3_gameState": "gameOn"}))

st.session_state["3_isCorrect"] = False if "3_isCorrect" not in st.session_state else st.session_state["3_isCorrect"]

def onNextClick():
    st.session_state.update({"3_currQuestion": st.session_state["3_currQuestion"] + 1})
    if st.session_state["3_isCorrect"]:
        st.session_state.update({"3_currScore": st.session_state["3_currScore"] + 1})

def restartGame():
    st.session_state = {}

if gameState == "gameOn":
    # show 2 buttons, prev and next
    col1, col2 = st.columns([8, 1])
    if st.session_state["3_currQuestion"] != num_questions-1:
        col2.button("Next", disabled=st.session_state["3_currQuestion"] == num_questions-1, on_click=lambda: onNextClick())
    else:
        col2.button("Finish", on_click=lambda: st.session_state.update({"3_gameState": "gameOver"}))

    question = questions[currQuestion]
    choices = parse_choices(choices[currQuestion])
    correctAnswer = answerKey[currQuestion]

    st.write(f"Question {currQuestion+1}: {question}")
    # create radio buttons
    chosenAnswer = st.radio("Choose Answer", choices)
    st.write(f"Your Answer: {chosenAnswer}")

    if chosenAnswer[0] == correctAnswer:
        st.session_state["3_isCorrect"] = True
    else:
        st.session_state["3_isCorrect"] = False

if gameState == "gameOver":
    st.write(f"Your score is {currScore}/{num_questions}")
    st.write("Thank you for playing!")
    st.button("Play Again", on_click=lambda: restartGame())