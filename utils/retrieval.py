from utils.utils import get_collection


async def fetch_posts(name: str):
    filter = {"userid": name}
    collection = get_collection("posts")
    posts = collection.find(filter, {"userid": name})
    posts = str(list(posts))
    return posts
