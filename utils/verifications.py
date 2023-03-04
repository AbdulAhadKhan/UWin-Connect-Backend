from ._mongo_connection import get_collection

def email_exists(email) -> bool:
    """!@brief Check if email exists in the database"""
    collection = get_collection("users")
    return collection.find_one({"email": email}) is not None
