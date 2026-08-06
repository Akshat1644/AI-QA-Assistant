import json
import pandas as pd


def clean_ai_response(result: str) -> str:
    """
    Removes markdown code fences returned by Gemini.
    """

    if not result:
        return ""

    tags = [
        "```json",
        "```JSON",
        "```"
    ]

    for tag in tags:
        result = result.replace(tag, "")

    return result.strip()



def parse_ai_json(result):

    cleaned = clean_ai_response(result)

    data = json.loads(cleaned)

    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("AI returned an empty response.")

    return df


def clean_code_response(result):

    if not result:
        return ""

    tags = [
        "```typescript",
        "```javascript",
        "```ts",
        "```js",
        "```python",
        "```java",
        "```"
    ]

    for tag in tags:
        result = result.replace(tag, "")

    return result.strip()