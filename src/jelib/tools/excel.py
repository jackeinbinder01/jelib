import pandas as pd
from pathlib import Path

FILE_NAME = "file.xlsx"  # Excel file name
FILE_PATH = Path(rf"C:\Users\YourName\Documents\{FILE_NAME}")  # The path to the file's folder on your machine

P_NAME_ROW_IDX = 3  # The row index (row number - 1) of the partner name on each sheet
P_NAME_COL_IDX = 0  # The col index (col number - 1) of the partner name on each sheet
MAX_CHARS = 25  # The maximum number of characters before it becomes a problem


def find_long_names(
        path: Path = FILE_PATH,
        row_idx: int = P_NAME_ROW_IDX,
        col_idx: int = P_NAME_COL_IDX,
        max_chars: int = MAX_CHARS,
) -> list[str]:
    excel_file = pd.read_excel(path, sheet_name=None)

    too_long_sheets = []
    for sheet_name, df in excel_file.items():
        if df.shape[0] <= row_idx or df.shape[1] <= col_idx:
            continue

        partner_name = str(df.iloc[row_idx, col_idx]).strip()
        if pd.isna(partner_name) or partner_name == "":
            continue

        partner_name_len = len(partner_name)
        if partner_name_len > max_chars:
            too_long_sheets.append(
                f"File: {str(path)} | Sheet: {sheet_name} | Name: {partner_name} | # Chars: {partner_name_len}"
            )

    return too_long_sheets


def main() -> None:
    too_long_names = find_long_names()
    for each in too_long_names:
        print(each)


if __name__ == "__main__":
    main()
