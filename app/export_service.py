import io
import pandas as pd

def convert_df_to_excel(df):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Test Cases"
        )

    return output.getvalue()