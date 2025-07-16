'''
import praw
import argparse
import sys

# Set stdout to UTF-8 encoding to handle Unicode characters
sys.stdout.reconfigure(encoding='utf-8')

# Reddit API credentials (replace with your own if needed, these are placeholders)
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
        "comments": [],
        "citations": {}
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

def build_persona(data, username):
    """Build a user persona based on scraped data."""
    persona = {
        "citations": {}
    }

    # Basic Info
    persona["name"] = username
    persona["age"] = "Unknown"
    persona["occupation"] = "Unknown"
    persona["location"] = "Unknown"
    persona["tier"] = "Unknown"
    persona["archetype"] = "Unknown"
    for post in data["posts"]:
        if "body" in post and post["body"] and isinstance(post["body"], str):
            text = post["body"].lower()
            if "lucknow" in text or "lko" in text:
                persona["location"] = "Lucknow, India"
                persona["citations"]["location"] = post["url"]
            if "business" in text:
                persona["occupation"] = "Possible business professional"
                persona["citations"]["occupation"] = post["url"]
            if "new" in text or "shift" in text:
                persona["tier"] = "Early Adopters"
                persona["archetype"] = "The Explorer"
                persona["citations"]["tier_archetype"] = post["url"]

    # Motivations
    motivations = {"convenience": 0, "wellness": 0, "speed": 0, "preferences": 0, "comfort": 0, "dietary needs": 0}
    keywords = {
        "convenience": ["easy", "quick"],
        "wellness": ["healthy", "well", "power"],
        "speed": ["fast", "quick"],
        "preferences": ["like", "prefer", "love"],
        "comfort": ["relax", "enjoy", "cozy", "power"],
        "dietary needs": ["diet", "vegan", "eat", "food", "meal", "cook", "menu", "nutrition"]
    }
    for item in data["posts"] + data["comments"]:
        text = item.get("body", "").lower()
        if text and isinstance(text, str):
            for mot, kw in keywords.items():
                if any(k in text for k in kw):
                    motivations[mot] += 1
    persona["motivations"] = {k: min(v, 5) for k, v in motivations.items()}

    # Personality
    persona["personality"] = {
        "introvert/extrovert": "Neutral",
        "intuition/sensing": "Neutral",
        "feeling/thinking": "Neutral",
        "perceiving/judging": "Neutral"
    }
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if "😂" in text or "great" in text:
            persona["personality"]["feeling/thinking"] = "Feeling"
        if "new" in text or "shift" in text:
            persona["personality"]["intuition/sensing"] = "Intuition"

    # Behavior & Habits
    habits = []
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if ("cook" in text or "menu" in text) and "habits_cook" not in persona["citations"]:
            habits.append("Explores healthy cooking habits")
            for c in data["comments"]:  # Find the first matching comment
                if ("cook" in c.get("body", "").lower() or "menu" in c.get("body", "").lower()):
                    persona["citations"]["habits_cook"] = c["url"]
                    break
        if ("lucknow" in text or "delhi" in text) and "habits_community" not in persona["citations"]:
            habits.append("Engages in community discussions")
            for c in data["comments"]:  # Find the first matching comment
                if ("lucknow" in c.get("body", "").lower() or "delhi" in c.get("body", "").lower()):
                    persona["citations"]["habits_community"] = c["url"]
                    break
    persona["behavior_habits"] = habits if habits else ["No clear habits identified"]

    # Frustrations
    frustrations = []
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if ("cop" in text or "fine" in text or "bribe" in text) and "frustrations_law" not in persona["citations"]:
            frustrations.append("Expresses frustration with law enforcement")
            for c in data["comments"]:  # Find the first matching comment
                if ("cop" in c.get("body", "").lower() or "fine" in c.get("body", "").lower() or "bribe" in c.get("body", "").lower()):
                    persona["citations"]["frustrations_law"] = c["url"]
                    break
    persona["frustrations"] = frustrations if frustrations else ["No clear frustrations identified"]

    # Goals & Needs
    goals = []
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if ("cook" in text or "healthy" in text) and "goals_diet" not in persona["citations"]:
            goals.append("Aims to improve dietary habits")
            for c in data["comments"]:  # Find the first matching comment
                if ("cook" in c.get("body", "").lower() or "healthy" in c.get("body", "").lower()):
                    persona["citations"]["goals_diet"] = c["url"]
                    break
        if ("lucknow" in text or "shift" in text) and "goals_adapt" not in persona["citations"]:
            goals.append("Seeks to adapt to new environment")
            for p in data["posts"]:  # Use post if comment lacks match
                if "body" in p and "shift" in p["body"].lower():
                    persona["citations"]["goals_adapt"] = p["url"]
                    break
            if "goals_adapt" not in persona["citations"]:  # Fallback to first comment with "lucknow"
                for c in data["comments"]:
                    if "lucknow" in c.get("body", "").lower():
                        persona["citations"]["goals_adapt"] = c["url"]
                        break
    persona["goals_needs"] = goals if goals else ["No clear goals identified"]

    # Quote
    top_motivation = max(persona["motivations"], key=persona["motivations"].get)
    persona["quote"] = f"I want to improve my {top_motivation} experience."

    return persona

def write_persona_to_file(persona, username):
    """Write persona to a text file with citations using UTF-8 encoding."""
    with open(f"{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(f"Name: {persona['name']}\n")
        f.write(f"Age: {persona['age']}\n")
        f.write(f"Occupation: {persona['occupation']} (Source: {persona['citations'].get('occupation', 'N/A')})\n")
        f.write(f"Location: {persona['location']} (Source: {persona['citations'].get('location', 'N/A')})\n")
        f.write(f"Tier: {persona['tier']} (Source: {persona['citations'].get('tier_archetype', 'N/A')})\n")
        f.write(f"Archetype: {persona['archetype']} (Source: {persona['citations'].get('tier_archetype', 'N/A')})\n\n")

        f.write("Motivations:\n")
        for mot, score in persona["motivations"].items():
            f.write(f"- {mot}: {'█' * score} (Score: {score}/5)\n")

        f.write("\nPersonality:\n")
        for trait, value in persona["personality"].items():
            f.write(f"- {trait.replace('/', ' / ')}: {'█' * (5 if value == 'Neutral' else 3)} {value}\n")

        f.write("\nBehavior & Habits:\n")
        for habit in persona["behavior_habits"]:
            if habit == "Explores healthy cooking habits":
                source_key = "habits_cook"
            elif habit == "Engages in community discussions":
                source_key = "habits_community"
            else:
                source_key = "N/A"
            f.write(f"- {habit} (Source: {persona['citations'].get(source_key, 'N/A')})\n")

        f.write("\nFrustrations:\n")
        for frust in persona["frustrations"]:
            if frust == "Expresses frustration with law enforcement":
                source_key = "frustrations_law"
            f.write(f"- {frust} (Source: {persona['citations'].get(source_key, 'N/A')})\n")

        f.write("\nGoals & Needs:\n")
        for goal in persona["goals_needs"]:
            if goal == "Aims to improve dietary habits":
                source_key = "goals_diet"
            elif goal == "Seeks to adapt to new environment":
                source_key = "goals_adapt"
            f.write(f"- {goal} (Source: {persona['citations'].get(source_key, 'N/A')})\n")

        f.write(f"\nQuote:\n{persona['quote']}\n")

def main():
    # Parse command line argument for Reddit user profile URL
    parser = argparse.ArgumentParser(description="Generate a user persona from Reddit data.")
    parser.add_argument("url", help="Reddit user profile URL (e.g., https://www.reddit.com/user/kojied/)")
    args = parser.parse_args()
    
    # Extract username from URL
    username = args.url.split("/user/")[1].split("/")[0]
    
    # Scrape data
    print(f"Scraping data for {username}...")
    data = scrape_reddit_data(username)

    # Print scraped data for debugging with error handling for Unicode
    print("\n--- Scraped Posts ---")
    for post in data["posts"]:
        try:
            print(f"Title: {post['title']}")
            print(f"Body Type: {type(post['body'])}, Body: {post['body'][:100]}...")  # Print type and first 100 chars
        except UnicodeEncodeError:
            print(f"Title: {post['title'].encode('utf-8', errors='replace').decode('utf-8')}")
            print(f"Body Type: {type(post['body'])}, Body: {post['body'][:100].encode('utf-8', errors='replace').decode('utf-8')}...")
        print("-" * 20)

    print("\n--- Scraped Comments ---")
    for comment in data["comments"]:
        try:
            print(f"Body Type: {type(comment['body'])}, Body: {comment['body'][:100]}...")  # Print type and first 100 chars
        except UnicodeEncodeError:
            print(f"Body Type: {type(comment['body'])}, Body: {comment['body'][:100].encode('utf-8', errors='replace').decode('utf-8')}...")
        print("-" * 20)

    # Build persona
    print("Building persona...")
    persona = build_persona(data, username)

    # Write to file
    print(f"Writing persona to {username}_persona.txt...")
    write_persona_to_file(persona, username)
    print("Done!")

if __name__ == "__main__":
    main()
    '''
import praw
import argparse
import sys

# Set stdout to UTF-8 encoding to handle Unicode characters
sys.stdout.reconfigure(encoding='utf-8')

# Reddit API credentials (replace with your own if needed, these are placeholders)
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
        "comments": [],
        "citations": {}
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

def build_persona(data, username):
    """Build a user persona based on scraped data."""
    persona = {
        "citations": {}
    }

    # Basic Info
    persona["name"] = username
    persona["age"] = "Unknown"
    persona["occupation"] = "Unknown"
    persona["location"] = "Unknown"
    persona["tier"] = "Unknown"
    persona["archetype"] = "Unknown"
    for post in data["posts"]:
        if "body" in post and post["body"] and isinstance(post["body"], str):
            text = post["body"].lower()
            if "lucknow" in text or "lko" in text:
                persona["location"] = "Lucknow, India"
                persona["citations"]["location"] = post["url"]
            if "business" in text:
                persona["occupation"] = "Possible business professional"
                persona["citations"]["occupation"] = post["url"]
            if "new" in text or "shift" in text:
                persona["tier"] = "Early Adopters"
                persona["archetype"] = "The Explorer"
                persona["citations"]["tier_archetype"] = post["url"]

    # Motivations
    motivations = {"convenience": 0, "wellness": 0, "speed": 0, "preferences": 0, "comfort": 0, "dietary needs": 0}
    keywords = {
        "convenience": ["easy", "quick"],
        "wellness": ["healthy", "well", "power"],
        "speed": ["fast", "quick"],
        "preferences": ["like", "prefer", "love"],
        "comfort": ["relax", "enjoy", "cozy", "power"],
        "dietary needs": ["diet", "vegan", "eat", "food", "meal", "cook", "menu", "nutrition"]
    }
    for item in data["posts"] + data["comments"]:
        text = item.get("body", "").lower()
        if text and isinstance(text, str):
            for mot, kw in keywords.items():
                if any(k in text for k in kw):
                    motivations[mot] += 1
    persona["motivations"] = {k: min(v, 5) for k, v in motivations.items()}

    # Personality
    persona["personality"] = {
        "introvert/extrovert": "Neutral",
        "intuition/sensing": "Neutral",
        "feeling/thinking": "Neutral",
        "perceiving/judging": "Neutral"
    }
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if "😂" in text or "great" in text:
            persona["personality"]["feeling/thinking"] = "Feeling"
        if "new" in text or "shift" in text:
            persona["personality"]["intuition/sensing"] = "Intuition"

    # Behavior & Habits
    habits = []
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if ("cook" in text or "menu" in text) and "habits_cook" not in persona["citations"]:
            habits.append("Explores healthy cooking habits")
            for c in data["comments"]:
                if ("cook" in c.get("body", "").lower() or "menu" in c.get("body", "").lower()):
                    persona["citations"]["habits_cook"] = c["url"]
                    break
        if ("lucknow" in text or "delhi" in text) and "habits_community" not in persona["citations"]:
            habits.append("Engages in community discussions")
            for c in data["comments"]:
                if ("lucknow" in c.get("body", "").lower() or "delhi" in c.get("body", "").lower()):
                    persona["citations"]["habits_community"] = c["url"]
                    break
    persona["behavior_habits"] = habits if habits else ["No clear habits identified"]

    # Frustrations
    frustrations = []
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if ("cop" in text or "fine" in text or "bribe" in text) and "frustrations_law" not in persona["citations"]:
            frustrations.append("Expresses frustration with law enforcement")
            for c in data["comments"]:
                if ("cop" in c.get("body", "").lower() or "fine" in c.get("body", "").lower() or "bribe" in c.get("body", "").lower()):
                    if "lucknow" in c.get("body", "").lower():  # Prioritize LKO-related comments
                        persona["citations"]["frustrations_law"] = c["url"]
                        break
            if "frustrations_law" not in persona["citations"]:  # Fallback to first match
                for c in data["comments"]:
                    if ("cop" in c.get("body", "").lower() or "fine" in c.get("body", "").lower() or "bribe" in c.get("body", "").lower()):
                        persona["citations"]["frustrations_law"] = c["url"]
                        break
    persona["frustrations"] = frustrations if frustrations else ["No clear frustrations identified"]

    # Goals & Needs
    goals = []
    for comment in data["comments"]:
        text = comment.get("body", "").lower()
        if ("cook" in text or "healthy" in text) and "goals_diet" not in persona["citations"]:
            goals.append("Aims to improve dietary habits")
            for c in data["comments"]:
                if ("cook" in c.get("body", "").lower() or "healthy" in c.get("body", "").lower()):
                    persona["citations"]["goals_diet"] = c["url"]
                    break
        if ("lucknow" in text or "shift" in text) and "goals_adapt" not in persona["citations"]:
            goals.append("Seeks to adapt to new environment")
            for p in data["posts"]:
                if "body" in p and "shift" in p["body"].lower():
                    persona["citations"]["goals_adapt"] = p["url"]
                    break
            if "goals_adapt" not in persona["citations"]:
                for c in data["comments"]:
                    if "lucknow" in c.get("body", "").lower() or "shift" in c.get("body", "").lower():
                        persona["citations"]["goals_adapt"] = c["url"]
                        break
    persona["goals_needs"] = goals if goals else ["No clear goals identified"]

    # Quote
    top_motivation = max(persona["motivations"], key=persona["motivations"].get)
    persona["quote"] = f"I want to improve my {top_motivation} experience."

    return persona

def write_persona_to_file(persona, username):
    """Write persona to a text file with citations using UTF-8 encoding."""
    with open(f"{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(f"Name: {persona['name']}\n")
        f.write(f"Age: {persona['age']}\n")
        f.write(f"Occupation: {persona['occupation']} (Source: {persona['citations'].get('occupation', 'N/A')})\n")
        f.write(f"Location: {persona['location']} (Source: {persona['citations'].get('location', 'N/A')})\n")
        f.write(f"Tier: {persona['tier']} (Source: {persona['citations'].get('tier_archetype', 'N/A')})\n")
        f.write(f"Archetype: {persona['archetype']} (Source: {persona['citations'].get('tier_archetype', 'N/A')})\n\n")

        f.write("Motivations:\n")
        for mot, score in persona["motivations"].items():
            f.write(f"- {mot}: {'█' * score} (Score: {score}/5)\n")

        f.write("\nPersonality:\n")
        for trait, value in persona["personality"].items():
            f.write(f"- {trait.replace('/', ' / ')}: {'█' * (5 if value == 'Neutral' else 3)} {value}\n")

        f.write("\nBehavior & Habits:\n")
        for habit in persona["behavior_habits"]:
            if habit == "Explores healthy cooking habits":
                source_key = "habits_cook"
            elif habit == "Engages in community discussions":
                source_key = "habits_community"
            else:
                source_key = "N/A"
            f.write(f"- {habit} (Source: {persona['citations'].get(source_key, 'N/A')})\n")

        f.write("\nFrustrations:\n")
        for frust in persona["frustrations"]:
            if frust == "Expresses frustration with law enforcement":
                source_key = "frustrations_law"
            f.write(f"- {frust} (Source: {persona['citations'].get(source_key, 'N/A')})\n")

        f.write("\nGoals & Needs:\n")
        for goal in persona["goals_needs"]:
            if goal == "Aims to improve dietary habits":
                source_key = "goals_diet"
            elif goal == "Seeks to adapt to new environment":
                source_key = "goals_adapt"
            f.write(f"- {goal} (Source: {persona['citations'].get(source_key, 'N/A')})\n")

        f.write(f"\nQuote:\n{persona['quote']}\n")

def main():
    # Parse command line argument for Reddit user profile URL
    parser = argparse.ArgumentParser(description="Generate a user persona from Reddit data.")
    parser.add_argument("url", help="Reddit user profile URL (e.g., https://www.reddit.com/user/kojied/)")
    args = parser.parse_args()
    
    # Extract username from URL
    username = args.url.split("/user/")[1].split("/")[0]
    
    # Scrape data
    print(f"Scraping data for {username}...")
    data = scrape_reddit_data(username)

    # Print scraped data for debugging with error handling for Unicode
    print("\n--- Scraped Posts ---")
    for post in data["posts"]:
        try:
            print(f"Title: {post['title']}")
            print(f"Body Type: {type(post['body'])}, Body: {post['body'][:100]}...")  # Print type and first 100 chars
        except UnicodeEncodeError:
            print(f"Title: {post['title'].encode('utf-8', errors='replace').decode('utf-8')}")
            print(f"Body Type: {type(post['body'])}, Body: {post['body'][:100].encode('utf-8', errors='replace').decode('utf-8')}...")
        print("-" * 20)

    print("\n--- Scraped Comments ---")
    for comment in data["comments"]:
        try:
            print(f"Body Type: {type(comment['body'])}, Body: {comment['body'][:100]}...")  # Print type and first 100 chars
        except UnicodeEncodeError:
            print(f"Body Type: {type(comment['body'])}, Body: {comment['body'][:100].encode('utf-8', errors='replace').decode('utf-8')}...")
        print("-" * 20)

    # Build persona
    print("Building persona...")
    persona = build_persona(data, username)

    # Write to file
    print(f"Writing persona to {username}_persona.txt...")
    write_persona_to_file(persona, username)
    print("Done!")

if __name__ == "__main__":
    main()