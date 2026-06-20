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


GAP_ANALYSIS_PROMPT = """
Act as a Senior QA Engineer and Business Analyst.

Analyze the requirement and identify:

1. Missing requirements
2. Ambiguous statements
3. Potential risks
4. Clarification questions

Provide the response in markdown format.

Use the following sections:

## Missing Requirements

## Ambiguities

## Risks

## Clarification Questions

Requirement:
{requirement}
"""



TEST_DATA_PROMPT = """
Act as a Senior QA Engineer.

Analyze the requirement and generate test data.

Return ONLY valid JSON in this format:

[
  {{
    "field": "Email",
    "valid_data": "test@gmail.com",
    "invalid_data": "abc@"
  }}
]

Requirement:
{requirement}
"""