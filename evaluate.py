import json
import asyncio
import subprocess
from typing import Dict, Any

async def evaluate_test_case(test_case: Dict[str, Any]) -> Dict[str, Any]:
    test_id = test_case["test_id"]
    user_goal = test_case["data"]["input"]["user_goal"]
    expected_behavior = test_case["data"]["expected_behavior"]
    success_criteria = test_case["data"]["success_criteria"]

    result = {
        "test_id": test_id,
        "tool_trajectory_score": 0.0,
        "response_match_score": 0.0,
        "passed": True,
        "details": []
    }

    try:
        # Run 'adk run manager' as subprocess
        process = subprocess.Popen(
            ["adk", "run", "manager"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send user_goal as input
        input_payload = json.dumps({"user_goal": user_goal})
        stdout, stderr = process.communicate(input=input_payload)

        if process.returncode != 0:
            raise RuntimeError(f"Agent run failed: {stderr.strip()}")

        output = json.loads(stdout)

        # Check agent sequence
        actual_sequence = output.get("agent_sequence", [])
        expected_sequence = expected_behavior["agent_sequence"]
        result["tool_trajectory_score"] = 1.0 if actual_sequence == expected_sequence else 0.0
        if actual_sequence != expected_sequence:
            result["passed"] = False
            result["details"].append(f"Agent sequence mismatch: got {actual_sequence}, expected {expected_sequence}")

        # Check output fields
        response_match_score = 0.0
        total_checks = 0
        for agent in expected_behavior:
            if agent.endswith("_output"):
                expected_fields = expected_behavior[agent].get("required_fields", [])
                actual_output = output.get(agent, {})
                matches = sum(1 for field in expected_fields if field in actual_output)
                total_checks += len(expected_fields)
                response_match_score += matches

        result["response_match_score"] = response_match_score / total_checks if total_checks > 0 else 0.0
        if result["response_match_score"] < 1.0:
            result["passed"] = False
            result["details"].append(f"Response match score: {result['response_match_score']}")

    except Exception as e:
        result["passed"] = False
        result["details"].append(f"Error: {str(e)}")

    return result

async def run_evaluations(eval_file: str):
    with open(eval_file, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    results = []
    for test_case in eval_set["test_cases"]:
        result = await evaluate_test_case(test_case)
        results.append(result)
        print(f"\nTest {result['test_id']}: {'PASSED' if result['passed'] else 'FAILED'}")
        print(f" - Trajectory Score: {result['tool_trajectory_score']}")
        print(f" - Response Match Score: {result['response_match_score']}")
        for detail in result["details"]:
            print(f" - {detail}")

    avg_trajectory = sum(r["tool_trajectory_score"] for r in results) / len(results)
    avg_response = sum(r["response_match_score"] for r in results) / len(results)
    print(f"\nSummary: {sum(1 for r in results if r['passed'])}/{len(results)} tests passed")
    print(f"Average Tool Trajectory Score: {avg_trajectory}")
    print(f"Average Response Match Score: {avg_response}")

    with open("custom_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "test_results": results,
            "averages": {
                "tool_trajectory_avg_score": avg_trajectory,
                "response_match_score": avg_response
            }
        }, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run_evaluations("manager\eval1.evalset.json"))
