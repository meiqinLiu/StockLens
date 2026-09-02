import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_FILE_PATH = os.path.join(BASE_DIR, "股票研究数据库.xlsx")

DATA_DIR = os.path.join(BASE_DIR, "data")

SHEET_RECENT = "最近资料"
SHEET_COMPANY = "公司资料"

RECENT_COLUMNS = [
    "股票",
    "行业",
    "营收同比",
    "毛利率",
    "净利率",
    "负债率",
    "经营现金流/营业总收入",
    "PE",
    "PB",
    "ROE",
    "更新时间",
    "股价",
    "估值",
]

COMPANY_COLUMNS = [
    "股票",
    "行业",
    "主营业务",
    "市值",
    "商业模式",
    "核心护城河",
]

AI_PROVIDER = os.getenv("AI_PROVIDER", "deepseek")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.deepseek.com/v1")
