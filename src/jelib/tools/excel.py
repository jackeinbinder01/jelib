import pandas as pd
from pathlib import Path

FILE_NAME = "file.xlsx"
FILE_PATH = Path(rf"C:\Users\YourName\Documents\{FILE_NAME}")  # Where the excel file is

P_NAME_ROW_IDX = 3  # Row in each sheet where partner name is
P_NAME_COL_IDX = 0  # Col in each sheet where partner name is
MAX_CHARS = 25  # ~ number of chars before cell returns to \n


def find_long_names(
        path: Path = FILE_PATH,
        row_idx: int = P_NAME_ROW_IDX,
        col_idx: int = P_NAME_COL_IDX,
        max_chars: int = MAX_CHARS,
) -> list[str]:
    excel_file = pd.read_excel(path, sheet_name=None)  # Excel -> Pandas

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
