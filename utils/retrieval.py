from utils.utils import get_collection


async def fetch_posts(name: str):
    filter = {"userid": name}
    collection = get_collection("posts")
    posts = collection.find(filter, {"userid": name})
    posts = str(list(posts))
    return posts

async def fetch_user(name: str) -> dict:
    collection = get_collection("users")
    return collection.find_one({"email": name}, {"_id": 0, "password": 0})
