import os
import pandas as pd
from config import EXCEL_FILE_PATH, SHEET_RECENT, SHEET_COMPANY, RECENT_COLUMNS, COMPANY_COLUMNS


def init_excel():
    if os.path.exists(EXCEL_FILE_PATH):
        return
    with pd.ExcelWriter(EXCEL_FILE_PATH, engine="openpyxl") as writer:
        pd.DataFrame(columns=RECENT_COLUMNS).to_excel(writer, sheet_name=SHEET_RECENT, index=False)
        pd.DataFrame(columns=COMPANY_COLUMNS).to_excel(writer, sheet_name=SHEET_COMPANY, index=False)


def read_sheet(sheet_name):
    init_excel()
    if not os.path.exists(EXCEL_FILE_PATH):
        return pd.DataFrame()
    try:
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name, engine="openpyxl")
        return df.fillna("")
    except Exception:
        return pd.DataFrame()


def write_sheet(sheet_name, df):
    init_excel()
    all_sheets = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None, engine="openpyxl")
    all_sheets[sheet_name] = df
    with pd.ExcelWriter(EXCEL_FILE_PATH, engine="openpyxl") as writer:
        for name, data in all_sheets.items():
            data.to_excel(writer, sheet_name=name, index=False)


def upsert_recent(stock_name, row_data):
    df = read_sheet(SHEET_RECENT)
    if df.empty:
        df = pd.DataFrame(columns=RECENT_COLUMNS)
    mask = df["股票"] == stock_name
    if mask.any():
        for col, val in row_data.items():
            if col in df.columns:
                df.loc[mask, col] = val
    else:
        new_row = {col: row_data.get(col, "") for col in RECENT_COLUMNS}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    write_sheet(SHEET_RECENT, df)


def upsert_company(stock_name, row_data):
    df = read_sheet(SHEET_COMPANY)
    if df.empty:
        df = pd.DataFrame(columns=COMPANY_COLUMNS)
    mask = df["股票"] == stock_name
    if mask.any():
        for col, val in row_data.items():
            if col in df.columns:
                df.loc[mask, col] = val
    else:
        new_row = {col: row_data.get(col, "") for col in COMPANY_COLUMNS}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    write_sheet(SHEET_COMPANY, df)


def get_all_stocks():
    df = read_sheet(SHEET_RECENT)
    if df.empty:
        return []
    return df["股票"].dropna().astype(str).tolist()


def company_exists(stock_name):
    df = read_sheet(SHEET_COMPANY)
    if df.empty:
        return False
    return stock_name in df["股票"].values
