from app.api.getPostsList import get_posts_from_json

def get_post_by_id(post_id):
    posts = get_posts_from_json("./app/db/post_data.json")
    for post in posts:
        if post["time"] == post_id:
            return post
    return None