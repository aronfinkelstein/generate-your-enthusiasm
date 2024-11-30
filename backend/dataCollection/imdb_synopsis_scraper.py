import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import time
import random

class IMDbSynopsisFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.synopses = {}  # Store synopses in memory
        
    def get_imdb_synopsis(self, episode_id):
        """Fetch synopsis for a single episode."""
        url = f"https://www.imdb.com/title/{episode_id}/plotsummary/?ref_=tt_stry_pl#synopsis"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            synopsis_section = soup.find('div', {'data-testid': 'sub-section-synopsis'})
            
            if synopsis_section:
                synopsis_content = synopsis_section.find('div', {
                    'class': 'ipc-html-content-inner-div',
                    'role': 'presentation'
                })
                
                if synopsis_content:
                    for br in synopsis_content.find_all('br'):
                        br.replace_with('\n')
                    return synopsis_content.get_text(strip=True)
            
            return None
            
        except Exception as e:
            print(f"Error with episode {episode_id}: {str(e)}")
            return None

    def save_synopses(self):
        """Save all synopses to JSON file at once."""
        with open('synopses.json', 'w', encoding='utf-8') as f:
            json.dump(self.synopses, f, indent=4, ensure_ascii=False)

    def process_episodes_csv(self, csv_file):
        """Process all episodes from a CSV file."""
        df = pd.read_csv(csv_file)
        total_episodes = len(df)
        print(f"Processing {total_episodes} episodes...")
        
        for index, row in df.iterrows():
            episode_id = row['tconst']
            print(f"Processing episode {episode_id} (Progress: {index + 1}/{total_episodes})")
            
            synopsis = self.get_imdb_synopsis(episode_id)
            
            if synopsis:
                self.synopses[episode_id] = synopsis
                print(f"Synopsis found for episode {episode_id}")
                # Save after each successful fetch in case of interruption
                self.save_synopses()
            else:
                print(f"No synopsis found for episode {episode_id}")
            
            # Add a random delay between requests to avoid rate limiting
            time.sleep(random.uniform(1, 3))

def main():
    fetcher = IMDbSynopsisFetcher()
    
    # Replace with your CSV file name
    csv_file = "tt0264235_episodes.csv"  # Change this to your CSV file name
    
    if not os.path.exists(csv_file):
        print(f"Error: Could not find {csv_file}")
        return
    
    fetcher.process_episodes_csv(csv_file)
    print("Processing complete!")

if __name__ == "__main__":
    main()