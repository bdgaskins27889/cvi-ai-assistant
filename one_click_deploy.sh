#!/bin/bash

# --- CVI AI Assistant: One-Click Kaggle Deployment ---

echo "===================================================="
echo "   CVI AI Assistant: One-Click Kaggle Deployment   "
echo "===================================================="

# 1. Check for Kaggle Credentials
if [ ! -f ~/.kaggle/kaggle.json ] && [ -z "$KAGGLE_USERNAME" ]; then
    echo "Error: Kaggle credentials not found!"
    echo "Please place your kaggle.json in ~/.kaggle/ or set KAGGLE_USERNAME and KAGGLE_API_TOKEN."
    exit 1
fi

# 2. Install Dependencies
echo -e "\n[1/4] Installing required Python packages..."
pip install -q kaggle kaggle-benchmarks pandas openai evaluate transformers

# 3. Initialize Kaggle Environment
echo -e "\n[2/4] Initializing Kaggle Benchmarks..."
kaggle b init -y

# 4. Push Task to Kaggle
echo -e "\n[3/4] Deploying Benchmark Task to Kaggle..."
# Using a timestamped name to ensure uniqueness
TASK_NAME="cvi-benchmark-$(date +%s)"
kaggle b t push -f cvi_benchmark.py --include cvi_fine_tuning_data.jsonl "$TASK_NAME"

# 5. Start Initial Evaluation
echo -e "\n[4/4] Starting initial evaluation (gpt-4o-mini)..."
kaggle b t run --llm gpt-4o-mini "$TASK_NAME"

echo -e "\n===================================================="
echo "              DEPLOYMENT SUCCESSFUL!                "
echo "===================================================="
echo "Task Name: $TASK_NAME"
echo -e "\nTo check your results later, run:"
echo "kaggle b r list"
echo "===================================================="
