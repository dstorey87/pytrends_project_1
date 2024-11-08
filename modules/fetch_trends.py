# File: modules/fetch_trends.py

import logging
from pytrends.request import TrendReq
import urllib3
import traceback
import pandas as pd

# Suppress SSL warnings (if necessary)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_basic_trends(keywords, timeframe):
    """
    Fetch basic trends data from Google Trends.

    Args:
        keywords (list): List of keywords to fetch trends for.
        timeframe (str): Timeframe for the trends data.

    Returns:
        list: List of dictionaries containing trends data.
    """
    logging.debug(f"Fetching basic trends for keywords: {keywords} and timeframe: {timeframe}")
    pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
    try:
        pytrends.build_payload(keywords, timeframe=timeframe)
        trends_data = pytrends.interest_over_time()
        if trends_data is None or trends_data.empty:
            logging.error("No trends data returned.")
            return []
        if "isPartial" in trends_data.columns:
            trends_data = trends_data.drop(columns=["isPartial"])
        # Convert DataFrame to list of dictionaries
        return trends_data.reset_index().to_dict(orient="records")
    except Exception as e:
        logging.error(f"Error fetching basic trends data: {e}")
        return []

def fetch_related_queries(keyword):
    """
    Fetch related queries for a given keyword.

    Args:
        keyword (str): Keyword to fetch related queries for.

    Returns:
        list: List of related queries.
    """
    logging.debug(f"Fetching related queries for keyword: {keyword}")
    pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
    try:
        pytrends.build_payload([keyword])
        related = pytrends.related_queries()
        if related and keyword in related:
            keyword_related = related[keyword]
            top_queries = keyword_related.get('top')
            rising_queries = keyword_related.get('rising')

            # Check if 'top' related queries are available
            if isinstance(top_queries, pd.DataFrame) and not top_queries.empty:
                return top_queries.to_dict('records')
            # Optionally check for 'rising' related queries
            elif isinstance(rising_queries, pd.DataFrame) and not rising_queries.empty:
                return rising_queries.to_dict('records')
            else:
                logging.warning(f"No related queries found for {keyword}.")
                return []
        else:
            logging.warning(f"No related queries data found for {keyword}.")
            return []
    except IndexError:
        # Handle the specific IndexError when 'rankedList' is empty
        logging.warning(f"No related queries found for {keyword} (IndexError).")
        return []
    except Exception as e:
        logging.error(f"Error fetching related queries for {keyword}: {e}")
        return []

def fetch_top_trending_topics():
    """
    Fetch top trending topics from Google Trends.

    Returns:
        list: List of top trending topics.
    """
    logging.debug("Fetching top trending topics.")
    pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
    try:
        trending = pytrends.trending_searches(pn="united_states")
        if trending.empty:
            logging.warning("No trending topics found.")
            return []
        topics = trending[0].tolist()
        return topics
    except Exception as e:
        logging.error(f"Error fetching top trending topics: {e}")
        return []
