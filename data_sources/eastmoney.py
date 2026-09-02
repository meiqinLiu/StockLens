import time

import requests

EASTMONEY_API = "https://82.push2.eastmoney.com/api/qt/clist/get"
EASTMONEY_API_FALLBACK = "https://push2.eastmoney.com/api/qt/clist/get"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

MAX_RETRIES = 5
RETRY_DELAY = 1.5


def get_stock_list(page=1, page_size=100):
    """
    获取 A 股股票列表
    """
    params = {
        "pn": page,
        "pz": page_size,
        "po": 1,
        "np": 1,
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": 2,
        "invt": 2,
        "fid": "f12",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23",
        "fields": "f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f15,f16,f17,f18,f20,f21,f23",
    }

    last_exc = None
    for attempt in range(MAX_RETRIES):
        api = EASTMONEY_API if attempt % 2 == 0 else EASTMONEY_API_FALLBACK
        try:
            response = requests.get(
                api,
                params=params,
                headers=HEADERS,
                timeout=10,
                proxies={"http": None, "https": None},
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_exc = exc
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))

    raise last_exc


if __name__ == "__main__":
    result = get_stock_list(page=1, page_size=100)
    data = result.get("data", {})
    print("diff:", data.get("diff"))
    print("total:", data.get("total"))
