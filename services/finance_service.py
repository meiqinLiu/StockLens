import akshare as ak
import pandas as pd


def get_finance_indicators(stock_code):
    result = {}
    try:
        if stock_code.startswith("6"):
            symbol = "SH" + stock_code
        else:
            symbol = "SZ" + stock_code
        df = ak.stock_financial_abstract_ths(symbol=symbol, indicator="按报告期")
        if df is not None and not df.empty:
            latest = df.iloc[0]
            result["revenue_yoy"] = _safe_float(latest.get("营业总收入同比增长率", None))
            result["gross_margin"] = _safe_float(latest.get("销售毛利率", None))
            result["net_margin"] = _safe_float(latest.get("销售净利率", None))
            result["debt_ratio"] = _safe_float(latest.get("资产负债率", None))
            result["roe"] = _safe_float(latest.get("净资产收益率", None))
            result["ocf_to_revenue"] = _calc_ocf_ratio(latest)
    except Exception as e:
        print(f"获取财务指标失败: {e}")
    return result


def _calc_ocf_ratio(row):
    try:
        ocf = _safe_float(row.get("经营活动产生的现金流量净额", None))
        rev = _safe_float(row.get("营业总收入", None))
        if ocf is not None and rev and rev != 0:
            return round(ocf / rev * 100, 2)
    except Exception:
        pass
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
