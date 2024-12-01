import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_wikipedia_synopses():
    # Load existing JSON data
    with open('curbdata.json', 'r') as f:
        data = json.load(f)
    
    # Make request to Wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_Curb_Your_Enthusiasm_episodes"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all episode tables
    episode_tables = soup.find_all('table', class_='wikiepisodetable')
    
    current_season = 1  # Initialize season counter
    updates_made = 0  # Track number of updates
    
    for table in episode_tables:
        # Check if this is a season table by looking for the header
        season_header = table.find_previous('h3')
        if season_header:
            season_match = re.search(r'Season (\d+)', season_header.text)
            if season_match:
                current_season = int(season_match.group(1))
        
        # Find all episode rows
        episode_rows = table.find_all('tr', class_='vevent')
        
        for row in episode_rows:
            try:
                # Extract episode number
                episode_cell = row.find('td', style='text-align:center')
                if not episode_cell:  # Some episodes might have different styling
                    episode_cell = row.find('td')
                episode_num = episode_cell.text.strip()
                
                # Extract title
                title = row.find('td', class_='summary').text.strip().replace('"', '')
                
                # Find the synopsis
                synopsis_row = row.find_next_sibling('tr', class_='expand-child')
                if synopsis_row:
                    synopsis_div = synopsis_row.find('div', class_='shortSummaryText')
                    if synopsis_div:
                        synopsis = synopsis_div.text.strip()
                        
                        # Create the key in the format "(season,episode)"
                        key = f"({current_season},{episode_num})"
                        
                        # Only update if the key exists and wikipedia_synopsis is empty
                        if key in data:
                            if not data[key].get('wikipedia_synopsis'):
                                print(f"Adding synopsis for episode {key}")
                                data[key]['wikipedia_synopsis'] = synopsis
                                updates_made += 1
                            else:
                                print(f"Synopsis already exists for episode {key}")
                        else:
                            print(f"Key not found: {key}")
            except AttributeError as e:
                print(f"Error processing row: {e}")
                continue
    
    print(f"\nTotal updates made: {updates_made}")
    
    # Save updated JSON only if updates were made
    if updates_made > 0:
        with open('curbdata.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("File updated successfully")
    else:
        print("No updates were necessary")

if __name__ == "__main__":
    scrape_wikipedia_synopses()