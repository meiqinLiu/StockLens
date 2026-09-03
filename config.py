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

# ===== 雪球 (XueQiu) 配置 =====
# xq_a_token 是雪球的登录令牌，可从浏览器访问 xueqiu.com 后拷贝 Cookie 中的 xq_a_token 值。
# 令牌会过期，失效后只需更新下面这一行（或用环境变量 XQ_A_TOKEN 覆盖）。
XQ_A_TOKEN = os.getenv("XQ_A_TOKEN", "e089ef84783e609bfb50f1f4b788280bcb1f01ff")
