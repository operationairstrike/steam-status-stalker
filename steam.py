import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def check_steam_status(steam_id):
    url = f"https://steamcommunity.com/profiles/{steam_id}?l=english"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    status_indicators = [
        soup.find('div', {'class': 'profile_in_game_header'}),
        soup.find('div', {'class': 'profile_in_game_name'}),
        soup.find('div', {'class': 'profile_online_status'}),
        soup.find('div', {'class': 'persona_name'})
    ]
    
    for indicator in status_indicators:
        if indicator:
            text = indicator.text.lower()
            if 'currently in-game' in text or 'in-game' in text:
                return 'in-game'
            elif 'online' in text:
                return 'online'
            elif 'offline' in text:
                return 'offline'
    
    return 'unknown'

def log_status(steam_id, log_file):
    last_status = None
    while True:
        try:
            current_status = check_steam_status(steam_id)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if current_status != last_status:
                log_entry = f"{current_time} : User username_here is now {current_status}\n"
                
                with open(log_file, 'a') as f:
                    f.write(log_entry)
                
                print(log_entry.strip())
            
            last_status = current_status
        except Exception as e:
            print(f"Error occurred: {e}")
        
        time.sleep(60)  # Wait for 1 minute

if __name__ == "__main__":
    STEAM_ID = "YOUR_STEAM_ID"  # Replace with the Steam ID you want to track
    LOG_FILE = "steam_user_log.txt"
    
    log_status(STEAM_ID, LOG_FILE)
