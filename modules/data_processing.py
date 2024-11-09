import logging
import statistics

def process_trend_data(trend_data):
    """Process trend data and calculate statistics."""
    processed_data = {}
    for entry in trend_data:
        for keyword, value in entry.items():
            if keyword == "date":
                continue
            values = processed_data.setdefault(keyword, [])
            values.append(value)

    for keyword, values in processed_data.items():
        try:
            avg = round(statistics.mean(values), 2)
            min_val, max_val = min(values), max(values)
            growth_rate = round((values[-1] - values[0]) / values[0] * 100, 2) if values[0] else 0
            processed_data[keyword] = {
                "average": avg,
                "min": min_val,
                "max": max_val,
                "growth_rate": growth_rate,
            }
        except Exception as e:
            logging.error(f"Error processing data for {keyword}: {e}")
    return processed_data

def generate_blog_prompts(processed_data, related_queries, news_headlines):
    """Generate blog prompts using processed data."""
    prompts = []
    for keyword, stats in processed_data.items():
        try:
            related = ", ".join(q.get("query", "unknown") for q in related_queries.get(keyword, [])[:5])
            news = "; ".join(f"{item.get('title')} ({item.get('source', 'unknown')})" for item in news_headlines.get(keyword, [])[:3])
            prompts.append(f"Write a detailed blog about '{keyword}' highlighting: {news}. Related topics: {related}.")
        except Exception as e:
            logging.error(f"Error generating prompt for {keyword}: {e}")
    return prompts
