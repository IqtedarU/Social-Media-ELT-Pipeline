# config.py

# Reddit API credentials and settings
reddit_config = {
    "client_id": "",
    "client_secret": "",
    "username": "",,
    "user_agent": "scraper by u/popdell",
    "subreddit": "dataengineering", 
    "limit": 50,  # Limit of posts to retrieve
    "sort_by": "hot"  # Sorting order: hot, new, top
}

# Kafka settings (for future usage)
kafka_config = {
    "topic": "reddit-topic",
    "bootstrap_servers": "localhost:9092"
}

# Spark settings (for future usage)
spark_config = {
    "app_name": "reddit-scraper",
    "master": "local[*]"
}

# Storage paths (HDFS, local media storage paths, etc.)
storage_config = {
    "hdfs_path": "/path/to/hdfs",
    "media_storage_path": "/path/to/media_storage"
}

# Output format (can be ORC, Parquet, etc.)
output_config = {
    "type": "orc"  # Can be 'parquet', 'orc', 'json'
}
