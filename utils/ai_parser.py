import json

from gemini_service import generate_ai_response


def get_json_response(prompt):

    result = generate_ai_response(prompt)

    result = (
        result.replace("```json", "")
              .replace("```", "")
              .strip()
    )

    return json.loads(result)