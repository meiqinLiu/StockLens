import akshare as ak
import pandas as pd


def get_finance_indicators(stock_code):
    result = {}
    try:
        df = ak.stock_financial_analysis_indicator(symbol=str(stock_code))
        if df is None or df.empty:
            return result
        df = df.fillna(pd.NA)
        result["revenue_yoy"] = _latest_notna(df, "主营业务收入增长率(%)")
        result["gross_margin"] = _latest_gross_margin(df)
        result["net_margin"] = _latest_notna(df, "销售净利率(%)")
        result["debt_ratio"] = _latest_notna(df, "资产负债率(%)")
        result["roe"] = _latest_notna(df, "净资产收益率(%)")
        result["ocf_to_revenue"] = _latest_notna(df, "经营现金净流量对销售收入比率(%)")
    except Exception as e:
        print(f"获取财务指标失败: {e}")
    return result


def _latest_gross_margin(df):
    """销售毛利率为空时，用 100 - 主营业务成本率 估算。"""
    direct = _latest_notna(df, "销售毛利率(%)")
    if direct is not None:
        return direct
    cost = _latest_notna(df, "主营业务成本率(%)")
    if cost is None:
        return None
    return round(100.0 - cost, 2)


def _latest_notna(df, col):
    """从最新一期向前回溯，取该指标最近一次非空的值（只看最近 N 期）。"""
    if col not in df.columns:
        return None
    for val in reversed(df[col].tolist()[-16:]):
        if val is not None and pd.notna(val):
            return _safe_float(val)
    return None


def _safe_float(val):
    if val is None or pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        s = str(val).strip().replace("%", "").replace(",", "")
        if s == "" or s == "-" or s == "--":
            return None
        return float(s)
    except Exception:
        return None
