import pandas as pd
import json


def clean_ai_response(result):

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return result


def parse_ai_json(result):

    result = clean_ai_response(result)

    data = json.loads(result)

    return pd.DataFrame(data)


def clean_code_response(result):

    for tag in [
        "```typescript",
        "```javascript",
        "```ts",
        "```js",
        "```python",
        "```java",
        "```"
    ]:
        result = result.replace(tag, "")

    return result.strip()