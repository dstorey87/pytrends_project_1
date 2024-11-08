# File: modules/process_data.py

import logging
import statistics
import traceback

def process_trend_data(trend_data):
    """
    Process trend data and compute statistics like averages, min, max, and growth rate.

    Args:
        trend_data (list): List of dictionaries containing trend data.

    Returns:
        dict: Processed data with statistics for each keyword.
    """
    logging.info("Processing trend data.")
    processed_data = {}

    if not trend_data:
        logging.error("No trend data provided.")
        return processed_data

    # Transform the list of dictionaries into a dictionary with keywords as keys
    keyword_data = {}
    for entry in trend_data:
        for keyword, value in entry.items():
            if keyword != "date":  # Skip the date column
                keyword_data.setdefault(keyword, []).append(value)

    # Compute statistics for each keyword
    for keyword, values in keyword_data.items():
        if not values:
            logging.warning(f"No data available for keyword: {keyword}.")
            continue

        try:
            avg = round(statistics.mean(values), 2)
            min_val = min(values)
            max_val = max(values)
            growth_rate = (
                round(((values[-1] - values[0]) / values[0]) * 100, 2)
                if values[0] != 0 else 0
            )

            processed_data[keyword] = {
                "average": avg,
                "min": min_val,
                "max": max_val,
                "growth_rate": growth_rate,
            }
        except Exception as e:
            logging.error(f"Error processing data for keyword '{keyword}': {e}")
            traceback.print_exc()
            continue

    logging.info(f"Processed data: {processed_data}")
    return processed_data

def generate_blog_prompts(processed_data, related_queries, trending_topics):
    logging.info("Generating blog prompts.")
    prompts = []

    for keyword in processed_data.keys():
        try:
            # Fetch related queries or use trending topics
            queries = related_queries.get(keyword, [])
            if queries:
                # Extract related topics from queries
                topics = ", ".join([q.get("query", "unknown topic") for q in queries[:5]])
            else:
                # Exclude the keyword itself from trending topics
                filtered_topics = [topic for topic in trending_topics if topic != keyword]
                topics = ", ".join(filtered_topics[:5])

            # Build a specific blog prompt
            prompt = (
                f"Write a detailed and engaging article about '{keyword}', focusing on its significance and recent developments. "
                f"Include insights into how this topic is impacting society and any important events associated with it. "
                f"Also, discuss related topics such as {topics}. Provide valuable information for readers looking to stay updated."
            )
            prompts.append(prompt)
        except Exception as e:
            logging.error(f"Error generating prompt for keyword '{keyword}': {e}")
            traceback.print_exc()
            continue

    logging.info(f"Generated {len(prompts)} blog prompts.")
    return prompts
