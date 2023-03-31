from utils.utils import get_collection


async def fetch_n_posts_by_user_le_time(email: str, next_timestamp: str, page_size: int):
    collection = get_collection("posts")
    result = collection.aggregate([
        {
            '$sort': {
                'timestamp': -1
            }
        }, {
            '$match': {
                'email': email,
                'timestamp': {
                    '$lt': next_timestamp
                }
            }
        }, {
            '$limit': page_size
        }, {
            '$project': {
                'id': {
                    '$toString': '$_id'
                },
                'email': 1,
                'description': 1,
                'timestamp': 1,
                'image': 1,
                '_id': 0
            }
        }
    ])
    posts = list(result)
    last_timestamp = posts[-1]["timestamp"] if posts else None

    return posts, last_timestamp


async def fetch_user(name: str) -> dict:
    collection = get_collection("users")
    return collection.find_one({"email": name}, {"password": 0})


async def fetch_n_posts_by_friends(email, next_timestamp, page_size):
    collection = get_collection("users")
    friends = collection.find_one({"email": email}, {"friends": 1, "_id": 0})
    friends = friends.get("friends", [])
    friends.append(email)

    collection = get_collection("posts")
    result = collection.aggregate([
        {
            '$sort': {
                'timestamp': -1
            }
        }, {
            '$match': {
                'email': {
                    '$in': friends
                },
                'timestamp': {
                    '$lt': next_timestamp
                }
            }
        }, {
            '$limit': page_size
        }, {
            '$project': {
                'id': {
                    '$toString': '$_id'
                },
                'email': 1,
                'description': 1,
                'timestamp': 1,
                'image': 1,
                '_id': 0
            }
        }
    ])
    posts = list(result)
    last_timestamp = posts[-1]["timestamp"] if posts else None

    return posts, last_timestamp
