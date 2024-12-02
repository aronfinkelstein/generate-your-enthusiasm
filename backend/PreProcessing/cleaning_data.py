import json
import re
import unicodedata
from pathlib import Path

def clean_text(text):
    if not isinstance(text, str):
        return text
    
    # Remove all backslashes
    text = text.replace('\\', '')
    
    text = unicodedata.normalize('NFKD', text)
    text = ' '.join(text.split())
    text = ''.join(char for char in text if ord(char) < 128 or char in '.,!?-\'\"')
    text = text.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def clean_json_file(input_file, output_file=None):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cleaned_data = {}
        for episode_id, episode_data in data.items():
            cleaned_episode = {}
            for key, value in episode_data.items():
                if key in ['imdb_synopsis', 'wikipedia_synopsis', 'title']:
                    cleaned_episode[key] = clean_text(value)
                else:
                    cleaned_episode[key] = value
            cleaned_data[episode_id] = cleaned_episode
        
        output_file = output_file or input_file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully cleaned and saved to {output_file}")
        return cleaned_data
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    file_path = Path(__file__).parents[2] / "backend/data" / "curbdata.json"
    output_dir = Path(__file__).parents[2] / "backend/data" / "clean_curbdata.json"
    
    cleaned_data = clean_json_file(file_path, output_dir)