import subprocess
import os
import sys

def run_command(command, description):
    """Executes a shell command and prints the output."""
    print(f"\n--- {description} ---")
    print(f"Executing: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}:")
        print(e.stderr)
        return False

def main():
    # --- Configuration ---
    # Change these values as needed
    TASK_NAME = "cvi-ai-assistant-benchmark"
    BENCHMARK_SCRIPT = "cvi_benchmark.py"
    DATASET_FILE = "cvi_fine_tuning_data.jsonl"
    EVAL_MODEL = "gpt-4o-mini"

    # --- Step 1: Validation ---
    print("Starting CVI AI Assistant Kaggle Deployment Automation...")

    # Check for required files
    if not os.path.exists(BENCHMARK_SCRIPT) or not os.path.exists(DATASET_FILE):
        print(f"Error: Required files ({BENCHMARK_SCRIPT} or {DATASET_FILE}) not found in the current directory.")
        sys.exit(1)

    # Check for Kaggle credentials
    if not os.path.exists(os.path.expanduser("~/.kaggle/kaggle.json")) and not (os.getenv("KAGGLE_USERNAME") and os.getenv("KAGGLE_API_TOKEN")):
        print("Error: Kaggle credentials not found. Please set up ~/.kaggle/kaggle.json or KAGGLE_USERNAME/KAGGLE_API_TOKEN environment variables.")
        sys.exit(1)

    # --- Step 2: Initialize Kaggle Benchmarks ---
    if not run_command(["kaggle", "b", "init", "-y"], "Initializing Kaggle Benchmarks Environment"):
        sys.exit(1)

    # --- Step 3: Push Task to Kaggle ---
    push_command = [
        "kaggle", "b", "t", "push",
        "-f", BENCHMARK_SCRIPT,
        "--include", DATASET_FILE,
        TASK_NAME
    ]
    if not run_command(push_command, f"Pushing Task '{TASK_NAME}' to Kaggle"):
        sys.exit(1)

    # --- Step 4: Run Initial Evaluation ---
    eval_command = [
        "kaggle", "b", "t", "run",
        "--llm", EVAL_MODEL,
        TASK_NAME
    ]
    if not run_command(eval_command, f"Running Initial Evaluation with {EVAL_MODEL}"):
        print("\nWarning: Initial evaluation run failed. You can try running it manually later.")
    else:
        print("\nInitial evaluation run successfully initiated.")

    # --- Step 5: Final Status ---
    print("\n--- Deployment Summary ---")
    print(f"Task Name: {TASK_NAME}")
    print(f"Benchmark Script: {BENCHMARK_SCRIPT}")
    print(f"Dataset: {DATASET_FILE}")
    print("\nNext Steps:")
    print("1. Monitor your runs: kaggle b r list")
    print("2. Download results: kaggle b r download <RUN_ID>")
    print("\nDeployment automation complete!")

if __name__ == "__main__":
    main()
