import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.stock_service import search_stock_code, get_stock_spot, get_stock_industry
from services.finance_service import get_finance_indicators
from services.ai_service import analyze_company_profile
from utils.excel_utils import (
    init_excel,
    upsert_recent,
    upsert_company,
    get_all_stocks,
    company_exists,
    read_sheet,
)
from config import SHEET_RECENT


def add_stock(stock_name):
    print(f"\n>>> 开始新增股票：{stock_name}")
    info = search_stock_code(stock_name)
    if not info:
        print(f"✗ 未找到股票：{stock_name}")
        return False
    stock_code = info["code"]
    actual_name = info["name"]
    print(f"✓ 识别股票：{actual_name} ({stock_code})")

    print("  获取行情数据...")
    spot = get_stock_spot(stock_code)
    print("  获取行业数据...")
    industry = get_stock_industry(stock_code)
    print("  获取财务指标...")
    finance = get_finance_indicators(stock_code)

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recent_row = {
        "股票": actual_name,
        "行业": industry or "",
        "营收同比": finance.get("revenue_yoy", "") if finance.get("revenue_yoy") is not None else "",
        "毛利率": finance.get("gross_margin", "") if finance.get("gross_margin") is not None else "",
        "净利率": finance.get("net_margin", "") if finance.get("net_margin") is not None else "",
        "负债率": finance.get("debt_ratio", "") if finance.get("debt_ratio") is not None else "",
        "经营现金流/营业总收入": finance.get("ocf_to_revenue", "") if finance.get("ocf_to_revenue") is not None else "",
        "PE": spot.get("pe", "") if spot.get("pe") is not None else "",
        "PB": spot.get("pb", "") if spot.get("pb") is not None else "",
        "ROE": finance.get("roe", "") if finance.get("roe") is not None else "",
        "更新时间": update_time,
        "股价": info.get("price") or spot.get("price", "") if (info.get("price") or spot.get("price")) is not None else "",
        "估值": "",
    }
    print("  写入「最近资料」...")
    upsert_recent(actual_name, recent_row)

    if not company_exists(actual_name):
        print("  AI 分析公司资料（首次新增）...")
        raw_info = f"行业：{industry or '未知'}\n"
        ai_result = analyze_company_profile(actual_name, raw_info)
        company_row = {
            "股票": actual_name,
            "行业": industry or "",
            "主营业务": ai_result.get("主营业务", ""),
            "市值": spot.get("market_cap", "") if spot.get("market_cap") is not None else "",
            "商业模式": ai_result.get("商业模式", ""),
            "核心护城河": ai_result.get("核心护城河", ""),
        }
        print("  写入「公司资料」...")
        upsert_company(actual_name, company_row)
    else:
        print("  公司资料已存在，跳过 AI 分析（可使用「重新 AI 分析」功能更新）")

    print(f"✓ 股票「{actual_name}」新增完成\n")
    return True


def update_existing_stocks():
    stocks = get_all_stocks()
    if not stocks:
        print("✗ Excel 中暂无股票，请先使用「新增股票」")
        return
    print(f"\n>>> 开始批量更新，共 {len(stocks)} 只股票")
    success = 0
    for idx, name in enumerate(stocks, 1):
        print(f"[{idx}/{len(stocks)}] 更新 {name} ...")
        info = search_stock_code(name)
        if not info:
            print(f"  ✗ 未找到股票代码，跳过")
            continue
        stock_code = info["code"]
        spot = get_stock_spot(stock_code)
        industry = get_stock_industry(stock_code)
        finance = get_finance_indicators(stock_code)
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        recent_row = {
            "股票": info["name"],
            "行业": industry or "",
            "营收同比": finance.get("revenue_yoy", "") if finance.get("revenue_yoy") is not None else "",
            "毛利率": finance.get("gross_margin", "") if finance.get("gross_margin") is not None else "",
            "净利率": finance.get("net_margin", "") if finance.get("net_margin") is not None else "",
            "负债率": finance.get("debt_ratio", "") if finance.get("debt_ratio") is not None else "",
            "经营现金流/营业总收入": finance.get("ocf_to_revenue", "") if finance.get("ocf_to_revenue") is not None else "",
            "PE": spot.get("pe", "") if spot.get("pe") is not None else "",
            "PB": spot.get("pb", "") if spot.get("pb") is not None else "",
            "ROE": finance.get("roe", "") if finance.get("roe") is not None else "",
            "更新时间": update_time,
            "股价": info.get("price") or spot.get("price", "") if (info.get("price") or spot.get("price")) is not None else "",
            "估值": "",
        }
        upsert_recent(info["name"], recent_row)
        success += 1
    print(f"\n✓ 批量更新完成：成功 {success}/{len(stocks)}\n")


def reanalyze_ai(stock_name):
    print(f"\n>>> 重新 AI 分析：{stock_name}")
    df = read_sheet(SHEET_RECENT)
    if df.empty or stock_name not in df["股票"].values:
        print(f"✗ 股票「{stock_name}」不在数据库中，请先新增")
        return False
    info = search_stock_code(stock_name)
    stock_code = info["code"] if info else None
    industry = None
    if stock_code:
        industry = get_stock_industry(stock_code)
    raw_info = f"行业：{industry or '未知'}\n"
    ai_result = analyze_company_profile(stock_name, raw_info)
    company_row = {
        "股票": stock_name,
        "行业": industry or "",
        "主营业务": ai_result.get("主营业务", ""),
        "商业模式": ai_result.get("商业模式", ""),
        "核心护城河": ai_result.get("核心护城河", ""),
    }
    upsert_company(stock_name, company_row)
    print(f"✓ 股票「{stock_name}」AI 重新分析完成\n")
    return True


def print_menu():
    print("================================")
    print("       A股股票研究工具")
    print("================================")
    print()
    print("股票名称：")
    print()
    print("[                            ]")
    print()
    print("        [ 1. 新增股票 ]")
    print()
    print("--------------------------------")
    print()
    print("        [ 2. 更新已有股票 ]")
    print()
    print("--------------------------------")
    print()
    print("        [ 3. 重新 AI 分析 ]")
    print()
    print("        [ 0. 退出 ]")
    print()
    print("================================")


def main():
    init_excel()
    while True:
        print_menu()
        choice = input("请选择操作 (0-3)：").strip()
        if choice == "0":
            print("退出程序，再见！")
            break
        elif choice == "1":
            name = input("请输入股票名称：").strip()
            if name:
                add_stock(name)
            else:
                print("✗ 股票名称不能为空")
        elif choice == "2":
            update_existing_stocks()
        elif choice == "3":
            name = input("请输入要重新分析的股票名称：").strip()
            if name:
                reanalyze_ai(name)
            else:
                print("✗ 股票名称不能为空")
        else:
            print("✗ 无效选择，请输入 0-3")
        input("按 Enter 继续...")


if __name__ == "__main__":
    main()
