import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def seed_database():

    story_data = {
        "title": "Z-Day: New York",
        "description": "A quiet night in your 10th floor NYC apartment turns into a fight for survival. Every choice matters.",
        "status": "published"
    }
    
    r = requests.post(f"{BASE_URL}/stories", json=story_data)
    if r.status_code != 201:
        print(f"Error: ({r.status_code})")
        sys.exit(1)
    
    story = r.json()
    story_id = story['id']
    print(f"Story Created: '{story['title']}' (ID: {story_id})")

    p_start_data = {
        "text": "You are lounging on your couch, half-watching a rerun of 'Friends' and destroying a bag of Spicy Nacho Doritos. Outside, the NYC traffic hums as usual.\n\nSuddenly, the screen cuts to black. An Emergency Broadcast System tone screams through the speakers.\n\n'CIVIL DANGER WARNING. FATAL CONTAGION REPORTED IN MIDTOWN. DO NOT ATTEMPT TO LEAVE YOUR HOMES. INFECTED ARE EXTREMELY AGGRESSIVE.'\n\nYou look out your 10th-floor window. Down on the street, people are running. Screaming.",
        "is_ending": False
    }
    p_start = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_start_data).json()

    # PATH A: BUNKER DOWN
    p_bunker_data = {
        "text": "You slam the window shut and lock the deadbolt. You're safer inside. You push the couch against the door.\n\nHours pass. You hear running footsteps in the hallway, then pounding on your neighbor's door. Then, silence.\n\nYou have limited food. Do you wait it out or check the hallway?",
        "is_ending": False
    }
    p_bunker = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_bunker_data).json()

    # PATH B: RUN TO FRIEND
    p_friend_data = {
        "text": "Your friend Marcus lives three blocks away in a fortified brownstone. If anyone has guns and canned beans, it's him.\n\nYou grab your baseball bat and sprint into the hallway. The elevator is doused in blood. You take the stairs. On the 4th floor, you see a figure hunched over a body.",
        "is_ending": False
    }
    p_friend = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_friend_data).json()

    # PATH C: EVACUATE
    p_evac_data = {
        "text": "Panic takes over. You need to get out of the city NOW. You grab your keys and run for the fire escape.\n\nThe metal ladder rattles as you descend. Below, the alleyway is chaos. A military truck is plowing through cars on the main avenue.",
        "is_ending": False
    }
    p_evac = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_evac_data).json()

    # ENDING 1: THE STARVATION (From Bunker)
    p_starve_data = {
        "text": "You wait. And wait. The screaming outside stops eventually. You run out of chips after 3 days. Water shuts off after 5.\n\nWeak and dehydrated, you eventually unlock the door. They were waiting in the hall.",
        "is_ending": True,
        "ending_label": "The Silent End"
    }
    p_starve = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_starve_data).json()

    # ENDING 2: THE SURVIVOR (From Bunker)
    p_scavenge_data = {
        "text": "You carefully open the door. The hallway is empty. You raid the neighbor's apartment and find a stockpile of water and a ham radio. You hear a voice on the radio: 'Safe zone established at Central Park.' You have a chance.",
        "is_ending": True,
        "ending_label": "Hope Remains"
    }
    p_scavenge = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_scavenge_data).json()

    # ENDING 3: THE FIGHT (From Friend)
    p_fight_data = {
        "text": "You swing the bat! It connects with a sickening crunch. The infected neighbor goes down. Adrenaline surging, you sprint out the lobby door and make it to Marcus's place. He opens the door, armed to the teeth. 'Took you long enough,' he grins.",
        "is_ending": True,
        "ending_label": "Team Up"
    }
    p_fight = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_fight_data).json()

    # ENDING 4: THE SWARM (From Friend)
    p_sneak_data = {
        "text": "You try to sneak past. You step on a discarded squeaky toy. The figure snaps its head around. It screeches. Doors open all around you. You are swarmed before you can reach the stairs.",
        "is_ending": True,
        "ending_label": "Overwhelmed"
    }
    p_sneak = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_sneak_data).json()

    # ENDING 5: THE ESCAPE (From Evac)
    p_chopper_data = {
        "text": "You ignore the street and climb back UP to the roof. A news helicopter is hovering low, looking for a place to land. You wave your arms. The pilot spots you! He lowers a rope ladder. As you fly away, you watch the city burn.",
        "is_ending": True,
        "ending_label": "Aerial Extraction"
    }
    p_chopper = requests.post(f"{BASE_URL}/stories/{story_id}/pages", json=p_chopper_data).json()

    print(f"Created 9 Pages")

    # 3. Link Start Page
    requests.put(f"{BASE_URL}/stories/{story_id}", json={"start_page_id": p_start['id']})
    print(f"Linked Start Page")

    # 4. Create Choices (The Branching Logic)
    
    # Choices for Start Page
    requests.post(f"{BASE_URL}/pages/{p_start['id']}/choices", json={
        "text": "Stay inside and barricade the door", 
        "next_page_id": p_bunker['id']
    })
    requests.post(f"{BASE_URL}/pages/{p_start['id']}/choices", json={
        "text": "Run to Marcus's house (3 blocks away)", 
        "next_page_id": p_friend['id']
    })
    requests.post(f"{BASE_URL}/pages/{p_start['id']}/choices", json={
        "text": "Evacuate the city immediately via Fire Escape", 
        "next_page_id": p_evac['id']
    })

    # Choices for Bunker Path
    requests.post(f"{BASE_URL}/pages/{p_bunker['id']}/choices", json={
        "text": "Keep waiting. It's too dangerous.", 
        "next_page_id": p_starve['id']
    })
    requests.post(f"{BASE_URL}/pages/{p_bunker['id']}/choices", json={
        "text": "Risk it. Scavenge the hallway.", 
        "next_page_id": p_scavenge['id']
    })

    # Choices for Friend Path
    requests.post(f"{BASE_URL}/pages/{p_friend['id']}/choices", json={
        "text": "Attack the infected neighbor!", 
        "next_page_id": p_fight['id']
    })
    requests.post(f"{BASE_URL}/pages/{p_friend['id']}/choices", json={
        "text": "Try to sneak past quietly", 
        "next_page_id": p_sneak['id']
    })

    # Choices for Evac Path
    requests.post(f"{BASE_URL}/pages/{p_evac['id']}/choices", json={
        "text": "Climb up to the roof instead!", 
        "next_page_id": p_chopper['id']
    })
    requests.post(f"{BASE_URL}/pages/{p_evac['id']}/choices", json={
        "text": "Jump down to the alley and run", 
        "next_page_id": p_sneak['id'] # Reusing the 'Overwhelmed' ending for efficiency
    })

    print(f"Created Choices")
    print("\nZ-Day is ready to play!")

if __name__ == "__main__":
    seed_database()