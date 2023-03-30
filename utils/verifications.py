from utils.utils import get_collection, compare_hashed_password


def email_exists(email) -> bool:
    """!@brief Check if email exists in the database"""
    collection = get_collection("users")
    return collection.find_one({"email": email}) is not None


def verify_password(email, password) -> bool:
    """!@brief Verify password for a given email"""
    collection = get_collection("users")
    hashed_password = collection.find_one({"email": email})["password"]
    return compare_hashed_password(password, hashed_password)


async def check_if_friends(email, friends_email):
    """!@brief Check if two users are friends"""
    collection = get_collection("users")
    cursor = collection.aggregate([
        {
            '$match': {
                'email': email,
                'friends': {
                    '$exists': True
                }
            }
        }, {
            '$project': {
                'areFriends': {
                    '$in': [
                        friends_email, '$friends'
                    ]
                },
                '_id': 0
            }
        }
    ])

    cursor = list(cursor)
    return False if len(cursor) == 0 else cursor[0]['areFriends']
