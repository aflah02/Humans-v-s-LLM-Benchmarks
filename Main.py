import streamlit as st
import os
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Main",
    page_icon="🎯",
)

st.title("Humans v/s LLM Benchmarks")

st.write("LLM Benchmarks are increasingly being used to evaluate the performance of LLMs. However, the benchmarks are not perfect and have their own limitations.")
st.write("This tool allows you to play a quiz game on some popular LLM benchmarks and investigate the limitations of the benchmarks while playing the game.")
st.write("The chosen benchmarks are the ones used to evaluate LLMs on the [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)")
st.write("The benchmarks (as described in the leaderboard) are:")
st.write("1. [ARC](https://arxiv.org/abs/1803.05457) - a set of grade-school science questions.")
st.write("2. [HellaSwag](https://arxiv.org/abs/1905.07830) - a test of commonsense inference, which is easy for humans (~95%) but challenging for SOTA models.")
st.write("3. [MMLU](https://arxiv.org/abs/2009.03300) - a test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more.")
st.write("4. [TruthfulQA](https://arxiv.org/abs/2109.07958) - a test to measure a model's propensity to reproduce falsehoods commonly found online.")
st.write("5. [WinoGrande](https://arxiv.org/abs/1907.10641) - an adversarial and difficult Winograd benchmark at scale, for commonsense reasoning.")
st.write("6. [GSM8k](https://arxiv.org/abs/2110.14168) - diverse grade school math word problems to measure a model's ability to solve multi-step mathematical reasoning problems.")
