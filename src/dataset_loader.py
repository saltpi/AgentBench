# src/dataset_loader.py
import json
import random
import os

def load_dataset(workload: str, shuffle: bool = False):
    """
    Loads and returns the dataset based on the workload.
    """
    data = []
    
    # --- Define dataset paths ---
    paths = {
        "hotpotqa": "dataset/hotpot_dev_fullwiki_v1.json",
        "webshop": "dataset/webshop_session_ids.json",
        "math": "dataset/math_500.jsonl", 
        "gsm8k": "dataset/gsm8k_test.jsonl",
        "humaneval": "dataset/HumanEval.json"
    }

    dataset_path = paths.get(workload)
    
    if not dataset_path or not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found for workload '{workload}'. Searched at: {dataset_path}")

    # --- Load data based on file type ---
    try:
        if workload == "math" or workload == "gsm8k":
            # Handle .jsonl
            with open(dataset_path, "r", encoding="utf-8") as f:
                data = [json.loads(line) for line in f]
        
        elif workload == "webshop":
            # Handle webshop session IDs
            with open(dataset_path, "r", encoding="utf-8") as f:
                # Both agents iterate over the session IDs list
                data = json.load(f)["session_ids"] 
        
        else:
            # Handle standard .json
            with open(dataset_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
    except Exception as e:
        print(f"Error loading dataset file {dataset_path}: {e}")
        return []

    if shuffle:
        print("Shuffling dataset...")
        random.shuffle(data)
            
    return data

from src.tools.hotpotqa_tools.hotpot_evaluate import evaluate_hotpotqa
from src.tools.math_tools.math_equivalence import evaluate_math
from src.tools.webshop_tools.webshop_tools import evaluate_webshop
from src.tools.humaneval_tools.coding_tools import evaluate_humaneval

def get_evaluation_function(workload):
    if workload == "hotpotqa":
        return evaluate_hotpotqa

    if workload == "webshop":
        return evaluate_webshop

    if workload == "math":
        return evaluate_math

    if workload == "humaneval":
        return evaluate_humaneval

    raise ValueError(f"Unsupported workload: {workload}")