import os
import sys
import json
import dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.crews.customer_churn_crew import CustomerChurnCrew
from backend.orchestrator import WorkflowOrchestrator

# Load environment
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

def test_churn_analysis_pipeline():
    query = "why are the customers churning ?"
    print(f"Testing pipeline with query: '{query}'")
    
    # 1. Generate Query Plan
    inputs = {"user_query": query}
    result = CustomerChurnCrew().crew().kickoff(inputs=inputs)
    plan = result.pydantic
    
    print("\n--- Generated Query Plan ---")
    print(json.dumps(plan.model_dump(), indent=2))
    
    # Verify that the query plan correctly turned on the other stages
    assert plan.needs_data_analysis is True, "needs_data_analysis should be True"
    assert plan.needs_prediction is True, "needs_prediction should be True"
    assert plan.needs_recommendation is True, "needs_recommendation should be True"
    assert plan.needs_validation is True, "needs_validation should be True"
    assert plan.needs_report is True, "needs_report should be True"
    
    # 2. Run orchestrator
    print("\n--- Executing Workflow Orchestrator (All Stages) ---")
    orchestrator = WorkflowOrchestrator()
    completed = orchestrator.run(plan)
    
    print("\n--- Execution Completed Successfully! Stage Outputs: ---")
    for stage in ["analysis", "prediction", "recommendation", "validation", "report"]:
        if stage in completed:
            print(f"\n[{stage.upper()}] STAGE COMPLETED:")
            print(completed[stage].model_dump_json(indent=2))
        else:
            print(f"\n[{stage.upper()}] STAGE WAS SKIPPED!")

if __name__ == "__main__":
    test_churn_analysis_pipeline()
