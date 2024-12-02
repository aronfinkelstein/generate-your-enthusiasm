'''
Splitting the data into:
- manually labelled set
- training set
- validation set
- testing set
'''
import json
import random
import re
from pathlib import Path
from sklearn.model_selection import train_test_split

def get_random_sentences(text, n=3):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    if len(sentences) <= n:
        return ' '.join(sentences)
    return ' '.join(random.sample(sentences, n))

def get_word_count(text):
    return len(text.split())

def split_dataset(input_file, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Separate IMDB and Wikipedia synopses
    imdb_synopses = []
    wiki_synopses = []
    
    for episode_id, episode_data in data.items():
        if 'imdb_synopsis' in episode_data and episode_data['imdb_synopsis'].strip():
            imdb_synopses.append({
                'episode_id': episode_id,
                'source': 'imdb',
                'text': episode_data['imdb_synopsis'],
                'season': episode_data.get('season', 'unknown'),
                'episode': episode_data.get('episode', 'unknown'),
                'full_text': episode_data['imdb_synopsis']  # Keep original text
            })
        if 'wikipedia_synopsis' in episode_data:
            wiki_synopses.append({
                'episode_id': episode_id,
                'source': 'wikipedia',
                'text': episode_data['wikipedia_synopsis'],
                'season': episode_data.get('season', 'unknown'),
                'episode': episode_data.get('episode', 'unknown'),
                'full_text': episode_data['wikipedia_synopsis']  # Keep original text
            })
    
    # Select manual samples from each source
    manual_per_source = 10
    manual_imdb = random.sample(imdb_synopses, manual_per_source)
    manual_wiki = random.sample(wiki_synopses, manual_per_source)
    
    # Process manual set with random sentences
    manual_set = []
    for synopsis in (manual_imdb + manual_wiki):
        sampled_text = get_random_sentences(synopsis['full_text'])
        manual_set.append({
            'episode_id': synopsis['episode_id'],
            'source': synopsis['source'],
            'text': sampled_text,
            'word_count': get_word_count(sampled_text),
            'season': synopsis['season'],
            'episode': synopsis['episode'],
            'full_text': synopsis['full_text']  # Include full text for reference
        })
    
    # Sort manual set chronologically
    manual_set.sort(key=lambda x: (x['season'], x['episode']))
    
    # Remove manual samples from main sets
    remaining_imdb = [s for s in imdb_synopses if s['episode_id'] not in [m['episode_id'] for m in manual_imdb]]
    remaining_wiki = [s for s in wiki_synopses if s['episode_id'] not in [m['episode_id'] for m in manual_wiki]]
    
    # Split remaining data
    train_imdb, temp_imdb = train_test_split(remaining_imdb, test_size=0.3, random_state=42)
    val_imdb, test_imdb = train_test_split(temp_imdb, test_size=0.5, random_state=42)
    
    train_wiki, temp_wiki = train_test_split(remaining_wiki, test_size=0.3, random_state=42)
    val_wiki, test_wiki = train_test_split(temp_wiki, test_size=0.5, random_state=42)
    
    datasets = {
        'manual': manual_set,
        'train': train_imdb + train_wiki,
        'val': val_imdb + val_wiki,
        'test': test_imdb + test_wiki
    }
    
    # Save and print statistics
    for name, dataset in datasets.items():
        output_file = output_dir / f'{name}_set.json'
        with open(output_file, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        if name == 'manual':
            print(f"\nManual Set Statistics:")
            print(f"Total samples: {len(dataset)}")
            print(f"IMDB samples: {sum(1 for s in dataset if s['source'] == 'imdb')}")
            print(f"Wiki samples: {sum(1 for s in dataset if s['source'] == 'wikipedia')}")
            print(f"Average word count: {sum(s['word_count'] for s in dataset) / len(dataset):.1f}")
        else:
            imdb_count = sum(1 for s in dataset if s['source'] == 'imdb')
            wiki_count = sum(1 for s in dataset if s['source'] == 'wikipedia')
            print(f'{name.capitalize()} set - Total: {len(dataset)} (IMDB: {imdb_count}, Wiki: {wiki_count})')

if __name__ == "__main__":
    input_file = Path(__file__).parents[2] / "backend/data/clean_curbdata.json"
    output_dir = Path(__file__).parents[2] / "backend/data/split_data"
    split_dataset(input_file, output_dir)