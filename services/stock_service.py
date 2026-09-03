import ast

import akshare as ak

from config import XQ_A_TOKEN

_code_name_cache = None


def _normalize_name(name: str) -> str:
    """去除空白，并把全角字母数字转为半角，用于名称模糊匹配。"""
    if name is None:
        return ""
    s = str(name).replace(" ", "").replace("\u3000", "")
    s = s.translate(str.maketrans(
        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    ))
    s = s.translate(str.maketrans(
        "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
        "abcdefghijklmnopqrstuvwxyz",
    ))
    return s


def _get_code_name_list():
    """获取全部 A 股代码与名称（缓存）。"""
    global _code_name_cache
    if _code_name_cache is None:
        df = ak.stock_info_a_code_name()
        _code_name_cache = df
    return _code_name_cache


def _to_xq_symbol(stock_code):
    """把 6 位股票代码转成雪球 symbol，如 600000 -> SH600000。"""
    code = str(stock_code).zfill(6)
    if code.startswith(("6", "9")):
        return "SH" + code
    if code.startswith(("0", "3")):
        return "SZ" + code
    return "BJ" + code


def _parse_spot(df):
    """把雪球 item/value 两列的行情表转成字典。"""
    if df is None or df.empty:
        return {}
    return {str(row["item"]): row["value"] for _, row in df.iterrows()}


def search_stock_code(stock_name):
    try:
        info = _get_code_name_list()
        target = _normalize_name(stock_name)
        def _match(row):
            if _normalize_name(row["name"]) == target:
                return True
            return False
        matched = info[info.apply(_match, axis=1)]
        if matched.empty:
            return None
        row = matched.iloc[0]
        return {
            "code": str(row["code"]),
            "name": _normalize_name(row["name"]),
            "price": None,
        }
    except Exception as e:
        print(f"搜索股票代码失败: {e}")
    return None


def get_stock_spot(stock_code):
    try:
        df = ak.stock_individual_spot_xq(
            symbol=_to_xq_symbol(stock_code), token=XQ_A_TOKEN
        )
        d = _parse_spot(df)
        if not d:
            return {}
        return {
            "price": _to_float(d.get("现价")),
            "pe": _to_float(d.get("市盈率(TTM)") or d.get("市盈率(动)")),
            "pb": _to_float(d.get("市净率")),
            "market_cap": _to_float(d.get("资产净值/总市值") or d.get("流通值")),
        }
    except Exception as e:
        print(f"获取行情数据失败: {e}")
    return {}


def get_stock_industry(stock_code):
    try:
        df = ak.stock_individual_basic_info_xq(
            symbol=_to_xq_symbol(stock_code), token=XQ_A_TOKEN
        )
        if df is None or df.empty:
            return None
        m = {str(row["item"]): row["value"] for _, row in df.iterrows()}
        industry = m.get("affiliate_industry")
        if isinstance(industry, dict):
            name = industry.get("ind_name")
            return name if name else None
        if isinstance(industry, str):
            try:
                parsed = ast.literal_eval(industry)
                if isinstance(parsed, dict):
                    return parsed.get("ind_name")
            except Exception:
                pass
        return None
    except Exception as e:
        print(f"获取行业数据失败: {e}")
    return None


def _to_float(val):
    if val is None:
        return None
    try:
        if isinstance(val, (int, float)):
            return float(val)
        s = str(val).strip().replace(",", "").replace("%", "")
        if s in ("", "-", "--", "nan"):
            return None
        return float(s)
    except Exception:
        return None
