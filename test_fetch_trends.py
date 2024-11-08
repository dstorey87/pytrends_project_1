# test_fetch_trends.py
from pytrends.request import TrendReq

pytrends = TrendReq(hl="en-US", tz=360)
keywords = ["Technology", "Innovation", "AI"]
timeframe = "2023-09-01 2023-09-30"

pytrends.build_payload(keywords, timeframe=timeframe)
trends_data = pytrends.interest_over_time()
print(trends_data)