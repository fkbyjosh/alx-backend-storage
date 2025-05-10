#!/usr/bin/env python3
"""
Module for working with MongoDB and student data
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    
    Args:
        mongo_collection: pymongo collection object
    
    Returns:
        List of students sorted by average score in descending order,
        with the average score added as a field
    """
    # Pipeline for the aggregation
    pipeline = [
        {
            "$addFields": {
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]
    
    # Execute the aggregation
    return list(mongo_collection.aggregate(pipeline))
