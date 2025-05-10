#!/usr/bin/env python3
"""
Provides stats about Nginx logs stored in MongoDB
and shows the top 10 most present IPs
"""
from pymongo import MongoClient


def log_stats():
    """
    Connect to MongoDB and display statistics about Nginx logs
    including the top 10 most frequent IP addresses
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Count total logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Count methods
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    # Count status check logs
    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check} status check")

    # Get top 10 IPs
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = nginx_collection.aggregate(pipeline)
    
    for ip_info in top_ips:
        print(f"    {ip_info['_id']}: {ip_info['count']}")


if __name__ == "__main__":
    log_stats()
