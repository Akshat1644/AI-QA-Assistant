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

Analyze the requirement and identify:

1. Covered Scenarios
2. Missing Test Scenarios
3. High Risk Areas
4. Additional Recommendations

Return the response in markdown format.

Use this structure:

## Covered Scenarios

- Scenario 1

## Missing Scenarios

- Scenario 1

## High Risk Areas

- Risk 1

## Recommendations

- Recommendation 1

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

Analyze the software requirement below and predict the areas most likely to contain software defects.

Return ONLY valid JSON.

Format:

[
    {{
        "module": "Authentication",
        "risk": "High",
        "probability": 95,
        "reason": [
            "Password validation rules are not clearly defined.",
            "No password complexity requirement is mentioned.",
            "Boundary conditions are missing."
        ],
        "recommendation": [
            "Perform boundary value testing.",
            "Execute negative testing.",
            "Validate password complexity rules."
        ]
    }}
]

Rules:

1. Analyze these areas wherever applicable:
   - Authentication
   - Authorization
   - Business Logic
   - Input Validation
   - Database
   - API
   - UI
   - Session Management
   - Security
   - Performance
   - Error Handling
   - Edge Cases

2. Probability must be an integer between 0 and 100.

3. Risk must be exactly one of:
   - High
   - Medium
   - Low

4. "reason" MUST always be a JSON array of strings.
Never return a paragraph or a single string.

Example:
"reason": [
    "Input validation rules are missing.",
    "Password complexity is not specified.",
    "Boundary conditions are undefined."
]

5. "recommendation" MUST always be a JSON array of strings.

Example:
"recommendation": [
    "Perform boundary value testing.",
    "Execute negative testing.",
    "Validate password complexity."
]

6. Return ONLY valid JSON.
   - No markdown.
   - No explanations.
   - No extra text.

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
You are a Senior QA Lead with expertise in Regression Testing.

Analyze the requirement below and determine the regression testing impact.

Return ONLY valid JSON.

Format:

[
    {{
        "risk_level":"High",

        "affected_modules":[
            {{
                "module":"Authentication",
                "impact":"High"
            }},
            {{
                "module":"Login API",
                "impact":"High"
            }},
            {{
                "module":"Database",
                "impact":"Medium"
            }}
        ],

        "regression_suites":[
            {{
                "suite":"Smoke Testing",
                "priority":"High"
            }},
            {{
                "suite":"Authentication Testing",
                "priority":"High"
            }},
            {{
                "suite":"Security Testing",
                "priority":"Medium"
            }}
        ],

        "focus_areas":[
            "Boundary Testing",
            "Negative Testing",
            "Session Management",
            "Input Validation"
        ],

        "summary":"The login functionality affects multiple authentication components. Complete regression testing is recommended before release."
    }}
]

Rules:

1. Return ONLY JSON.
2. Risk Level must be High, Medium or Low.
3. Impact must be High, Medium or Low.
4. Priority must be High, Medium or Low.
5. Focus Areas must be an array.
6. Keep summary concise.
7. Make recommendations realistic.

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