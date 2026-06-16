# Kaggle CLI Commands for CVI AI Assistant Benchmark Deployment

Follow these steps to deploy and manage your CVI AI Assistant benchmark on Kaggle. Ensure you have the Kaggle CLI installed and authenticated with your API token.

## 1. Authentication and Initialization

First, set your Kaggle credentials as environment variables and initialize the local development environment.

```bash
# Set your Kaggle username and API token (if not already set in ~/.kaggle/kaggle.json)
export KAGGLE_USERNAME="your_username"
export KAGGLE_API_TOKEN="your_api_token"

# Initialize the Kaggle Benchmarks local development environment
# This will create a .env file with model proxy credentials
kaggle b init -y
```

## 2. Pushing the Benchmark Task

Push your `cvi_benchmark.py` script and the associated dataset to Kaggle as a new benchmark task.

```bash
# Push the benchmark task to Kaggle
# Replace 'your_task_name' with a unique name for your task (e.g., 'cvi-ai-assistant-benchmark')
kaggle b t push -f cvi_benchmark.py --include cvi_fine_tuning_data.jsonl your_task_name
```

## 3. Running Evaluations

Once the task is pushed, you can run evaluations against different LLMs.

```bash
# Run evaluation for a specific model (e.g., gpt-4o-mini)
kaggle b t run --llm gpt-4o-mini your_task_name

# Run evaluation for another model (e.g., gemini-1.5-flash)
kaggle b t run --llm gemini-1.5-flash your_task_name
```

## 4. Monitoring and Downloading Results

You can check the status of your runs and download the results once they are complete.

```bash
# List all your benchmark runs and their status
kaggle b r list

# Download the results for a specific run
# Replace 'your_run_id' with the actual ID from the list command
kaggle b r download your_run_id
```

## 5. Local Testing (Optional)

You can always test your benchmark logic locally before pushing to Kaggle.

```bash
# Run the benchmark script locally
# This will use the mock LLM if no OPENAI_API_KEY is set
python3 cvi_benchmark.py
```

## Summary Table of Key Commands

| Action                 | Command                                                                 |
| :--------------------- | :---------------------------------------------------------------------- |
| **Initialize**         | `kaggle b init -y`                                                      |
| **Push Task**          | `kaggle b t push -f cvi_benchmark.py --include dataset.jsonl task_name` |
| **Run Evaluation**     | `kaggle b t run --llm model_name task_name`                             |
| **List Runs**          | `kaggle b r list`                                                       |
| **Download Results**   | `kaggle b r download run_id`                                            |

By following these commands, you can effectively manage the lifecycle of your CVI AI Assistant benchmark on Kaggle, from initial deployment to comprehensive evaluation and result analysis.
