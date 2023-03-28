from utils.utils import get_collection


async def search_users(query: str):
    """!@brief Search for a user in the database"""
    collection = get_collection("users")
    cursor = collection.aggregate([
        {
            "$search": {
                "index": "search_user",
                "compound": {
                    "should": [
                        {
                            "autocomplete": {
                                "query": query,
                                "path": "firstname",
                                "tokenOrder": "any",
                                "fuzzy": {}
                            }
                        },
                        {
                            "autocomplete": {
                                "query": query,
                                "path": "lastname",
                                "tokenOrder": "any",
                                "fuzzy": {}
                            }
                        },
                        {
                            "autocomplete": {
                                "query": query,
                                "path": "email",
                                "tokenOrder": "any",
                                "fuzzy": {}
                            }
                        }
                    ]
                }
            }
        },
        {
            "$project": {
                "firstname": 1,
                "lastname": 1,
                "email": 1,
                "image": 1,
                "_id": 0
            }
        }
    ])
    return list(cursor)
