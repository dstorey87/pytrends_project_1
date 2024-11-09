import logging
import traceback
import os
import requests

# Import functions from modules
from modules.fetch_trends import fetch_basic_trends, fetch_related_queries, fetch_top_trending_topics, fetch_news_headlines
from modules.process_data import process_trend_data, generate_blog_prompts
from modules.utils import save_data


def generate_blog_content(prompt):
    """Generate blog content using the running model server."""
    try:
        response = requests.post("http://127.0.0.1:5000/generate", json={"prompt": prompt, "max_length": 1500})
        response.raise_for_status()
        return response.json().get("text", "")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with the model server: {e}")
        return None


def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Starting trend processing and blog generation.")

    # Fetch top trending topics
    try:
        trending_topics = fetch_top_trending_topics()
        if not trending_topics:
            logging.error("No top trending topics fetched. Exiting.")
            return
        logging.info(f"Successfully fetched top trending topics: {trending_topics[:5]}")
    except Exception as e:
        logging.error(f"Error fetching trending topics: {e}")
        traceback.print_exc()
        return

    # Use top N trending topics as keywords
    keywords = trending_topics[:5]
    timeframe = "now 7-d"  # Last 7 days

    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Fetch trends data
    try:
        basic_trends = fetch_basic_trends(keywords, timeframe)
        if not basic_trends:
            logging.error("No basic trends data fetched. Exiting.")
            return
        logging.info("Successfully fetched basic trends data.")
    except Exception as e:
        logging.error(f"Error fetching basic trends data: {e}")
        traceback.print_exc()
        return

    # Fetch related queries
    related_queries = {}
    for keyword in keywords:
        try:
            queries = fetch_related_queries(keyword)
            if not queries:
                logging.warning(f"No related queries found for {keyword}.")
            related_queries[keyword] = queries
            logging.info(f"Successfully fetched related queries for {keyword}.")
        except Exception as e:
            logging.error(f"Error fetching related queries for {keyword}: {e}")
            traceback.print_exc()

    # Fetch news headlines for correlation
    try:
        news_headlines = fetch_news_headlines(keywords)
        if not news_headlines:
            logging.warning("No news headlines fetched.")
        else:
            logging.info("Successfully fetched and correlated news headlines.")
    except Exception as e:
        logging.error(f"Error fetching news headlines: {e}")
        traceback.print_exc()

    # Save data for debugging if needed
    try:
        save_data(os.path.join(output_dir, "basic_trends.json"), basic_trends)
        save_data(os.path.join(output_dir, "related_queries.json"), related_queries)
        save_data(os.path.join(output_dir, "trending_topics.json"), trending_topics)
        save_data(os.path.join(output_dir, "news_headlines.json"), news_headlines)
        logging.info("Saved fetched data to output files.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        traceback.print_exc()

    # Process trend data
    try:
        processed_data = process_trend_data(basic_trends)
        if not processed_data:
            logging.error("Processed data is empty. Exiting.")
            return
        logging.info("Processed trend data successfully.")
    except Exception as e:
        logging.error(f"Error processing trend data: {e}")
        traceback.print_exc()
        return

    # Generate blog prompts
    try:
        blog_prompts = generate_blog_prompts(processed_data, related_queries, news_headlines)
        if not blog_prompts:
            logging.error("No blog prompts generated. Exiting.")
            return
        logging.info("Generated blog prompts successfully.")
    except Exception as e:
        logging.error(f"Error generating blog prompts: {e}")
        traceback.print_exc()
        return

    # Generate blogs
    for i, prompt in enumerate(blog_prompts[:3], 1):  # Generate 3 blogs
        try:
            logging.info(f"Generating blog {i} with prompt: {prompt}")
            blog_content = generate_blog_content(prompt)
            if not blog_content:
                logging.error(f"Failed to generate content for blog {i}.")
                continue
            blog_path = os.path.join(output_dir, f"blog_{i}.txt")
            with open(blog_path, 'w', encoding='utf-8') as f:
                f.write(blog_content)
            logging.info(f"Saved blog {i} to {blog_path}")

            # Print blog content to console
            print(f"\n--- Blog {i} ---\n")
            print(blog_content)
            print("\n--- End of Blog ---\n")
        except Exception as e:
            logging.error(f"Error generating blog {i}: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
