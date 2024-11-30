import json
import pandas as pd

def transform_files(json_path, csv_path):
    # Read the JSON file
    with open(json_path, 'r') as f:
        synopsis_data = json.load(f)
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Create new structure
    transformed = {}
    
    # Iterate through DataFrame rows
    for _, row in df.iterrows():
        # Create episode identifier in format (season,episode)
        episode_key = f"({row['seasonNumber']},{row['episodeNumber']})"
        
        # Get the synopsis from JSON using IMDB ID (tconst)
        imdb_id = row['tconst']
        
        # Create episode entry
        transformed[episode_key] = {
            "imdb_synopsis": synopsis_data.get(imdb_id, ""),  # Get synopsis if exists
            "wikipedia_synopsis": "",  # Placeholder for Wikipedia synopsis
            "imdbid": imdb_id,
            "title": row['primaryTitle']
        }
    
    return transformed

def save_transformed_json(transformed_data, output_path):
    # Save the transformed data to a new JSON file
    with open(output_path, 'w') as f:
        json.dump(transformed_data, f, indent=2)

# Example usage:
if __name__ == "__main__":
    # Replace these with your actual file paths
    json_file = "synopses.json"
    csv_file = "tt0264235_episodes.csv"
    output_file = "curbdata.json"
    
    try:
        # Transform the data
        transformed_data = transform_files(json_file, csv_file)
        
        # Save the transformed data
        save_transformed_json(transformed_data, output_file)
        
        print(f"Successfully transformed data and saved to {output_file}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file - {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")