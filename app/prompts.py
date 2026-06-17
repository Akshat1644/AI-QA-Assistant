TEST_CASE_PROMPT = """
Act as a Senior QA Engineer.

Analyze the requirement and generate:

1. Functional Test Cases
2. Negative Test Cases
3. Boundary Test Cases
4. Edge Test Cases

Return only valid JSON.

Format:

[
  {{
    "tc_id": "TC001",
    "type": "Functional",
    "scenario": "Scenario Description",
    "expected_result": "Expected Result",
    "priority": "High"
  }}
]

Requirement:
{requirement}
"""