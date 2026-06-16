# CVI AI Assistant: Kaggle Benchmarks Grant Application Response

> **"Knowledge without experience can miss the moment. Experience without structure can miss the pattern. This CVI AI Assistant brings both together."**

This document outlines the implementation of the CVI AI Assistant benchmark in compliance with the Kaggle Benchmarks Grant application requirements. It details the problem statement, success benchmarks, impact, data usage, scoring methodology, and estimated quota requirements.

## Problem Statement

> Please provide clearly scoped definition of the intelligence you are trying to measure.

The intelligence being measured is the ability of Large Language Models (LLMs) to provide contextually appropriate, trauma-informed, and non-punitive decision support for Community Violence Intervention (CVI) practitioners. Specifically, we are measuring the model's proficiency in de-escalation guidance, scenario-based coaching, trauma-informed reframing, documentation assistance, and reflective post-intervention analysis within high-stress, trust-based community environments.

## Success Benchmark Objectives

> Please briefly describe the overall objective of your benchmark. What does success look like in your field?

The objective is to establish a benchmark for evaluating AI models on their adherence to CVI ethical frameworks and trauma-informed care standards. Success in this field looks like a model that consistently prioritizes safety and trust-building, avoids recommending punitive or enforcement-based actions, uses culturally competent language, and provides actionable, evidence-based guidance that augments the expertise of violence interrupters and credible messengers.

## Impact of the Benchmark

> What impact would this benchmark have on your industry or field?

This benchmark would introduce a standard for the ethical and effective use of generative AI in community-based violence intervention. It would help organizations identify models that are genuinely supportive of social-emotional learning and the core role of providing unbiased advice in high-stakes situations. Ultimately, it legitimizes AI as a support tool for the CVI workforce, potentially increasing program efficiency and reducing practitioner burnout.

## Data Usage and Total Data Size

> Please briefly describe the data you plan to use for the benchmark. How much data is available and what is the total data size?

The data consists of a curated dataset of high-quality, anonymized CVI intervention scenarios, de-escalation techniques, and documentation templates. This includes: 1) Anonymized CVI case narratives and role-play scenarios. 2) Trauma-informed communication standards and manuals. 3) Evidence-based violence prevention frameworks (e.g., Cure Violence, CVI). The current dataset is in `.JSONL` format, designed to be expandable through community contribution and practitioner feedback.

Our fine-tuning dataset, `cvi_fine_tuning_data.jsonl`, currently contains **56 high-quality examples**. Each example is a JSON object representing a conversation turn, suitable for fine-tuning and evaluation.

## Scoring Methodology

We propose a hybrid scoring metric to evaluate the CVI AI Assistant, combining automated and LLM-based assessments:

1.  **Safety/Ethical Filter (Pass/Fail)**: An automated check to ensure the model's response does not recommend punitive or enforcement-based actions. This is a binary pass/fail metric.
2.  **LLM-as-a-Judge (1-5 scale)**: An LLM (e.g., `gpt-4o-mini` or `google/gemini-3-flash-preview`) will evaluate the model's response for trauma-informedness, cultural competence, and non-punitive stance. A score of 1-5 will be assigned, with higher scores indicating better performance. We will assert that the score must be at least 3 for a successful response.
3.  **BLEU/ROUGE Scores**: These metrics will measure the n-gram overlap and recall between the model's response and a human-generated reference response. While primarily useful for documentation tasks or assessing fluency/similarity, they provide an additional quantitative measure.

## Kaggle Benchmarks Implementation

The benchmark is implemented using the Kaggle Benchmarks SDK in `cvi_benchmark.py`. This script:

*   Loads the `cvi_fine_tuning_data.jsonl` dataset.
*   Defines a `@kbench.task` that takes an LLM and an example as input.
*   Generates a response from the LLM under test for each example.
*   Applies the ethical filter.
*   Invokes an LLM-as-a-Judge to score the response.
*   Calculates BLEU and ROUGE scores against a reference response.
*   Uses `kbench.assertions` to enforce minimum performance standards (e.g., ethical filter pass, judge score >= 3).

## Quota Requirements

We estimate the following quota requirements for running the CVI AI Assistant benchmark on Kaggle, assuming an initial evaluation set of 5 models and 2 runs per day:

| Metric             | Value     |
| :----------------- | :-------- |
| Number of Examples | 56        |
| Number of Models   | 5         |
| Tokens per Run     | 392,000   |
| Daily Tokens       | 784,000   |
| Monthly Tokens     | 23,520,000|
| Daily Inferences   | 1,120     |
| Monthly Inferences | 33,600    |

These estimates are based on the following token counts per example:

*   **Prompt Tokens**: 250
*   **Response Tokens**: 350
*   **Judge Prompt Tokens**: 700
*   **Judge Response Tokens**: 100

## Conclusion

The CVI AI Assistant benchmark is designed to rigorously evaluate LLMs for their suitability in sensitive CVI contexts, ensuring ethical, trauma-informed, and culturally competent support. The implementation on Kaggle Benchmarks, coupled with a robust scoring methodology and clear quota estimates, positions this project for significant impact in the field of community violence intervention. We are ready to deploy this benchmark and contribute to the development of responsible AI for social good.
