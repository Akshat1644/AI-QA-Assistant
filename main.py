import json

from app.gemini_service import generate_test_cases
from app.prompts import TEST_CASE_PROMPT

requirement = input("Enter Requirement: ")

prompt = TEST_CASE_PROMPT.format(
    requirement=requirement
)

result = generate_test_cases(prompt)

try:
    data = json.loads(result)

    print("\nGenerated Test Cases:\n")

    for tc in data:
        print(f"ID: {tc['tc_id']}")
        print(f"Type: {tc['type']}")
        print(f"Scenario: {tc['scenario']}")
        print(f"Expected: {tc['expected_result']}")
        print(f"Priority: {tc['priority']}")
        print("-" * 50)

except Exception as e:
    print("JSON Parsing Error")
    print(result)