"""
MLflow-based evaluation for LLM responses.

This module provides functionality to evaluate language model responses using MLflow's
GenAI evaluation framework. It loads test data, sets up MLflow tracking, and runs
evaluations using multiple scorers to assess the quality of LLM responses.

Key Features:
    - Loads test data from JSON files
    - Configures MLflow tracking and experiment settings
    - Evaluates responses using Correctness and Guidelines scorers
    - Logs evaluation results to MLflow for tracking and comparison

Usage:
    python -m evaluation.eval
"""
import mlflow
from mlflow.genai.scorers import Correctness, Guidelines
import logging
import json
from typing import List
from evaluation.llm import chat
from evaluation.settings import APP_SETTINGS

logger = logging.getLogger(__name__)

def load_test_data(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)

def setup_mlflow():
    mlflow.openai.autolog() # type: ignore
    mlflow.set_tracking_uri(APP_SETTINGS.mlflow_tracing_uri) # type: ignore
    mlflow.set_experiment(APP_SETTINGS.mlflow_experiment_name) # type: ignore
    logger.info(f"MLflow tracking URI set to: {APP_SETTINGS.mlflow_tracing_uri}") # type: ignore
    logger.info(f"MLflow experiment set to: {APP_SETTINGS.mlflow_experiment_name}") # type: ignore

def get_scorers() -> List:
    correctness_scorer = Correctness(model=APP_SETTINGS.eval_model) # type: ignore
    guidelines_scorer = Guidelines(
        model=APP_SETTINGS.eval_model,  # type: ignore
        guidelines=[
            "The answer should be factually correct.",
            "The answer should be concise and to the point."
        ]
    )
    return [correctness_scorer, guidelines_scorer] 

def fn_evaluate(question: str) -> str:
    """
    Evaluate the model's response to a given question.
    
    Args:
        question (str): The input question to evaluate.
    
    Returns:
        str: The model's response.
    """
    return chat(question)

def main():
    print("Starting evaluation...")
    setup_mlflow()
    test_data = load_test_data(APP_SETTINGS.eval_dataset_path) # type: ignore
    mlflow.genai.evaluate( # type: ignore
        data=test_data,
        predict_fn=fn_evaluate,
        scorers=get_scorers(),
    )
    logger.info("Evaluation complete.")

if __name__ == "__main__":
    main()