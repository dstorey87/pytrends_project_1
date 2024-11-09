# File: main.py

import logging
import traceback
import os

# Import functions from modules
from modules.fetch_trends import fetch_basic_trends, fetch_related_queries, fetch_top_trending_topics
from modules.process_data import process_trend_data, generate_blog_prompts
from modules.ai_models import initialize_generator, generate_blog_content
from modules.utils import save_data

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

    # Save data for debugging if needed
    try:
        save_data(os.path.join(output_dir, "basic_trends.json"), basic_trends)
        save_data(os.path.join(output_dir, "related_queries.json"), related_queries)
        save_data(os.path.join(output_dir, "trending_topics.json"), trending_topics)
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
        blog_prompts = generate_blog_prompts(processed_data, related_queries, trending_topics)
        if not blog_prompts:
            logging.error("No blog prompts generated. Exiting.")
            return
        logging.info("Generated blog prompts successfully.")
    except Exception as e:
        logging.error(f"Error generating blog prompts: {e}")
        traceback.print_exc()
        return

    # Initialize language generation model
    model_path = r"F:\models\gpt-j-6b\models--EleutherAI--gpt-j-6B\snapshots\47e169305d2e8376be1d31e765533382721b2cc1"
    offload_folder = "F:/models/offload"
    try:
        generator = initialize_generator(model_path, offload_folder=offload_folder)
        if generator is None:
            logging.error("Generator model initialization failed. Exiting.")
            return
    except Exception as e:
        logging.error(f"Error initializing generator model: {e}")
        traceback.print_exc()
        return

    # Generate blogs
    for i, prompt in enumerate(blog_prompts, 1):
        try:
            logging.info(f"Generating blog {i} with prompt: {prompt}")
            blog_content = generate_blog_content(generator, prompt)
            if blog_content is None:
                logging.error(f"Failed to generate content for blog {i}.")
                continue
            blog_path = os.path.join(output_dir, f"blog_{i}.txt")
            with open(blog_path, 'w', encoding='utf-8') as f:
                f.write(blog_content)
            logging.info(f"Saved blog {i} to {blog_path}")

            # Print to console for easy copying
            print(f"\n--- Blog {i} ---\n")
            print(blog_content)
            print("\n--- End of Blog ---\n")
        except Exception as e:
            logging.error(f"Error generating blog {i}: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    main()
