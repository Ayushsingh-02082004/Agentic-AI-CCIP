import os
import sys
import io
import pandas as pd
# import pytest

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.vectorstore.ingestion_service import IngestionService
from backend.vectorstore.chroma_service import ChromaService

def test_custom_csv_ingestion():
    print("Starting custom CSV ingestion unit tests...")
    
    # 1. Prepare valid CSV data
    valid_csv_content = """customer_id,age,tenure_months,support_tickets,contract_type,monthly_charges,total_charges,internet_service,payment_method,churn
9901,35,12,2,One Year,55.5,666.0,Fiber,Credit Card,0
9902,48,6,5,Month-to-Month,85.0,510.0,Fiber,UPI,1
"""
    
    valid_buffer = io.StringIO(valid_csv_content)
    
    # 2. Run Ingestion
    ingestion = IngestionService()
    print("Testing valid dataset ingestion...")
    ingestion.ingest_csv(valid_buffer)
    
    # 3. Verify it was written to ChromaDB
    db = ChromaService()
    cust_1 = db.get_customer_by_id(9901)
    cust_2 = db.get_customer_by_id(9902)
    
    assert cust_1 is not None, "Customer 9901 should be ingested"
    assert cust_1["metadata"]["contract"] == "One Year"
    assert cust_1["metadata"]["churn"] == 0
    
    assert cust_2 is not None, "Customer 9902 should be ingested"
    assert cust_2["metadata"]["contract"] == "Month-to-Month"
    assert cust_2["metadata"]["churn"] == 1
    
    print("Valid dataset ingestion verified successfully!")

    # 4. Prepare invalid CSV data (missing 'churn' column)
    invalid_csv_content = """customer_id,age,tenure_months,support_tickets,contract_type,monthly_charges,total_charges,internet_service,payment_method
9903,22,3,1,Month-to-Month,45.0,135.0,DSL,Cash
"""
    invalid_buffer = io.StringIO(invalid_csv_content)
    
    print("Testing invalid dataset validation (missing column)...")
    try:
        ingestion.ingest_csv(invalid_buffer)
        assert False, "Should have raised ValueError due to missing 'churn' column"
    except ValueError as e:
        print(f"Correctly caught validation error: {e}")
        assert "churn" in str(e)
        
    print("CSV validation logic verified successfully!")

if __name__ == "__main__":
    test_custom_csv_ingestion()
    print("\n--- ALL DATASET INGESTION TESTS PASSED! ---")
