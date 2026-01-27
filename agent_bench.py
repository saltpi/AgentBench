# agent_bench.py
import argparse
import yaml
import sys
import os
from typing import Dict, Any
from colorama import Fore, Back, Style

try:
    from run_react import main as react_main
    from run_reflexion import main as reflexion_main
except ImportError as e:
    print(f"Error: Failed to import modules. {e}", file=sys.stderr)
    print("Please ensure react_agent.py, reflexion_agent.py, and src/dataset_loader.py are correct.", file=sys.stderr)
    sys.exit(1)

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Loads the YAML configuration file from the specified path.
    """
    if not os.path.exists(config_path):
        print(f"Error: Configuration file ({config_path}) not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            print(f"Error: Failed to parse YAML file: {e}", file=sys.stderr)
            sys.exit(1)
            
            
def main(args):
    config_data = load_config(args.config)
    if args.agent not in config_data["agents"]:
        print(f"Error: Section '{args.agent}' not found in '{args.config}'.", file=sys.stderr)
        sys.exit(1)
    agent_config_dict = {**config_data["global"], 
                         **config_data["agents"][args.agent]}
    agent_args = argparse.Namespace(**agent_config_dict)
    print(f"--- Running {args.agent} ---")
    print(f"Config File: {args.config}")
    print(f"Using Config: {agent_args}") 
    print("-" * 40)
    try:        
        print(f"Running agent type: {agent_args.type}")
        if agent_args.type == "react":
            react_main(agent_args)
        elif agent_args.type == "reflexion":
            reflexion_main(agent_args)
    except KeyboardInterrupt:
        print("\nExecution was interrupted by the user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: An exception occurred during agent execution: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified Agent Benchmark Runner")
    parser.add_argument(
        "--agent",
        type=str,
        help="Name of agent (must match a key in config.yaml)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to the configuration file to use"
    )
    parser.add_argument("--print-log", help="Pring logs", action="store_true")
    parser.add_argument("--enable-tracing", help="Enable tracing", action="store_true")
    args = parser.parse_args()
    main(args)