import praw
import json
import argparse
import sys

# Set stdout to UTF-8 encoding to handle Unicode characters
sys.stdout.reconfigure(encoding='utf-8')

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
    client_id="t9nZjakaCPv10i1e1hlB1w",
    client_secret="juN28QiOx1-XJnepphlWneka1z_FaA",
    user_agent="script:beyondchats_internship:v1.0 (by /u/Downtown_Spite_530)"
)

def scrape_reddit_data(username):
    """Scrape posts and comments for a given Reddit username."""
    user = reddit.redditor(username)
    data = {
        "posts": [],
        "comments": []
    }
    try:
        for submission in user.submissions.new(limit=10):
            data["posts"].append({
                "title": submission.title,
                "body": submission.selftext,
                "url": submission.url,
                "id": submission.id
            })
        for comment in user.comments.new(limit=20):
            data["comments"].append({
                "body": comment.body,
                "url": f"https://www.reddit.com{comment.permalink}",
                "id": comment.id
            })
    except Exception as e:
        print(f"Error scraping data: {e}")
    return data

def save_data(data, username):
    """Save scraped data to a JSON file."""
    with open(f"{username}_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {username}_data.json")

def main():
    # Parse command line argument for Reddit user profile URL
    parser = argparse.ArgumentParser(description="Scrape Reddit data for a user.")
    parser.add_argument("url", help="Reddit user profile URL (e.g., https://www.reddit.com/user/kojied/)")
    args = parser.parse_args()
    
    # Extract username from URL
    username = args.url.split("/user/")[1].split("/")[0]
    
    # Scrape data
    print(f"Scraping data for {username}...")
    data = scrape_reddit_data(username)

    # Print scraped data for debugging
    print("\n--- Scraped Posts ---")
    for post in data["posts"]:
        try:
            print(f"Title: {post['title']}")
            print(f"Body Type: {type(post['body'])}, Body: {post['body'][:100]}...")  # First 100 chars
        except UnicodeEncodeError:
            print(f"Title: {post['title'].encode('utf-8', errors='replace').decode('utf-8')}")
            print(f"Body Type: {type(post['body'])}, Body: {post['body'][:100].encode('utf-8', errors='replace').decode('utf-8')}...")
        print("-" * 20)

    print("\n--- Scraped Comments ---")
    for comment in data["comments"]:
        try:
            print(f"Body Type: {type(comment['body'])}, Body: {comment['body'][:100]}...")  # First 100 chars
        except UnicodeEncodeError:
            print(f"Body Type: {type(comment['body'])}, Body: {comment['body'][:100].encode('utf-8', errors='replace').decode('utf-8')}...")
        print("-" * 20)

    # Save data
    save_data(data, username)
    print("Done!")

if __name__ == "__main__":
    main()