"""
Fine-Tuning Script for CVI AI Assistant
========================================
DSC 670 - Advanced Uses of Generative AI
Barbara D. Gaskins | Bellevue University

This script demonstrates the fine-tuning process for the Community Violence
Intervention (CVI) AI Assistant using OpenAI's fine-tuning API.

The model is fine-tuned on curated, anonymized CVI training data including:
- De-escalation guidance scenarios
- Scenario-based coaching examples
- Trauma-informed response framing
- Documentation assistance templates
- Reflective post-intervention analysis

Usage:
    python fine_tune_model.py

Requirements:
    pip install openai
"""

import os
import json
import time
from openai import OpenAI

# ============================================================================
# Configuration
# ============================================================================

TRAINING_FILE = "cvi_fine_tuning_data.jsonl"
BASE_MODEL = "gpt-4.1-mini"
FINE_TUNED_SUFFIX = "cvi-assistant"
N_EPOCHS = 3

# ============================================================================
# Initialize OpenAI Client
# ============================================================================

client = OpenAI()


def validate_training_data(filepath: str) -> bool:
    """Validate the JSONL training data format before uploading."""
    print(f"Validating training data: {filepath}")
    
    with open(filepath, "r") as f:
        lines = f.readlines()
    
    print(f"  Total training examples: {len(lines)}")
    
    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            assert "messages" in data, f"Line {i+1}: Missing 'messages' key"
            messages = data["messages"]
            assert len(messages) >= 2, f"Line {i+1}: Need at least 2 messages"
            
            roles = [m["role"] for m in messages]
            assert "system" in roles, f"Line {i+1}: Missing system message"
            assert "user" in roles, f"Line {i+1}: Missing user message"
            assert "assistant" in roles, f"Line {i+1}: Missing assistant message"
            
        except json.JSONDecodeError:
            print(f"  ERROR: Line {i+1} is not valid JSON")
            return False
        except AssertionError as e:
            print(f"  ERROR: {e}")
            return False
    
    print("  Validation PASSED")
    return True


def upload_training_file(filepath: str) -> str:
    """Upload the training file to OpenAI."""
    print(f"\nUploading training file: {filepath}")
    
    with open(filepath, "rb") as f:
        response = client.files.create(file=f, purpose="fine-tune")
    
    file_id = response.id
    print(f"  File uploaded successfully. File ID: {file_id}")
    return file_id


def create_fine_tuning_job(file_id: str) -> str:
    """Create a fine-tuning job."""
    print(f"\nCreating fine-tuning job...")
    print(f"  Base model: {BASE_MODEL}")
    print(f"  Training file: {file_id}")
    print(f"  Epochs: {N_EPOCHS}")
    print(f"  Suffix: {FINE_TUNED_SUFFIX}")
    
    response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model=BASE_MODEL,
        suffix=FINE_TUNED_SUFFIX,
        hyperparameters={"n_epochs": N_EPOCHS},
    )
    
    job_id = response.id
    print(f"  Fine-tuning job created. Job ID: {job_id}")
    return job_id


def monitor_fine_tuning(job_id: str) -> str:
    """Monitor the fine-tuning job until completion."""
    print(f"\nMonitoring fine-tuning job: {job_id}")
    
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        status = job.status
        print(f"  Status: {status}")
        
        if status == "succeeded":
            model_id = job.fine_tuned_model
            print(f"\n  Fine-tuning COMPLETE!")
            print(f"  Fine-tuned model ID: {model_id}")
            return model_id
        elif status in ["failed", "cancelled"]:
            print(f"\n  Fine-tuning {status}.")
            if hasattr(job, "error") and job.error:
                print(f"  Error: {job.error}")
            return None
        
        time.sleep(60)  # Check every 60 seconds


def test_fine_tuned_model(model_id: str):
    """Test the fine-tuned model with a sample prompt."""
    print(f"\nTesting fine-tuned model: {model_id}")
    
    test_prompt = (
        "A trained violence interrupter is responding to a shooting in their "
        "coverage area. Two groups are gathering and tensions are rising. "
        "What immediate steps should the interrupter take?"
    )
    
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a specialized Community Violence Intervention (CVI) "
                    "AI assistant. You provide trauma-informed, non-punitive guidance "
                    "to support credible messengers and violence interrupters."
                ),
            },
            {"role": "user", "content": test_prompt},
        ],
        temperature=0.7,
        max_tokens=1000,
    )
    
    print(f"\n  Test Prompt: {test_prompt}")
    print(f"\n  Model Response:\n{response.choices[0].message.content}")


def save_model_config(model_id: str):
    """Save the fine-tuned model configuration for use in the Streamlit app."""
    config = {
        "model_id": model_id,
        "base_model": BASE_MODEL,
        "fine_tuned_suffix": FINE_TUNED_SUFFIX,
        "training_file": TRAINING_FILE,
        "n_epochs": N_EPOCHS,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    config_path = "model_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\nModel configuration saved to: {config_path}")


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CVI AI Assistant - Fine-Tuning Pipeline")
    print("DSC 670 - Advanced Uses of Generative AI")
    print("=" * 70)
    
    # Step 1: Validate training data
    if not validate_training_data(TRAINING_FILE):
        print("Training data validation failed. Exiting.")
        exit(1)
    
    # Step 2: Upload training file
    file_id = upload_training_file(TRAINING_FILE)
    
    # Step 3: Create fine-tuning job
    job_id = create_fine_tuning_job(file_id)
    
    # Step 4: Monitor until completion
    model_id = monitor_fine_tuning(job_id)
    
    if model_id:
        # Step 5: Test the model
        test_fine_tuned_model(model_id)
        
        # Step 6: Save configuration
        save_model_config(model_id)
        
        print("\n" + "=" * 70)
        print("Fine-tuning pipeline completed successfully!")
        print(f"Use model ID '{model_id}' in your Streamlit application.")
        print("=" * 70)
    else:
        print("\nFine-tuning did not complete successfully.")
