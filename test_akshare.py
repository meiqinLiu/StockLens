# xq_a_token = "e089ef84783e609bfb50f1f4b788280bcb1f01ff"
# import akshare as ak

# stock_individual_spot_xq_df = ak.stock_individual_spot_xq(
#     symbol="SH600000",
#     token=xq_a_token,
# )
# print(stock_individual_spot_xq_df)


# import akshare as ak

# stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000001")
# print(stock_individual_info_em_df)

import akshare as ak

stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000001", start_date="19910403", end_date="20231027", adjust="qfq")
print(stock_zh_a_daily_qfq_df)