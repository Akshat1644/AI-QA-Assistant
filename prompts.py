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

Analyze the following software requirement and identify:

1. Missing Requirements
2. Ambiguities
3. Risks
4. Clarification Questions

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use headings.
Do NOT use explanations.
Do NOT wrap the response inside ```json.

Return ONLY a JSON array in the following format:

[
  {{
    "Category": "Missing Requirement",
    "Finding": "",
    "Impact": "",
    "Recommendation": ""
  }},
  {{
    "Category": "Ambiguity",
    "Finding": "",
    "Impact": "",
    "Recommendation": ""
  }},
  {{
    "Category": "Risk",
    "Finding": "",
    "Impact": "",
    "Recommendation": ""
  }},
  {{
    "Category": "Clarification Question",
    "Finding": "",
    "Impact": "",
    "Recommendation": ""
  }}
]

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




API_TEST_CASE_PROMPT = """
Act as a Senior API QA Engineer.

Analyze the API details and generate:

1. Positive Test Cases
2. Negative Test Cases
3. Validation Test Cases
4. Boundary Test Cases
5. Authorization Test Cases
6. Error Handling Test Cases

Return ONLY valid JSON.

Format:

[
  {{
    "tc_id": "TC001",
    "type": "Positive",
    "scenario": "Valid request with all mandatory fields",
    "expected_result": "API returns 200 OK",
    "priority": "High"
  }}
]

API Details:
{requirement}
"""


PLAYWRIGHT_SCRIPT_PROMPT = """
Act as a Senior Automation QA Engineer.

Generate a Playwright Python automation script based on the requirement.

Requirements:
{requirement}

Rules:

1. Use Playwright Python syntax.
2. Include test function.
3. Add comments where appropriate.
4. Return only Python code.
"""


QUALITY_SCORE_PROMPT = """
Act as a Senior QA Lead.

Analyze the requirement.

Return ONLY in this format:

COMPLETENESS: XX

CLARITY: XX

TESTABILITY: XX

AMBIGUITY: XX

STRENGTHS:
- Point 1
- Point 2

WEAKNESSES:
- Point 1
- Point 2

RECOMMENDATIONS:
- Point 1
- Point 2

Requirement:
{requirement}
"""


COVERAGE_ANALYSIS_PROMPT = """
Act as a Senior QA Lead.

Analyze the software requirement and evaluate its test coverage.

Return ONLY valid JSON.

Do NOT return markdown.
Do NOT return explanations.
Do NOT wrap the response inside ```json.

Return the response exactly in this format:

[
    {{
        "Requirement Area":"User Login",
        "Coverage":"Login with valid credentials is covered",
        "Status":"Covered",
        "Recommendation":"No additional action required"
    }},
    {{
        "Requirement Area":"Forgot Password",
        "Coverage":"Password reset flow is missing",
        "Status":"Missing",
        "Recommendation":"Add password reset test scenarios"
    }}
]

Rules:

1. Return ONLY JSON.
2. Status must be one of:
   - Covered
   - Partial
   - Missing
3. Recommendation should be concise.
4. Generate multiple requirement areas whenever possible.

Requirement:

{requirement}
"""


RISK_ANALYSIS_PROMPT = """
You are a Senior QA Lead and Test Architect.

Analyze the software requirement and identify potential testing risks.

Return ONLY valid JSON.

Format:

[
    {{
        "risk_area": "Authentication",
        "severity": "High",
        "reason": "Password complexity is not specified.",
        "recommendation": "Add password validation and account lockout test cases."
    }}
]

Rules:

1. Identify all major testing risks.
2. Severity must be one of:
   - High
   - Medium
   - Low
3. Keep reasons concise.
4. Recommendations should be actionable.
5. Return ONLY JSON.
6. Do not include markdown or explanations.

Requirement:
{requirement}
"""



DEFECT_PREDICTION_PROMPT = """
Act as a Senior QA Lead with experience in defect prevention.

Analyze the following requirement and identify:

1. Potential defect-prone areas
2. Possible production issues
3. Likely defect severity
4. Recommended testing focus
5. Suggestions to reduce defects

Return the response in markdown format using the following structure:

## Potential Defect-Prone Areas

- Point

## Possible Production Issues

- Point

## Likely Severity

High / Medium / Low

## Recommended Testing Focus

- Point

## Prevention Suggestions

- Point

Requirement:
{requirement}
"""


RTM_PROMPT = """
Act as a Senior QA Engineer.

Analyze the requirement and generate a Requirement Traceability Matrix.

Return ONLY valid JSON.

Format:

[
  {{
    "requirement_id": "REQ001",
    "requirement": "",
    "mapped_test_case": "",
    "coverage_status": "Covered"
  }}
]

If a requirement is not covered, write:

"mapped_test_case": "Not Available"

"coverage_status": "Missing"

Requirement:
{requirement}
"""


SMART_RTM_PROMPT = """
Act as a Senior QA Lead.

You are given:

1. Software Requirement
2. Generated Test Cases

Review whether every requirement is covered by the generated test cases.

Return ONLY valid JSON.

[
    {{
        "requirement": "",
        "status": "Covered",
        "missing_scenario": "None",
        "recommendation": "Good Coverage"
    }}
]

Status should be one of:
- Covered
- Partial
- Missing

Requirement:

{requirement}

Generated Test Cases:

{test_cases}
"""



COMPLETENESS_ANALYSIS_PROMPT = """
You are a Senior QA Lead and Business Analyst.

Review the software requirement and evaluate whether it is complete and ready for testing.

Return ONLY valid JSON.

Format:

[
    {{
        "category": "Business Rules",
        "status": "Partial",
        "details": "Password complexity requirements are missing.",
        "recommendation": "Define password length, special characters and validation rules."
    }}
]

Rules:

1. Review the following categories:
   - Functional Requirements
   - Business Rules
   - Acceptance Criteria
   - Validation Rules
   - Error Handling
   - Security
   - Performance
   - Edge Cases
   - Testability

2. Status must be one of:
   - Complete
   - Partial
   - Missing

3. Keep details concise.

4. Recommendations should be actionable.

5. Return ONLY valid JSON.

Requirement:
{requirement}
"""



BUG_PREDICTION_PROMPT = """
You are an experienced QA Architect with expertise in defect prevention and risk-based testing.

Analyze the software requirement and predict modules most likely to contain defects.

Return ONLY valid JSON.

Do NOT return markdown.
Do NOT return explanations.
Do NOT wrap inside ```json.

Return the response exactly in this format:

[
    {{
        "Module":"Authentication",
        "Risk":"High",
        "Probability":95,
        "Reason":[
            "Password rules are not clearly defined.",
            "Boundary conditions are missing."
        ],
        "Recommendation":[
            "Perform boundary testing.",
            "Execute negative testing."
        ]
    }},
    {{
        "Module":"API",
        "Risk":"Medium",
        "Probability":70,
        "Reason":[
            "Error handling scenarios are missing."
        ],
        "Recommendation":[
            "Add API validation tests."
        ]
    }}
]

Rules:

1. Return ONLY JSON.
2. Risk must be:
   - High
   - Medium
   - Low
3. Probability must be an integer between 0 and 100.
4. Reason must always be an array.
5. Recommendation must always be an array.
6. Generate multiple modules whenever possible.

Requirement:

{requirement}
"""


DEFECT_REPORT_PROMPT = """
You are an experienced Senior QA Engineer.

Based on the software requirement below, assume that a critical test case has failed.

Generate a professional defect report.

Return ONLY valid JSON.

Format:

[
    {{
        "bug_summary": "Login fails with valid credentials",
        "description": "Users cannot log in using valid email and password.",
        "steps_to_reproduce": [
            "Open Login Page",
            "Enter valid email",
            "Enter valid password",
            "Click Login"
        ],
        "expected_result": "User should be redirected to Dashboard.",
        "actual_result": "User remains on Login page with an error.",
        "severity": "High",
        "priority": "High",
        "root_cause": [
          "Authentication service validation failed.",
          "Password comparison logic is incorrect."
        ]
        "suggested_fix": [
          "Review authentication logic.",
          "Add unit tests for login validation.",
          "Verify API response handling."
        ]
    }}
]

Rules:

1. Return ONLY JSON.
2. Severity must be:
   - Critical
   - High
   - Medium
   - Low
3. Priority must be:
   - High
   - Medium
   - Low
4. steps_to_reproduce MUST be an array.
5. Make the defect realistic and professional.

Requirement:

{requirement}
"""



REGRESSION_IMPACT_PROMPT = """
You are a Senior QA Lead.

Analyze the requirement and identify modules affected by the change.

Return ONLY valid JSON.

Do NOT return markdown.
Do NOT wrap inside ```json.

Return the response exactly in this format:

[
    {{
        "Affected Module":"Authentication",
        "Impact Level":"High",
        "Reason":"Login functionality has changed.",
        "Recommended Regression Tests":"Login, Logout, Session Timeout"
    }},
    {{
        "Affected Module":"User Profile",
        "Impact Level":"Medium",
        "Reason":"Profile loads after login.",
        "Recommended Regression Tests":"Profile Update, View Profile"
    }}
]

Rules:

1. Return ONLY JSON.
2. Impact Level must be High, Medium or Low.
3. Recommended Regression Tests should be comma separated.
4. Generate multiple affected modules whenever possible.

Requirement:

{requirement}
"""



AUTOMATION_FEASIBILITY_PROMPT = """
You are a Senior Automation Test Architect.

Analyze the software requirement below and determine its automation feasibility.

Return ONLY valid JSON.

Format:

[
    {{
        "automation_score": 92,
        "feasibility": "High",
        "recommended_framework": "Playwright",
        "framework_reason": "Fast execution, auto-waiting, cross-browser support and modern architecture.",
        "automation_challenges": [
        "CAPTCHA",
        "OTP Authentication",
        "Dynamic Locators"
        ],
        "automation_strategy": [
        "Automate UI using Playwright",
        "Validate APIs separately",
        "Mock third-party services"
        ],
        "estimated_effort": "2-3 Days",
        "maintenance_level": "Low",
        "summary": "This requirement is highly suitable for automation and can be efficiently automated using Playwright."
    }}
]

Rules:

1. Return ONLY valid JSON.
2. automation_score must be an integer between 0 and 100.
3. feasibility must be exactly one of:
   - High
   - Medium
   - Low
4. automation_challenges must be an array.
5. automation_strategy must be an array.
6. Keep the summary concise and practical.

Requirement:

{requirement}
"""