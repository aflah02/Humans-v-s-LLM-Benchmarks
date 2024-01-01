# [LLM Benchmark Quiz Game](https://play-with-llm-benchmarks.streamlit.app/)

LLM Benchmarks play a crucial role in assessing the performance of Language Model Models (LLMs). However, it is essential to recognize that these benchmarks have their own limitations. This interactive tool is designed to engage users in a quiz game based on popular LLM benchmarks, offering an insightful way to explore and understand the constraints of these benchmarks during gameplay.

## Purpose

The primary goal of this tool is to provide a hands-on experience that allows users to not only test their knowledge but also gain a deeper understanding of the challenges and limitations associated with LLM benchmarks. By participating in the quiz game, users can appreciate the nuances involved in evaluating LLMs and how well these models perform on diverse tasks.

## Featured Benchmarks

The chosen benchmarks are the ones prominently used for evaluating LLMs on the [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard). Here's a brief overview of the benchmarks included:

1. **[ARC](https://arxiv.org/abs/1803.05457):** A set of grade-school science questions.
2. **[HellaSwag](https://arxiv.org/abs/1905.07830):** A test of commonsense inference, challenging for state-of-the-art models despite being easy for humans (~95% accuracy).
3. **[MMLU](https://arxiv.org/abs/2009.03300):** A multitask accuracy test covering 57 diverse tasks, including mathematics, US history, computer science, law, and more.
4. **[TruthfulQA](https://arxiv.org/abs/2109.07958):** A test to measure a model's tendency to reproduce falsehoods commonly found online.
5. **[WinoGrande](https://arxiv.org/abs/1907.10641):** An adversarial Winograd benchmark at scale, focusing on commonsense reasoning.
6. **[GSM8k](https://arxiv.org/abs/2110.14168):** Diverse grade school math word problems to assess a model's ability to solve multi-step mathematical reasoning problems.

## How to Use

### Hosted Preview - 

Simply go to https://play-with-llm-benchmarks.streamlit.app/ and get the full experience

### Local Development - 
Simply clone the repo and run `streamlit run Main.py` and enjoy the quiz game based on the selected benchmarks. Answer questions related from these benchmarks and measure your own performance.

Feel free to contribute, report issues, or suggest improvements to enhance the overall experience. Happy quizzing!