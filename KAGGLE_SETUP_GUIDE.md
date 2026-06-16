# Step-by-Step Guide: Setting Up CVI AI Assistant on Kaggle Benchmarks

This guide provides a comprehensive walkthrough for setting up, deploying, and evaluating the CVI AI Assistant benchmark on the Kaggle Benchmarks platform.

---

## Prerequisites

1.  **Kaggle Account**: Ensure you have an active account on [Kaggle](https://www.kaggle.com).
2.  **Kaggle API Token**: 
    *   Go to your [Kaggle Account Settings](https://www.kaggle.com/settings/account).
    *   Scroll down to the **API** section and click **Create New API Token**.
    *   This will download a `kaggle.json` file containing your `username` and `key`.
3.  **Python Installed**: Ensure Python 3.10+ is installed on your local machine.

---

## Step 1: Install the Kaggle CLI

Open your terminal or command prompt and install the Kaggle Python package, which includes the necessary CLI tools.

```bash
pip install kaggle
```

---

## Step 2: Configure Authentication

You need to let the Kaggle CLI know who you are. You can do this by placing the `kaggle.json` file in the correct directory or by setting environment variables.

### Option A: Using `kaggle.json` (Recommended)
*   **Windows**: Place `kaggle.json` in `C:\Users\<Windows-username>\.kaggle\`
*   **Mac/Linux**: Place `kaggle.json` in `~/.kaggle/` and ensure it has restricted permissions:
    ```bash
    mkdir -p ~/.kaggle
    cp /path/to/your/kaggle.json ~/.kaggle/
    chmod 600 ~/.kaggle/kaggle.json
    ```

### Option B: Using Environment Variables
```bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_API_TOKEN="your_api_token_key"
```

---

## Step 3: Initialize the Benchmarks Environment

Navigate to your project directory (`cvi-ai-assistant`) and initialize the Kaggle Benchmarks environment. This setup allows you to test your benchmark locally using Kaggle's model proxy.

```bash
cd path/to/cvi-ai-assistant
kaggle b init -y
```

---

## Step 4: Prepare Your Benchmark Files

Ensure the following files are in your project directory:
1.  `cvi_benchmark.py`: The script containing the benchmark logic and scoring metrics.
2.  `cvi_fine_tuning_data.jsonl`: The dataset of CVI scenarios used for evaluation.

---

## Step 5: Deploy the Benchmark Task to Kaggle

Push your local benchmark script and dataset to the Kaggle platform. This creates a "Task" that others can see or that you can run evaluations against.

```bash
# Replace 'cvi-ai-benchmark' with your desired unique task name
kaggle b t push -f cvi_benchmark.py --include cvi_fine_tuning_data.jsonl cvi-ai-benchmark
```

---

## Step 6: Run an Evaluation

Now that the task is on Kaggle, you can evaluate how different AI models perform on your CVI scenarios.

```bash
# Run the benchmark against the gpt-4o-mini model
kaggle b t run --llm gpt-4o-mini cvi-ai-benchmark
```

---

## Step 7: Monitor Progress and View Results

You can track the status of your evaluation runs directly from the terminal.

### List Your Runs
```bash
kaggle b r list
```

### Download and Inspect Results
Once a run's status is `Succeeded`, download the results to see the scores (Ethical Filter, LLM-as-a-Judge, BLEU/ROUGE).

```bash
# Replace <RUN_ID> with the actual ID from the 'list' command
kaggle b r download <RUN_ID>
```

The results will be saved as a `.run.json` file, providing a detailed breakdown of the model's performance on each scenario.

---

## Troubleshooting

*   **Authentication Errors**: Double-check your `KAGGLE_USERNAME` and `KAGGLE_API_TOKEN`. Ensure `kaggle.json` has the correct permissions (`chmod 600`).
*   **Missing Dependencies**: If you run the script locally, ensure you've installed the required Python libraries:
    ```bash
    pip install kaggle-benchmarks pandas openai evaluate transformers
    ```
*   **Task Name Conflicts**: If the task name is already taken on Kaggle, try a more unique name (e.g., `cvi-ai-assistant-benchmark-2024`).

---

By following these steps, you have successfully integrated the CVI AI Assistant into the Kaggle Benchmarks ecosystem, fulfilling the requirements for the grant application and providing a standardized way to evaluate AI in the field of community violence intervention.
