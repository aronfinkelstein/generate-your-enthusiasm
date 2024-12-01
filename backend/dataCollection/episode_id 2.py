import gzip
import pandas as pd
import requests
from pathlib import Path
import os

class IMDbEpisodeFetcher:
    def __init__(self):
        self.base_url = "https://datasets.imdbws.com/"
        self.episode_file = "title.episode.tsv.gz"
        self.basics_file = "title.basics.tsv.gz"
        self.data_dir = Path("imdb_data")
        
    def download_file(self, filename):
        """Download a file from IMDb datasets if it doesn't exist locally."""
        self.data_dir.mkdir(exist_ok=True)
        local_path = self.data_dir / filename
        
        if not local_path.exists():
            print(f"Downloading {filename}...")
            response = requests.get(f"{self.base_url}{filename}", stream=True)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_path

    def get_show_episodes(self, show_id):
        """
        Get all episode IDs for a given show ID.
        
        Args:
            show_id (str): The IMDb ID of the show (starts with 'tt')
            
        Returns:
            DataFrame: Contains episode information including season and episode numbers
        """
        # Download necessary files
        episode_path = self.download_file(self.episode_file)
        basics_path = self.download_file(self.basics_file)
        
        # Read episode data
        print("Reading episode data...")
        episodes_df = pd.read_csv(
            episode_path,
            compression='gzip',
            sep='\t',
            usecols=['tconst', 'parentTconst', 'seasonNumber', 'episodeNumber']
        )
        
        # Filter episodes for the specific show
        show_episodes = episodes_df[episodes_df['parentTconst'] == show_id].copy()
        
        if show_episodes.empty:
            print(f"No episodes found for show ID {show_id}")
            return None
            
        # Sort by season and episode number
        show_episodes.sort_values(['seasonNumber', 'episodeNumber'], inplace=True)
        
        # Read basics data to get episode titles
        print("Reading basic title data...")
        basics_df = pd.read_csv(
            basics_path,
            compression='gzip',
            sep='\t',
            usecols=['tconst', 'primaryTitle']
        )
        
        # Merge with basics to get episode titles
        show_episodes = show_episodes.merge(
            basics_df,
            left_on='tconst',
            right_on='tconst',
            how='left'
        )
        
        return show_episodes

    def save_episodes_to_csv(self, episodes_df, show_id):
        """Save the episodes data to a CSV file."""
        if episodes_df is not None:
            output_file = f"{show_id}_episodes.csv"
            episodes_df.to_csv(output_file, index=False)
            print(f"Episodes saved to {output_file}")

def main():
    # Example usage
    fetcher = IMDbEpisodeFetcher()
    
    show_id = "tt0264235"
    
    episodes = fetcher.get_show_episodes(show_id)
    fetcher.save_episodes_to_csv(episodes, show_id)

if __name__ == "__main__":
    main()