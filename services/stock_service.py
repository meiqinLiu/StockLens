import akshare as ak
import pandas as pd


def search_stock_code(stock_name):
    try:
        spot_df = ak.stock_zh_a_spot_em()
        matched = spot_df[spot_df["名称"] == stock_name]
        if not matched.empty:
            row = matched.iloc[0]
            return {
                "code": str(row["代码"]),
                "name": str(row["名称"]),
                "price": float(row["最新价"]) if pd.notna(row["最新价"]) else None,
            }
    except Exception as e:
        print(f"搜索股票代码失败: {e}")
    return None


def get_stock_spot(stock_code):
    try:
        spot_df = ak.stock_zh_a_spot_em()
        matched = spot_df[spot_df["代码"] == stock_code]
        if not matched.empty:
            row = matched.iloc[0]
            return {
                "price": float(row["最新价"]) if pd.notna(row["最新价"]) else None,
                "pe": float(row["市盈率-动态"]) if pd.notna(row["市盈率-动态"]) else None,
                "pb": float(row["市净率"]) if pd.notna(row["市净率"]) else None,
                "market_cap": float(row["总市值"]) if pd.notna(row["总市值"]) else None,
            }
    except Exception as e:
        print(f"获取行情数据失败: {e}")
    return {}


def get_stock_industry(stock_code):
    try:
        industry_df = ak.stock_board_industry_name_em()
        spot_df = ak.stock_zh_a_spot_em()
        spot_row = spot_df[spot_df["代码"] == stock_code]
        if spot_row.empty:
            return None
        stock_name = spot_row.iloc[0]["名称"]
        for _, industry_row in industry_df.iterrows():
            board_name = industry_row["板块名称"]
            try:
                cons = ak.stock_board_industry_cons_em(symbol=board_name)
                if stock_name in cons["名称"].values:
                    return board_name
            except Exception:
                continue
    except Exception as e:
        print(f"获取行业数据失败: {e}")
    return None
