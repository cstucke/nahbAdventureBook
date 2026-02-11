import requests

BASE_URL = "http://127.0.0.1:5000"

def seed_database():

    story_data = {
        "title": "Z-Day",
        "description": "Your TV flashes: ALERT! Zombie outbreak! Find shelter immediately. Expect further correspondence briefly.",
        "status": "published"
    }
    r = requests.post(f"{BASE_URL}/stories", json=story_data)
    if r.status_code != 201:
        print(f"Story creation failed")
        return
    
    story = r.json()
    print(f"Created creation succeeded")


if __name__ == "__main__":
    seed_database()