import os
import pathlib
import pytest
from dotenv import load_dotenv
from google.adk.evaluation.agent_evaluator import AgentEvaluator

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

def test_agent():
    AgentEvaluator.evaluate(
        agent_module="manager",
        eval_dataset_file_path_or_dir=str(
            pathlib.Path(__file__).parent / "eval_sets/multi_agent_eval_set.json",
        ),
        num_runs=2
    )
